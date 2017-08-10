import sys, time
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np

from ROC import PRF_vs_FFT_v2
from config import default_filtration_params as filt_params
from DCE.DCE import embed
from PH import Filtration, make_movie, load_saved_filtration
from PubPlots import plot_filtration_pub, plot_PD_pub, plot_waveform_sec, plot_dce_pub
from Tools import normalize_volume, sec_to_samp


piano_sig = np.loadtxt('datasets/time_series/C135B/49-C135B.txt')

piano_traj = embed(
	piano_sig,
	tau=.001216,		# T / pi
	m=2,
	crop=(1.72132, 1.7679),
	time_units='seconds',
	normalize_crop=True,
)


# paper_path = '/home/elliott/programming/phets_notes/IDA 2017/figs/final/'
paper_path = '/home/elliott/Dropbox/Data and Topology/Papers/IDA 2017/figs/'
ticks = [-1, -.33, .33, 1]
# ticks = None


def	fig1():
	print 'figure 1...'
	# figure 1a, 1b
	# add time (s) label
	fig = plt.figure(figsize=(10, 3), tight_layout=True, dpi=600)

	gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])

	ax1 = fig.add_subplot(gs[0])
	ax2 = fig.add_subplot(gs[1])

	plot_waveform_sec(
		ax1,
		piano_sig,
		crop=(1.72132, 1.77132),
		label='(a)',
		normalize_crop=True,
		yticks=ticks
	)

	plot_dce_pub(
		ax2,
		piano_traj,
		ticks=ticks,
		label='(b)'
	)

	plt.savefig(paper_path + 'fig1.png')



def fig2():
	print 'figure 2...'
	# figure 2a, 2b, 2c

	fig = plt.figure(figsize=(10, 3.5), tight_layout=True, dpi=700)
	ax1 = fig.add_subplot(131)
	ax2 = fig.add_subplot(132)
	ax3 = fig.add_subplot(133)

	# 2a #

	filt_params.update(
		{
			'ds_rate': 1,
			'worm_length': 2000,
			'min_filtration_param': .001,
			'max_filtration_param': .073222,
			'num_divisions': 2,
			'use_cliques': False
		})

	filtration = Filtration(piano_traj, filt_params)

	plot_filtration_pub(
		filtration, 2,
		ax1,
		landmark_size=3,
		line_width=.3,
		show_eps=False,
		label='(a)',
		ticks=ticks
	)

	# 2b #

	filt_params.update(
		{
			'ds_rate': 10,
			'worm_length': 2000,
			'min_filtration_param': .001,
			'max_filtration_param': .073222,
			'num_divisions': 2,
			'use_cliques': False,
		})

	filtration = Filtration(piano_traj, filt_params)

	plot_filtration_pub(
		filtration, 2,
		ax2,
		landmark_size=5,
		show_eps=False,
		label='(b)',
		ticks=ticks,

	)

	# 2c #

	filt_params.update(
		{
			'ds_rate': 40,
			'worm_length': 2000,
			'min_filtration_param': .001,
			'max_filtration_param': .073222,
			'num_divisions': 2,
			'use_cliques': False,
		})

	filtration = Filtration(piano_traj, filt_params)

	plot_filtration_pub(
		filtration, 2,
		ax3,
		landmark_size=10,
		show_eps=False,
		label='(c)',
		ticks=ticks,
	)

	plt.savefig(paper_path + 'fig2.png')


def fig3():
	print 'figure 3...'
	# figures 3a, 3b, 3c, 3d

	filt_params.update(
		{
			'ds_rate': 10,
			'worm_length': 2000,
			'min_filtration_param': 0,
			'max_filtration_param': -20,
			'num_divisions': 10,
			'use_cliques': False,
		})

	filtration = Filtration(piano_traj, filt_params)

	fig = plt.figure(figsize=(8.5, 7.5), tight_layout=True, dpi=700)
	ax1 = fig.add_subplot(221)
	ax2 = fig.add_subplot(222)
	ax3 = fig.add_subplot(223)
	ax4 = fig.add_subplot(224)

	plot_filtration_pub(
		filtration, 1, ax1,
		label='(a) $\epsilon \\approx 0.013$',
		show_eps=False,
		ticks=ticks,
	)

	plot_filtration_pub(
		filtration, 2, ax2,
		label='(b) $\epsilon \\approx 0.025$',
		show_eps=False,
		ticks=ticks
	)

	plot_filtration_pub(
		filtration, 4, ax3,
		label='(c) $\epsilon  \\approx 0.050$',
		show_eps=False,
		ticks=ticks
	)

	plot_PD_pub(filtration, ax4, label='(d)')

	plt.savefig(paper_path + 'fig3.png')





def fig4():
	print 'figure 4...'
	# figures 4a, 4b, 4c, 4d

	# ticks, labels (with epsilon in filt frames)

	fig = plt.figure(figsize=(8.5, 7.5), tight_layout=True, dpi=700)
	ax1 = fig.add_subplot(221)
	ax2 = fig.add_subplot(222)
	ax3 = fig.add_subplot(223)
	ax4 = fig.add_subplot(224)

	# CLARINET #

	sig = np.loadtxt('datasets/time_series/clarinet/sustained/high_quality/40-clarinet-HQ.txt')
	traj = embed(sig, tau=32, m=2, time_units='samples', crop=(100000, 102205), normalize_crop=True)

	filt_params.update(
		{
			'ds_rate': 20,
			'worm_length': 2000,
			'min_filtration_param': 0,
			'max_filtration_param': -20,
			'num_divisions': 10,

		})

	filtration = Filtration(traj, filt_params)

	plot_filtration_pub(filtration, 4, ax1,
						label='(a) $\epsilon  \\approx 0.099$',
						ticks=ticks,
						show_eps=False
						)
	plot_PD_pub(filtration, ax3, label='(c)')


	# VIOL #

	sig = np.loadtxt('datasets/time_series/viol/40-viol.txt')
	traj = embed(sig, tau=32, m=2, time_units='samples', crop=(50000, 52205), normalize_crop=True)

	filt_params.update(
		{
			'ds_rate': 20,
			'worm_length': 2000,
			'min_filtration_param': 0,
			'max_filtration_param': -20,
			'num_divisions': 10,

		})

	filtration = Filtration(traj, filt_params)

	plot_filtration_pub(filtration, 4, ax2,
						label='(b) $\epsilon  \\approx 0.114$',
						ticks=ticks,
						show_eps=False
						)
	plot_PD_pub(filtration, ax4, label='(d)')


	plt.savefig(paper_path + 'fig4.png')



def fig5():
	print 'figure 5...'
	# small tau
	# what kind of threshold to use???
	# include FFTs?
	filt_params.update(
		{
			'max_filtration_param': -20,
			'num_divisions': 10,
			# 'use_cliques': True,
		}
	)

	PRF_vs_FFT_v2(
		'datasets/time_series/clarinet/sustained/high_quality/40-clarinet-HQ.txt',
		'datasets/time_series/viol/40-viol.txt',
		paper_path + 'fig5.png',

		'clarinet',
		'viol',

		crop_1=(75000, 180000),
		crop_2=(35000, 140000),

		tau=32,  # samples
		m=2,

		window_length=2033,
		num_windows=50,
		num_landmarks=100,
		FT_bins=2000,
		FT_bin_mode='log',
		k=(0, 10, .01),  # min, max, int
		load_saved_filts=True,
		normalize_volume=True

	)

from DCE.Plots import plot_signal


def fig6():
	print 'figure 6...'

	tau = 54

	c1 = 50000
	l = 2000
	crop = (c1, c1 + l + tau + 1)


	fig = plt.figure(figsize=(8.5, 3.5), tight_layout=True, dpi=700)
	ax1 = fig.add_subplot(121)
	ax2 = fig.add_subplot(122)

	ticks = [0, .05, .1, .15, .2]

	# figure 6a, PD upright piano #
	sig = np.loadtxt('datasets/time_series/piano_revisit/C144F/a440/07-consolidated.txt')
	# plot_signal(paper_path + 'fig6a_sig.png', sig, crop=crop, time_units='samples')

	crop_a = sec_to_samp((1.603, 1.653))
	traj = embed(sig, tau=tau, m=2, time_units='samples',
				 crop=crop_a, normalize_crop=True)

	filt_params.update(
		{
			'ds_rate': 20,
			'worm_length': 2000,
			'min_filtration_param': 0,
			'max_filtration_param': -20,
			'num_divisions': 10,
			'use_cliques': False

		})

	filtration = Filtration(traj, filt_params)
	plot_PD_pub(filtration, ax1, label='(a)', cbar=False)
	# plot_filtration_pub(filtration, 5, paper_path + 'fig6a_filt.png')
	# make_movie(filtration, paper_path + 'fig6amovie.mp4')


	# figure 6b, PD grand piano #


	sig = np.loadtxt('datasets/time_series/piano_revisit/C134C/a440/07- C134C-consolidated.txt')
	# plot_signal(paper_path + 'fig6b_sig.png', sig, crop=crop, time_units='samples')
	crop_b = sec_to_samp((1.966, 2.016))
	traj = embed(sig, tau=tau, m=2, time_units='samples',
				 crop=crop_b, normalize_crop=True)

	filt_params.update(
		{
			'ds_rate': 20,
			'worm_length': 2000,
			'min_filtration_param': 0,
			'max_filtration_param': -20,
			'num_divisions': 10,
			'use_cliques': False

		})

	filtration = Filtration(traj, filt_params)
	plot_PD_pub(filtration, ax2, label='(b)', cbar=True)
	# plot_filtration_pub(filtration, 5, paper_path + 'fig6b_filt.png')
	# make_movie(filtration, paper_path + even'fig6bmovie.mp4')

	plt.savefig(paper_path + 'fig6.png')


if __name__ == '__main__':
	pass
	# fig1()
	# fig2()
	# fig3()
	# fig4()
	# fig5()
	fig6()
