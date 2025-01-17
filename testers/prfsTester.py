from boilerplate import change_dir, get_test
change_dir()

from signals import TimeSeries, Trajectory
from prfstats import *
from config import default_filtration_params as filt_params
from utilities import idx_to_freq

test, start_time = get_test(set_test=9)


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

if test == 15:
	ts = TimeSeries(
		'datasets/time_series/viol/40-viol.txt',
		crop=(35000, 140000),
		num_windows=10,
		window_length=5000,
		vol_norm=(0, 0, 1)
	)

	traj = ts.embed(tau=32, m=2)
	filt_params.update({
		'ds_rate': ('worm_length', lambda x: x / 50),
		'num_divisions': 10,
		'max_filtration_param': -8
	})

	plot_variance(
		traj,
		out_fname(),
		filt_params,
		vary_param_1=('worm_length', (3500, 4000, 4500, 5000)),
		quiet=False,
		load_filts=False,
	)


# no ops: 57.7s


