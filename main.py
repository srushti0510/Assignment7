import sys
import qrcode
from dotenv import load_dotenv
import logging
import os
import argparse
from datetime import datetime
import validators  # Import the validators package
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Environment Variables for Configuration
QR_DIRECTORY = os.getenv('QR_CODE_DIR', 'qr_codes')  # Directory for saving QR code
FILL_COLOR = os.getenv('FILL_COLOR', 'red')  # Fill color for the QR code
BACK_COLOR = os.getenv('BACK_COLOR', 'white')  # Background color for the QR code
DEFAULT_URL = os.getenv('QR_DATA_URL', 'https://github.com/srushti0510')  # Default URL

# Set up logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)],
    )

# Create directory if it doesn't exist
def create_directory(path: Path):
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        exit(1)

# Validate the URL
def is_valid_url(url):
    if validators.url(url):
        return True
    else:
        logging.error(f"Invalid URL provided: {url}")
        return False

# Generate and save the QR code
def generate_qr_code(data, path, fill_color='red', back_color='white'):
    if not is_valid_url(data):
        return  # Exit if the URL is invalid

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill=fill_color, back_color=back_color)

        # Save the QR code image to the specified path
        with path.open('wb') as qr_file:
            img.save(qr_file)
        logging.info(f"QR code successfully saved to {path}")

    except Exception as e:
        logging.error(f"An error occurred while generating or saving the QR code: {e}")

# Main function
def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Generate a QR code.')
    parser.add_argument('--url', help='The URL to encode in the QR code', default=DEFAULT_URL)
    args = parser.parse_args()

    # Initial logging setup
    setup_logging()

    # Generate a timestamped filename for the QR code
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename = f"QRCode_{timestamp}.png"

    # Create the full path for the QR code file
    qr_code_full_path = Path.cwd() / QR_DIRECTORY / qr_filename
    
    # Ensure the QR code directory exists
    create_directory(Path.cwd() / QR_DIRECTORY)

    # Generate and save the QR code
    generate_qr_code(args.url, qr_code_full_path, FILL_COLOR, BACK_COLOR)

if __name__ == "__main__":
    main()
