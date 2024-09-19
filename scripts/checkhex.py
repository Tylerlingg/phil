# -----------------------------------------
# This script will check the Hexadecimals created and decompress them, turning them back into SVGs so we're able to know that the compression worked.
# -----------------------------------------

import base64
import brotli
import os

# Define the directories
hex_dir = 'hex_svgs'
output_svg_dir = 'verify_output_svgs'

# Create output directory if it doesn't exist
os.makedirs(output_svg_dir, exist_ok=True)

# Function to convert hexadecimal to base64
def hex_to_base64(hex_data):
    return base64.b64encode(bytes.fromhex(hex_data)).decode('utf-8')

# Function to decode base64 to brotli
def base64_to_brotli(base64_data):
    return base64.b64decode(base64_data)

# Function to decompress brotli to SVG
def decompress_brotli(brotli_data):
    return brotli.decompress(brotli_data).decode('utf-8')

# Process each hex file
for root, dirs, files in os.walk(hex_dir):
    for file in files:
        if file.endswith('.hex'):
            relative_path = os.path.relpath(root, hex_dir)
            hex_input_path = os.path.join(root, file)
            svg_output_path = os.path.join(output_svg_dir, os.path.splitext(relative_path)[0] + '.svg')

            # Create necessary directories
            os.makedirs(os.path.dirname(svg_output_path), exist_ok=True)

            # Read hex data
            with open(hex_input_path, 'r') as hex_file:
                hex_data = hex_file.read()

            # Convert hex to base64
            base64_data = hex_to_base64(hex_data)

            # Decode base64 to brotli
            brotli_data = base64_to_brotli(base64_data)

            # Decompress brotli to SVG
            svg_data = decompress_brotli(brotli_data)
            
            # Save the SVG data correctly with an .svg extension and ensure it's properly handled as text
            with open(svg_output_path, 'w', encoding='utf-8') as svg_file:
                svg_file.write(svg_data)

print("Verification complete. SVG files are saved in the verify_output_svgs directory.")
