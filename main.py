import os
import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

import Brightness_Correction as BC


SOURCE_DIR = './source'
OUTPUT_DIR = './output'
EXTENSIONS = set(["bmp", "jpeg", "jpg", "png", "tif", "tiff"])


if __name__ == "__main__":

	if not os.path.exists(OUTPUT_DIR):
		os.makedirs(OUTPUT_DIR)

	for root, subdirectories, files in os.walk(SOURCE_DIR):
		for file in files:

			# File name
			print os.path.join(root, file)
			image = cv2.imread(os.path.join(root, file))
			print "Image shape: {}".format(image.shape)
			
			# BGR Histogram
			histogram = BC.createHistogram(image)
			graph = BC.drawHistogram(histogram)
			graph.title("%s Histogram" % file)
			graph.savefig(os.path.join(OUTPUT_DIR, '%s_Hist.jpg' % file))

			# Combine image layers
			joinedlayers = BC.joinLayers(image)
			print "Joined layers shape: {}".format(joinedlayers.shape)

			# Joined Histogram
			joined_hist = BC.createJoinedHistogram(joinedlayers)
			joinedhistgraph = BC.drawHistogram([joined_hist])
			joinedhistgraph.savefig(os.path.join(OUTPUT_DIR, '%s_Comb_Hist.jpg' % file))

			# Find target range
			start, end = BC.findRange(joined_hist, .10)
			print "90%% of pixels lie between %d and %d" % (start, end)

			# Rescale brightness linearly
			print "Scaling images to between {} and {}".format(start, end)
			rescaled = BC.linearRescale(image, joinedlayers, start, end)
			cv2.imwrite(os.path.join(OUTPUT_DIR, '%s_LinearScaling.jpg' % file), rescaled)
			print "Min val: {} \t Max val: {}".format(np.min(rescaled), np.max(rescaled))