import sys
import time
import math
from DCE.Utilities import wav_to_txt, batch_wav_to_txt
from DCE.Tools import plot_power_spectrum
from DCE.Plotter import make_window_frame
from DCE.MovieTools import frames_to_movie
from DCE.Movies import vary_tau, slide_window, compare_vary_tau, compare_multi
from DCE.Plotter import plot_waveform_zoom_only

# slide_window, vary_tau, compare_vary_tau: tau is in samples not seconds
# compare_multi: tau is in seconds; has all options for tau and crop *****




test = 6
# test = int(sys.argv[1])

print 'running test %d...' % test

start_time = time.time()

if test == 0:
	batch_wav_to_txt('datasets/time_series/piano_revisit/C134C/scale')


if test == 1:
	for i in xrange(10):
		print 'Hello'
		note = i + 10
		piano = 'C134C'
		vary_tau(
			'datasets/time_series/%s/%s-%s.txt' % (piano, str(note), piano),
			tau_lims=(.001, .005),
			tau_inc=.001,			# seconds
			embed_crop=(.5*i, .5*(i+1)),  	# aka window position, in seconds
			ds_rate=20
		)             		# downsample rate (takes every third sample)
		print 'hi'
		frames_to_movie('output/DCE/vary_tau_%s_%s.mp4' % (str(note), piano), framerate=1)


if test == 2:
	for i in xrange(7):
		note = i*10+10
		piano = 'C134C'
		slide_window(
			'datasets/time_series/%s/%s-%s.txt' % (piano, str(note), piano),
			window_size=.05*(i+1),    # seconds
			ds_rate=1,
			tau=.001,					# seconds
			step_size=1)      # how much to move window each frame
		frames_to_movie('output/DCE/slide_window_scale_tau_%s_%s.mp4' % (str(note), piano), framerate=1)


if test == 3:
	for i in xrange(7):
		note = (i+1)*10
		print 'note is %s ' % str(note)
		compare_vary_tau(
			'datasets/time_series/C135B/%s-C135B.txt' % str(note),
			'datasets/time_series/C134C/%s-C134C.txt' % str(note),
			tau_lims=(.001, .005),
			tau_inc=.001, 	# seconds
			embed_crop=(.5, .7),
			ds_rate=5
		)
		print 'note is still %s ' % str(note)
		frames_to_movie('output/DCE/compare_tau_%s.mp4' % str(note), framerate=1)


if test == 4:
	vary_tau(
		'datasets/time_series/C134C/49-C134C.txt',
		tau_lims=(.001, .008),
		tau_inc=.001,  # seconds
		embed_crop=(1, 2),  # aka window position, in seconds
		ds_rate=1
	)  # downsample rate (takes every third sample)
	frames_to_movie('output/DCE/test_4.mp4', framerate=1)


if test == 5:
	slide_window(
		'datasets/time_series/C134C/49-C134C.txt',
		window_size=.1,    	# seconds
		tau=.001,			# seconds
		step_size=1)      	# how much to move window each frame
	frames_to_movie('output/DCE/test_5.mp4')


if test == 6:
	compare_vary_tau(
		'datasets/time_series/C135B/49-C135B.txt',
		'datasets/time_series/C134C/49-C134C.txt',
		tau_lims=(.001, .005),
		tau_inc=.001, 			 # seconds
		embed_crop=(.5, .7),
		ds_rate=5
	)
	frames_to_movie('output/DCE/test_6.mp4')




if test == 8:
	# still trying to figure out exactly how the units should work here
	plot_power_spectrum(
		'datasets/time_series/C134C/34-C134C.txt',
		'output/DCE/power_spectrum_34-C134C.png',
		crop=(1, 2),    # window for analysis (seconds)
	)



if test == 9:
	dir1, base1 = 'datasets/time_series/C134C', '-C134C.txt'
	dir2, base2 = 'datasets/time_series/viol', '-viol.txt'

	compare_multi(
		dir1, base1,
		dir2, base2,

		i_lims=(36, 64), 		 # specify note range

		embed_crop_1='auto',	 # seconds or 'auto'
		embed_crop_2=(2, 2.3),	 # seconds or 'auto'
		auto_crop_length=.3,  	 	 # seconds for when embed_crop = 'auto'

		tau_1='auto detect',  	 # seconds 'auto detect' or 'auto ideal'. NOTE: 'auto detect' is considerably slower that 'auto ideal'
		tau_2='auto ideal',
		tau_T=math.pi, 		 	 # for auto tau. tau = period * tau_T

		save_worms=True,		 # to output/DCE/saved_worms
		save_movie=True,			 # False for faster worm creation

		ds_rate=1


		# As of now tau cannot be specified for file1 and file 2 seperately. Let me know if this functionality is needed.

	)

	frames_to_movie('output/DCE/viol_test_7_tau.25T.mp4', framerate=1)


if test == 10:
	
	dir1, base1 = 'datasets/time_series/C134C', '-C134C.txt'  # numerical index goes in front of base
	dir2, base2 = "datasets/time_series/C135B", '-C135B.txt'
	
	compare_multi(
		dir1, base1,
		dir2, base2,

		i_lims=(40, 41), 		 # specify note range

		embed_crop_1='auto',	 # seconds or 'auto'
		embed_crop_2='auto',	 # seconds or 'auto'
		auto_crop_length=.05,  	 	 # seconds for when embed_crop = 'auto'

		tau='auto detect',  	 # seconds 'auto detect' or 'auto ideal'. note 'auto detect' is considerably slower that 'auto ideal'
		tau_T=math.pi, 		 	 # for auto tau. tau = period * tau_T

		save_worms=True,		 # to output/DCE/saved_worms
		save_movie=True			 # False for faster worm creation
		
	)

	frames_to_movie('output/DCE/C134vC135.mp4', framerate=1)

if test == 11:
	dir1, base1 = 'datasets/time_series/C134C', '-C134C.txt'  # numerical index goes in front of base
	dir2, base2 = "datasets/time_series/C135B", '-C135B.txt'

	out_filename = 'output/DCE/C134vC135_fontsize.mp4'

	compare_multi(
		dir1, base1,
		dir2, base2,

		i_lims=(49, 50), 			 	# specify note range

		embed_crop_1='auto',		 	# seconds or 'auto'
		embed_crop_2='auto',  			# seconds or 'auto'
		auto_crop_length=.05, 			# seconds for when embed_crop = 'auto'

		tau_1='auto detect', 			# seconds 'auto detect' or 'auto ideal'. note 'auto detect' is considerably slower that 'auto ideal'
		tau_2=.01192,
		tau_T=math.pi,  				# for auto tau. tau = period * tau_T

		normalize_volume=True,

		save_worms=True,  				# to output/DCE/saved_worms
		save_movie=True,  				# False for faster worm creation

		waveform_zoom = out_filename

	)

	frames_to_movie(out_filename, framerate=1)

	plot_waveform_zoom_only(

		'datasets/time_series/C135B/49-C135B.txt',		# in filename
		'output/DCE/time_series_zoom.png',				# out filename

		embed_crop='auto',
		auto_crop_length=.05,
	)

print("time elapsed: %d seconds" % (time.time() - start_time))

# PARAMETER TEST CASES 5/3/17 #
#################################################################
#  tau: auto ideal		crop: explicit	  #             #
#  tau: auto ideal		crop: auto        #             #
#  tau: auto detect		crop: explicit    #             #
#  tau: auto detect		crop: auto        #             #
#  tau: explicit		crop: explicit    #             #
#  tau: explicit		crop: auto        #             #
#################################################################