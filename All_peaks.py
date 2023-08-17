import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.signal import savgol_filter #for smoothing spiky graphs

ts = np.loadtxt('TimeAxis.dat')
fs = np.loadtxt('FrequencyAxis.dat')
spectrum = np.loadtxt('SpectrumArray.dat')
spectrum = np.log10(spectrum)  # makes it easier to see features without changing contrast

p = np.argmin(abs(ts-(10.45)))
array=[]
old_peaks=[]
old_peaks2=[]
k=2000
q=0
while k<2929:
	smooth=savgol_filter(spectrum[:,k], window_length=15,  polyorder=3)
	peaks=find_peaks(spectrum[:,k], distance=12,height=-3.7)
	#peaks=find_peaks(smooth, distance=10.5,height=-3.7, width=5) #was at helight -3.8 and width 2
	#plt.plot(spectrum[:,k], color='blue')
	#plt.plot(smooth, color='red')
	#plt.axhline(y=-3.7, color='yellow', linestyle='-')
	#plt.plot(peaks[0], spectrum[:,k][peaks[0]], color='yellow',marker='x', linestyle='none',label=k)
	#plt.legend()
	#plt.show()
	
	peak_freq=peaks[0]*(500/2048)
	
	#removing some noise
	a=0
	while a<len(old_peaks):
		b=0
		while b<len(peak_freq):
			c=0
			while c<len(old_peaks2):
				if abs(peak_freq[b]-old_peaks[a])<=1 or abs(old_peaks2[c]-old_peaks[a])<=1:
					array.append([k-1,old_peaks[a]])
					c=len(old_peaks2)
					b=len(peak_freq)
				else:
					c=c+1
			b=b+1
		a=a+1
			
	old_peaks2=old_peaks
	old_peaks=peak_freq
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
	plt.scatter(ts[array[j][0]],array[j][1], c='blue',marker='o',s=0.5)
	j=j+1
plt.show()
