from boilerplate import change_dir, get_test
change_dir()

from signals import TimeSeries, Trajectory
from prfstats import *
from config import default_filtration_params as filt_params
from utilities import idx_to_freq, generate_label
import sys

test_num = 21412
test_label = ''

if len(sys.argv) == 3:
    test_num = int(sys.argv[1]);
    test_label = sys.argv[2];
    generate_label(test_label);

test, start_time = get_test(set_test=test_num)


def out_fname(t='png'):
	return 'output/prfstats/test_{}.{}'.format(test, t)


if test == 1:

	ts1 = TimeSeries(
		'datasets/time_series/clarinet/sustained/high_quality/40-clarinet-HQ.txt',
		crop=(75000, 180000),
		num_windows=50,
		window_length=2000,
		vol_norm=(0, 0, 1)  # (full, crop, windows)
	)


	ts2 = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=50,
		window_length=2000,
		vol_norm=(0, 0, 1)
	)

	ts1.plot_full('output/prfstats/ts1.png')
	ts2.plot_full('output/prfstats/ts2.png')

	traj1 = ts1.embed(tau=32, m=2)
	traj2 = ts2.embed(tau=32, m=2)


	filt_params.update({
		'max_filtration_param': -21,
		'num_divisions': 20,
		'ds_rate': 20
	})

	plot_rocs(
		traj1, traj2,
		out_fname(),
		filt_params,
		k=(0, 5.01, .01),
		load_filts=False,
		quiet=False,
		samples=2
	)


if test == 2:
	# testing the vary_param capabilities #

	ts1 = TimeSeries(
		'datasets/time_series/clarinet/sustained/high_quality/40-clarinet-HQ.txt',
		crop=(75000, 180000),
		num_windows=10,
		window_length=2000,
		vol_norm=(0, 0, 1)
	)

	ts2 = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=2000,
		vol_norm=(0, 0, 1)
	)

	traj1 = ts1.embed(tau=32, m=2)
	traj2 = ts2.embed(tau=32, m=2)

	filt_params.update({
		'ds_rate': 200,
		'num_divisions': 10,
	})

	plot_rocs(
		traj1, traj2,
		out_fname(),
		filt_params,
		k=(0, 5.01, .01),
		load_filts=False,
		quiet=True,
		vary_param=('max_filtration_param', (-3, -6)),
		samples=5

	)



if test == 3:
	# testing the vary_param capabilities #

	traj1 = Trajectory(
		'datasets/trajectories/L63_x_m2/L63_x_m2_tau35.txt',
		crop=(100, 9100),
		num_windows=5,
		window_length=1500,
		vol_norm=(0, 0, 1)      # (full, crop, window)
	)

	traj2 = Trajectory(
		'datasets/trajectories/L63_x_m2/L63_x_m2_tau50.txt',
		crop=(100, 9100),
		num_windows=5,
		window_length=1500,
		vol_norm=(0, 0, 1)
	)

	filt_params.update({
		'ds_rate': 200,
		'num_divisions': 10,
	})

	plot_rocs(
		traj1, traj2,
		out_fname(),
		filt_params,
		k=(0, 5.01, .01),
		load_filts=False,
		quiet=True,
		vary_param=('max_filtration_param', (-3, -6)),
		samples=5

	)


if test == 4:

	traj1 = Trajectory(
		'datasets/trajectories/L63_x_m2/L63_x_m2_tau35.txt',
		crop=(100, 9100),
		num_windows=5,
		window_length=1500,
		vol_norm=(0, 0, 1)      # (full, crop, window)
	)

	traj2 = Trajectory(
		'datasets/trajectories/L63_x_m2/L63_x_m2_tau50.txt',
		crop=(100, 9100),
		num_windows=5,
		window_length=1500,
		vol_norm=(0, 0, 1)
	)

	filt_params.update({
		'ds_rate': 200,
		'num_divisions': 10,
		'max_filtration_param': -5
	})

	plot_dists_to_means(
		traj1, traj2,
		out_fname(),
		filt_params,
		quiet=False
	)

if test == 5:

	ts1 = TimeSeries(
		'datasets/time_series/clarinet/sustained/high_quality/40-clarinet-HQ.txt',
		crop=(1, 2),
		num_windows=5,
		window_length=.01,
		vol_norm=(0, 1, 1),      # (full, crop, window)
		time_units='seconds'
	)

	ts2 = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(1, 2),
		num_windows=5,
		window_length=.01,
		vol_norm=(0, 1, 1),
		time_units='seconds'
	)

	tau = (1 / idx_to_freq(40)) / np.e
	traj1 = ts1.embed(tau=tau, m=2)
	traj2 = ts2.embed(tau=tau, m=2)

	filt_params.update({
		'ds_rate': 20,
		'num_divisions': 10,
		'max_filtration_param': -5
	})

	plot_dists_to_means(
		traj1, traj2,
		out_fname(),
		filt_params,
		quiet=False,
		samples={'interval': 1, 'filt_step': 5}
	)


if test == 6:

	ts1 = TimeSeries(
		'datasets/time_series/clarinet/sustained/high_quality/40-clarinet-HQ.txt',
		crop=(1, 2),
		num_windows=5,
		window_length=.01,
		vol_norm=(0, 1, 1),      # (full, crop, window)
		time_units='seconds'
	)

	ts2 = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(1, 2),
		num_windows=5,
		window_length=.01,
		vol_norm=(0, 1, 1),
		time_units='seconds'
	)

	tau = (1 / idx_to_freq(40)) / np.e
	traj1 = ts1.embed(tau=tau, m=2)
	traj2 = ts2.embed(tau=tau, m=2)

	filt_params.update({
		'ds_rate': 20,
		'num_divisions': 10,
		'max_filtration_param': -5
	})

	plot_clusters(
		traj1, traj2,
		out_fname(),
		filt_params,
		quiet=False,
		load_filts=True
	)


if test == 7:

	filt_params.update({
		'max_filtration_param': -10,
		'num_divisions': 10,
		'ds_rate': 500
	})

	plot_dists_to_ref(
		'datasets/trajectories/L63_x_m2/L63_x_m2_tau{}.txt',
		out_fname(),
		filt_params,
		i_ref=15,
		i_arr=np.arange(2, 30, 3),
		quiet=False,
		# save_filts='testing.npy',
		load_filts='testing.npy',
		samples={'interval': 5, 'filt_step': 5}
	)

if test == 9:
	# testing the vary_param capabilities #

	ts1 = TimeSeries(
		'datasets/time_series/clarinet/sustained/high_quality/40-clarinet-HQ.txt',
		crop=(75000, 180000),
		num_windows=10,
		window_length=2000,
		vol_norm=(0, 0, 1)
	)

	ts2 = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=2000,
		vol_norm=(0, 0, 1)
	)

	traj1 = ts1.embed(tau=32, m=2)
	traj2 = ts2.embed(tau=32, m=2)

	filt_params.update({
		'ds_rate': 100,
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_rocs(
		traj1, traj2,
		out_fname(),
		filt_params,
		k=(0, 5.01, .01),
		# save_filts=('testing1.npy', 'testing2.npy'),
		# load_filts=('testing1.npy', 'testing2.npy'),
		quiet=False,
		vary_param=('d_use_hamiltonian', (-1, 1)),
		samples=5

	)

if test == 10:

	ts = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=2000,
		vol_norm=(0, 0, 1)
	)

	traj = ts.embed(tau=32, m=2)
	filt_params.update({
		'ds_rate': 100,
		'num_divisions': 10,
		'max_filtration_param': -8
	})


	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', np.arange(80, 150, 10)),
		quiet=False,
		annot_hm=False,
		load_filts=False
	)


if test == 11:
	ts = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=2000,
		vol_norm=(0, 0, 1)
	)

	traj = ts.embed(tau=32, m=2)
	filt_params.update({
		'ds_rate': 100,
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', np.arange(80, 150, 10)),
		vary_param_2=('max_filtration_param', (-5, -6, -7)),
		quiet=False,
		annot_hm=False,
		load_filts=False
	)

if test == 12:

	traj = None
	traj = Trajectory(
		'datasets/Lorenz/StandardLorenz63_IC123.txt',
		crop=(10000, 150000),
		num_windows=10,
		window_length=10500
	)

	filt_params.update({
		'ds_rate': 10,
		'num_divisions': 10,
	})

	dists = pairwise_mean_dists(
		traj,
		filt_params,
		vary_param_1=('worm_length', (200, 500, 700)),
		vary_param_2=('max_filtration_param', (-5, -8, -12)),
		quiet=True,
		load_filts=False,
		samples={'interval': 4, 'filt_step': 5}
	)

	np.savetxt(out_fname(t='txt'), dists)


if test == 13:
	ts = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=2000,
		vol_norm=(0, 0, 1)
	)

	traj = ts.embed(tau=32, m=2)
	filt_params.update({
		'ds_rate': -20,
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (1000, 1300, 1700, 2000)),
		quiet=False,
		annot_hm=False,
		load_filts=False,
		samples={'interval': 4, 'filt_step': 5}
	)

if test == 14:
	ts = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=2000,
		vol_norm=(0, 0, 1)
	)

	traj = ts.embed(tau=32, m=2)
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 20),   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (1000, 1300, 1700, 2000)),
		quiet=False,
		annot_hm=False,
		load_filts=False,
		samples={'interval': 4, 'filt_step': 5}
	)

# start Nikki tests: 
if test == 15:
	ts = TimeSeries(
		'datasets/time_series/viol/49-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(0, 0, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
if test == 16:
	ts = TimeSeries(
		'datasets/time_series/viol/49-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(0, 0, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 200),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
	
if test == 17:
	ts = TimeSeries(
		'datasets/time_series/clarinet/40-clarinet.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(0, 0, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
## Nikki 12/12: Start of Tests to Match Joe's
	
if test == 18:
	ts = TimeSeries(
		'datasets/time_series/clarinet/40-clarinet.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(0, 0, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 200),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
if test == 19:
	ts = TimeSeries(
		'datasets/time_series/Clarinet/short/49-clarinet.txt',
		crop=(3000, 10000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
if test == 20:
	ts = TimeSeries(
		'datasets/time_series/Clarinet/short/49-clarinet.txt',
		crop=(3000, 10000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 200),  # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	

# Nikki 12/11: weird, when i ran test 18 the downsample rate to (roughly) constant landmarks worked (need to fix crop) but when i ran test 20 it didn't seem to, or maybe it was also the dat itself? :/ print statements in terminal also seemed suggestive

# Nikki 12/12: new crop to see if weird data and try to fix tests

if test == 21:
	ts = TimeSeries(
		'datasets/time_series/Clarinet/short/49-clarinet.txt', # This data is only:  raise CropError(err.format(len(self.data_full)))
#signals.signals.CropError: crop out of bounds. len(self.data_full) == 15197 <- this long
		crop=(1000, 14000),
		num_windows=10,
		vol_norm=(0, 0, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 200),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
# N: getting some "zero speed" comments from find_landmarks.c (doesn't directly effect our plots yet but should check out data - pre and post embedding)
	
	# N: 59-clarinet-HQ, redo for new data - that might have been too short? though the intervals just should have overlapped - either way, confusing

if test == 22:
	ts = TimeSeries(
		'datasets/time_series/Clarinet/sustained/high_quality/59-clarinet-HQ.txt',
		crop=(10000, 120000),
		num_windows=10,
		vol_norm=(1, 1, 1),
		window_length=10000,
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 200),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	

if test == 23:
	ts = TimeSeries(
		'datasets/time_series/Clarinet/sustained/high_quality/59-clarinet-HQ.txt',
		crop=(10000, 120000),
		num_windows=10,
		vol_norm=(1, 1, 1),
		window_length=10000,
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30, 50, 100, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
		
# N: ran fine, re-running 20 with only 1 window to see if issue was amount of data - seems like it was cause this ran :/

if test == 24:
	ts = TimeSeries(
		'datasets/time_series/Clarinet/short/49-clarinet.txt',
		crop=(1000, 12000),
		num_windows=2,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 200),  # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
# N: 4 other tests of method: 40-C135B, 40-C134C, 49-C135B, 49-C134C

if test == 25:
	ts = TimeSeries(
		'datasets/time_series/C135B/40-C135B.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

if test == 26:
	ts = TimeSeries(
		'datasets/time_series/C135B/40-C135B.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 200),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
if test == 27:
	ts = TimeSeries(
		'datasets/time_series/C134C/40-C134C.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

if test == 28:
	ts = TimeSeries(
		'datasets/time_series/C134C/40-C134C.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 200),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
if test == 29:
	ts = TimeSeries(
		'datasets/time_series/C135B/49-C135B.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

if test == 30:
	ts = TimeSeries(
		'datasets/time_series/C135B/49-C135B.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 200),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
if test == 31:
	ts = TimeSeries(
		'datasets/time_series/C134C/49-C134C.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

if test == 32:
	ts = TimeSeries(
		'datasets/time_series/C134C/49-C134C.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 200),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)	

# 12/12 Nikki Test Lorenz 63; and Rossler (need to generate data)
	
if test == 33:

	traj = Trajectory(
		'datasets/trajectories/REALDEAL/L63_full_IC123.txt',
		crop=(10000, 201500),
		num_windows=5,
		window_length=200000,
		vol_norm=(1, 1, 1)      # (full, crop, window)
	)
	
	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

if test == 34:  # Dependent on test = 33 , not default 200
	traj = Trajectory(
		'datasets/trajectories/REALDEAL/L63_full_IC123.txt',
		crop=(10000, 201500),
		num_windows=5,
		window_length=200000,
		vol_norm=(1, 1, 1)      # (full, crop, window)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100), 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (100,200, 500, 1000, 1500, 2000, 3000, 5000, 8000, 12000, 16000)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

##### N: Repeat Joe's experiment with my numbers and my computer	

if test == 35:
	ts = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

if test == 36:
	ts = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 200),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
## 12/14 Nikki: Repeat Joe experiment with his numbers

if test == 37:
	ts = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'worm_length': 2000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (2, 3, 4, 5, 6, 10, 20, 26,40, 45, 50, 57,66,80,100,133,200)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)	

## 12/15 Nikki: Test Less Landmarks on 40-viol, and another one or two - start running MATLAB code and pulling together full story
if test == 38:
	ts = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (100, 200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
	
if test == 39:
	ts = TimeSeries(
		'datasets/time_series/clarinet/40-clarinet.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (100,200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
if test == 40:
	ts = TimeSeries(
		'datasets/time_series/C135B/40-C135B.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 60),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (60, 120, 200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
## 12/15 Nikki: Do methodology on Neuron Data

if test == 41:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I4G6_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		window_length=200000,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
		
	)

	
if test == 42:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I4G6_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
	
if test == 43:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I2G3_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		window_length=200000,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
		
	)

	
if test == 44:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I2G3_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
	
if test == 45:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I2G5_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		window_length=200000,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
		
	)

	
if test == 46:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I2G5_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 30),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
	
if test == 47:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I1G4p5_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		window_length=200000,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('ds_rate', (1, 10, 15, 20, 30,50, 100, 150, 200, 300)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
		
	)

	
if test == 48:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I1G4p5_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 60),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
## 12/20 Nikki Tests: Pairwise distances for Music and Neuron Data

if test == 49:

	
	ts = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100),
		'num_divisions': 10,
		'max_filtration_param': -8,
	})


	dists = pairwise_mean_dists(
		traj,
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('d_use_hamiltonian', (1, -2)),
		quiet=True,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	np.savetxt(out_fname(t='txt'), dists)
	

if test == 50:

	
	ts = TimeSeries(
		'datasets/time_series/clarinet/40-clarinet.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'num_divisions': 10,
		'max_filtration_param': -8,
		'ds_rate': ('worm_length', lambda x: x / 100)
	})


	dists = pairwise_mean_dists(
		traj,
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('d_use_hamiltonian', (1, -1.1)),
		quiet=True,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	np.savetxt(out_fname(t='txt'), dists)
	
if test == 51:

	
	ts = TimeSeries(
		'datasets/time_series/C135B/40-C135B.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'num_divisions': 10,
		'max_filtration_param': -8,
		'ds_rate': ('worm_length', lambda x: x / 100)
	})


	dists = pairwise_mean_dists(
		traj,
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('d_use_hamiltonian', (1, -2)),
		quiet=True,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	np.savetxt(out_fname(t='txt'), dists)
	
if test == 52:

	
	ts = TimeSeries(
		'datasets/time_series/C134C/40-C134C.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'num_divisions': 10,
		'max_filtration_param': -8,
		'ds_rate': ('worm_length', lambda x: x / 100)
	})


	dists = pairwise_mean_dists(
		traj,
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('d_use_hamiltonian', (1, -2)),
		quiet=True,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	np.savetxt(out_fname(t='txt'), dists)
	
if test == 53:

	
	ts = TimeSeries(
		'datasets/time_series/C135B/49-C135B.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'num_divisions': 10,
		'max_filtration_param': -8,
		'ds_rate': ('worm_length', lambda x: x / 100)
	})


	dists = pairwise_mean_dists(
		traj,
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('d_use_hamiltonian', (1, -2)),
		quiet=True,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	np.savetxt(out_fname(t='txt'), dists)
	
if test == 54:

	
	ts = TimeSeries(
		'datasets/time_series/C134C/49-C134C.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'num_divisions': 10,
		'max_filtration_param': -8,
		'ds_rate': ('worm_length', lambda x: x / 100)
	})


	dists = pairwise_mean_dists(
		traj,
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('d_use_hamiltonian', (1, -2)),
		quiet=True,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	np.savetxt(out_fname(t='txt'), dists)
	
if test == 55:

	
	ts = TimeSeries(
		'datasets/time_series/viol/49-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=53, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'num_divisions': 10,
		'max_filtration_param': -8,
		'ds_rate': ('worm_length', lambda x: x / 100)
	})


	dists = pairwise_mean_dists(
		traj,
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('d_use_hamiltonian', (1, -2)),
		quiet=True,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	np.savetxt(out_fname(t='txt'), dists)
	
if test == 56:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I1G4p5_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 60),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -8
	})
	
	dists = pairwise_mean_dists(
		traj,
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('d_use_hamiltonian', (1, -2)),
		quiet=True,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	np.savetxt(out_fname(t='txt'), dists)
	
	
if test == 57:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I2G3_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -8
	})
	
	dists = pairwise_mean_dists(
		traj,
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('d_use_hamiltonian', (1, -2)),
		quiet=True,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	np.savetxt(out_fname(t='txt'), dists)
	
	
if test == 58:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I2G5_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 30),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -8
	})
	
	dists = pairwise_mean_dists(
		traj,
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('d_use_hamiltonian', (1, -2)),
		quiet=True,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	np.savetxt(out_fname(t='txt'), dists)
	
	
if test == 59:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I4G6_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100),  
		'num_divisions': 10,
		'max_filtration_param': -8
	})
	
	dists = pairwise_mean_dists(
		traj,
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('d_use_hamiltonian', (1, -2)),
		quiet=True,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	np.savetxt(out_fname(t='txt'), dists)
	
	
##### 1/3 Nikki Wed tests:


if test == 60:  # NEED TO RUN 

	traj1 = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I4G6_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=20,
		vol_norm=(1, 1, 1)
	)
	
	traj2 = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I2G3_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'worm_length': 2000,
		'ds_rate': ('worm_length', lambda x: x / 100),    
		'num_divisions': 10,
		'max_filtration_param': -10
	})
		
	plot_l2rocs(
		traj1, traj2,
		out_fname(),
		filt_params,
		k=(0, 5.01, .01),
		load_saved_filts=False,
		vary_param=('d_use_hamiltonian',(1,-1.01,-1.1,-1.5,-2,-10)),
		quiet=False,
		see_samples=2
	)

if test == 61: # CURRENTLY RUNNING 

	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I4G6_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		window_length=200000,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100),    # note: '/' does floor division
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1100, 1400, 1700,2000,2300,2600,2900,3200,3500,3800,4100,4400,4700,5000)),
		vary_param_2 = ('d_use_hamiltonian', (1, -1.01, -1.1, -1.5, -2)),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
		)


## TESTING 3D PLOT CODE

if test == 62:  

	traj = Trajectory(
		'datasets/Lorenz/StandardLorenz63_IC123.txt',
		crop=(10000, 150000),
		num_windows=4,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'num_divisions': 10,
		'max_filtration_param': -8
	})
	
	norms = toward_3D_plot(traj,
		filt_params,
		vary_param_1=('worm_length', (200,500,1000)),
		vary_param_2 = ('ds_rate', (('worm_length', lambda x: x / 10),('worm_length',lambda x: x / 100))),
		weight_func=lambda i, j: 1,
		see_samples=False,
		quiet=True,
		load_saved_filts=False
		)
		
	np.savetxt(out_fname(t='txt'), norms)	
		
if test == 63:  

	traj = Trajectory(
		'datasets/Lorenz/StandardLorenz63_IC123.txt',
		crop=(10000, 150000),
		num_windows=5,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'num_divisions': 10,
		'max_filtration_param': -8
	})
	
	norms = toward_3D_plot(traj,
		filt_params,
		vary_param_1=('worm_length', (2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 20000 )),
		vary_param_2 = ('ds_rate', (('worm_length', lambda x: x / 10), ('worm_length', lambda x: x / 25),('worm_length', lambda x: x / 50), ('worm_length', lambda x: x / 100), ('worm_length', lambda x: x / 150),('worm_length', lambda x: x / 200), ('worm_length', lambda x: x / 300),('worm_length', lambda x: x / 500),('worm_length', lambda x: x / 800), ('worm_length', lambda x: x / 1200),('worm_length', lambda x: x / 2000))),
		weight_func=lambda i, j: 1,
		see_samples=False,
		quiet=True,
		load_saved_filts=False
		)
		
	np.savetxt(out_fname(t='txt'), norms)
	
if test == 64:  

	traj = Trajectory(
		'datasets/Lorenz/StandardLorenz63_IC123.txt',
		crop=(10000, 150000),
		num_windows=5,
		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'num_divisions': 10,
		'max_filtration_param': -8
	})
	
	norms = toward_3D_plot(traj,
		filt_params,
		vary_param_1=('worm_length', (22000, 24000, 26000, 28000, 30000, 32000, 34000, 36000, 38000, 40000 )),
		vary_param_2 = ('ds_rate', (('worm_length', lambda x: x / 10), ('worm_length', lambda x: x / 25),('worm_length', lambda x: x / 50), ('worm_length', lambda x: x / 100), ('worm_length', lambda x: x / 150),('worm_length', lambda x: x / 200), ('worm_length', lambda x: x / 300),('worm_length', lambda x: x / 500),('worm_length', lambda x: x / 800), ('worm_length', lambda x: x / 1200),('worm_length', lambda x: x / 2000))),
		weight_func=lambda i, j: 1,
		see_samples=False,
		quiet=True,
		load_saved_filts=False
		)
		
	np.savetxt(out_fname(t='txt'), norms)

## 1/9: Nikki to re-run basic investigation of W and L on music and neurons with weight function

if test == 65:

	ts = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,

		window_length=5000,
		vol_norm=(0, 0, 1)
	)

	traj = ts.embed(tau=32, m=2)
	
	
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (100, 200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('FIGURE OUT SYNTAX FOR WEIGHT FUNCTION'),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
	
if test == 66:
	ts = TimeSeries(
		'datasets/time_series/clarinet/40-clarinet.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (100,200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('FIGURE OUT SYNTAX FOR WEIGHT FUNCTION'),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

if test == 67:
	ts = TimeSeries(
		'datasets/time_series/C135B/40-C135B.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 60),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (60, 120, 200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('FIGURE OUT SYNTAX FOR WEIGHT FUNCTION'),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
if test == 68:
	ts = TimeSeries(
		'datasets/time_series/C134C/40-C134C.txt',
		crop=(35000, 140000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2) # WHAT IS TAU CONVERSION? 1/ F*PI - here f = 261.2 b/c middle c instead of 440 = a,  ; F = 1/P3R ? ; F = 2^k-12? ; 
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 60),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (60, 120, 200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
			vary_param_2=('FIGURE OUT SYNTAX FOR WEIGHT FUNCTION'),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

if test == 69:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I4G6_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		window_length=200000,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'worm_length': 3000,   # note: '/' does floor division

		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('FIGURE OUT SYNTAX FOR WEIGHT FUNCTION'),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	
if test == 70:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I4G6_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('FIGURE OUT SYNTAX FOR WEIGHT FUNCTION'),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	

	
if test == 71:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I2G3_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 100),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('FIGURE OUT SYNTAX FOR WEIGHT FUNCTION'),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)

	
if test == 72:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I2G5_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 30),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('FIGURE OUT SYNTAX FOR WEIGHT FUNCTION'),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)
	
	
if test == 73:
	traj = Trajectory(
		'datasets/PHETS_NeuronVoltageDATA/I1G4p5_Exc_Avg_3thru7_dcem2t200.txt',
		crop=(10000, 240000),
		num_windows=10,
		vol_norm=(1, 1, 1)
	)

	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 60),   # note: '/' does floor division - ###!! FIGURING OUT FROM TEST ABOVE! :D HAI METHODOLOGY 
		'num_divisions': 10,
		'max_filtration_param': -10
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100)),
		vary_param_2=('FIGURE OUT SYNTAX FOR WEIGHT FUNCTION'),
		quiet=False,
		annot_hm=False,
		load_saved_filts=False,
		see_samples={'interval': 4, 'filt_step': 5}
	)	

if test == 21413:

	ts1 = TimeSeries(
		'datasets/time_series/Clarinet/40-clarinet.txt',
		crop=(35000, 140000),
		num_windows=2,

		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj1 = ts1.embed(tau=32, m=2)
	
	
	filt_params.update({
		'num_divisions': 10,
		'max_filtration_param': -5
	})
	
	ts2 = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,

		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj2 = ts2.embed(tau=32, m=2)
	
	
	filt_params.update({
		'num_divisions': 10,
		'max_filtration_param': -5,
		'worm_length': 4000,
	})


	plot_rocs(
		traj1, 
		traj2,
		out_fname(),
		filt_params,
		k= [0,5],
		vary_param=('ds_rate',(('worm_length', lambda x: x / 10), ('worm_length', lambda x: x / 25))),
	)

if test == 21412:

	ts = TimeSeries(
		'datasets/time_series/Clarinet/40-clarinet.txt',
		crop=(35000, 140000),
		num_windows=10,

		window_length=100000,
		vol_norm=(1, 1, 1)
	)

	traj = ts.embed(tau=32, m=2)
	
	
	filt_params.update({
		'num_divisions': 10,
		'max_filtration_param': -9
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		#vary_param_1=('worm_length', (101, 200, 500, 800, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600,3900, 4200,4500, 4800,5100)),
		vary_param_1=('worm_length', (101, 200, 500, 800)),
		vary_param_2=('ds_rate',(('worm_length', lambda x: x / 100),('worm_length', lambda x: x / 100))),
		weight_func=lambda i, j: 1,
		quiet=True,
		annot_hm=False,
		samples={'interval': 5}
	)
