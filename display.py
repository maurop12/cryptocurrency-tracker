from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from config import SCREEN_WIDTH, SCREEN_HEIGHT, OLED_I2C_ADDRESS, BITMAP_FILES, MENU_ITEMS, PIN
from api import get_historical_prices, fetch_crypto_data
import time

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
    font = ImageFont.load_default()
    print_center(draw, "MENU", 0, font)
    num_items = len(MENU_ITEMS)
    menu_area_height = SCREEN_HEIGHT - 16
    line_spacing = menu_area_height // num_items
    start_y = 16
    for i, item in enumerate(MENU_ITEMS):
        prefix = "> " if i == current_menu_index else "  "
        text = prefix + item
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        y = start_y + i * line_spacing
        x = (SCREEN_WIDTH - w) // 2
        draw.text((x, y), text, font=font, fill=255)
    device.display(img)

def display_crypto(name, price, change):
    img = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
    draw = ImageDraw.Draw(img)
    font_small = ImageFont.load_default()
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    print_center(draw, name, 0, font_small)
    print_center(draw, price, 22, font_large)
    print_center(draw, f"24hr Change: {change}%", 50, font_small)
    device.display(img)

def clear_display():
    img = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
    device.display(img)
    device.clear()

def display_graph(index, graph_intervals, current_graph_interval_index):
    interval = graph_intervals[current_graph_interval_index]
    prices = get_historical_prices(index, interval)
    img = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    font_labels = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)

    print_center(draw, f"Graph {interval}", 0, font)

    label_padding_top = 9.5
    label_padding_bottom = 14
    graph_top = 16 + label_padding_top
    graph_bottom = SCREEN_HEIGHT - label_padding_bottom
    graph_left = 10
    graph_right = SCREEN_WIDTH - 10
    graph_width = graph_right - graph_left
    graph_height = graph_bottom - graph_top

    min_p = min(prices)
    max_p = max(prices)
    if max_p == min_p:
        max_p += 1

    def y_pos(p):
        return graph_bottom - int((p - min_p) / (max_p - min_p) * graph_height) if max_p != min_p else graph_bottom

    points = []
    for i, price in enumerate(prices):
        x = graph_left + int(i * graph_width / (len(prices) - 1))
        y = y_pos(price)
        points.append((x, y))

    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        draw.line((x1, y1, x2, y2), fill=255)
        draw.line((x1, y1-1, x2, y2-1), fill=255)
        draw.line((x1, y1+1, x2, y2+1), fill=255)

    min_text = f"${min_p:.2f}"
    max_text = f"${max_p:.2f}"

    max_bbox = draw.textbbox((0, 0), max_text, font=font_labels)
    max_w = max_bbox[2] - max_bbox[0]
    max_h = max_bbox[3] - max_bbox[1]
    draw.text((graph_left, graph_top - max_h - 2), max_text, font=font_labels, fill=255)

    min_bbox = draw.textbbox((0, 0), min_text, font=font_labels)
    min_h = min_bbox[3] - min_bbox[1]
    draw.text((graph_left, graph_bottom + 2), min_text, font=font_labels, fill=255)

    device.display(img)

def prompt_pin(current_crypto_index, CRYPTO_NAMES):
    font = ImageFont.load_default()
    input_pin = ""
    attempts = 0
    while attempts < 3:
        img = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
        draw = ImageDraw.Draw(img)
        print_center(draw, "Enter PIN", 10, font)
        print_center(draw, input_pin, 30, font)
        print_center(draw, f"Attempts: {attempts+1}/3", 50, font)
        device.display(img)
        key = input("Enter PIN: ")
        input_pin = key
        if input_pin == PIN:
            price, change = fetch_crypto_data(current_crypto_index)
            display_crypto(CRYPTO_NAMES[current_crypto_index], price, change)
            return True
        else:
            img = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
            draw = ImageDraw.Draw(img)
            print_center(draw, "Wrong PIN", 10, font)
            print_center(draw, f"Attempts: {attempts+1}/3", 30, font)
            device.display(img)
            time.sleep(2)
            input_pin = ""
            attempts += 1
    img = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
    draw = ImageDraw.Draw(img)
    print_center(draw, "Access denied", 10, font)
    print_center(draw, "Exiting...", 30, font)
    device.display(img)
    time.sleep(2)
    return False