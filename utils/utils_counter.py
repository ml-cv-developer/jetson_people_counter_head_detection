from utils.CheckSideUtils     import CheckSideLine
from shapely.geometry   import Point, Polygon



class Counter_Polygon() :
    def __init__(self, coords, maxlist = 100) :
        self.point_polygon  = coords
        self.polygon        = Polygon(coords)
        self.counter        = 0        
        self.listObject     = []

        self.maxlist        = maxlist
    
    def isinside(self, bbox) :
        x, y, w, h = bbox
        points = []
        points.append(Point(x, y))
        points.append(Point(x + w, y))
        points.append(Point(x, y + h))
        points.append(Point(x + w, y + h))

        sum_point = 0 
        for point in points :
            if self.polygon.contains(point) :
                sum_point += 1
        
        if sum_point >= 2 :
            return True
        else :
            return False    

    def update(self, trackerlist) :
        for object_track in trackerlist :
            (x, y, w, h) = object_track.bbox
            y_feet      = y + h//2
            x_center    = x + w//2

            if (object_track.objectID not in self.listObject) :
                # if(self.polygon.contains(Point(x_center, y_feet))) :
                # if(self.isinside(object_track.bbox)) :
                if(self.isinside(object_track.bbox)) and object_track.appeared >= 5:
                    self.counter +=1
                    self.listObject.append(object_track.objectID)
                    # print("polygon :{}".format(object_track.objectID))
            
        
        self.clean_track()
        # print('left : {}, right : {}'.format(self.counterRL,self.counterLR))
    def get_counter(self) :
        # save counter object in current
        counter_ob = self.counter
        # clearn object save
        return counter_ob

    def get_counter_and_clean(self) :
        # save counter object in current
        counter_ob = self.counter
        # clearn object save
        self.counter = 0
        return counter_ob

    def clean_track(self) :
        # clearn object tracking in list counter
        if len(self.listObject) > self.maxlist :
            for i in range(len(self.listObject) - self.maxlist) :
                del self.listObject[0]
        # clearn object tracking in list counter
    
    def clean(self) :
        self.counter                = 0
        self.listObject           = []



# this class will counter two way of utils


# ---------------------------------------------------------------------------
# Counter Object in two way
# ---------------------------------------------------------------------------


class Counter_Line2Way() :
    def __init__(self, line, points) :
        self.point_line     = line
        self.line           = CheckSideLine(line=line,point1=points[0:2], point2=points[2:4])
        self.counterLR      = 0        
        self.listLR         = []

        self.counterRL      = 0
        self.listRL         = []
        
        self.maxlist        = 2
    
    def isinside(self, point) :
        x1_line, y1_line = self.point_line[:2]
        x2_line, y2_line = self.point_line[2:]
        x_min = min(x1_line,x2_line)
        x_max = max(x1_line,x2_line)

        y_min = min(y1_line,y2_line)
        y_max = max(y1_line,y2_line)

        x, y = point
        # print("x_min :{} x_max : {}".format(x_min, x_max))
        # print("y_min :{} y_max : {}".format(y_min, y_max))
        # print("x : {}, y :{}".format(x,y))

        if (x > x_min and x < x_max) or (y > y_min and y < y_max) :
            # print("isinside")
            return True
        else :
            # print("not isinside")
            return False

    def update(self, trackerlist) :
        light_trackid   = []
        light_aciton    = []
        for object_track in trackerlist :

            # if (object_track.objectID not in self.listLR) and len(object_track.trace) > 2 and self.isinside(object_track.trace[-1]):
            if len(object_track.trace) > 2 and (object_track.objectID not in self.listLR)  :
            # if len(object_track.trace) > 2   :
                if self.line.check_right(object_track.trace[-2], object_track.trace[-1]) :
                # if self.line.check_right(object_track.trace[-2], object_track.trace[-1]) and self.line.not_same_side(object_track.trace[-3], object_track.trace[-1]):
                    self.counterLR +=1
                    self.listLR.append(object_track.objectID)
                    
                    light_trackid.append(object_track.objectID)
                    light_aciton.append('in')
                    # print("LR :{}".format(object_track.objectID))
                
        
        for object_track in trackerlist :
            # if len(object_track.trace) > 2 and self.isinside(object_track.trace[-1]):
            # if (object_track.objectID not in self.listRL) and len(object_track.trace) > 2 and self.isinside(object_track.trace[-1]):
            if len(object_track.trace) > 2 and (object_track.objectID not in self.listRL) :
            # if len(object_track.trace) > 2 :
                if self.line.check_lelf(object_track.trace[-2], object_track.trace[-1]) :
                # if self.line.check_lelf(object_track.trace[-2], object_track.trace[-1]) and self.line.not_same_side(object_track.trace[-3], object_track.trace[-1]):
                    self.counterRL +=1
                    self.listRL.append(object_track.objectID)

                    light_trackid.append(object_track.objectID)
                    light_aciton.append('out')                    
                    # print("RL : {}".format(object_track.objectID))
        
        
        self.clean_track()
        # print('left : {}, right : {}'.format(self.counterRL,self.counterLR))
        return light_trackid, light_aciton
        
    def get_counter(self) :
        # save counter object in current
        counter_LR = self.counterLR
        counter_RL = self.counterRL
        # clearn object save
        return counter_LR, counter_RL

    def get_counter_and_clean(self) :
        # save counter object in current
        counter_LR = self.counterLR
        counter_RL = self.counterRL
        # clearn object save
        self.counterLR = 0
        self.counterRL = 0
        return counter_LR, counter_RL

    def clean_track(self) :
        # clearn object tracking in list counter
        if len(self.listLR) > self.maxlist :
            for i in range(len(self.listLR) - self.maxlist) :
                del self.listLR[0]
        # clearn object tracking in list counter
        if len(self.listRL) > self.maxlist :
            for i in range(len(self.listRL) - self.maxlist) :
                del self.listRL[0]
    
    def clean(self) :
        self.counterLR        = 0
        self.counterRL        = 0
        self.listLR           = []
        self.listRL           = []
