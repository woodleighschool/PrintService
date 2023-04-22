# PrintService

This Python script provides a REST API to print images on a Brother QL-820NWB label printer. The script uses the `flask` library to create a REST API and the `PIL` library to open and manipulate image files. The `brother_ql` library is used to convert the image to printer instructions and send them to the printer.

## Dependencies

-   Python 3.11
-   Flask
-   Pillow
-   brother_ql

## Setup

1. Clone the repository.
2. Install the required packages using pip: `pip install -r requirements.txt`
3. Connect your Brother QL-820NWB printer to your computer.
4. Set the `backend` and `model` variables in the script to match your printer's settings. You can find the `backend` identifier in the Brother QL-820NWB manual or by using the `brother_ql.list_models()` function. The `model` should match the printer model you are using.
5. Set the `printer` variable to match your printer's USB address. You can find this by running `lsusb` in the terminal and looking for your printer's vendor ID (`04f9`) and product ID (`209d`).
6. Set the `API_TOKEN` environment variable to a secure token that will be used to authenticate API requests.
7. Run the script using `python3 main.py`.

The application should now be listening for POST requests at `http://localhost:5000/print_image`.

## Usage

-   Send a POST request to `http://localhost:5000/print_image` with a PNG image file attached in the `file` field of the request body and an `Authorization` header set to `Bearer <API_TOKEN>`.
-   The image will be added to a queue and printed by the printer.
-   If the image cannot be printed, a JSON response with an error message will be returned. If the image is printed successfully, a JSON response with a success message will be returned.
