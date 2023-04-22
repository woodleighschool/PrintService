import os
from flask import Flask, jsonify, request
from PIL import Image
from brother_ql.backends.helpers import send
from brother_ql.conversion import convert
from brother_ql.raster import BrotherQLRaster

app = Flask(__name__)

# make sure queue path exists
if not os.path.exists("queue"):
    os.makedirs("queue")

# Set printer properties
backend = 'pyusb'
model = 'QL-820NWB'
printer = 'usb://0x04f9:0x209d'


def print_image(image_name):
    try:
        # Open image file
        im = Image.open(f'queue/{image_name}')

        # Convert image to printer instructions
        qlr = BrotherQLRaster(model)
        qlr.exception_on_warning = True
        instructions = convert(
            qlr=qlr,
            images=[im],
            label='62',
            rotate='0',
            threshold=70.0,
            dither=False,
            compress=False,
            red=False,
            dpi_600=False,
            hq=True,
            cut=True
        )

        # Send instructions to printer
        send(instructions=instructions, printer_identifier=printer,
             backend_identifier=backend, blocking=True)

        # Remove image file
        os.remove(f'queue/{image_name}')

    except Exception as e:
        # Send error response
        response = {'status': f'Error printing image {image_name}: {e}'}
        return jsonify(response), 400

    # Send success response
    response = {'status': 'Print successful'}
    return jsonify(response), 200


@app.route('/print_image', methods=['POST'])
def print_image_endpoint():
    # Check for authentication
    api_token = os.getenv('API_TOKEN')
    api_key = request.headers.get('Authorization')
    if api_key != f'Bearer {api_token}':
        response = {'status': 'Unauthorized'}
        return jsonify(response), 401

    # Check if file was sent
    if 'file' not in request.files:
        response = {'status': 'No file uploaded'}
        return jsonify(response), 400

    file = request.files['file']

    # Check if file is PNG
    if not file.filename.endswith('.png'):
        response = {'status': 'Only PNG files are allowed'}
        return jsonify(response), 400

    # Save file
    file.save(f'queue/{file.filename}')

    # Print image
    return print_image(file.filename)


if __name__ == '__main__':
    app.run()
