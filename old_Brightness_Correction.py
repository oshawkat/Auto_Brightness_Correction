import cv2
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot as plt



# Construct a histogram for a given image
# Returns a list of 256 x 1 arrays, with one array for each color channel
# B/W pictures have a single array, color is ordered as BGR
def createHistogram(image, mask):
	histogram = []

	for channel in range(image.shape[2]):
		hist = cv2.calcHist([image.astype(np.uint8)], [channel], None, [256], [0, 256])
		histogram.append(hist)
		
	return histogram


# Similar to createHistogram but can process the summation of up to 3 joined layers
# Outputs a single histogram of with 3x the range 
def createJoinedHistogram(image):
	histogram = cv2.calcHist(image.astype(np.uint16), [0], None, [768], [0, 768])
	# histogram = cv2.calcHist(image, [0], None, [256 * 3], [0, 256 * 3])

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

	plt.axis('tight')
	plt.title("Histogram")

	return plt


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
	start = i - 1

	# Also find upper bound
	total = 0
	i = histogram.shape[0]
	while np.sum(histogram[i:]) <= total_pixels * threshold:
		i -= 1
	end = i + 1

	return start, end


# Produces a numpy array of the same shape as the input image but the range is the sum of each 
# color channel.  
# Returns a numpy array
def joinLayers(image):

	output = np.zeros((image.shape[0], image.shape[1]), dtype=np.float)

	for channel in range(image.shape[2]):
		output += image[:, :, channel]

	return output


# Given an image, it's joined values, and a target range, scale the original image to fit the desired histogram
# Outputs a float numpy array of the same size and shape as image
def old_linearRescale(image, start, end):

	output = np.zeros(image.shape, dtype=np.float)

	scale = 255 / (end - start)

	# for index, pixel in np.ndenumerate(image):
	# 	image[index] = max(( pixel - start ) * scale, 0)

	for index in range(image.shape[2]):
		output[:,:,index] = (image[:,:,index] - start ) * scale

	lower_bound_mask = output < 0
	output[lower_bound_mask] = 0
	upper_bound_mask = output > 255
	output[upper_bound_mask] = 255

	return output.astype(np.uint8)

# Given an image, it's joined values, and a target range, scale the original image to fit the desired histogram
# Outputs a float numpy array of the same size and shape as image
def linearRescale(image, joinedimage, start, end):

	output = np.zeros(image.shape, dtype=np.float)
	scale = (end - start) / 255.0

	# print "Image size: {}".format(image.shape)
	# print "joinedimage size: {}".format(joinedimage.shape)
	# print "Output size: {}".format(output.shape)

	scale_factor = (joinedimage - start) 
	for i in range(image.shape[2]):
		output[:,:,i] = scale_factor * image[:,:,i] / joinedimage * scale


	# for index, pixel in np.ndenumerate(joinedimage):
	# 	scaled = (pixel - start) * scale
	# 	print "index = {} \t Output: {}".format(index, output[index])
	# 	for i in range(image.shape[2]):
	# 		output[index][i] = scaled * (image[index][i] / pixel)

	# lower_bound_mask = output < 0
	# output[lower_bound_mask] = 0
	# upper_bound_mask = output > 255
	# output[upper_bound_mask] = 255

	return output
	# return output.astype(np.uint8)

