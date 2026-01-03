#!/usr/bin/env python3
"""
Create minimal placeholder PNG icons without external dependencies.
These are simple colored squares - replace with proper icons for production.
"""

import zlib
import struct
import os

def create_png(width, height, color, filename):
    """Create a simple solid-color PNG file."""
    def png_chunk(chunk_type, data):
        chunk_len = struct.pack('>I', len(data))
        chunk_crc = struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)
        return chunk_len + chunk_type + data + chunk_crc

    # PNG signature
    signature = b'\x89PNG\r\n\x1a\n'

    # IHDR chunk (image header)
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = png_chunk(b'IHDR', ihdr_data)

    # IDAT chunk (image data)
    raw_data = b''
    r, g, b = color
    for y in range(height):
        raw_data += b'\x00'  # Filter type: None
        for x in range(width):
            raw_data += bytes([r, g, b])

    compressed = zlib.compress(raw_data, 9)
    idat = png_chunk(b'IDAT', compressed)

    # IEND chunk
    iend = png_chunk(b'IEND', b'')

    # Write PNG file
    with open(filename, 'wb') as f:
        f.write(signature + ihdr + idat + iend)
    print(f"Created {filename} ({width}x{height})")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    # Streamlit red color
    streamlit_red = (255, 75, 75)
    create_png(72, 72, streamlit_red, 'PACKAGE_ICON.PNG')
    create_png(256, 256, streamlit_red, 'PACKAGE_ICON_256.PNG')
    print("\nPlaceholder icons created. Replace with proper icons for production.")
