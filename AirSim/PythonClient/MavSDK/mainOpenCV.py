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
    # 31 m
    pass

def main():
    # clear tracked objects from previous run
    if(os.path.exists("objects.csv")):
        os.remove("objects.csv")


    # Create tracker object
    tracker = EuclideanDistTracker()
    cap = cv2.VideoCapture("../test1.mp4")


    # Object detection from Stable camera
    out = cv2.VideoWriter('out.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 12.0, (864,486))
    object_detector = cv2.createBackgroundSubtractorKNN(history=0, dist2Threshold=15000, detectShadows=True)
    while True:
        ret, frame = cap.read()
        frame = rescale_frame(frame, percent=45)
        height, width, _ = frame.shape

        # calculate_speed(frame)
        
        # Extract Region of interest
        # roi = frame[0: 460,290: 1152]
        roi = frame[300: 420,0: 1152]
    

        # 1. Object Detection
        mask = object_detector.apply(roi)
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            if area > 400:
                # Draw contours if needed
                # cv2.drawContours(roi, [cnt], -1, (0, 0, 255), )
                x, y, w, h = cv2.boundingRect(cnt)
                detections.append([x, y, w, h])

        # 2. Object Tracking
        boxes_ids = tracker.update(detections)
        for box_id in boxes_ids:
            x, y, w, h, id, = box_id
            cv2.putText(roi, "obj: " + str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if ret == True:
            cv2.putText(frame, 'Detection Region', (0, 280), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)    
            cv2.rectangle(frame, (0,290), (1152,460), (0, 255, 0), 1)
            cv2.imshow("Frame", frame)
            frame = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
            out.write(mask)
            cv2.imshow("Masked Region", mask)
            cv2.imshow("Detection Region", roi)
            

        key = cv2.waitKey(30)
        if key == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
