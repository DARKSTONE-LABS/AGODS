import random
from PIL import Image, ImageFont, ImageDraw, ImageStat, ImageEnhance

def get_block_brightness(img_block):
    grayscale = img_block.convert("L")
    stat = ImageStat.Stat(grayscale)
    return stat.mean[0]

def enhance_color(color):
    r, g, b = color
    enhance = lambda x: int(255 * ((x / 255.0) ** 0.33))  # tweak this for more pop
    return enhance(r), enhance(g), enhance(b)

def get_block_color(img_block):
    stat = ImageStat.Stat(img_block)
    r, g, b = stat.mean[0], stat.mean[1], stat.mean[2]
    return enhance_color((int(r), int(g), int(b)))

def image_to_ascii(img, font_size=10, charset=None):
    if charset is None:
        charset = "@%#8WM*oahkbdpwmZO0QCJYXzcvnxrjft/\|()1{}[]?-_+~<>i!lI;:,\^`'. "

    width, height = img.size
    block_width = block_height = font_size

    ascii_img = []
    colors = []

    for y in range(0, height, block_height):
        line_chars = []
        line_colors = []
        for x in range(0, width, block_width):
            block = img.crop((x, y, x + block_width, y + block_height))
            brightness = get_block_brightness(block)
            color = get_block_color(block)
            char = charset[int(brightness * (len(charset)-1) / 255)]
            line_chars.append(char)
            line_colors.append(color)
        ascii_img.append(line_chars)
        colors.append(line_colors)

    return ascii_img, colors

def ascii_to_image(ascii_data, base_image, font_size=10):
    ascii_img, colors = ascii_data
    img = base_image.copy()
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    y_offset = 0
    for line_idx, line in enumerate(ascii_img):
        x_offset = 0
        for char_idx, char in enumerate(line):
            char_color = colors[line_idx][char_idx]
            random_offset_x = random.randint(-3, 3)
            random_offset_y = random.randint(-3, 3)
            draw.text((x_offset + random_offset_x, y_offset + random_offset_y), char, font=font, fill=char_color)
            x_offset += font_size
        y_offset += font_size

    return img

def dim_image(img, factor=0.95):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)

if __name__ == "__main__":
    img_path = 'IMG_1414.png'
    font_size = 11
    img = Image.open(img_path)
    dimmed_img = dim_image(img)
    ascii_data = image_to_ascii(dimmed_img, font_size)
    output_img = ascii_to_image(ascii_data, dimmed_img, font_size)
    output_img.save('BUNJIL.png')
