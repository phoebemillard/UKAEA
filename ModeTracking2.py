import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.signal import savgol_filter #for smoothing spiky graphs

ts = np.loadtxt('TimeAxis.dat')
fs = np.loadtxt('FrequencyAxis.dat')
spectrum = np.loadtxt('SpectrumArray.dat')
spectrum = np.log10(spectrum)  # makes it easier to see features without changing contrast

## if you want to find the index of some value x in the time array Y, you find the closest entry. i.e. the minimum of | Y - x |.
## if you want the timeslice corresponding to t = 11.6
## the spectrum at time t=11.6 is    spectrum[:,k]
p = np.argmin(abs(ts-(11.6)))
array=[]
array4=[]
array4.append([0,0,0])
array4.append([0,0,0])
array5=[]
k=1000
a=0
while k<2900: #1829-1834
	smooth=savgol_filter(spectrum[:,k], window_length=15,  polyorder=3)
	peaks=find_peaks(smooth, distance=10.5,height=-4, width=5) #was at helight -3.8 and width 2
	#plt.plot(spectrum[:,k], color='blue')
	#plt.plot(smooth, color='red')
	#plt.axhline(y=np.mean(smooth), color='yellow', linestyle='-')
	#plt.plot(peaks[0], smooth[peaks[0]], color='yellow',marker='x', linestyle='none',label=k)
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
	k=k+1
np.savetxt('array.txt',array,delimiter=',')

#setting initial array2 and array33
array2=[]
array3=[]
j=0 #Index for all peaks (length of 'array')
while j<len(array):
	if array[j][0]==1:
		array2.append([array[j][1],array[j][2]]) #array2=[time,freq] of peaks with time index t 
	if array[j][0]==2:
		array3.append([array[j][1],array[j][2]])  #array2=[time,freq] of peaks with time index t+1 
	j=j+1	


i=0 #mode number index
t=1 #Index for groups of peaks at in time segment (left column of 'array')
while t<array[-1][0]-1: #less than index of last element in 'array'
	array33=[]


	j=0 #Index for all peaks (length of 'array')
	while j<len(array):
		#if array[j][0]==t:
			#array2.append([array[j][1],array[j][2]]) #array2=[time,freq] of peaks with time index t 
		#if array[j][0]==t+1:
			#array3.append([array[j][1],array[j][2]])  #array2=[time,freq] of peaks with time index t+1 
		if array[j][0]==t+2:
			array33.append([array[j][1],array[j][2]])  #array2=[time,freq] of peaks with time index t+2
		j=j+1	

	#print('\n\narray2',array2,'\n\narray3',array3,'\n\narray33',array33)

	a=0
	while a<len(array2):
		b=0
		while b<len(array3):	
			if abs(array2[a][1]-array3[b][1])<1:
				c=0 #allows the starting of while below
			elif abs(array2[a][1]-array3[b][1])>=1 and abs(array2[a][1]-array3[b][1])<2.5: #checks for anomalies
				f=0
				while f<len(array33):
					if abs(array2[a][1]-array33[f][1])<2:
						array3[b][1] = (array2[a][1]+array33[f][1])/2 #sets anomalous value to midpoint of two surrounding points
						c=0 #allows the starting of while below
						f=len(array33) #ends loop
					else:
						if f==len(array33)-1:
							c=len(array4) #doesnt allow the starting of while below
							f=len(array33) #ends loop
						else:
							f=f+1
			else:
				c=len(array4) #doesnt allow the starting of while below
				



			while c<len(array4): #array4: mode index i, time, freq
				if array2[a][0]==array4[c][1] and array2[a][1]==array4[c][2]: #searches for if its mode has already been recorded 
					array4.append([array4[c][0],array3[b][0],array3[b][1]])
					c=len(array4) #ends for loop
				else:
					if c==len(array4)-1:
						i=i+1 #creates new mode index
						array4.append([i,array3[b][0],array3[b][1]]) #adds new mode to array4
						c=len(array4) #ends loop
					else:
						c=c+1 #goes to next row of array4

			b=b+1
		a=a+1
	array2=array3
	array3=array33 #resets arrays
	t=t+1

array4.sort()
np.savetxt('array4',array4,delimiter=',')

q=0
while q<len(array4):
	if array4[q][0]==157 or  array4[q][0]==159 or  array4[q][0]==281 or array4[q][0]==322 or  array4[q][0]==550 or  array4[q][0]==872 or  array4[q][0]==885 or  array4[q][0]==1489:

	#if array4[q][0]==209 or  array4[q][0]==557 or  array4[q][0]==795 or array4[q][0]==203 or  array4[q][0]==211 or  array4[q][0]==287 or  array4[q][0]==331:
		array5.append([array4[q][1],array4[q][2]])
		q=q+1
	else:
		q=q+1


cMap = plt.get_cmap('inferno') # colormap to use for 2D plot
j=0

plt.figure(figsize=(8,6))#(15,9))
plt.imshow(spectrum, interpolation='nearest', cmap=cMap, extent=[ts.min(), ts.max(), fs.min(), fs.max()], aspect='auto', origin='lower')
plt.xlabel('$t$ $[s]$')
plt.ylabel('$f$ $[kHz]$')
plt.colorbar(label=r'Amplitude [a.u.]')
while j<len(array5):
	plt.scatter(ts[array5[j][0]],array5[j][1], c='blue',marker='o',s=0.5)
	j=j+1
plt.show()


	

