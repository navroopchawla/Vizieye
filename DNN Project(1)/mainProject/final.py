# # # # # import tkinter as tk
# # # # # from tkinter import ttk
# # # # # import cv2
# # # # # import mediapipe as mp
# # # # # import numpy as np
# # # # # from AppOpener import open
# # # # # from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# # # # # from ctypes import cast, POINTER
# # # # # from comtypes import CLSCTX_ALL
# # # # # import threading
# # # # # import PIL.Image, PIL.ImageTk

# # # # # class HandGestureControllerApp:
# # # # #     def __init__(self, root):
# # # # #         self.root = root
# # # # #         self.root.title("Hand Gesture App Controller")
# # # # #         self.root.geometry("600x700")
        
# # # # #         # Mediapipe setup
# # # # #         self.mp_hands = mp.solutions.hands
# # # # #         self.mp_drawing = mp.solutions.drawing_utils
        
# # # # #         # Apps dictionary
# # # # #         self.apps = {
# # # # #             'A': 'whatsapp',
# # # # #             'B': 'telegram',
# # # # #             'C': 'chrome'
# # # # #         }
        
# # # # #         # Volume control setup
# # # # #         devices = AudioUtilities.GetSpeakers()
# # # # #         interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# # # # #         self.volume = cast(interface, POINTER(IAudioEndpointVolume))
# # # # #         self.minVol, self.maxVol, _ = self.volume.GetVolumeRange()
        
# # # # #         # App state variables
# # # # #         self.last_opened_app = None
# # # # #         self.last_gesture = None
# # # # #         self.consecutive_gesture_frames = 0
        
# # # # #         # Camera and recognition state
# # # # #         self.camera_active = False
# # # # #         self.cap = None
        
# # # # #         # Create GUI components
# # # # #         self.create_widgets()
        
# # # # #     def create_widgets(self):
# # # # #         # Frame for app status
# # # # #         app_frame = ttk.LabelFrame(self.root, text="App Status")
# # # # #         app_frame.pack(padx=10, pady=10, fill='x')
        
# # # # #         self.app_status = {}
# # # # #         for app in ['WhatsApp', 'Telegram', 'Chrome']:
# # # # #             app_label = ttk.Label(app_frame, text=f"{app}: Closed", 
# # # # #                                   foreground='red')
# # # # #             app_label.pack(anchor='w', padx=10, pady=5)
# # # # #             self.app_status[app.lower()] = app_label
        
# # # # #         # Volume control frame
# # # # #         volume_frame = ttk.LabelFrame(self.root, text="Volume Control")
# # # # #         volume_frame.pack(padx=10, pady=10, fill='x')
        
# # # # #         self.volume_scale = ttk.Scale(volume_frame, from_=0, to=100, 
# # # # #                                       orient='horizontal', 
# # # # #                                       command=self.manual_volume_adjust)
# # # # #         self.volume_scale.set(50)
# # # # #         self.volume_scale.pack(padx=10, pady=10, fill='x')
        
# # # # #         self.volume_label = ttk.Label(volume_frame, text="Volume: 50%")
# # # # #         self.volume_label.pack()
        
# # # # #         # Camera feed frame
# # # # #         self.camera_frame = ttk.LabelFrame(self.root, text="Camera Feed")
# # # # #         self.camera_frame.pack(padx=10, pady=10, expand=True, fill='both')
        
# # # # #         self.camera_label = ttk.Label(self.camera_frame)
# # # # #         self.camera_label.pack(padx=10, pady=10)
        
# # # # #         # Control buttons
# # # # #         button_frame = ttk.Frame(self.root)
# # # # #         button_frame.pack(padx=10, pady=10, fill='x')
        
# # # # #         self.camera_button = ttk.Button(button_frame, text="Start Camera", 
# # # # #                                         command=self.toggle_camera)
# # # # #         self.camera_button.pack(side='left', expand=True, padx=5)
        
# # # # #         quit_button = ttk.Button(button_frame, text="Quit", 
# # # # #                                  command=self.on_closing)
# # # # #         quit_button.pack(side='right', expand=True, padx=5)
        
# # # # #         # Gesture info
# # # # #         info_label = ttk.Label(self.root, 
# # # # #             text="Gestures: A (Close) - WhatsApp, B (Far) - Telegram, C (Spread) - Chrome",
# # # # #             font=('Arial', 10, 'italic')
# # # # #         )
# # # # #         info_label.pack(padx=10, pady=5)
        
# # # # #         # Protocol for closing
# # # # #         self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
# # # # #     def manual_volume_adjust(self, val):
# # # # #         volume_val = float(val)
# # # # #         self.volume_label.config(text=f"Volume: {int(volume_val)}%")
# # # # #         vol = np.interp(volume_val, [0, 100], [self.minVol, self.maxVol])
# # # # #         self.volume.SetMasterVolumeLevel(vol, None)
    
# # # # #     def calculate_distance(self, point1, point2):
# # # # #         return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
    
# # # # #     def recognize_gesture(self, hand1, hand2):
# # # # #         if hand1 and hand2:
# # # # #             hand1_thumb_tip = hand1.landmark[4]
# # # # #             hand1_index_tip = hand1.landmark[8]
# # # # #             hand2_thumb_tip = hand2.landmark[4]
# # # # #             hand2_index_tip = hand2.landmark[8]

# # # # #             thumb_distance = self.calculate_distance(hand1_thumb_tip, hand2_thumb_tip)
# # # # #             index_distance = self.calculate_distance(hand1_index_tip, hand2_index_tip)

# # # # #             if thumb_distance < 0.1 and index_distance < 0.1:
# # # # #                 return 'A'
# # # # #             if thumb_distance > 0.4 and index_distance > 0.4:
# # # # #                 return 'B'

# # # # #             thumb1_to_index1 = self.calculate_distance(hand1_thumb_tip, hand1_index_tip)
# # # # #             thumb2_to_index2 = self.calculate_distance(hand2_thumb_tip, hand2_index_tip)

# # # # #             if thumb1_to_index1 > 0.2 and thumb2_to_index2 > 0.2:
# # # # #                 return 'C'
        
# # # # #         if hand1:
# # # # #             thumb_tip = hand1.landmark[4]
# # # # #             index_tip = hand1.landmark[8]
# # # # #             thumb_to_index_distance = self.calculate_distance(thumb_tip, index_tip)
# # # # #             return thumb_to_index_distance

# # # # #         return None
    
# # # # #     def trigger_app(self, gesture):
# # # # #         if gesture in self.apps:
# # # # #             app = self.apps[gesture]
# # # # #             for app_name, label in self.app_status.items():
# # # # #                 if app_name == app:
# # # # #                     label.config(text=f"{app_name.capitalize()}: Open", foreground='green')
# # # # #                 else:
# # # # #                     label.config(text=f"{app_name.capitalize()}: Closed", foreground='red')
            
# # # # #             open(app, match_closest=True)
# # # # #             print(f'Opening {app}...')
    
# # # # #     def process_camera_frame(self):
# # # # #         if not self.camera_active:
# # # # #             return
        
# # # # #         ret, frame = self.cap.read()
# # # # #         if not ret:
# # # # #             return
        
# # # # #         frame = cv2.flip(frame, 1)
# # # # #         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
# # # # #         with self.mp_hands.Hands(
# # # # #             model_complexity=0, 
# # # # #             min_detection_confidence=0.5, 
# # # # #             min_tracking_confidence=0.5, 
# # # # #             max_num_hands=2
# # # # #         ) as hands:
# # # # #             results = hands.process(frame_rgb)
            
# # # # #             if results.multi_hand_landmarks:
# # # # #                 hand1 = results.multi_hand_landmarks[0] if len(results.multi_hand_landmarks) > 0 else None
# # # # #                 hand2 = results.multi_hand_landmarks[1] if len(results.multi_hand_landmarks) > 1 else None
                
# # # # #                 for hand_landmarks in results.multi_hand_landmarks:
# # # # #                     self.mp_drawing.draw_landmarks(
# # # # #                         frame_rgb, 
# # # # #                         hand_landmarks, 
# # # # #                         self.mp_hands.HAND_CONNECTIONS
# # # # #                     )
                
# # # # #                 if hand1 and hand2:
# # # # #                     gesture = self.recognize_gesture(hand1, hand2)
# # # # #                     if isinstance(gesture, str):
# # # # #                         if gesture == self.last_gesture:
# # # # #                             self.consecutive_gesture_frames += 1
# # # # #                         else:
# # # # #                             self.consecutive_gesture_frames = 0
# # # # #                             self.last_gesture = gesture
                        
# # # # #                         if self.consecutive_gesture_frames > 10:
# # # # #                             print(f"Recognized Gesture: {gesture}")
# # # # #                             self.trigger_app(gesture)
# # # # #                             self.consecutive_gesture_frames = 0
                
# # # # #                 elif hand1:
# # # # #                     distance = self.recognize_gesture(hand1, None)
# # # # #                     if isinstance(distance, float):
# # # # #                         normalized_distance = np.clip(distance, 0.05, 0.3)
# # # # #                         vol = np.interp(normalized_distance, [0.05, 0.3], [0, 100])
# # # # #                         self.volume_scale.set(vol)
        
# # # # #         # Convert frame for Tkinter
# # # # #         photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_rgb))
# # # # #         self.camera_label.config(image=photo)
# # # # #         self.camera_label.image = photo
        
# # # # #         # Schedule next frame
# # # # #         self.root.after(10, self.process_camera_frame)
    
# # # # #     def toggle_camera(self):
# # # # #         if not self.camera_active:
# # # # #             self.cap = cv2.VideoCapture(0)
# # # # #             self.cap.set(3, 640)
# # # # #             self.cap.set(4, 480)
# # # # #             self.camera_active = True
# # # # #             self.camera_button.config(text="Stop Camera")
# # # # #             self.process_camera_frame()
# # # # #         else:
# # # # #             self.camera_active = False
# # # # #             if self.cap:
# # # # #                 self.cap.release()
# # # # #             self.camera_button.config(text="Start Camera")
# # # # #             self.camera_label.config(image='')
    
# # # # #     def on_closing(self):
# # # # #         if self.cap:
# # # # #             self.cap.release()
# # # # #         self.root.destroy()

# # # # # def main():
# # # # #     root = tk.Tk()
# # # # #     app = HandGestureControllerApp(root)
# # # # #     root.mainloop()

# # # # # if __name__ == "__main__":
# # # # #     main()







# # # # import cv2
# # # # import mediapipe as mp
# # # # import numpy as np
# # # # from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# # # # from comtypes import CLSCTX_ALL
# # # # from tkinter import Tk, Button
# # # # import os

# # # # # Volume Control Setup
# # # # devices = AudioUtilities.GetSpeakers()
# # # # interface = devices.Activate(
# # # #     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# # # # volume = interface.QueryInterface(IAudioEndpointVolume)

# # # # # Mediapipe Hand Tracking
# # # # mp_hands = mp.solutions.hands
# # # # hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
# # # # mp_draw = mp.solutions.drawing_utils

# # # # # OpenCV Hand Gesture Volume Control
# # # # def volume_control():
# # # #     cap = cv2.VideoCapture(0)
# # # #     while True:
# # # #         success, img = cap.read()
# # # #         if not success:
# # # #             break

# # # #         img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# # # #         results = hands.process(img_rgb)

# # # #         if results.multi_hand_landmarks:
# # # #             for hand_landmarks in results.multi_hand_landmarks:
# # # #                 lm_list = []
# # # #                 for id, lm in enumerate(hand_landmarks.landmark):
# # # #                     h, w, _ = img.shape
# # # #                     cx, cy = int(lm.x * w), int(lm.y * h)
# # # #                     lm_list.append((id, cx, cy))

# # # #                 if len(lm_list) > 8:
# # # #                     thumb_tip = lm_list[4]
# # # #                     index_tip = lm_list[8]

# # # #                     x1, y1 = thumb_tip[1], thumb_tip[2]
# # # #                     x2, y2 = index_tip[1], index_tip[2]
# # # #                     cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
# # # #                     cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)

# # # #                     distance = np.hypot(x2 - x1, y2 - y1)
# # # #                     vol = np.interp(distance, [30, 300], [-65.25, 0])
# # # #                     volume.SetMasterVolumeLevel(vol, None)

# # # #         cv2.imshow("Volume Control", img)
# # # #         if cv2.waitKey(1) & 0xFF == ord('q'):
# # # #             break

# # # #     cap.release()
# # # #     cv2.destroyAllWindows()

# # # # # Launch Apps
# # # # def open_app(app):
# # # #     if app == "whatsapp":
# # # #         os.system("start whatsapp://")
# # # #     elif app == "telegram":
# # # #         os.system("start telegram://")
# # # #     elif app == "chrome":
# # # #         os.system("start chrome")

# # # # # GUI for App Launch
# # # # def create_gui():
# # # #     root = Tk()
# # # #     root.title("App Launcher")

# # # #     Button(root, text="WhatsApp", command=lambda: open_app("whatsapp"), width=20).pack(pady=10)
# # # #     Button(root, text="Telegram", command=lambda: open_app("telegram"), width=20).pack(pady=10)
# # # #     Button(root, text="Chrome", command=lambda: open_app("chrome"), width=20).pack(pady=10)
# # # #     Button(root, text="Volume Control", command=volume_control, width=20).pack(pady=10)

# # # #     root.mainloop()

# # # # if __name__ == "__main__":
# # # #     create_gui()



# # # import cv2
# # # import mediapipe as mp
# # # import numpy as np
# # # from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# # # from comtypes import CLSCTX_ALL
# # # from tkinter import Tk, Button
# # # import os
# # # import threading
# # # import PIL.Image, PIL.ImageTk

# # # # Volume Control Setup
# # # devices = AudioUtilities.GetSpeakers()
# # # interface = devices.Activate(
# # #     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# # # volume = interface.QueryInterface(IAudioEndpointVolume)

# # # # Mediapipe Hand Tracking
# # # mp_hands = mp.solutions.hands
# # # hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
# # # mp_draw = mp.solutions.drawing_utils

# # # # OpenCV Hand Gesture Volume Control
# # # def volume_control():
# # #     cap = cv2.VideoCapture(0)
# # #     while True:
# # #         success, img = cap.read()
# # #         if not success:
# # #             break

# # #         img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# # #         results = hands.process(img_rgb)

# # #         if results.multi_hand_landmarks:
# # #             for hand_landmarks in results.multi_hand_landmarks:
# # #                 lm_list = []
# # #                 for id, lm in enumerate(hand_landmarks.landmark):
# # #                     h, w, _ = img.shape
# # #                     cx, cy = int(lm.x * w), int(lm.y * h)
# # #                     lm_list.append((id, cx, cy))

# # #                 if len(lm_list) > 8:
# # #                     thumb_tip = lm_list[4]
# # #                     index_tip = lm_list[8]

# # #                     x1, y1 = thumb_tip[1], thumb_tip[2]
# # #                     x2, y2 = index_tip[1], index_tip[2]
# # #                     cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
# # #                     cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)

# # #                     distance = np.hypot(x2 - x1, y2 - y1)
# # #                     vol = np.interp(distance, [30, 300], [-65.25, 0])
# # #                     volume.SetMasterVolumeLevel(vol, None)

# # #         cv2.imshow("Volume Control", img)
# # #         if cv2.waitKey(1) & 0xFF == ord('q'):
# # #             break

# # #     cap.release()
# # #     cv2.destroyAllWindows()

# # # # Launch Apps
# # # def open_app(app):
# # #     if app == "whatsapp":
# # #         os.system("start whatsapp://")
# # #     elif app == "telegram":
# # #         os.system("start telegram://")
# # #     elif app == "chrome":
# # #         os.system("start chrome")

# # # # GUI for App Launch
# # # def create_gui():
# # #     root = Tk()
# # #     root.title("App Launcher")

# # #     Button(root, text="WhatsApp", command=lambda: open_app("whatsapp"), width=20).pack(pady=10)
# # #     Button(root, text="Telegram", command=lambda: open_app("telegram"), width=20).pack(pady=10)
# # #     Button(root, text="Chrome", command=lambda: open_app("chrome"), width=20).pack(pady=10)
# # #     Button(root, text="Volume Control", command=volume_control, width=20).pack(pady=10)

# # #     # Camera Feed Section
# # #     camera_frame = Tk.Frame(root)
# # #     camera_frame.pack(padx=10, pady=10, expand=True, fill="both")
# # #     camera_label = Tk.Label(camera_frame)
# # #     camera_label.pack()

# # #     def update_camera_feed():
# # #         cap = cv2.VideoCapture(0)
# # #         while True:
# # #             ret, frame = cap.read()
# # #             if not ret:
# # #                 break

# # #             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# # #             photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_rgb))
# # #             camera_label.config(image=photo)
# # #             camera_label.image = photo
# # #             root.update_idletasks()

# # #         cap.release()

# # #     threading.Thread(target=update_camera_feed, daemon=True).start()

# # #     root.mainloop()

# # # if __name__ == "__main__":
# # #     create_gui()



# # import cv2
# # import mediapipe as mp
# # import numpy as np
# # from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# # from comtypes import CLSCTX_ALL
# # from tkinter import Tk, Button, Label, Frame
# # import os
# # import threading
# # import PIL.Image, PIL.ImageTk

# # # Volume Control Setup
# # devices = AudioUtilities.GetSpeakers()
# # interface = devices.Activate(
# #     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# # volume = interface.QueryInterface(IAudioEndpointVolume)

# # # Mediapipe Hand Tracking
# # mp_hands = mp.solutions.hands
# # hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
# # mp_draw = mp.solutions.drawing_utils

# # # OpenCV Hand Gesture Volume Control
# # def volume_control():
# #     cap = cv2.VideoCapture(0)
# #     while True:
# #         success, img = cap.read()
# #         if not success:
# #             break

# #         img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# #         results = hands.process(img_rgb)

# #         if results.multi_hand_landmarks:
# #             for hand_landmarks in results.multi_hand_landmarks:
# #                 lm_list = []
# #                 for id, lm in enumerate(hand_landmarks.landmark):
# #                     h, w, _ = img.shape
# #                     cx, cy = int(lm.x * w), int(lm.y * h)
# #                     lm_list.append((id, cx, cy))

# #                 if len(lm_list) > 8:
# #                     thumb_tip = lm_list[4]
# #                     index_tip = lm_list[8]

# #                     x1, y1 = thumb_tip[1], thumb_tip[2]
# #                     x2, y2 = index_tip[1], index_tip[2]
# #                     cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
# #                     cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)

# #                     distance = np.hypot(x2 - x1, y2 - y1)
# #                     vol = np.interp(distance, [30, 300], [-65.25, 0])
# #                     volume.SetMasterVolumeLevel(vol, None)

# #         cv2.imshow("Volume Control", img)
# #         if cv2.waitKey(1) & 0xFF == ord('q'):
# #             break

# #     cap.release()
# #     cv2.destroyAllWindows()

# # # Launch Apps
# # def open_app(app):
# #     if app == "whatsapp":
# #         os.system("start whatsapp://")
# #     elif app == "telegram":
# #         os.system("start telegram://")
# #     elif app == "chrome":
# #         os.system("start chrome")

# # # GUI for App Launch
# # def create_gui():
# #     root = Tk()
# #     root.title("App Launcher")

# #     Button(root, text="WhatsApp", command=lambda: open_app("whatsapp"), width=20).pack(pady=10)
# #     Button(root, text="Telegram", command=lambda: open_app("telegram"), width=20).pack(pady=10)
# #     Button(root, text="Chrome", command=lambda: open_app("chrome"), width=20).pack(pady=10)
# #     Button(root, text="Volume Control", command=volume_control, width=20).pack(pady=10)

# #     # Camera Feed Section
# #     camera_frame = Frame(root)  # Use `Frame` here
# #     camera_frame.pack(padx=10, pady=10, expand=True, fill="both")
# #     camera_label = Label(camera_frame)  # Use `Label` here
# #     camera_label.pack()

# #     def update_camera_feed():
# #         cap = cv2.VideoCapture(0)
# #         while True:
# #             ret, frame = cap.read()
# #             if not ret:
# #                 break

# #             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #             photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_rgb))
# #             camera_label.config(image=photo)
# #             camera_label.image = photo
# #             root.update_idletasks()

# #         cap.release()

# #     threading.Thread(target=update_camera_feed, daemon=True).start()

# #     root.mainloop()

# # if __name__ == "__main__":
# #     create_gui()







# import tkinter as tk
# from tkinter import ttk
# import cv2
# import mediapipe as mp
# import numpy as np
# from AppOpener import open
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# import threading
# import PIL.Image, PIL.ImageTk

# class HandGestureControllerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Hand Gesture App Controller")
#         self.root.geometry("600x700")
        
#         # Mediapipe setup
#         self.mp_hands = mp.solutions.hands
#         self.mp_drawing = mp.solutions.drawing_utils
        
#         # Apps dictionary
#         self.apps = {
#             'A': 'whatsapp',
#             'B': 'telegram',
#             'C': 'chrome'
#         }
        
#         # Volume control setup
#         devices = AudioUtilities.GetSpeakers()
#         interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#         self.volume = cast(interface, POINTER(IAudioEndpointVolume))
#         self.minVol, self.maxVol, _ = self.volume.GetVolumeRange()
        
#         # App state variables
#         self.last_opened_app = None
#         self.last_gesture = None
#         self.consecutive_gesture_frames = 0
        
#         # Camera and recognition state
#         self.camera_active = False
#         self.cap = None
        
#         # Create GUI components
#         self.create_widgets()
        
#     def create_widgets(self):
#         # Frame for app status
#         app_frame = ttk.LabelFrame(self.root, text="App Status")
#         app_frame.pack(padx=10, pady=10, fill='x')
        
#         self.app_status = {}
#         for app in ['WhatsApp', 'Telegram', 'Chrome']:
#             app_label = ttk.Label(app_frame, text=f"{app}: Closed", 
#                                   foreground='red')
#             app_label.pack(anchor='w', padx=10, pady=5)
#             self.app_status[app.lower()] = app_label
        
#         # Volume control frame
#         volume_frame = ttk.LabelFrame(self.root, text="Volume Control")
#         volume_frame.pack(padx=10, pady=10, fill='x')
        
#         self.volume_scale = ttk.Scale(volume_frame, from_=0, to=100, 
#                                       orient='horizontal', 
#                                       command=self.manual_volume_adjust)
#         self.volume_scale.set(50)
#         self.volume_scale.pack(padx=10, pady=10, fill='x')
        
#         self.volume_label = ttk.Label(volume_frame, text="Volume: 50%")
#         self.volume_label.pack()
        
#         # Camera feed frame
#         self.camera_frame = ttk.LabelFrame(self.root, text="Camera Feed")
#         self.camera_frame.pack(padx=10, pady=10, expand=True, fill='both')
        
#         self.camera_label = ttk.Label(self.camera_frame)
#         self.camera_label.pack(padx=10, pady=10)
        
#         # Control buttons
#         button_frame = ttk.Frame(self.root)
#         button_frame.pack(padx=10, pady=10, fill='x')
        
#         self.camera_button = ttk.Button(button_frame, text="Start Camera", 
#                                         command=self.toggle_camera)
#         self.camera_button.pack(side='left', expand=True, padx=5)
        
#         quit_button = ttk.Button(button_frame, text="Quit", 
#                                  command=self.on_closing)
#         quit_button.pack(side='right', expand=True, padx=5)
        
#         # Gesture info
#         info_label = ttk.Label(self.root, 
#             text="Gestures: A (Close) - WhatsApp, B (Far) - Telegram, C (Spread) - Chrome",
#             font=('Arial', 10, 'italic')
#         )
#         info_label.pack(padx=10, pady=5)
        
#         # Protocol for closing
#         self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
#     def manual_volume_adjust(self, val):
#         volume_val = float(val)
#         self.volume_label.config(text=f"Volume: {int(volume_val)}%")
#         vol = np.interp(volume_val, [0, 100], [self.minVol, self.maxVol])
#         self.volume.SetMasterVolumeLevel(vol, None)
    
#     def calculate_distance(self, point1, point2):
#         return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
    
#     def recognize_gesture(self, hand1, hand2):
#         if hand1 and hand2:
#             hand1_thumb_tip = hand1.landmark[4]
#             hand1_index_tip = hand1.landmark[8]
#             hand2_thumb_tip = hand2.landmark[4]
#             hand2_index_tip = hand2.landmark[8]

#             thumb_distance = self.calculate_distance(hand1_thumb_tip, hand2_thumb_tip)
#             index_distance = self.calculate_distance(hand1_index_tip, hand2_index_tip)

#             if thumb_distance < 0.1 and index_distance < 0.1:
#                 return 'A'
#             if thumb_distance > 0.4 and index_distance > 0.4:
#                 return 'B'

#             thumb1_to_index1 = self.calculate_distance(hand1_thumb_tip, hand1_index_tip)
#             thumb2_to_index2 = self.calculate_distance(hand2_thumb_tip, hand2_index_tip)

#             if thumb1_to_index1 > 0.2 and thumb2_to_index2 > 0.2:
#                 return 'C'
        
#         if hand1:
#             thumb_tip = hand1.landmark[4]
#             index_tip = hand1.landmark[8]
#             thumb_to_index_distance = self.calculate_distance(thumb_tip, index_tip)
#             return thumb_to_index_distance

#         return None
    
#     def trigger_app(self, gesture):
#         if gesture in self.apps:
#             app = self.apps[gesture]
#             for app_name, label in self.app_status.items():
#                 if app_name == app:
#                     label.config(text=f"{app_name.capitalize()}: Open", foreground='green')
#                 else:
#                     label.config(text=f"{app_name.capitalize()}: Closed", foreground='red')
            
#             open(app, match_closest=True)
#             print(f'Opening {app}...')

#     def process_camera_frame(self):
#         if not self.camera_active:
#             return
        
#         ret, frame = self.cap.read()
#         if not ret:
#             return
        
#         frame = cv2.flip(frame, 1)
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
#         with self.mp_hands.Hands(
#             model_complexity=0, 
#             min_detection_confidence=0.5, 
#             min_tracking_confidence=0.5, 
#             max_num_hands=2
#         ) as hands:
#             results = hands.process(frame_rgb)
            
#             if results.multi_hand_landmarks:
#                 hand1 = results.multi_hand_landmarks[0] if len(results.multi_hand_landmarks) > 0 else None
#                 hand2 = results.multi_hand_landmarks[1] if len(results.multi_hand_landmarks) > 1 else None
                
#                 for hand_landmarks in results.multi_hand_landmarks:
#                     self.mp_drawing.draw_landmarks(
#                         frame_rgb, 
#                         hand_landmarks, 
#                         self.mp_hands.HAND_CONNECTIONS
#                     )
                
#                 if hand1 and hand2:
#                     gesture = self.recognize_gesture(hand1, hand2)
#                     if isinstance(gesture, str):
#                         if gesture == self.last_gesture:
#                             self.consecutive_gesture_frames += 1
#                         else:
#                             self.consecutive_gesture_frames = 0
#                             self.last_gesture = gesture
                    
#                         if self.consecutive_gesture_frames > 10:
#                             print(f"Recognized Gesture: {gesture}")
#                             self.trigger_app(gesture)
#                             self.consecutive_gesture_frames = 0
                
#                 elif hand1:
#                     distance = self.recognize_gesture(hand1, None)
#                     if isinstance(distance, float):
#                         normalized_distance = np.clip(distance, 0.05, 0.3)
#                         vol = np.interp(normalized_distance, [0.05, 0.3], [0, 100])
#                         self.volume_scale.set(vol)
        
#         # Convert frame for Tkinter
#         photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_rgb))
#         self.camera_label.config(image=photo)
#         self.camera_label.image = photo
        
#         # Schedule next frame
#         self.root.after(10, self.process_camera_frame)
    
#     def toggle_camera(self):
#         if not self.camera_active:
#             self.cap = cv2.VideoCapture(0)
#             self.cap.set(3, 640)
#             self.cap.set(4, 480)
#             self.camera_active = True
#             self.camera_button.config(text="Stop Camera")
#             self.process_camera_frame()
#         else:
#             self.camera_active = False
#             if self.cap:
#                 self.cap.release()
#             self.camera_button.config(text="Start Camera")
#             self.camera_label.config(image='')
    
#     def on_closing(self):
#         if self.cap:
#             self.cap.release()
#         self.root.destroy()

# def main():
#     root = tk.Tk()
#     app = HandGestureControllerApp(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()






import tkinter as tk
from tkinter import ttk
import cv2
import mediapipe as mp
import numpy as np
import subprocess
import threading
import PIL.Image, PIL.ImageTk

class HandGestureControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Gesture App Controller")
        self.root.geometry("600x700")
        
        # Mediapipe setup
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Apps dictionary
        self.apps = {
            'A': 'whatsapp',
            'B': 'telegram',
            'C': 'chrome'
        }
        
        # App state variables
        self.last_opened_app = None
        self.last_gesture = None
        self.consecutive_gesture_frames = 0
        
        # Camera and recognition state
        self.camera_active = False
        self.cap = None
        
        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Frame for app status
        app_frame = ttk.LabelFrame(self.root, text="App Status")
        app_frame.pack(padx=10, pady=10, fill='x')
        
        self.app_status = {}
        for app in ['WhatsApp', 'Telegram', 'Chrome']:
            app_label = ttk.Label(app_frame, text=f"{app}: Closed", 
                                  foreground='red')
            app_label.pack(anchor='w', padx=10, pady=5)
            self.app_status[app.lower()] = app_label
        
        # Volume control frame
        volume_frame = ttk.LabelFrame(self.root, text="Volume Control")
        volume_frame.pack(padx=10, pady=10, fill='x')
        
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=100, 
                                      orient='horizontal', 
                                      command=self.manual_volume_adjust)
        self.volume_scale.set(50)
        self.volume_scale.pack(padx=10, pady=10, fill='x')
        
        self.volume_label = ttk.Label(volume_frame, text="Volume: 50%")
        self.volume_label.pack()
        
        # Camera feed frame
        self.camera_frame = ttk.LabelFrame(self.root, text="Camera Feed")
        self.camera_frame.pack(padx=10, pady=10, expand=True, fill='both')
        
        self.camera_label = ttk.Label(self.camera_frame)
        self.camera_label.pack(padx=10, pady=10)
        
        # Control buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(padx=10, pady=10, fill='x')
        
        self.camera_button = ttk.Button(button_frame, text="Start Camera", 
                                        command=self.toggle_camera)
        self.camera_button.pack(side='left', expand=True, padx=5)
        
        quit_button = ttk.Button(button_frame, text="Quit", 
                                 command=self.on_closing)
        quit_button.pack(side='right', expand=True, padx=5)
        
        # Gesture info
        info_label = ttk.Label(self.root, 
            text="Gestures: A (Close) - WhatsApp, B (Far) - Telegram, C (Spread) - Chrome",
            font=('Arial', 10, 'italic')
        )
        info_label.pack(padx=10, pady=5)
        
        # Protocol for closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def manual_volume_adjust(self, val):
        volume_val = float(val)
        self.volume_label.config(text=f"Volume: {int(volume_val)}%")
        # You may add code here to adjust the system volume

    def calculate_distance(self, point1, point2):
        return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    def recognize_gesture(self, hand1, hand2):
        if hand1 and hand2:
            hand1_thumb_tip = hand1.landmark[4]
            hand1_index_tip = hand1.landmark[8]
            hand2_thumb_tip = hand2.landmark[4]
            hand2_index_tip = hand2.landmark[8]

            thumb_distance = self.calculate_distance(hand1_thumb_tip, hand2_thumb_tip)
            index_distance = self.calculate_distance(hand1_index_tip, hand2_index_tip)

            if thumb_distance < 0.1 and index_distance < 0.1:
                return 'A'
            if thumb_distance > 0.4 and index_distance > 0.4:
                return 'B'

            thumb1_to_index1 = self.calculate_distance(hand1_thumb_tip, hand1_index_tip)
            thumb2_to_index2 = self.calculate_distance(hand2_thumb_tip, hand2_index_tip)

            if thumb1_to_index1 > 0.2 and thumb2_to_index2 > 0.2:
                return 'C'
        
        if hand1:
            thumb_tip = hand1.landmark[4]
            index_tip = hand1.landmark[8]
            thumb_to_index_distance = self.calculate_distance(thumb_tip, index_tip)
            return thumb_to_index_distance

        return None

    def trigger_app(self, gesture):
        if gesture in self.apps:
            app = self.apps[gesture]
            for app_name, label in self.app_status.items():
                if app_name == app:
                    label.config(text=f"{app_name.capitalize()}: Open", foreground='green')
                else:
                    label.config(text=f"{app_name.capitalize()}: Closed", foreground='red')
            
            # Open app using subprocess
            self.open_app(app)
            print(f'Opening {app}...')

    def open_app(self, app_name):
        try:
            if app_name == 'whatsapp':
                subprocess.run(["start", "whatsapp"], shell=True)
            elif app_name == 'telegram':
                subprocess.run(["start", "telegram"], shell=True)
            elif app_name == 'chrome':
                subprocess.run(["start", "chrome"], shell=True)
            else:
                print(f"Unknown app: {app_name}")
        except Exception as e:
            print(f"Error opening app: {e}")

    def process_camera_frame(self):
        if not self.camera_active:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return
        
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        with self.mp_hands.Hands(
            model_complexity=0, 
            min_detection_confidence=0.5, 
            min_tracking_confidence=0.5, 
            max_num_hands=2
        ) as hands:
            results = hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                hand1 = results.multi_hand_landmarks[0] if len(results.multi_hand_landmarks) > 0 else None
                hand2 = results.multi_hand_landmarks[1] if len(results.multi_hand_landmarks) > 1 else None
                
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame_rgb, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS
                    )
                
                if hand1 and hand2:
                    gesture = self.recognize_gesture(hand1, hand2)
                    if isinstance(gesture, str):
                        if gesture == self.last_gesture:
                            self.consecutive_gesture_frames += 1
                        else:
                            self.consecutive_gesture_frames = 0
                            self.last_gesture = gesture
                    
                        if self.consecutive_gesture_frames > 10:
                            print(f"Recognized Gesture: {gesture}")
                            self.trigger_app(gesture)
                            self.consecutive_gesture_frames = 0
                
                elif hand1:
                    distance = self.recognize_gesture(hand1, None)
                    if isinstance(distance, float):
                        normalized_distance = np.clip(distance, 0.05, 0.3)
                        vol = np.interp(normalized_distance, [0.05, 0.3], [0, 100])
                        self.volume_scale.set(vol)
        
        # Convert frame for Tkinter
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_rgb))
        self.camera_label.config(image=photo)
        self.camera_label.image = photo
        
        # Schedule next frame
        self.root.after(10, self.process_camera_frame)

    def toggle_camera(self):
        if not self.camera_active:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(3, 640)
            self.cap.set(4, 480)
            self.camera_active = True
            self.camera_button.config(text="Stop Camera")
            self.process_camera_frame()
        else:
            self.camera_active = False
            if self.cap:
                self.cap.release()
            self.camera_button.config(text="Start Camera")
            self.camera_label.config(image='')

    def on_closing(self):
        if self.cap:
            self.cap.release()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = HandGestureControllerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
