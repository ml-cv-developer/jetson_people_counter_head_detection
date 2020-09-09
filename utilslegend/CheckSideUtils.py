
class CheckSideLine :
    def __init__(self, line, point1, point2) :
        self.__line = self.__lineFrompoint(line[:2],line[2:])
        self.point1 = point1
        self.point2 = point2
        
        self.distp1 = self.__distance(self.point1)
        self.distp2 = self.__distance(self.point2)
    
    def __lineFrompoint(self,P, Q) :
        # print(Q)
        # print(P)
        line = []
        a = Q[1] - P[1] 
        b = P[0] - Q[0]  
        c = a*(P[0]) + b*(P[1])
        # if(b < 0):  
        #     print("The line passing through points P:", P ,"and Q", Q ," is:",
        #       a ,"x ",b ,"y = ",c ,"\n")  
        # else: 
        #     print("The line passing through points P:", P ,"and Q", Q ," is:", 
        #       a ,"x + " ,b ,"y = ",c ,"\n")  
        line.append(a)
        line.append(b)
        line.append(c)
        return line
    
    def __distance(self, point) :
        distance = self.__line[0]*point[0] + self.__line[1]*point[1] - self.__line[2]
        return distance

    def inside(self, point) :
        """
            Args :
                Point to check 
            Return :
                True if point inside line
                Fale if point outside line
        """
        distpc1 = self.__distance(point)
        inside = self.__same_side(self.distp2, distpc1)
        return inside

    def check_right(self,pc1, pc2) :
        """
            Args :
                point1, point2 is point tracking
            Return :
                True if from outsite to inside
        """
        distpc1 = self.__distance(pc1)
        distpc2 = self.__distance(pc2)
        
        is_right = self.__same_side(self.distp1, distpc1) and self.__same_side(self.distp2, distpc2)
        # print("is_right : {}".format(is_right))
        return is_right
    
    def check_lelf(self,pc1, pc2) :
        distpc1 = self.__distance(pc1)
        distpc2 = self.__distance(pc2)
        
        is_lelf = self.__same_side(self.distp1, distpc2) and self.__same_side(self.distp2, distpc1)
        # print("is_lelf : {}".format(is_lelf))
        return is_lelf    
    
    def not_same_side(self,pc1, pc2) :
        distpc1 = self.__distance(pc1)
        distpc2 = self.__distance(pc2)
        
        is_lelf = self.__same_side(distpc1, distpc2) 
        # print("is_lelf : {}".format(is_lelf))
        return not is_lelf
    
    def __same_side(self, dist1, dist2) :
        # print("dist1 * dist2 : {}".format(dist1 * dist2))
        return True if (dist1 * dist2) > 0 else False
        
    