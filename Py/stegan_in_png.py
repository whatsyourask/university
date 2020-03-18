from PIL import Image

original = Image.open('container.png')
width, height = original.size

steg = Image.new('RGB', (width, height))
# For instance
bits = [1, 0, 0, 1, 1, ...]

idx = 0
# Pixel selection
for i in range(width):
    for j in range(height):
        # Get r, g, b from pixel
        r, g, b = original.getpixel((i, j))
        # Only red channel
        if bits[idx] == 0:
            # 10011011 & 11111110 = 10011010 (change last bit)
            r &= 254
        else:
            # 01001100 | 00000001 = 01001101 (change last bit)
            r |= 1
        steg.putpixel((i, j), (r, g, b))
        idx += 1
# Save file
steg.save('with_message.png')
