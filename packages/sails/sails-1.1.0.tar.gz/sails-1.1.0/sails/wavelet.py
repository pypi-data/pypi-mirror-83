from scipy import signal
import numpy as np


def morlet(x, freqs, sample_rate, window_len=4, ncycles=5, ret_basis=False,
           ret_mode='power', normalise=False):
    """Compute a morlet wavelet time-frequency transform on a univariate dataset.

    Parameters
    ----------
    x : vector array_like
        Time-series to compute wavelet transform from.
    freqs : array_like
        Array of frequency values in Hz
    sample_rate : scalar
        Sampling frequency of data in Hz
    window_len : scalar
        Length of wavelet window
    ncycles : int
        Width of wavelets in number of cycles
    ret_basis : bool
        Boolean flag indicating whether to return the basis set alongside the transform.
    ret_mode : {'power','amplitude','complex'}
        Flag indicating whether which form of the wavelet transform to return.

    Returns
    -------
    2D array
        Array containing morlet wavelet transformed data [nfreqs x nsamples]
    """

    cwt = np.zeros((len(freqs), *x.shape[:]), dtype=complex)

    # Get morlet basis
    mlt = get_morlet_basis(freqs, ncycles, sample_rate, normalise=normalise)

    for ii in range(len(freqs)):
        a = signal.convolve(x, mlt[ii].real, mode='same', method='fft')
        b = signal.convolve(x, mlt[ii].imag, mode='same', method='fft')
        cwt[ii, ...] = a+1j*b

    if ret_mode == 'power':
        cwt = np.power(np.abs(cwt), 2)
    elif ret_mode == 'amplitude':
        cwt = np.abs(cwt)
    elif ret_mode != 'complex':
        raise ValueError("'ret_mode not recognised, please use one of {'power','amplitude','complex'}")

    if ret_basis:
        return cwt, mlt
    else:
        return cwt


def get_morlet_basis(freq, ncycles, sample_rate, normalise=False, win_len=5):
    """Compute a morlet wavelet basis set based on specified parameters.

    Parameters
    ----------
    freq : array_like
        Array of frequency values in Hz
    ncycles : int
        Width of wavelets in number of cycles
    sample_rate : scalar
        Sampling frequency of data in Hz
    normalise : {None,'simple','tallon','wikipedia','mne'}
        Flag indicating which normalisation factor to apply to the wavelet basis.
    win_len : float
        Window length duration factor

    Returns
    -------
    list of vector arrays
        Complex valued arrays containing morlet wavelets

    """

    m = []
    for ii in range(len(freq)):
        # Sigma controls the width of the gaussians applied to each wavelet. This
        # is adaptive for each frequency to match ncycles
        sigma = ncycles / (2*np.pi*freq[ii])

        # Compute time vector for this wavelet
        t = np.arange(-win_len*sigma, win_len*sigma, 1/sample_rate)

        # Compute oscillatory component
        wave = np.exp(2*np.pi*1j*t*freq[ii])

        # Compute gaussian-window component
        gauss = np.exp((-(t/2)**2) / (2*sigma**2))

        # Make wavelet
        mlt = wave * gauss

        if normalise == 'simple':
            # Set simple normalisation (output amplitude should match
            # oscillation amplitude)
            mlt = 2 * mlt / np.abs(mlt).sum()
        elif normalise == 'tallon':
            # Set normalisation factor from Tallon-Baudry 1997
            A = (sigma*np.sqrt(np.pi))**(-1/2)
            mlt = A * mlt
        elif normalise == 'wikipedia':
            # Set normlisation from wikipedia: https://en.wikipedia.org/wiki/Morlet_wavelet
            A = (1 + np.exp(-sigma**2) - 2 * np.exp(-3/4 * sigma**2)) ** -0.5
            A = np.pi**(-.25) * A
            mlt = A * mlt
        elif normalise == 'mne':
            # Set normalisation step from MNE-python
            # https://github.com/mne-tools/mne-python/blob/master/mne/time_frequency/tfr.py#L98
            mlt = mlt / (np.sqrt(0.5) * np.linalg.norm(mlt.ravel()))

        m.append(mlt)
    return m
