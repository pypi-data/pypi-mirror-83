__copyright__ = """
Machine Learning for Distributed Acoustic Sensing data (MLDAS)
Copyright (c) 2020, The Regents of the University of California,
through Lawrence Berkeley National Laboratory (subject to receipt of
any required approvals from the U.S. Dept. of Energy). All rights reserved.

If you have questions about your rights to use or distribute this software,
please contact Berkeley Lab's Intellectual Property Office at
IPO@lbl.gov.

NOTICE.  This Software was developed under funding from the U.S. Department
of Energy and the U.S. Government consequently retains certain rights.  As
such, the U.S. Government has been granted for itself and others acting on
its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the
Software to reproduce, distribute copies to the public, prepare derivative 
works, and perform publicly and display publicly, and to permit others to do so.
"""
__license__ = "Modified BSD license (see LICENSE.txt)"
__maintainer__ = "Vincent Dumont"
__email__ = "vincentdumont11@gmail.com"

# Internals
import os
import re

# Externals
import numpy
import scipy
import h5py
import hdf5storage
import scipy.io as sio
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Local
from .loading import hdf5read

def Xcorr2mat(mat,h5Xcorr):
  # Copy data and metadata into dictionary
  dsi_xcorr = {}
  dsi_xcorr['fh']=mat['variable'][0][0]
  dsi_xcorr['th']=mat['variable'][0][1]
  dsi_xcorr['dat']=mat['variable'][0][2]
  # Open file in read mode
  xfile = h5py.File(h5Xcorr,'r')
  # Load cross-correlated HDF5 data
  xdata = xfile.get('Xcorr')[:,:].T
  # Close HDF5 file
  xfile.close()
  # Extract sample time from file header
  dt = mat['variable'][0][0][0][7][0][0]
  # Define new sample time
  dt_new = 0.008
  # Estimate new relative samping rate 
  R = round(dt_new/dt)
  # Length of resampledcross-correlated data array
  lres = mat['variable'][0][2][0][0].shape[0]/R
  # Maximum duration of new data
  tmax = round((lres-1)*dt_new,6)
  # Update data and file header in dictionary
  dsi_xcorr['dat'][0][0]=numpy.array(xdata[:,:],dtype=numpy.double)
  dsi_xcorr['fh'][0][6]=len(xdata)
  dsi_xcorr['fh'][0][7]=dt_new
  dsi_xcorr['fh'][0][8]=-tmax
  dsi_xcorr['fh'][0][9]=tmax
  dsi_xcorr['fh'][0][10]=[]
  # Save MAT cross-correlated file
  sio.savemat(h5Xcorr.replace('h5','mat'), {'dsi_xcorr': dsi_xcorr})

def xcorr_au(data_path,nstep):
  fname = re.split('[/.]',data_path)[-2]
  os.system('ln -s %s %s.mat'%(data_path,fname))
  mat = hdf5storage.loadmat(fname+'.mat')
  if nstep==1:
    data = mat['variable'][0][2][0,0].T
    f = h5py.File(fname+'.h5','w')
    f.create_dataset("DataTimeChannel",data=data,dtype="i2")
    f.close()
  if nstep==2:
    xcorr_name = fname.replace('westSac','1minXcorr')+'.h5'
    Xcorr2mat(mat,xcorr_name)
  os.system('rm %s.mat'%fname)

def avg_fft(data,fs=500.):
  N = data.shape[1]
  freqs = numpy.linspace(fs/N,fs/2,N//2)
  ffts = numpy.array([2.0/N*numpy.abs(scipy.fft.fft(ts)[:N//2]) for ts in data])
  fft = numpy.average(ffts,axis=0)
  return freqs, fft

def xcorr_freq(data,xcorr,lag_range=500,threshold=5e-2):
  plt.style.use('seaborn')
  fig,ax = plt.subplots(2,2,figsize=(18,8),dpi=80)
  ax[0][0].imshow(abs(data),extent=[0,data.shape[1]/500,200,0],cmap='plasma',aspect='auto',norm=LogNorm())
  ax[0][0].set_title('Raw strain measurements')
  ax[0][0].set_xlabel('Time [sec]')
  ax[0][0].set_ylabel('Channels')
  ax[0][1].imshow(xcorr[:,xcorr.shape[1]//2-lag_range:xcorr.shape[1]//2+lag_range],
                  extent=[-lag_range*59/xcorr.shape[1],lag_range*59/xcorr.shape[1],200,0],
                  aspect ='auto',cmap='seismic',vmin=-threshold,vmax=threshold)
  ax[0][1].set_title('Cross-correlation')
  ax[0][1].set_xlabel('Time lag [sec]')
  ax[1][0].plot(*avg_fft(data))
  ax[1][0].set_title('Average FFT from raw data')
  ax[1][0].set_xlabel('Frequency [Hz]')
  ax[1][0].set_ylabel('Amplitude')
  ax[1][1].plot(*avg_fft(xcorr))
  ax[1][1].set_title('Average FFT from cross-correlated data')
  ax[1][1].set_xlabel('Frequency [Hz]')
  plt.tight_layout()
  plt.show()
