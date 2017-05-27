import os
import sys
import time
import pickle
import subprocess

import numpy as np
import itertools

import BuildFiltration

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_saved_filtration():
	caller_dir = os.getcwd()
	os.chdir(SCRIPT_DIR)
	filtration = pickle.load(open('temp_data/filtration.p'))
	os.chdir(caller_dir)
	return filtration



import subprocess
from config import find_landmarks_c_compile_str
class Filtration:

	def __init__(self, in_filename, params, start=0):
		caller_dir = os.getcwd()
		os.chdir(SCRIPT_DIR)

		self.filename = caller_dir + '/' +  in_filename
		self.params = params

		arr = self._build(self.filename, params, start=0)

		self.witness_coords = arr[0]
		self.landmark_coords = arr[1]
		self.complexes = self._unpack_complexes(arr[2])
		self.epsilons = arr[3]

		self.ambient_dim = len(self.witness_coords[0])
		self.num_div = len(self.complexes)

		self.intervals = None
		self.PD_data = None
		self.PRF = None

		pickle.dump(self, open('temp_data/filtration.p', 'wb'))

		os.chdir(caller_dir)


	# private #
	def _build(self, sig, params, start=0):
		print "building filtration..."
		start_time = time.time()

		if isinstance(sig, basestring):			# is filename
			lines = open(sig).readlines()
			start_idx = int(len(lines) * start)
			worm = lines[start_idx:]
		else:									# is array
			start_idx = int(len(sig) * start)
			worm = sig[start_idx]

		open('temp_data/worm_data.txt', 'w').writelines(worm)

		try:
			filtration = BuildFiltration.build_filtration('temp_data/worm_data.txt', params)
		except OSError:
			print "WARNING: invalid PersistentHomology/find_landmarks binary. Recompiling..."

			if sys.platform == "linux" or sys.platform == "linux2":
				compile_str = find_landmarks_c_compile_str['linux']
			elif sys.platform == 'darwin':
				compile_str = find_landmarks_c_compile_str['macOS']
			else:
				print 'Sorry, PHETS requires linux or macOS.'
				sys.exit()

			subprocess.call(compile_str, shell=True)
			print "find_landmarks recompilation complete. Please repeat your test."
			sys.exit()


		witness_coords = filtration[1][1]
		landmark_coords = filtration[1][0]
		abstract_filtration = sorted(list(filtration[0]))
		epsilons = filtration[2]		# add to build_filtration return

		print("build_and_save_filtration() time elapsed: %d seconds \n" % (time.time() - start_time))
		return [witness_coords, landmark_coords, abstract_filtration, epsilons]

	def _unpack_complexes(self, filt_ID_list):

		def group_by_birth_time(ID_list):
			"""Reformats 1D list of SimplexBirth objects into 2D array of
			landmark_set lists, where 2nd index is  birth time (? see below)"""

			ID_array = []  # list of complex_at_t lists
			complex_at_t = []  # list of simplices with same birth_time
			i = 0
			time = 0
			list_length = len(ID_list)
			while i < list_length:
				birth_time = ID_list[i].birth_time
				if birth_time == time:
					complex_at_t.append(ID_list[i].landmark_set)
					if i == list_length - 1:
						ID_array.append(complex_at_t)
					i += 1
				else:
					ID_array.append(complex_at_t)
					complex_at_t = []
					time += 1
			return ID_array

		def expand_to_2simplexes(ID_array):
			"""for each k-simplex in filtration array, if k > 2, replaces with the
			component 2-simplexes(i.e. all length-3 subsets of landmark_ID_set) """
			for row in ID_array:
				expanded_row = []
				for landmark_ID_set in row:
					if len(landmark_ID_set) > 3:
						expanded_set = list(itertools.combinations(landmark_ID_set, 3))
					else:
						expanded_set = [list(landmark_ID_set)]
					# expanded_row.extend(expanded_set)		# flatten
					expanded_row.append(expanded_set)		# group by parent
				row[:] = expanded_row


			def count_triangles():
				print 'counting triangles...'
				num_tris=0
				count =0
				triangles=[]
				for i in ID_array:
					for j in i:
						if len(j)==3:
							tri=set(j)
							if tri not in triangles:
								triangles.append(tri)


				with open("PersistentHomology/output/num_triangles.txt","wb") as f:
					f.write("Number of triangles: "+str(len(triangles)))

		filt_ID_array = group_by_birth_time(filt_ID_list)	# 1d list -> 2d array
		expand_to_2simplexes(filt_ID_array)
		return filt_ID_array

	def _get_intervals(self):
		if self.intervals:
			return

		def build_perseus_in_file(filt_array):
			print 'building perseus_in.txt...'
			out_file = open('PersistentHomology/perseus/perseus_in.txt', 'a')
			out_file.truncate(0)
			out_file.write('1\n')
			for idx, row in enumerate(filt_array):
				for simplex in row:
					#   format for perseus...
					line_str = str(len(simplex) - 1) + ' ' + ' '.join(
						str(ID) for ID in simplex) + ' ' + str(idx + 1) + '\n'
					out_file.write(line_str)
			out_file.close()

		def call_perseus():

			os.chdir('PersistentHomology/perseus')

			if sys.platform == "linux" or sys.platform == "linux2":
				subprocess.call("./perseusLin nmfsimtop perseus_in.txt perseus_out", shell=True)

			elif sys.platform == "darwin":  # macOS
				subprocess.call("./perseusMac nmfsimtop perseus_in.txt perseus_out", shell=True)

			else:  # Windows
				subprocess.call("perseusWin.exe nmfsimtop perseus_in.txt perseus_out", shell=True)

		def load_perseus_out_file():
			try:
				self.intervals = np.loadtxt('PersistentHomology/perseus/perseus_out_1.txt', ndmin=1)
			except ValueError:
				print 'WARNING: no homology for', self.filename
				self.intervals = 'empty'

		build_perseus_in_file(self.complexes)
		call_perseus()
		load_perseus_out_file()

	def _build_PD_data(self):
		""" formats perseus output """
		if self.PD_data:
			return

		if self.intervals == 'empty':
			self.PD_data = 'empty'
			return

		birth_t, death_t = self.intervals
		epsilons = self.epsilons
		lim = np.max(epsilons)

		birth_e = []
		death_e = []

		timess = np.vstack([birth_t, death_t]).T
		for times in timess:
			if times[1] != - 1:
				birth_e.append(epsilons[int(times[0])])
				death_e.append(epsilons[int(times[1])])

		immortal_holes = []
		for i, death_time in np.ndenumerate(death_t):  # place immortal holes at [birth time, time lim]
			if death_time == -1:
				immortal_holes.append([epsilons[int(birth_t[i])], lim * .95])
		immortal_holes = np.array(immortal_holes)

		if len(immortal_holes):
			birth_e.extend(immortal_holes[:, 0])
			death_e.extend(immortal_holes[:, 1])

		try:
			count = np.zeros(len(birth_t))
		except TypeError:  # only one interval point
			count = [0]
		for i, pt in enumerate(zip(birth_e, death_e)):
			for scanner_pt in zip(birth_e, death_e):
				if pt == scanner_pt:
					count[i] += 1

		points = np.asarray([birth_e, death_e, count]).T
		points = np.vstack({tuple(row) for row in points})  # toss duplicates

		x, y, z = points[:, 0], points[:, 1], points[:, 2]

		self.PD_data = [x, y, z, lim]

	def _build_PRF(self, num_div):

		if self.PRF:
			return

		if self.PD_data == 'empty':
			print
			return [None, None, np.zeros([num_div, num_div]), None]

		x, y, z, max_lim = self.PD_data
		min_lim = 0

		x_ = y_ = np.linspace(min_lim, max_lim, num_div)
		xx, yy = np.meshgrid(x_, y_)

		pts = zip(x, y, z)
		grid_pts = zip(np.nditer(xx), np.nditer(yy))
		grid_vals = np.zeros(len(grid_pts))
		for i, grid_pt in enumerate(grid_pts):
			if grid_pt[0] <= grid_pt[1]:
				for pt in pts:
					if pt[0] <= grid_pt[0] and pt[1] >= grid_pt[1]:
						grid_vals[i] += pt[2]
			else:
				grid_vals[i] = np.nan
		grid_vals = np.reshape(grid_vals, xx.shape)

		self.PRF = [xx, yy, grid_vals, max_lim]


	# public #
	def get_complexes_mpl(self):

		def IDs_to_coords(ID_array):
			"""Replaces each landmark_ID with corresponding coordinates"""
			for row in ID_array:
				for parent_simplex in row:
					new_parent_simplex = []
					for child in parent_simplex:
						new_parent_simplex.append(list(child))
					for child in new_parent_simplex:
						new_child = []
						for landmark_ID in child:
							landmark_coords = self.landmark_coords[landmark_ID]
							new_child.append(landmark_coords)
						child[:] = new_child
					parent_simplex[:] = new_parent_simplex

		def flatten_rows(ID_array):
			for row in ID_array:
				new_row = []
				for parent in row:
					for child in parent:
						new_row.append(child)
				row[:] = new_row

		data = self.complexes
		IDs_to_coords(data)
		flatten_rows(data)		# if grouped by parent simplex
		return data

	def get_complexes_mayavi(self):

		def separate_by_k(array):
			lines = []
			triangles = []
			for row in array:
				lines_row = []
				triangles_row = []
				for simplex in row:
					if len(simplex) == 2:
						lines_row.append(simplex)
					else:  # if len(simplex) == 3:
						triangles_row.append(simplex)
				triangles.append(triangles_row)
				lines.append(lines_row)
			return [lines, triangles]

		return separate_by_k(self.complexes)

	def get_PD_data(self):
		self._get_intervals()	# calls perseus, sets self.intervals
		self._build_PD_data()	# sets self.PD_data, returns PD_data
		return self.PD_data

	def get_PRF(self, num_div):
		self._get_intervals()
		self._build_PD_data()
		self._build_PRF(num_div)
		return self.PRF

