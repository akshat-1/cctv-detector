from ultralytics import YOLO
import cv2
import cvzone
import math

class begin_capture():
    def __init__ (self ,stop_btn, frame_placeholder , model = "yolov8n.pt" ,capture_index =0, stream = True):
        self.model = model
        self.capture_index = capture_index
        self.stream = stream
        self.stop_btn = stop_btn
        self.frame_placeholder = frame_placeholder

    def begin(self):
        cap = cv2.VideoCapture(0)
        cap.set(3,1280)
        cap.set(4,720)

        model = YOLO("../weights/" + self.model)
        classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                    "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                    "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                    "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                    "teddy bear", "hair drier", "toothbrush"
                    ]

        while cap.isOpened() and not self.stop_btn:
            success , img = cap.read()
            img = cv2.flip(img , 1)
            results = model(img , stream=self.stream)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1,y1,x2,y2 = box.xyxy[0]
                    x1 , y1 , x2 ,y2 = int(x1) , int(y1) , int(x2) , int(y2)
                    cv2.rectangle(img , (x1,y1) , (x2,y2), (255 ,0 ,255), 3)

                    w,h = x2-x1 , y2-y1
                    cvzone.cornerRect(img , (x1,y1,w,h))

                    conf = math.ceil((box.conf[0]*100))/100
                    cls = int(box.cls[0])
                    cvzone.putTextRect(img , f'{classNames[cls]} {conf}' , (max(0 , x1),max(35 ,y1)) )

            frame = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)   
            self.frame_placeholder.image(img , channels="RGB")
             
            if ((cv2.waitKey(1) & 0xFF == ord('q'))or self.stop_btn):
                break

            
            cv2.imshow("Image" , img)

        cap.release()
        cv2.destroyAllWindows()