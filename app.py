from flask import Flask, request, jsonify, Response
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2
import pygame
import threading
import random
from PIL import Image

# Initialize Flask app
app = Flask(__name__)

# Load the TensorFlow model
model_path = "ai/keras_model.h5"  # Update to the correct path
model = load_model(model_path)

# Load labels for predictions
label_file_path = "ai/labels.txt"  # Update to the correct path
with open(label_file_path, "r") as f:
    labels = [line.strip() for line in f]

# Initialize Pygame
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Stream Example")

# Preprocess image function for prediction
def preprocess_image(image, target_size=(224, 224)):
    image = load_img(image, target_size=target_size)
    image = img_to_array(image) / 255.0
    return np.expand_dims(image, axis=0)

# Route for image prediction
@app.route('/predict', methods=['POST'])
def predict():
    if not os.path.exists(model_path):
        return jsonify({"error": "Model file not found"}), 500
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        # Save the file temporarily
        file_path = os.path.join("ai/temp", file.filename)
        file.save(file_path)
        
        # Check if the file was saved successfully
        if not os.path.exists(file_path):
            return jsonify({"error": "Failed to save file"}), 500

        # Preprocess the image
        preprocessed_image = preprocess_image(file_path)
        predictions = model.predict(preprocessed_image)
        predicted_label = labels[np.argmax(predictions)]

        # Clean up
        os.remove(file_path)

        return jsonify({"predicted_label": predicted_label})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to update pygame window
def pygame_game():
    clock = pygame.time.Clock()
    running = True
    x, y = 50, 50  # Initial position of the red square
    speed = 5  # Movement speed

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Randomly update the position of the red square
        x += random.randint(-speed, speed)
        y += random.randint(-speed, speed)

        # Keep the square within bounds of the screen
        x = max(0, min(width - 100, x))
        y = max(0, min(height - 100, y))

        screen.fill((0, 0, 255))  # Blue background
        pygame.draw.rect(screen, (255, 0, 0), (x, y, 100, 100))  # Red square
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Function to capture pygame screen and stream as MJPEG
def generate_frames():
    while True:
        # Capture pygame screen
        pygame_surface = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame_surface = pygame_surface.swapaxes(0, 1)  # Correct axis for OpenCV

        # Convert to OpenCV image
        frame = cv2.cvtColor(pygame_surface, cv2.COLOR_RGB2BGR)

        # Encode as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to stream the pygame output
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Start the Flask app with threading for Pygame
if __name__ == '__main__':
    # Run pygame in a separate thread
    threading.Thread(target=pygame_game, daemon=True).start()

    # Start Flask server
    app.run(debug=True, host='0.0.0.0')
