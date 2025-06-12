from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from config import SCREEN_WIDTH, SCREEN_HEIGHT, OLED_I2C_ADDRESS, BITMAP_FILES, MENU_ITEMS

serial = i2c(port=1, address=OLED_I2C_ADDRESS)
device = ssd1306(serial, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

def load_logo(index):
    img = Image.open(BITMAP_FILES[index]).convert("1")
    img = img.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
    return img

def print_center(draw, text, y, font=None):
    if font is None:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (SCREEN_WIDTH - w) // 2
    draw.text((x, y), text, font=font, fill=255)

def display_logo(index):
    img = load_logo(index)
    device.display(img)

def display_menu(current_menu_index):
    img = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
    draw = ImageDraw.Draw(img)
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()
    print_center(draw, "MENU", 0, font_large)
    for i, item in enumerate(MENU_ITEMS):
        prefix = "> " if i == current_menu_index else "  "
        draw.text((30, 20 + i * 12), prefix + item, font=font_small, fill=255)
    device.display(img)

def display_crypto(name, price, change):
    img = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
    draw = ImageDraw.Draw(img)
    font_small = ImageFont.load_default()
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    print_center(draw, name, 0, font_small)
    print_center(draw, price, 25, font_large)
    print_center(draw, f"24hr Change: {change}%", 55, font_small)
    device.display(img)

def display_switching(name):
    img = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((0, 0), f"Switching to: {name}", font=font, fill=255)
    device.display(img)

def clear_display():
    img = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
    device.display(img)
    device.clear()