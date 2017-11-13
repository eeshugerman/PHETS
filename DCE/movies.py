from plots import slide_window_frame
from utilities import remove_old_frames, print_still, frames_to_movie


def slide_window(timeseries, m, tau, out_fname, framerate=1):
	traj = timeseries.embed(m=m, tau=tau)
	remove_old_frames('DCE/frames/')
	frame_fname = 'DCE/frames/frame%03d.png'

	for i in range(traj.num_windows):
		print_still('frame {} of {}'.format(i, traj.num_windows))
		slide_window_frame(traj, i, frame_fname % i)

	print ''
	frames_to_movie(out_fname, frame_fname,
	                framerate=framerate, loglevel='error')

	return traj
