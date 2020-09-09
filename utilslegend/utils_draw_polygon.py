import numpy as np
import cv2

from utilslegend.utils_color import COLOR_TABEL_LINE
from utilslegend.utils_color import COLOR_TABEL_OB

X0 = 30
Y0 = 30

d_row   = 30
d_clo   = 100


COLOR_WHITE     = (255, 255, 255)
COLOR_RED       = (0, 0, 255)
COLOR_GREEN     = (0, 255, 0)
COLOR_BLUE      = (255, 0, 0)
COLOR_PURPLE    = (255, 0, 255)
COLOR_YELLOW    = (0, 255, 255)
COLOR_YELLOW1    = (135, 255, 255)
COLOR_YELLOW2    = (135, 135, 255)

COLOR_TABEL = [COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_PURPLE, COLOR_YELLOW,COLOR_YELLOW1,COLOR_YELLOW2]



def draw_no_object21() :
    label = "{}".format("C1 : motobike/bicycel C2 : Car")

    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(y, labelSize[1])
    print("labelSize {}, baseLine {}".format(labelSize, baseLine))
    
    cv2.rectangle(frame, (x - 1, top - round(labelSize[1])), (x+w+1, top ), (0, 255, 255), cv2.FILLED)
    cv2.putText(frame, label, (x, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)  

# def draw_no_object2(frame ) :
def draw_no_next_id(frame, per_id, motor_id,  car_id, bus_id, truck_id, index) :

    cv2.putText(frame, "Next_ID",       (X0 + 220 + 1*d_clo    ,Y0 ),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_LINE[index], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(per_id),     (X0 + 220 + 1*d_clo    ,Y0 + 1*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[1], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(motor_id),   (X0 + 220 + 1*d_clo    ,Y0 + 2*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[2], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(car_id),     (X0 + 220 + 1*d_clo    ,Y0 + 3*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[3], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(bus_id),     (X0 + 220 + 1*d_clo    ,Y0 + 4*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[4], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(truck_id),   (X0 + 220 + 1*d_clo    ,Y0 + 5*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[5], 2, lineType=cv2.LINE_AA)

# def draw_no_object2(frame ) :
def draw_no_current(frame, per_id, motor_id,  car_id, bus_id, truck_id, index) :

    cv2.putText(frame, "Currently",     (X0 + 220 + 2*d_clo    ,Y0 ),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_LINE[index], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(per_id),     (X0 + 220 + 2*d_clo    ,Y0 + 1*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[1], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(motor_id),   (X0 + 220 + 2*d_clo    ,Y0 + 2*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[2], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(car_id),     (X0 + 220 + 2*d_clo    ,Y0 + 3*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[3], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(bus_id),     (X0 + 220 + 2*d_clo    ,Y0 + 4*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[4], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(truck_id),   (X0 + 220 + 2*d_clo    ,Y0 + 5*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[5], 2, lineType=cv2.LINE_AA)

# def draw_no_object2(frame ) :
def draw_no_object(frame, per_up, motor_up, car_up, bus_up, truck_up, index) :

    cv2.putText(frame, "No",                    (X0 + 220               ,Y0 ),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_LINE[index], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(per_up),             (X0 + 220                ,Y0 + 1*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[1], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(motor_up),           (X0 + 220            ,Y0 + 2*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[2], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(car_up),             (X0 + 220                ,Y0 + 3*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[3], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(bus_up),             (X0 + 220                ,Y0 + 4*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[4], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, str(truck_up),           (X0 + 220                ,Y0 + 5*d_row),cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_TABEL_OB[5], 2, lineType=cv2.LINE_AA)





def draw_title(frame) :

    text_per = "person"
    text_mor = "motor"
    text_car = "car"
    text_bus = "bus"
    text_str = "truck"
    cv2.putText(frame, text_per, (X0,Y0 + 1*d_row),cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_TABEL_OB[1], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, text_mor, (X0,Y0 + 2*d_row),cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_TABEL_OB[2], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, text_car, (X0,Y0 + 3*d_row),cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_TABEL_OB[3], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, text_bus, (X0,Y0 + 4*d_row),cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_TABEL_OB[4], 2, lineType=cv2.LINE_AA)
    cv2.putText(frame, text_str, (X0,Y0 + 5*d_row),cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_TABEL_OB[5], 2, lineType=cv2.LINE_AA)

def draw_number_index(frame, index ) :
    text_index = '{}'.format(index)
    cv2.putText(frame, text_index, ((X0 + 220 + 1*d_clo    ,Y0 + 4*d_row)), cv2.FONT_HERSHEY_SIMPLEX, 5, COLOR_TABEL_LINE[index], 5, lineType=cv2.LINE_AA)



if __name__ =='__main__' :

    # Create a black image
    img = np.zeros((200,600,3), np.uint8)
    draw_title(img)
    draw_no_object(img, 1,3454,424,73,92,0)
    draw_no_next_id(img,122,43,54,45,345,0)
    draw_no_current(img,122,43,54,45,345,0)
    
    draw_number_index(img,0)
    # img = cv2.resize(img, (600,100))
    cv2.imshow('a',img)
    k = cv2.waitKey(0)
    # Press q to break
    # if k == ord('q'):
        # break