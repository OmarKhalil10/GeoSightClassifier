from flask import Flask, request, render_template, send_from_directory, jsonify, Response
import uuid
import os
import numpy as np
import torch
import torchvision.transforms as T
from PIL import Image
import io

app = Flask(__name__,template_folder='templates')

# Health check route
@app.route("/isalive")
def is_alive():
    print("/isalive request")
    status_code = Response(status=200)
    return status_code

# Load the model
learn_inf = torch.jit.load("model_data/transfer_exported.pt")

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file:
            try:
                # Generate a unique filename using a timestamp and a random string
                unique_filename = f"uploaded_image_{uuid.uuid4().hex}.jpg"

                # Save the uploaded image to a temporary location with the unique filename
                img_path = os.path.join("uploads", unique_filename)
                img = Image.open(uploaded_file)
                img.save(img_path)

                # Transform to tensor
                timg = T.ToTensor()(img).unsqueeze_(0)

                # Calling the model
                softmax = learn_inf(timg).data.cpu().numpy().squeeze()

                # Get the indexes of the classes ordered by softmax
                idxs = np.argsort(softmax)[::-1]

                # Get the top 5 predictions
                top_classes = [learn_inf.class_names[idx] for idx in idxs[:5]]
                top_probs = [float(softmax[idx]) for idx in idxs[:5]]

                # Calculate the maximum probability
                max_prob = max(top_probs)

                # Return predictions as JSON, including the unique filename
                return jsonify({
                    "classes": top_classes,
                    "probs": top_probs,
                    "image_path": img_path,
                    "max_prob": max_prob,
                })
            except Exception as e:
                return jsonify({"error": str(e)})

    # Return an empty JSON response if no file was uploaded or an error occurred
    return jsonify({})


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)  