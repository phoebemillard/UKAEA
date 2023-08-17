import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.signal import savgol_filter #for smoothing spiky graphs

ts = np.loadtxt('TimeAxis.dat')
fs = np.loadtxt('FrequencyAxis.dat')
spectrum = np.loadtxt('SpectrumArray.dat')
spectrum = np.log10(spectrum)  # makes it easier to see features without changing contrast

p = np.argmin(abs(ts-(10.2)))
array=[]
old_peaks=[]
k=p
a=0
while k<p+10:
	smooth=savgol_filter(spectrum[:,k], window_length=15,  polyorder=3)
	peaks=find_peaks(spectrum[:,k], distance=6,height=-3.7, width=3)
	#peaks=find_peaks(smooth, distance=10.5,height=-3.7, width=5) #was at helight -3.8 and width 2
	#plt.plot(spectrum[:,k], color='blue')
	#plt.plot(smooth, color='red')
	#plt.axhline(y=-3.5, color='yellow', linestyle='-')
	#plt.plot(peaks[0], spectrum[:,k][peaks[0]], color='yellow',marker='x', linestyle='none',label=k)
	#plt.legend()
	#plt.show()
	
	peak_freq=peaks[0]*(500/2048)
	
	#index for frames that have atleast on peak in 
	if len(peak_freq)>0:
		a=a+1
	
	i=0
	while i<len(peak_freq):
		array.append([a,k,peak_freq[i]])
		i=i+1
	
	#print('\nold',old_peaks,'\nnew',peak_freq)
	#while a<len(peak_freq):
		#b=0
		#while b<len(old_peaks):
			#if abs(peak_freq[a]-old_peaks[b])<=0.3:
				#array.append([k,peak_freq[a]])
				#b=len(old_peaks)
			#else:

				#b=b+1
		#a=a+1
	#print('\narray',array,'\n\n')
	#old_peaks=peak_freq
	k=k+1

np.savetxt('array.txt',array,delimiter=',')








cMap = plt.get_cmap('inferno') # colormap to use for 2D plot
j=0

plt.figure(figsize=(8,6))#(15,9))
plt.imshow(spectrum, interpolation='nearest', cmap=cMap, extent=[ts.min(), ts.max(), fs.min(), fs.max()], aspect='auto', origin='lower')
plt.xlabel('$t$ $[s]$')
plt.ylabel('$f$ $[kHz]$')
plt.colorbar(label=r'Amplitude [a.u.]')
while j<len(array):
	plt.scatter(ts[array[j][1]],array[j][2], c='blue',marker='o',s=0.5)
	j=j+1
plt.show()
