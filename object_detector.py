import cv2
import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import threading

# Initialize YOLO model (YOLOv5x by default)
model = YOLO('yolov5x.pt')

# Global variable to control the detection process
is_running = False
cap = None  # To store the video capture object

# Stop detection flag to manage stopping process
stop_flag = False

# Function to run detection on video
def detect_objects_on_video(video_path):
    global stop_flag, cap
    cap = cv2.VideoCapture(video_path)

    # Create the window for detection
    cv2.namedWindow('YOLO Object Detection', cv2.WINDOW_NORMAL)

    while cap.isOpened() and not stop_flag:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)  # Perform detection on the frame
        
        # Render results on the frame manually (no plot)
        rendered_frame = frame.copy()

        # Draw bounding boxes and labels manually
        for *xyxy, conf, cls in results[0].boxes.data:  # Access boxes using .boxes.data
            label = f'{model.names[int(cls)]} {conf:.2f}'
            # Draw bounding box
            cv2.rectangle(rendered_frame, (int(xyxy[0]), int(xyxy[1])), 
                          (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
            # Place label above the bounding box
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(rendered_frame, label, (int(xyxy[0]), int(xyxy[1]) - 10),
                        font, 0.5, (0, 255, 0), 2)

        # Display the frame with bounding boxes and labels
        cv2.imshow("YOLO Object Detection", rendered_frame)

        # Resize the window
        cv2.resizeWindow('YOLO Object Detection', 640, 360)

        # Check if 'q' is pressed to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to run detection on webcam
def detect_objects_on_webcam():
    global stop_flag, cap
    cap = cv2.VideoCapture(0)  # 0 for webcam

    # Create the window for webcam detection
    cv2.namedWindow('YOLO Object Detection', cv2.WINDOW_NORMAL)

    while cap.isOpened() and not stop_flag:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)  # Perform detection on the frame
        
        # Render results on the frame manually (no plot)
        rendered_frame = frame.copy()

        # Draw bounding boxes and labels manually
        for *xyxy, conf, cls in results[0].boxes.data:  # Access boxes using .boxes.data
            label = f'{model.names[int(cls)]} {conf:.2f}'
            # Draw bounding box
            cv2.rectangle(rendered_frame, (int(xyxy[0]), int(xyxy[1])), 
                          (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
            # Place label above the bounding box
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(rendered_frame, label, (int(xyxy[0]), int(xyxy[1]) - 10),
                        font, 0.5, (0, 255, 0), 2)

        # Display the frame with bounding boxes and labels
        cv2.imshow("YOLO Object Detection", rendered_frame)

        # Resize the window
        cv2.resizeWindow('YOLO Object Detection', 640, 360)

        # Check if 'q' is pressed to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to start detection on a video file
def start_video_detection():
    video_path = filedialog.askopenfilename(title="Select Video File", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))

    if video_path:
        global stop_flag
        stop_flag = False
        # Run the detection in a separate thread
        threading.Thread(target=detect_objects_on_video, args=(video_path,)).start()

# Function to start detection on webcam
def start_webcam_detection():
    global stop_flag
    stop_flag = False
    # Run the detection in a separate thread
    threading.Thread(target=detect_objects_on_webcam).start()

# Function to stop the detection
def stop_detection():
    global stop_flag
    stop_flag = True  # Set the stop flag to True
    print("Detection stopped.")

# Create the main window
root = tk.Tk()
root.title("YOLO Object Detection")

# Resize the main window to be larger
root.geometry("500x400")  # Set the main window size (width x height)

# Add buttons to start detection
btn_video = tk.Button(root, text="Run Detection on Video", command=start_video_detection, width=25)
btn_video.pack(pady=20)

btn_webcam = tk.Button(root, text="Run Detection on Webcam", command=start_webcam_detection, width=25)
btn_webcam.pack(pady=20)

btn_stop = tk.Button(root, text="Stop Detection", command=stop_detection, width=25)
btn_stop.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
