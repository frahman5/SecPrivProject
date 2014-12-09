import wave
import numpy as np
import matplotlib.pyplot as plt

def filter_file(input_file, min_freq, max_freq):
	# Open the output file
	f = wave.open(input_file, 'r')
	output_file = 'filtered_'+input_file
	wf = wave.open(output_file, 'w')
	wf.setparams(f.getparams()) # Use the same parameters as the input file.

	samples = f.getframerate()
	n = int(f.getnframes()/samples)

	for num in range(n):
	    print('Processing {}/{} s'.format(num+1, n))
	    da = np.fromstring(f.readframes(samples), dtype=np.int16)
	    left, right = da[0::2], da[1::2] # left and right channel
	    lf, rf = np.fft.rfft(left), np.fft.rfft(right)
	    lf[:min_freq], rf[:min_freq] = 0, 0
	    lf[max_freq:], rf[max_freq:] = 0, 0 
	    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
	    ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
	    wf.writeframes(ns.tostring())
	# Close the files.
	f.close()
	wf.close()
	return output_file

def plot_sound(figure, subplot, y, fft_y, num_samples, fps):
	plt.figure(figure)
	a = plt.subplot(subplot)
	r = 200
	a.set_ylim([-r, r])
	a.set_xlabel('time [s]')
	a.set_ylabel('value')
	x = num_samples*np.arange(num_samples*fps)/float(fps)
	plt.plot(x, y)
	b = plt.subplot(subplot+1)
	b.set_xscale('log')
	# b.set_xlim([min_freq, max_freq])
	b.set_xlabel('frequency [Hz]')
	b.set_ylabel('|amplitude|')
	plt.plot(abs(fft_y))


if __name__ == '__main__':
	input_file = 'horizontal_stripped.wav'
	min_freq = 4100 
	max_freq = 4700

	# Filter file 
	filtered_file = filter_file(input_file, min_freq, max_freq)

	# Open again to plot
	f = wave.open(filtered_file, 'r')
	fps = f.getframerate()
	n = int(f.getnframes()/fps) # length of sound in seconds
	data = f.readframes(n*fps)  # read all the frames of the sound
	data_arr = np.fromstring(data, dtype=np.int16)	
	all_left, all_right = data_arr[0::2], data_arr[1::2]

	# FFT
	all_lf, all_rf = np.fft.rfft(all_left), np.fft.rfft(all_right)

	# Plot
	figure = 1
	plot_sound(figure, 221, all_left, all_lf, n, fps)
	plot_sound(figure, 223, all_right, all_rf, n, fps)


	plt.show()

