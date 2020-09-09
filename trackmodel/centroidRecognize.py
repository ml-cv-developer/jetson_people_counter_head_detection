# import the necessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import time
import cv2
# import matplotlib.pyplot as plt
import datetime

class Human(object): 

	def __init__(self, objectID, centroid, inputRect,image=None, color=None, gender=None) :
		"""
			Feature Human :
				objectID 		: ID to recognize
				color 			: color of cothes
				gender 			: str (Male, Female)
				image 			: Newest image detected
				predict 		: centroid predict
				trace			: list centroid detected (limit number)
				iscountered 	: recognize countered or not
				disappeared 	: max numer frame, or second can't detect in one camera
				appeared 		: numer framed detected to voice noise

		"""    		
		self.objectID 		= objectID
		self.color 			= color
		self.gender 		= gender 
		self.image			= image
		self.trace 			= []
		self.bbox  			= inputRect

		self.appeared 			= 0
		self.disappeared 		= 0
		self.time_appeared 		= datetime.datetime.now()
		self.iscountered 		= False


class RdfTracker:
	# def __init__(self, maxObjectTrack=7, maxDistance=400, maxTrace=3,maxDisappeared = 180):
	def __init__(self, maxObjectTrack=7, maxDistance=400, maxTrace=3,  max_Timedisappeared = 10):
		"""
			maxObjectTrack 		: Max umber frame or second cann't detect object
			maxDistance			: Distance between two object to match
			maxTrace			: Max location skipp of one object

		"""
		# self.counter_object 	= 0
		self.nextObjectID 		= 0
		self.currentObjects 	= []
		self.hiddenObjects		= []

		self.max_Timedisappeared   	= max_Timedisappeared
		self.maxObjectTrack 	= maxObjectTrack
		self.maxDistance 		= maxDistance
		self.maxTrace  			= maxTrace
		self.cur_day 			= datetime.datetime.now().day

	def __register(self, centroid, imageObject, inputRect):
		"""
			Create new object feature
			add to object tracker list

		"""	
		now = datetime.datetime.now()
		id_s = now.strftime('%H%M%S')
		id_s = id_s + "00" + str(self.nextObjectID)
		id_i = int(id_s)

		track = Human(id_i, centroid,inputRect, imageObject)
		self.currentObjects.append(track)
		self.currentObjects[-1].trace.append(centroid)
		self.nextObjectID += 1
		# print("self.nextObjectID : {}".format(str(self.nextObjectID)))

	def __to_hiddenObjects(self, tracksId) :
		tracksObject 		= [self.currentObjects[index] for index in range(len(self.currentObjects)) if index in tracksId]
		self.currentObjects = [self.currentObjects[index] for index in range(len(self.currentObjects)) if index not in tracksId]
		self.hiddenObjects 	+= tracksObject

	def __to_currentObjects(self, tracksId) :

		tracksObject 		= [self.hiddenObjects[index] for index in range(len(self.hiddenObjects)) if index in tracksId]
		self.hiddenObjects 	= [self.hiddenObjects[index] for index in range(len(self.hiddenObjects)) if index not in tracksId]
		self.currentObjects += tracksObject


	def __deregister(self, objectID):
		"""
			Delete object from tracker list

		"""	
		# print('Delete Object {}'.format(objectID))
		del self.currentObjects[objectID]
	
	"""
		Match list object tracking end detect
		feature histogram of object

		return rows, cols object tracking, detect Matched
	"""


	def __match_hidden_distance(self,inputCentroids, inputCropObjects, inputRects) :
    	

		number_ob_tracking 	= len(self.hiddenObjects)
		number_ob_detect 	= len(inputCentroids)


		objectCentroids = [self.hiddenObjects[index].trace[-1] for index in range(number_ob_tracking)]
		D_dis = dist.cdist(np.array(objectCentroids), inputCentroids)

		usedDetects 	= set()
		usedTracks 		= set()


		# usedTracks_1, usedDetects_1 = self.__match_distance(self.hiddenObjects, inputCentroids , inputCropObjects, inputRects)
		# # usedTracks_1, usedDetects_1 = self.__match_iou(self.hiddenObjects, inputCentroids , inputCropObjects, inputRects)

		
		# for (detect1, track1) in zip(usedDetects_1, usedTracks_1) :
		# 	usedDetects.add(detect1)
		# 	usedTracks.add(track1)

		# for (detect1, track1) in zip(usedDetects, usedTracks) :
		# 	D_dis[track1, :] 	= self.maxDistance
		# 	D_dis[:, detect1] 	= self.maxDistance

		while (D_dis.min() < self.maxDistance and not (len(usedDetects) == number_ob_detect or len(usedTracks) == number_ob_tracking )): 

			tracks 	= D_dis.min(axis=1).argsort()
			detects = D_dis.argmin(axis=1)[tracks]

			for (track, detect) in zip(tracks, detects):
				if detect in usedDetects or track in usedTracks:
					continue
				# Next ID in create if maxDistance smale
				if D_dis[track, detect] >= self.maxDistance :
					continue
				# ------------------------------------------------------------------------------------
				# print("hidden : {}".format(D_dis[track, detect]))

				self.hiddenObjects[track].image 	= inputCropObjects[detect]
				self.hiddenObjects[track].bbox 		= inputRects[detect]
				self.hiddenObjects[track].trace.append(inputCentroids[detect])
				
				usedDetects.add(detect)
				usedTracks.add(track)
			
			for (track1, detect1) in zip(usedTracks, usedDetects) :
				D_dis[track1, :] 	= self.maxDistance
				D_dis[:, detect1] 	= self.maxDistance
			# print(D)
		# --------------------------------------------------------------------------------
		# Clear object matched
		# --------------------------------------------------------------------------------


		return usedTracks, usedDetects



	"""
		Match list object tracking end detect
		compare distance 
		return rows, cols object tracking, detect Matched
	# """	
	def __match_distance_current(self, inputCentroids , inputCropObjects, inputRects) :
		number_ob_tracking 	= len(self.currentObjects)
		number_ob_detect 	= len(inputCentroids)


		# ----------------------------------------------------------------------------------------------
		# Pool Maps ID Tracking And Detect
		# ----------------------------------------------------------------------------------------------
		objectCentroids = [self.currentObjects[index].trace[-1] for index in range(number_ob_tracking)]
		D_DIS = dist.cdist(np.array(objectCentroids), inputCentroids)
				
		tracks 		= D_DIS.min(axis=1).argsort()
		detects 	= D_DIS.argmin(axis=1)[tracks]

		usedTracks 	= set()
		usedDetects = set()
		# print(' ------ next match ------ ')
		for (track, detect) in zip(tracks, detects):

			if track in usedTracks or detect in usedDetects:

				continue
			if D_DIS[track, detect] > 80:
				# print("Distance Object: {} max {}".format(D[track, detect], self.maxDistance))
				continue
			
			# print('dis : {} {} {}'.format(track, detect,D_DIS[track, detect]))
			self.currentObjects[track].image  		= inputCropObjects[detect]
			self.currentObjects[track].bbox  		= inputRects[detect]
			self.currentObjects[track].trace.append(inputCentroids[detect])
			
			usedTracks.add(track)
			usedDetects.add(detect)

		return usedTracks, usedDetects

	"""
		Match list object tracking end detect
		compare distance 
		return rows, cols object tracking, detect Matched
	# """	

	def __clear_update_time(self) :

		# update time for object newest
		for currentObject in self.currentObjects :
			currentObject.time_appeared = datetime.datetime.now()

		# reset disappeared of object and delete if to long
		current_time    = datetime.datetime.now()
		maxHiddenList 	= []
		for i, hiddenObject in enumerate(self.hiddenObjects) :
			subtime         = current_time - hiddenObject.time_appeared
			total_seconds   = int(subtime.total_seconds())
			if total_seconds > self.max_Timedisappeared:
				# print("del hiddenObject : {}".format(hiddenObject.objectID))
				maxHiddenList.append(i)

		self.hiddenObjects 	= [self.hiddenObjects[index] for index in range(len(self.hiddenObjects)) if index not in maxHiddenList]

		# clear maximun object traing in hidden
		if(len(self.hiddenObjects) > self.maxObjectTrack) :
			for index in range(len(self.hiddenObjects) - self.maxObjectTrack) :
				# print("del max 8 hiddenObject : {}".format(self.hiddenObjects[0].objectID))
				del self.hiddenObjects[0]


		for i in range(len(self.currentObjects)) : 
			# Delete trace older than max
			if(len(self.currentObjects[i].trace) > self.maxTrace):
				for j in range(len(self.currentObjects[i].trace) - self.maxTrace):
					del self.currentObjects[i].trace[0]

		for i in range(len(self.hiddenObjects)) : 
			# Delete trace older than max
			if(len(self.hiddenObjects[i].trace) > self.maxTrace):
				for j in range(len(self.hiddenObjects[i].trace) - self.maxTrace):
					del self.hiddenObjects[i].trace[0]
		
		current_date = datetime.datetime.now().day

		if current_date != self.cur_day and self.cur_day != 0:
			for i in range(len(self.currentObjects)) : 
				del self.currentObjects[0]
			for i in range(len(self.hiddenObjects)) :
				del self.hiddenObjects[0]
			
			self.nextObjectID = 0
			
		self.cur_day = current_date


	def update(self, rects, frame):

		# If frame can't detect any object
		# All tracking object will increate number disapper

		if len(rects) == 0:
			trackID = range(len(self.currentObjects))
			self.__to_hiddenObjects(trackID)


			#  there is nothing to match, clear object
			self.__clear_update_time()
			return self.currentObjects

		# prepare data inport to tracking

		# Convert from rect to point
		inputCentroids = np.zeros((len(rects), 2), dtype="int")
		for (i, (x, y, w, h)) in enumerate(rects):
			cX = int(x + w // 2.0)
			cY = int(y + h // 2.0)
			inputCentroids[i] = (cX, cY)

		# Convert from rect to point
		inputRects 	= rects
		img_size 	= np.asarray(frame.shape)[0:2]

		inputCropObjects = []
		for (x, y, w, h) in rects :
			
	        
			xmin = np.maximum(int(x), 0)
			xmax = np.minimum(int(x + w) , img_size[1])

			ymin = np.maximum(int(y), 0)
			ymax = np.minimum(int(y + h) , img_size[0])

			cropObject = frame[ymin : ymax, xmin : xmax]

			cropObject_rgb = cv2.cvtColor(cropObject, cv2.COLOR_BGR2RGB)
			inputCropObjects.append(cropObject_rgb)
	

		# ---------------------------------------------------------------------------------
		# If tracking list is empty
		# Create object to tracking
		# ---------------------------------------------------------------------------------
		# this case Len(INPUT) > 0
		if len(self.currentObjects) == 0 and len(self.hiddenObjects) == 0 :
			for index in range(0, len(inputCentroids)):
				# print("Register new object ")
				# print(inputRects[index])
				self.__register(inputCentroids[index], inputCropObjects[index], inputRects[index])
			
			return self.currentObjects
		# centroids
		# Case for have Object in current, hiddent or both
		else :
			# grab the set of object IDs and corresponding centroids
			# Case for currebt Object  > 0 and check hiddent
			if (len(self.currentObjects) > 0 ) :
				usedTracks,usedDetects = self.__match_distance_current(inputCentroids, inputCropObjects, inputRects)
				# ----------------------------------------------------------------------------------------------
				# Counter frame object disappeared
				# ----------------------------------------------------------------------------------------------
				unusedTracks 	= set(range(0, len(self.currentObjects))).difference(usedTracks)
				unusedDetects 	= set(range(0, len(inputCentroids))).difference(usedDetects)
				# change object tracking current to hiddent
				self.__to_hiddenObjects(unusedTracks)
				# object unmatch detect
				inputCentroids_unmatch 		= [inputCentroids[index] for index in range(len(inputCentroids)) if index in unusedDetects]
				inputCropObjects_unmatch 	= [inputCropObjects[index] for index in range(len(inputCropObjects)) if index in unusedDetects]
				inputRects_unmatch 			= [inputRects[index] for index in range(len(inputRects)) if index in unusedDetects]
				
				# case for match hiddentObejct
				if(len(unusedDetects) > 0 and len(self.hiddenObjects) > 0) :
					usedTracks2, usedDetects2 = self.__match_hidden_distance(inputCentroids_unmatch, inputCropObjects_unmatch, inputRects_unmatch)
					
					unusedDetects2 = set(range(0, len(unusedDetects))).difference(usedDetects2)
					# Chang object tracking hiddent to current
					self.__to_currentObjects(usedTracks2)

					for detectID in unusedDetects2 :
						# Register new object if in other side
						self.__register(inputCentroids_unmatch[detectID], inputCropObjects_unmatch[detectID],inputRects_unmatch[detectID])
				else :
					for detectID in unusedDetects :
						# print("New object affter current ")
						self.__register(inputCentroids[detectID], inputCropObjects[detectID],inputRects[detectID])
			# Case for currebt Object  = 0 and hiddent Object > 0
			elif (len(self.hiddenObjects) > 0 and len(inputCentroids) > 0) :

				usedTracks,usedDetects = self.__match_hidden_distance(inputCentroids, inputCropObjects, inputRects)

				unusedDetects = set(range(0, len(inputCentroids))).difference(usedDetects)

				# Chang object tracking hiddent to current
				self.__to_currentObjects(usedTracks)

				for detectID in unusedDetects :
					# Register new object if in other side
					self.__register(inputCentroids[detectID], inputCropObjects[detectID],inputRects[detectID])					
			# ----------------------------------------------------------------------------------------------
			# Counter object have appeared > 5
			# ----------------------------------------------------------------------------------------------

			# ----------------------------------------------------------------------------------------------
			# Clear data 
			# ----------------------------------------------------------------------------------------------


			self.__clear_update_time()

		return self.currentObjects 
