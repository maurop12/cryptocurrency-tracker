import time
from config import CRYPTO_NAMES, MENU_ITEMS, REFRESH_INTERVAL, LONG_PRESS_DURATION
from api import fetch_crypto_data
from display import display_crypto, display_logo, display_menu, display_switching, clear_display
from buttons import button_pressed, BTN1_PIN, BTN2_PIN

current_crypto_index = 0
last_refresh_time = 0
last_press_time = 0
waiting_for_long_press = False
long_press_detected = False
display_on = True
in_menu_mode = False
current_menu_index = 0

try:
    price, change = fetch_crypto_data(current_crypto_index)
    display_crypto(CRYPTO_NAMES[current_crypto_index], price, change)
    last_refresh_time = time.time()

    while True:
        now = time.time()

        if button_pressed(BTN1_PIN):
            if not waiting_for_long_press:
                last_press_time = now
                waiting_for_long_press = True
            else:
                if now - last_press_time >= LONG_PRESS_DURATION:
                    waiting_for_long_press = False
                    display_logo(current_crypto_index)
                    time.sleep(3)
                    price, change = fetch_crypto_data(current_crypto_index)
                    display_crypto(CRYPTO_NAMES[current_crypto_index], price, change)
            time.sleep(0.2)
        else:
            if waiting_for_long_press:
                waiting_for_long_press = False
                current_crypto_index = (current_crypto_index + 1) % len(CRYPTO_NAMES)
                display_switching(CRYPTO_NAMES[current_crypto_index])
                time.sleep(1)
                price, change = fetch_crypto_data(current_crypto_index)
                display_crypto(CRYPTO_NAMES[current_crypto_index], price, change)

        if button_pressed(BTN2_PIN):
            press_start = now
            while button_pressed(BTN2_PIN):
                if time.time() - press_start >= LONG_PRESS_DURATION:
                    long_press_detected = True
                    if not in_menu_mode:
                        display_on = not display_on
                        if display_on:
                            price, change = fetch_crypto_data(current_crypto_index)
                            display_crypto(CRYPTO_NAMES[current_crypto_index], price, change)
                        else:
                            clear_display()
                    else:
                        in_menu_mode = False
                        current_crypto_index = current_menu_index
                        price, change = fetch_crypto_data(current_crypto_index)
                        display_crypto(CRYPTO_NAMES[current_crypto_index], price, change)
                    time.sleep(0.3)
                    break
            if not long_press_detected:
                if not in_menu_mode:
                    in_menu_mode = True
                    current_menu_index = 0
                    display_menu(current_menu_index)
                    time.sleep(0.2)
                else:
                    current_menu_index = (current_menu_index + 1) % len(MENU_ITEMS)
                    display_menu(current_menu_index)
                    time.sleep(0.2)
            else:
                long_press_detected = False

        if not in_menu_mode and display_on and (now - last_refresh_time >= REFRESH_INTERVAL):
            last_refresh_time = now
            price, change = fetch_crypto_data(current_crypto_index)
            display_crypto(CRYPTO_NAMES[current_crypto_index], price, change)

        time.sleep(0.05)

except KeyboardInterrupt:
    clear_display()
    import RPi.GPIO as GPIO
    GPIO.cleanup()
    print("Exiting.")