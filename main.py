import os
import sys
import cv2
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

			print os.path.join(root, file)
			image = cv2.imread(os.path.join(root, file))
			print image.shape
			histogram = BC.createHistogram(image)
			print len(histogram)
			# print histogram

			graph = BC.drawHistogram(histogram)
			graph.title("%s Histogram" % file)
			graph.savefig(os.path.join(OUTPUT_DIR, '%s_Hist.jpg' % file))

			combined_hist, combined_hist_plot = BC.joinHistLayers(histogram)
			combined_hist_plot.title("%s Color-Combined Histogram" % file)
			combined_hist_plot.savefig(os.path.join(OUTPUT_DIR, '%s_Comb_Hist.jpg' % file))

			start, end = BC.findRange(combined_hist, .10)
			print "90%% of pixels lie between %d and %d" % (start, end)