# -----------------------------------------
# This script will compress each SVG into Hexadecimal form which in turn will be uploaded as an Ethscription.
# -----------------------------------------

import os
import base64
import subprocess

# Define the directories and file paths
input_dir = 'input_svgs'
output_dir = 'output_svgs'
base64_dir = 'base64_svgs'
hex_dir = 'hex_svgs'

# Create output directories if they don't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(base64_dir, exist_ok=True)
os.makedirs(hex_dir, exist_ok=True)

# Function to optimize SVG with SVGO
def optimize_svg(input_path, output_path):
    subprocess.run(['svgo', input_path, '-o', output_path])

# Function to compress SVG with Brotli
def compress_brotli(input_path, output_path):
    subprocess.run(['brotli', input_path, '-o', output_path])

# Function to convert file to base64
def convert_to_base64(input_path, output_path):
    with open(input_path, 'rb') as file:
        base64_data = base64.b64encode(file.read()).decode('utf-8')
    with open(output_path, 'w') as file:
        file.write(base64_data)

# Function to convert base64 to hexadecimal
def convert_base64_to_hex(input_path, output_path):
    with open(input_path, 'r') as file:
        base64_data = file.read()
    hex_data = base64.b64decode(base64_data).hex()
    with open(output_path, 'w') as file:
        file.write(hex_data)

# Process each SVG file
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.svg'):
            relative_path = os.path.relpath(root, input_dir)
            svg_input_path = os.path.join(root, file)
            svg_output_path = os.path.join(output_dir, relative_path, file)
            brotli_output_path = os.path.join(output_dir, relative_path, file + '.br')
            base64_output_path = os.path.join(base64_dir, relative_path, file + '.base64')
            hex_output_path = os.path.join(hex_dir, relative_path, file + '.hex')

            # Create necessary directories
            os.makedirs(os.path.dirname(svg_output_path), exist_ok=True)
            os.makedirs(os.path.dirname(brotli_output_path), exist_ok=True)
            os.makedirs(os.path.dirname(base64_output_path), exist_ok=True)
            os.makedirs(os.path.dirname(hex_output_path), exist_ok=True)

            # Optimize, compress, convert to base64, and convert to hex
            optimize_svg(svg_input_path, svg_output_path)
            compress_brotli(svg_output_path, brotli_output_path)
            convert_to_base64(brotli_output_path, base64_output_path)
            convert_base64_to_hex(base64_output_path, hex_output_path)

# Display message to indicate processing is complete
print("Processing complete. Optimized, compressed, base64, and hex files are saved in their respective directories.")
