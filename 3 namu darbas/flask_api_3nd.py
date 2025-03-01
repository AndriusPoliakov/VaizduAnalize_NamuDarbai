from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
import os
import torch
import clip
from PIL import Image
from werkzeug.utils import secure_filename
from ND1_Final import predict_landmark, annotate_image
from ND2_Final import track_drone
from flask_cors import CORS  # Pridedame CORS biblioteką

app = Flask(__name__)
CORS(app)  # Leidžiame užklausas iš React (localhost:3000)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def load_clip_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess, device

model, preprocess, device = load_clip_model()

def process_image(image_path):
    texts = ["Eiffel Tower", "Statue of Liberty", "Big Ben", "Colosseum", "Unknown"]
    text_tokens = clip.tokenize(texts).to(device)
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_tokens)
        similarities = (image_features @ text_features.T).softmax(dim=-1).cpu().numpy()
    
    best_match_idx = np.argmax(similarities)
    return texts[best_match_idx], similarities[0][best_match_idx]

def annotate_image(image_path, label):
    image = cv2.imread(image_path)
    cv2.putText(image, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    processed_path = os.path.join(PROCESSED_FOLDER, os.path.basename(image_path))
    cv2.imwrite(processed_path, image)
    return processed_path

@app.route('/upload/image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    landmark, confidence = process_image(file_path)
    annotated_path = annotate_image(file_path, f"{landmark} ({confidence:.2f})")
    
    return send_file(annotated_path, mimetype='image/jpeg')

@app.route('/upload/video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    output_path = os.path.join(PROCESSED_FOLDER, "processed_" + filename)
    track_drone(file_path, output_path)
    
    return send_file(output_path, mimetype='video/x-msvideo')

def track_drone(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    
    ret, frame = cap.read()
    if not ret:
        return
    
    roi = (100, 100, 50, 50)  # Placeholder for drone region
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
            cv2.putText(frame, "Dronas", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        out.write(frame)
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    app.run(debug=True)