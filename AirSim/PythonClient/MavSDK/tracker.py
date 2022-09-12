
# Credit here

import math
import time
from datetime import datetime


class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                # print(f'Pt: {pt[0]} {pt[1]} Center {cx} {cy}')
                dist = math.hypot(cx - pt[0], cy - pt[1])

            # Maximun distance to be considered a detected object if distance is really low every minimum movement will create a "new" detected object
            # even tho it is the same and if distance is really high every distance movement will be considered the same object 
                if dist < 100:
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    f = open("objects.csv", "a")
                    # Writing on the CSV if it surpass the stimated distance
                    if self.center_points[id][0] > int(1920*0.5*0.45):
                        f.write(f'{id},{self.center_points[id][0]},{self.center_points[id][1]},{datetime.now()},1\n')
                    else:
                        f.write(f'{id},{self.center_points[id][0]},{self.center_points[id][1]},{datetime.now()},0\n')
                    f.close()
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids



