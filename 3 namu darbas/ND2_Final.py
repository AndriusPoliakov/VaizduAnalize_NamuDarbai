import cv2
import numpy as np
import os

def load_video(video_path):
    cap = cv2.VideoCapture(video_path)
    return cap

def select_drone_region(frame):
    """Leidžia vartotojui rankiniu būdu pasirinkti drono vietą pirmame kadre."""
    roi = cv2.selectROI("Pažymėkite droną", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()
    return roi

def track_drone(video_path, output_path):
    cap = load_video(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    
    ret, frame = cap.read()
    if not ret:
        print("Klaida: nepavyko nuskaityti vaizdo įrašo.")
        return
    
    roi = select_drone_region(frame)
    tracker = cv2.legacy.TrackerCSRT_create()
    tracker.init(frame, roi)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        success, box = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Dronas", (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        out.write(frame)
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "input_video_1080_2.mp4"
    output_path = "output_video_1080_2.avi"
    
    track_drone(video_path, output_path)
    print("Apdorotas vaizdo įrašas išsaugotas.")