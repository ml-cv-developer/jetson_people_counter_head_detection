
def filterSize(classesID, probs, rects, frame) :
	classesIDN 	= []
	probsN 		= []
	rectsN 		= []

	(HI,WI) = frame.shape[0:2]
	wmax = WI // 3
	hmax = HI // 3
	for i, (x, y, w, h) in enumerate(rects) :
		if (w < wmax) and (h < hmax) :
			classesIDN.append(classesID[i])
			probsN.append(probs[i])
			rectsN.append(rects[i])

	return classesIDN, probsN, rectsN


