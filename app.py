import os
from flask import Flask, render_template, send_from_directory, request, jsonify, send_file
from gradio_client import Client
from rembg import remove
from PIL import Image
import io
import shutil

app = Flask(__name__)

# Set the HF_TOKEN environment variable if needed
os.environ['HF_TOKEN'] = 'your_token_here'

# Initialize the client for the FLUX model
client = Client("black-forest-labs/FLUX.1-schnell")

# Folder to store generated images
GENERATED_IMAGES_DIR = 'generated_images'
os.makedirs(GENERATED_IMAGES_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    try:
        # Prompt received from the frontend
        prompt = request.json.get('prompt', 'Samurai realistic')  # Default prompt if nothing is entered
        
        # Normalize the prompt:
        # Remove 'tshirt' and 'design' if they appear anywhere in the prompt.
        normalized_prompt = prompt.lower().replace('tshirt', '').replace('design', '').strip()

        # Append 'T-shirt design of' to the modified prompt
        prompt_with_design = f"T-shirt design of {normalized_prompt}"

        # Make the prediction with the modified prompt
        result = client.predict(
            prompt=prompt_with_design,
            seed=0,
            randomize_seed=True,
            width=1024,
            height=1024,
            num_inference_steps=4,
            api_name="/infer"  # Corrected api_name with leading slash
        )

        # Assuming result is a tuple and the first element contains the local path
        image_url = result[0]

        # Save the generated image locally
        image_name = 'generated_image.webp'
        image_path_local = os.path.join(GENERATED_IMAGES_DIR, image_name)

        if image_url.startswith('/tmp'):
            shutil.move(image_url, image_path_local)

        # Return the path to the generated image
        return jsonify({'image_path': image_name})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/remove_background/<filename>', methods=['POST'])
def remove_background(filename):
    try:
        # Open the generated image
        image_path = os.path.join(GENERATED_IMAGES_DIR, filename)
        with Image.open(image_path) as input_image:
            # Save image to BytesIO and read the bytes
            byteImgIO = io.BytesIO()
            input_image.save(byteImgIO, format="PNG")
            byteImgIO.seek(0)
            byteImg = byteImgIO.read()

            # Process the image bytes with rembg
            output = remove(byteImg)

            # Create an Image object from the processed bytes
            output_image = Image.open(io.BytesIO(output))

            # Save the background-removed image in memory for display
            img_io = io.BytesIO()
            output_image.save(img_io, format="PNG")
            img_io.seek(0)

        # Return the processed image for preview
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(GENERATED_IMAGES_DIR, filename)


@app.route('/view_tshirt')
def view_tshirt():
    downloadURL = request.args.get('downloadURL')
    return render_template('view_tshirt.html', downloadURL=downloadURL)

if __name__ == '__main__':
    app.run(debug=True)
