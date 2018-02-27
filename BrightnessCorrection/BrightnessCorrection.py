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
		hist = cv2.calcHist([image.astype(np.uint8)], [channel], mask[:,:,channel], [256], [0, 256])
		histogram.append(hist)
		
	return histogram


# Similar to createHistogram but can process the summation of up to 3 joined layers
# Outputs a single histogram of with 3x the range 
def createJoinedHistogram(image, mask):
	histogram = cv2.calcHist([image.astype(np.uint16)], [0], mask, [768], [0, 768])

	return histogram


# Given a list of histograms, one for each color channel, return a plot of the histograms, all on one chart
def drawHistogram(histograms):

	colors = ('b', 'g', 'r')

	# Clear current plot before making any new ones
	plt.cla()
	plt.clf()

	# B&W vs color images 
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
def findRange(histogram, lower_threshold, upper_threshold):

	# Calculate total number of pixels in the histogram (if used 
	# with joinHistLayers, will count total for each channel)
	total_pixels = np.sum(histogram)

	# Starting from the bottom of the range, 0, find the intensity 
	# value for which a threshold percent of pixels are excluded
	total = 0
	i = 0
	while np.sum(histogram[:i]) <= total_pixels * lower_threshold:
		i += 1
	start = i - 1

	# Also find upper bound
	total = 0
	i = histogram.shape[0]
	while np.sum(histogram[i:]) <= total_pixels * upper_threshold:
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
def linearRescale(image, start, end):

	output = np.zeros(image.shape, dtype=np.float)

	scale = 255 / (end - start)

	for index in range(image.shape[2]):
		output[:,:,index] = (image[:,:,index] - start ) * scale

	lower_bound_mask = output < 0
	output[lower_bound_mask] = 0
	upper_bound_mask = output > 255
	output[upper_bound_mask] = 255

	return output.astype(np.uint8)

# Given an image, it's joined values, and a target range, scale the original image to fit the desired histogram
# Outputs a float numpy array of the same size and shape as image
def nonlinearRescale(image, joinedimage, start, end, light_mask, dark_mask):

	output = np.zeros(image.shape, dtype=np.float)
	scale = 255.0 / (end - start)
	print "Range is {} and scale is {:.2f}".format(end - start, scale)

	joined_rescaled = (joinedimage - start) * scale 
	for i in range(image.shape[2]):
		print "Color {}, at avg val of {:5.1f}, represents {:.1%} of the joined image, with avg of {:5.1f}".format(i, np.average(image[:,:,i]), np.average(image[:,:,i]) / np.average(joinedimage), np.average(joinedimage))
		output[:,:,i] = joined_rescaled * (image[:,:,i] / joinedimage) / (1.0/3.0)
		print "Average output for this color is {:.1f}".format(np.average(output[:,:,i]))


	adark_mask = output < 15
	output[adark_mask] = output[adark_mask] * 2
	bright_mask = output > 245
	output[bright_mask] = output[bright_mask] * .95

	# Only scale unmasked regions by copying over original image data that was masked
	mask_3Dl = np.full(image.shape, False, dtype=np.uint8)
	mask_3Dd = np.full(image.shape, False, dtype=np.uint8)
	for i in range(image.shape[2]):
		mask_3Dl[:,:, i] = light_mask
		mask_3Dd[:,:, i] = dark_mask
	almask = mask_3Dl == 0
	admask = mask_3Dd == 0
	output[almask] = image[almask] * .98
	output[admask] = image[admask] * 2
	print "Average output post mask {:.1f} \t Max: {}".format(np.average(output), np.max(output))

	lower_bound_mask = output < 0
	output[lower_bound_mask] = 0
	upper_bound_mask = output > 255
	output[upper_bound_mask] = 255
	
	# Adjust the brightest and darkest areas with a non-linear scaling
	# dark_boost_max = 2		# Max scaling to increase darkest areas
	# dark_boost_range = 15
	# for i in range(0, dark_boost_range):
	# 	adark_mask = output == i
	# 	output[adark_mask] = output[adark_mask] * dark_boost_max * (dark_boost_range - i) / dark_boost_range

	# light_boost_max = .1		# Max scaling to increase darkest areas
	# light_boost_range = 230
	# for i in range(dark_boost_range, 256):
	# 	alight_mask = output == i
	# 	output[alight_mask] = output[alight_mask] * (1 - (light_boost_max * (i - light_boost_range) / (255 - light_boost_range)))

	return output
	# return output.astype(np.uint8)

