import numpy as np
import cv2
import matplotlib.pyplot as plt
import imutils
import pickle
import numpy as np

class ManualWidth:
	"""
	image: defisheyed image
	dictPath: mapping dictionary path
	"""
	def __init__(self, Dimage, dictPath):
		self.image = Dimage
		self.mapPath = dictPath
		self.refPt = []
		self.cropping = False

		with open(self.mapPath, 'rb') as file:
			self.dict_combine_sorted = pickle.load(file)

	def click_and_crop(self, event, x, y, flags, param):
		# if the left mouse button was clicked, record the starting
		# (x, y) coordinates and indicate that self.cropping is being
		# performed
		if event == cv2.EVENT_LBUTTONDOWN:
			self.refPt = [(x, y)]
			self.cropping = True
		# check to see if the left mouse button was released
		elif event == cv2.EVENT_LBUTTONUP:
			# record the ending (x, y) coordinates and indicate that
			# the self.cropping operation is finished
			self.refPt.append((x, y))
			self.cropping = False
			# draw a rectangle around the region of interest
			cv2.rectangle(self.image, self.refPt[0], self.refPt[1], (0, 255, 0), 2)
			cv2.imshow("image", self.image)


	def get_manual_width(self):
		# load the image, clone it, and setup the mouse callback function
		
		self.image = imutils.resize(self.image, width=1000)
		# image = imutils.resize(image, width=400)
		
		cv2.rectangle(self.image, (0,575), (1000,675), (0, 0, 255), 4)
		# cv2.rectangle(image, (0,230), (400,260), (0, 0, 255), 4)
		
		clone = self.image.copy()
		cv2.namedWindow("image")
		cv2.setMouseCallback("image", self.click_and_crop)
		# keep looping until the 'q' key is pressed
		while True:
			# display the image and wait for a keypress
			cv2.imshow("image", self.image)
			key = cv2.waitKey(1) & 0xFF
			# if the 'r' key is pressed, reset the self.cropping region
			if key == ord("r"):
				self.image = clone.copy()
			# if the 'c' key is pressed, break from the loop
			elif key == ord("c"):
				break
		# We will be taking the top coordinates of the rectangle drawn. Start from the top left and then drag
		# the rectangle to the bottom right. 
		if len(self.refPt) == 2:
			# the coordinates of the boxed rectangle. We only take the coordinate of the top line
			# print(self.refPt[0][1], self.refPt[1][1], self.refPt[0][0],self.refPt[1][0])
			
			##############################################
			# print('length: {0}, original length: {1} pixels'.format((self.refPt[1][0]-self.refPt[0][0]), (self.refPt[1][0]-self.refPt[0][0])*4))
			# print('length: {0}, original length: {1} pixels'.format((self.refPt[1][0]-self.refPt[0][0]), (self.refPt[1][0]-self.refPt[0][0])*10))
			###############################################
			###############################################
			# print('location: {0}, dictionary location: {1}'.format(self.refPt[0][1], (self.refPt[0][1]*4)-2000))
			# print('location: {0}, dictionary location: {1}'.format(self.refPt[0][1], (self.refPt[0][1]*10)-2000))
			###############################################

			roi = clone[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]
			
			##############################################
			dict_location = (self.refPt[0][1]*4)-2000
			# dict_location = (self.refPt[0][1]*10)-2000
			##############################################
			
			pixels = np.round(np.mean(self.dict_combine_sorted[dict_location]))
			per_pixel_value = 4 / pixels
			
			print('Per pixel is {0} feet'.format(per_pixel_value))
			
			####################################
			print('Width of the road is {0} feet'.format(per_pixel_value * (self.refPt[1][0]-self.refPt[0][0])*4))
			# print('Width of the road is {0} feet'.format(per_pixel_value * (self.refPt[1][0]-self.refPt[0][0])*10))
			#####################################
		# close all open windows
		cv2.destroyAllWindows()