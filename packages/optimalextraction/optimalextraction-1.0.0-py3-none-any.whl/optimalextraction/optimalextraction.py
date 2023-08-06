import numpy as np
import pandas as pd
from astropy.modeling import models,fitting
from astropy.io import fits
from astropy.table import Table

class OptimalExtraction:
    """
    OptimalExtraction is a python class to perform optimal extraction of a spectrum from an image. Originally, the algorithm was proposed by [1]. In this adaptation, we followed [2].
    #####
    + Inputs:
      - image = an image in 2D array. 
        Assumptions: 
          i) image was processed, cleaned, and calibrated in a standard CCD processing steps (i.e., bias subtraction, flatfield, cosmic-ray removal/repair, and background subtracted).
          ii) image was resampling from the original image so that 
            a) dispersion is along x-axis and cross-dirspersion along y-axis. (See hstgrism.aperturedirection and hstgrism.resampling if you are working with HST images).
            b) Each x column is assumed to be one wavelength bin with line spreading along y-axis.
            c) Peak of each wavelength bin is aligned at the center row in the image. (See hstgrism.extractcompoundmodel1d for fitting the trace centers).
      - var = 2D array of variance corresponding to the image
      - bin_number = 1D array parallel to dispersion axis (i.e., x-axis) specifying bin numbers. Number 0 = skip the extraction on that column.
      - bin_kernel_initial = initial extraction kernel. Only astropy.modeling.models.Gaussian1D is supported for this version.
      - fitter = astropy.modeling.fitting.LevMarLSQFitter() recommended.
      - do_fit_bin = True to re-fit using the bin_initial_kernel, and new parameters will be used in the final step of extraction. If False, bin_initial_kernel would be used for extracting in the final step.
      - kernel_mode = 'Gaussian1D' only in this version.
    #####
    + Compute:
      - self.compute() to start the optimal extraction after properly instantiate.
          i) self.bin_image = 2D array of binned image, i.e., columns with the same bin_number are added. x-axis of bin_image corresponds to bin_number.
          ii) self.bin_var = 2D array of binned variance. Simply add columns of variance with the same bin_number.
          iii) self.bin_kernel_fit = dict of key:bin_number, value:extraction kernel. If do_fit_bin = False, bin_kernel_fit = bin_kernel_initial.
          iv) self.bin_image_kernel = 2D array of binned image using bin_kernel_fit for estimation.
          v) self.kernel_fit = 1D array of extraction kernel runs parallel to dispersion axis (unbinned), and re-normalized. This is simply prepared from bin_kernel_fit and bin_numer. Re-normalization is done for each dispersion column given bin_kernel_fit, but fixed the shape profile. For example, in Gaussian1D kernel, the re-normalization fixes mean and stddev of each column, and re-fit for the amplitude.
          vi) self.image_kernel = 2D array of unbinned image using kernel_fit for estimation.
          vii) self.optimal1d = 1D array of optimally extracted profile
    #####
    + Save:
      - container = optimalextraction.container.Container
      - wavelength = 1D array of wavelengths parallel to dispersion columns. (Use trace.csv if working with HSTGRISM environment).
      - optimalextraction.fits = multiextension fits file (See more in astropy.io.fits)
          EXT0: PrimaryHDU
          EXT1: ImageHDU as self.image_kernel
          EXT2: BinTableHDU with columns as bin_number (i.e., 1D array parallel to dispersion columns specifying bin numbers), and self.kernel_fit parameters (i.e., amplitude, mean, stddev for Gaussian1D kernel_mode).
      - optimalextraction.csv = csv table with columns as column_index, wavelength (if specified), spectrum. Spectrum is optimally extracted.
    #####
    + References:
      [1] Horne 1986, 'An optimal extraction algorithm for CCD spectroscopy': https://ui.adsabs.harvard.edu/abs/1986PASP...98..609H/abstract
      [2] Space Telescope Science Institute, 'NIRSpec MOS Optimal Spectral Extraction': https://github.com/spacetelescope/dat_pyinthesky/blob/master/jdat_notebooks/optimal_extraction/Spectral%20Extraction.ipynb
      [3] Astropy, 'Models and Fitting': https://docs.astropy.org/en/stable/modeling/index.html
    """
    def __init__(self,image,var,bin_number,bin_kernel_initial,fitter,do_fit_bin=True,kernel_mode='Gaussian1D'):
        self.image = image
        self.var = var
        self.bin_number = bin_number
        self.bin_kernel_initial = bin_kernel_initial
        self.fitter = fitter
        self.do_fit_bin = do_fit_bin
        self.kernel_mode = kernel_mode
    def compute(self):
        self.bin_image = self._make_bin_image(mode='image')
        self.bin_var = self._make_bin_image(mode='var')
        self.bin_kernel_fit = self.bin_kernel_initial
        if self.do_fit_bin:
            self.bin_kernel_fit = self._fit_bin()
        self.bin_image_kernel = self._compute_bin_image_kernel()
        self.kernel_fit,self.image_kernel = self._compute_kernel_fit()
        self.optimal1d = self._compute_optimal()
    def save(self,container=None,wavelength=None):
        if container is None:
            raise ValueError('container must be specified. See optimalextraction.container.Container.')
        #####
        # bin_number,kernel_fit,image_kernel >>> optimalextraction.fits
        string = './{0}/{1}_optimalextraction.fits'.format(container.data['savefolder'],container.data['saveprefix'])
        if self.kernel_mode=='Gaussian1D':
            amplitude,mean,stddev = [],[],[]
            for ii,i in enumerate(self.kernel_fit):
                amplitude.append(self.kernel_fit[ii].amplitude[0])
                mean.append(self.kernel_fit[ii].mean[0])
                stddev.append(self.kernel_fit[ii].stddev[0])
            t = {'bin_number':self.bin_number,'amplitude':amplitude,'mean':mean,'stddev':stddev}
        phdu = fits.PrimaryHDU()
        ihdu = fits.ImageHDU(self.image_kernel)
        bhdu = fits.BinTableHDU(Table(t))
        hdul = fits.HDUList([phdu,ihdu,bhdu])
        hdul.writeto(string,overwrite=True)
        print('Save {0}'.format(string))
        #####
        # optimal1d >>> optimalextraction.csv
        string = './{0}/{1}_optimalextraction.csv'.format(container.data['savefolder'],container.data['saveprefix'])
        ty,ty_name = self.optimal1d,'spectrum'
        tx,tx_name = np.arange(len(ty)),'column_index'
        t = {tx_name:tx, ty_name:ty}
        if wavelength is not None:
            tw,tw_name = wavelength,'wavelength'
            t = {tx_name:tx, tw_name:tw, ty_name:ty}
        pd.DataFrame(t).to_csv(string)
        print('Save {0}'.format(string))
    def _compute_optimal(self):
        ny,nx = self.image.shape
        cross_dispersion_array = np.arange(ny)
        dispersion_array = np.arange(nx)
        optimal1d = np.full_like(dispersion_array,0.,dtype=float)
        for i in dispersion_array:
            bin_number = self.bin_number[i]
            if bin_number==0:
                continue
            val = self.image[:,i]
            var = self.var[:,i]
            kernel = self.bin_kernel_fit[bin_number]
            if self.kernel_mode=='Gaussian1D':
                norm = np.sqrt(2. * np.pi) * kernel.amplitude * kernel.stddev
            else:
                raise ValueError('kernel_mode = Gaussian1D only available')
            kernel_normalized = kernel(cross_dispersion_array) / norm
            A = val * kernel_normalized / var
            B = np.power(kernel_normalized,2) / var
            C = A.sum(axis=0) / B.sum(axis=0)
            optimal1d[i] = C.copy()
        return optimal1d
    def _compute_kernel_fit(self):
        kernel_fit = []
        image_kernel = np.full_like(self.image,0.,dtype=float)
        ny,nx = self.image.shape
        cross_dispersion_array = np.arange(ny)
        for i in np.arange(nx):
            bin_number = self.bin_number[i]
            val = self.image[:,i]
            var = self.var[:,i]
            kernel = self.bin_kernel_fit[bin_number]
            if bin_number==0:
                kernel_fit.append(kernel)
                continue
            if self.kernel_mode=='Gaussian1D':
                kernel = models.Gaussian1D(amplitude=val.max(),mean=kernel.mean,stddev=kernel.stddev,fixed={'mean':True,'stddev':True})
                kernel = self.fitter(kernel,cross_dispersion_array,val,weights=var)
                kernel_fit.append(kernel)
                image_kernel[:,i] = kernel(cross_dispersion_array)
            else:
                raise ValueError('kernel_mode = Gaussian1D only available')
        return np.array(kernel_fit),image_kernel
    def _compute_bin_image_kernel(self):
        bin_image_kernel = np.full_like(self.bin_image,0.,dtype=float)
        ny,nx = bin_image_kernel.shape
        cross_dispersion_array = np.arange(ny)
        for i in np.arange(nx):
            if i==0:
                continue
            bin_image_kernel[:,i] = self.bin_kernel_fit[i](cross_dispersion_array)
        return bin_image_kernel
    def _fit_bin(self):
        ny,nx = self.image.shape
        bin_kernel_fit = {}
        for i in np.unique(self.bin_number):
            if i==0:
                bin_kernel_fit[i] = self.bin_kernel_initial[i]
                continue
            kernel = self.bin_kernel_initial[i]
            cross_dispersion_array = np.arange(ny)
            value_array = self.bin_image[:,i]
            weights = self.bin_var[:,i]
            bin_kernel_fit[i] = self.fitter(kernel,cross_dispersion_array,value_array,weights=weights)
        return bin_kernel_fit
    def _make_bin_image(self,mode):
        ny,nx = self.image.shape
        nx = np.unique(self.bin_number).max() + 1
        shape = (ny,nx)
        bin_image = np.zeros(shape)
        for i in np.unique(self.bin_number):
            if i==0:
                bin_image[:,i] = 0.
                continue
            t = np.argwhere(self.bin_number==i).flatten()
            if mode=='image':
                t = self.image[:,t]
            elif mode=='var':
                t = self.var[:,t]
            t = t.sum(axis=1)
            bin_image[:,i] = t.copy()
        return bin_image
    