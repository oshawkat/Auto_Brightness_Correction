import cv2
import numpy as np
from matplotlib import pyplot as plt



# Construct a histogram for a given image
# Returns a list of 256 x 1 arrays, with one array for each color channel
# B/W pictures have a single array, color is ordered as BGR
def createHistogram(image):
	histogram = []

	for channel in range(image.shape[2]):
		hist = cv2.calcHist(image, [channel], None, [256], [0, 256])
		histogram.append(hist)
		
	return histogram



# Given a list of histograms, one for each color channel, return a plot of the histograms, all on one chart
def drawHistogram(histograms):

	colors = ('b', 'g', 'r')

	# Clear current plot before making any new ones
	plt.cla()
	plt.clf()

	# B/W images
	if len(histograms) == 1:
		plt.plot(histograms[0], color='k')	# plot the single graph with a black line
	else:
		for index in range(len(histograms)):
			plt.plot(histograms[index], color=colors[index])

	plt.xlim([0, 256])
	plt.title("Histogram")

	return plt


# Combine the histograms channels by adding them
# Returns a single histogram and its plot
def joinHistLayers(histograms):

	output = np.zeros(histograms[0].shape, dtype=np.float)

	for channel in range(len(histograms)):
		output += histograms[channel]

	# Clear current plot before making any new ones
	plt.cla()
	plt.clf()

	plt.plot(output, color='k')
	plt.xlim([0, 256])

	return output, plt

# Finds the appropriate upper and lower pixel value bounds that excludes the threshold percentage
# of pixels on both sides of the histogram
def findRange(histogram, threshold):

	# Calculate total number of pixels in the histogram (if used with joinHistLayers, will count total for each channel)
	total_pixels = np.sum(histogram)

	# Starting from the bottom of the range, 0, find the intensity value for which a threshold percent of pixels are excluded
	total = 0
	i = 0
	while np.sum(histogram[:i]) <= total_pixels * threshold:
		i += 1
	start = i

	# Also find upper bound
	total = 0
	i = 255
	while np.sum(histogram[i:]) <= total_pixels * threshold:
		i -= 1
	end = i

	return start, end