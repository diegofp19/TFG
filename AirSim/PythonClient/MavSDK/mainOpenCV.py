import cv2
from tracker import *
import os

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


def calculate_speed(frame):
    cv2.line(frame, (int(1920*0.5*0.45), 0), (int(1920*0.5*0.45), 486), (255, 255, 0), 1)
    pass

def main():
    # clear tracked objects from previous run
    if(os.path.exists("objects.csv")):
        os.remove("objects.csv")


    # Create tracker object
    tracker = EuclideanDistTracker()
    cap = cv2.VideoCapture("../test1.mp4")


    # Creating Background subtractor using KNN algorithm (test parameters in each video to get the optimal result)
    object_detector = cv2.createBackgroundSubtractorKNN(history=100, dist2Threshold=10000, detectShadows=False)
    while True:
        ret, frame = cap.read()
        frame = rescale_frame(frame, percent=45)
        height, width, _ = frame.shape

        # To draw the line where velocity is calculated uncomment the next line and adjust it to the desired video
        # calculate_speed(frame)
        
        # Extract Region of interest to get only the part of the video that we want, specifically the road that is being monitorized
        roi = frame[0: 460,290: 1152]
    

        # 1. Object Detection
        mask = object_detector.apply(roi)
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            if area > 200:
                x, y, w, h = cv2.boundingRect(cnt)
                detections.append([x, y, w, h])

        # 2. Object Tracking passing to the tracker method class
        boxes_ids = tracker.update(detections)
        for box_id in boxes_ids:
            x, y, w, h, id, = box_id
            cv2.putText(roi, "obj: " + str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.putText(frame, 'Detection Region', (0, 380), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)    
        cv2.rectangle(frame, (0,290), (1152,460), (0, 255, 0), 1)
        #Binarized video
        cv2.imshow("Masked Region", mask)
        #Video of only the detection region
        cv2.imshow("Detection Region", roi)
        # Resulting video
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(30)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
