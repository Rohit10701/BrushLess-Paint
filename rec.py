from threading import Thread

from operator import rshift
import cv2 as cv
import numpy as np
import mediapipe as mp
import autopy
from canvas import *
from pynput.mouse import Button, Controller
mouse = Controller()


def mainfile():
    # import your script A
    mp_face_mesh = mp.solutions.face_mesh
    LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
    RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
    LEFT_IRIS = [474, 475, 476, 477]
    RIGHT_IRIS = [469, 470, 471, 472]
    cap = cv.VideoCapture(0)

    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
    ) as face_mesh:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv.flip(frame, 1)
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results = face_mesh.process(rgb_frame)
            if results.multi_face_landmarks:
                mesh_points = np.array(
                    [np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in
                     results.multi_face_landmarks[0].landmark])

                (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                center_left = np.array([l_cx, l_cy], dtype=np.int32)
                center_right = np.array([r_cx, r_cy], dtype=np.int32)

                print(l_radius)
                try:
                    autopy.mouse.move(center_right[0], center_right[1])
                    iris_coordinate = [center_right[0], center_right[1]]

                    mouse.press(Button.left)
                    data_collection(iris_coordinate)
                except:
                    continue
                cv.circle(frame, center_left, 1, (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, center_right, 1, (255, 0, 255), 1, cv.LINE_AA)

            # cv.imshow('img', frame)
            key = cv.waitKey(1)
            if key == ord('q'):
                break
    cap.release()
    cv.destroyAllWindows()

def subfile():
    # import your script B
    def data_collection(iris_coordinate):
        CanvasWithBrush.paint(iris_coordinate)

    class CanvasWithBrush(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("canvas")
            self.geometry("600x410")
            self.canvas = tk.Canvas(self, bg="white", cursor="pencil")
            self.canvas.pack(fill=tk.BOTH, expand=True)
            self.brush_size = 5
            self.canvas.bind("<B1-Motion>", self.paint)

        def paint(self, event):
            x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
            x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
            self.canvas.create_oval(x1, y1, x2, y2, fill="black")

    if __name__ == "__main__":
        app = CanvasWithBrush()
        app.mainloop()


Thread(target = subfile).start()
Thread(target = mainfile).start()
