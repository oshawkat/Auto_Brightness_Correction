import os
import sys
import cv2
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot as plt

import Brightness_Correction as BC


SOURCE_DIR = './source'
OUTPUT_DIR = './output'

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
			mask = np.full((image.shape[0], image.shape[1], 3), 255, dtype=np.uint8)
			cv2.imwrite(os.path.join(OUTPUT_DIR, '%s_color_mask.jpg' % file), mask)
			histogram = BC.createHistogram(image, mask)
			graph = BC.drawHistogram(histogram)
			graph.title("%s Histogram" % file)
			graph.savefig(os.path.join(OUTPUT_DIR, '%s_Hist.jpg' % file))

			# Combine image layers
			joinedlayers = BC.joinLayers(image)
			print "Joined layers shape: {}".format(joinedlayers.shape)

			# Joined Histogram
			mask = np.full(joinedlayers.shape, 255, dtype=np.uint8)
			im_mask =  joinedlayers >= 700
			mask[im_mask] = 0
			light_mask = mask
			im_mask = joinedlayers <= 45
			mask[im_mask] = 0
			dark_mask = mask
			cv2.imwrite(os.path.join(OUTPUT_DIR, '%s_joined_mask.jpg' % file), mask)
			joined_hist = BC.createJoinedHistogram(joinedlayers, mask)
			joinedhistgraph = BC.drawHistogram([joined_hist])
			joinedhistgraph.savefig(os.path.join(OUTPUT_DIR, '%s_Comb_Hist.jpg' % file))

			# Find target range
			start, end = BC.findRange(joined_hist, .00, .1)
			print "Target range is between %d and %d" % (start, end)

			# Rescale brightness
			print "Scaling images to between {} and {}".format(start, end)
			rescaled = BC.nonlinearRescale(image, joinedlayers, start, end, light_mask, dark_mask)
			cv2.imwrite(os.path.join(OUTPUT_DIR, '%s_Output.jpg' % file), rescaled)
			print "Min val: {} \t Max val: {}".format(np.min(rescaled), np.max(rescaled))

			# Create a Histogram for the output image
			output_hist = BC.createHistogram(rescaled, np.full(rescaled.shape, 255, dtype=np.uint8))
			draw_output_hist = BC.drawHistogram(output_hist)
			draw_output_hist.savefig(os.path.join(OUTPUT_DIR, '%s_Output_Hist.jpg' % file))

			print "\n"

	print "Processing Complete!"
