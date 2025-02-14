from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2


"""ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="")
ap.add_argument("-m", "--model", required=True,
	help="")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())"""
c=0
def main():
        CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                "sofa", "train", "tvmonitor"]
        COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
        #print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')
        #print("[INFO] starting video stream...")
        c=0
        detect=[]
        vs = VideoStream(src=2).start()
        time.sleep(2.0)
        fps = FPS().start()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output1.avi',fourcc, 20.0, (640,480))
        while True:
                frame = vs.read()
                frame = imutils.resize(frame, width=800)
                (h, w) = frame.shape[:2]
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                        0.007843, (300, 300), 127.5)
                labels = []
                net.setInput(blob)
                detections = net.forward()
                det_conf = detections[0, 0, :, 2]
                top_indices = [i for i, conf in enumerate(det_conf) if conf >=    0.2]
                top_conf = det_conf[top_indices]
                det_indx = detections[0, 0, :, 1]
                top_label_indices = det_indx[top_indices].tolist()
                if c==0:
                        for i in np.arange(0, detections.shape[2]):
                                confidence = detections[0, 0, i, 2]
                                if confidence > 0.99:
                                        idx = int(detections[0, 0, i, 1])
                                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                                        (startX, startY, endX, endY) = box.astype("int")
                                        label = "{}".format(CLASSES[idx])
                                        if label =='bottle' and c==0:
                                                for i in np.arange(0, detections.shape[2]):
                                                        idx = int(detections[0, 0, i, 1])
                                                        label = "{}".format(CLASSES[idx])
                                                        if label != 'person':
                                                                start=time.time()
                                                                print('Timer Started')
                                                                c=1
                                                                break
                                        cv2.rectangle(frame, (startX, startY), (endX, endY),
                                                COLORS[idx], 2)
                                        y = startY - 15 if startY - 15 > 15 else startY + 15
                                        cv2.putText(frame, label, (startX, y),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                if c==1:
                        for i in np.arange(0, detections.shape[2]):
                                confidence = detections[0, 0, i, 2]
                                if confidence > 0.40:
                                        idx = int(detections[0, 0, i, 1])
                                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                                        (startX, startY, endX, endY) = box.astype("int")

                                                # draw the prediction on the frame
                                        label = "{}".format(CLASSES[idx])
                                        cv2.rectangle(frame, (startX, startY), (endX, endY),
                                                COLORS[idx], 2)
                                        y = startY - 15 if startY - 15 > 15 else startY + 15
                                        if label =='bottle':
                                                cv2.putText(frame, 'Target Object', (startX, y),
                                                        cv2.FONT_HERSHEY_SIMPLEX, 1, COLORS[idx], 2)
                                        else:
                                                cv2.putText(frame, label, (startX, y),
                                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                        detect.append(label)
                        count1=detect.count('person')
                        print(detect)
                        print(count1)
                        end=time.time()
                        dif=end-start
                        print(dif)
                        stime=time.time()
                        if dif> 15 and count1<50:
                                c=2
                        if dif>20 and count1>100:
                                detect = []
                                c=0
                if c==2:
                        for i in np.arange(0, detections.shape[2]):
                                        # extract the confidence (i.e., probability) associated with
                                        # the prediction
                                confidence = detections[0, 0, i, 2]

                                        # filter out weak detections by ensuring the `confidence` is
                                        # greater than the minimum confidence
                                if confidence > 0.40:
                                                # extract the index of the class label from the
                                                # `detections`, then compute the (x, y)-coordinates of
                                                # the bounding box for the object
                                        idx = int(detections[0, 0, i, 1])
                                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                                        (startX, startY, endX, endY) = box.astype("int")

                                                # draw the prediction on the frame
                                        label = "{}".format(CLASSES[idx])
                                        cv2.rectangle(frame, (startX, startY), (endX, endY),
                                                COLORS[idx], 2)
                                        y = startY - 15 if startY - 15 > 15 else startY + 15
                                        if label =='bottle':
                                                cv2.putText(frame, 'Warning', (startX, y),
                                                        cv2.FONT_HERSHEY_SIMPLEX, 1, COLORS[idx], 2)
                                        else:
                                                cv2.putText(frame, label, (startX, y),
                                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                out.write(frame)
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                        break
                fps.update()
        fps.stop()
        cv2.destroyAllWindows()
        vs.stop()
main()
