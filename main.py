import time
from config import CRYPTO_NAMES, MENU_ITEMS, REFRESH_INTERVAL, LONG_PRESS_DURATION
from api import fetch_crypto_data, get_historical_prices
from display import display_crypto, display_logo, display_menu, clear_display, display_graph
from buttons import button_pressed, BTN1_PIN, BTN2_PIN

current_crypto_index = 0
last_refresh_time = 0
waiting_for_btn1_long_press = False
btn1_press_start = 0
waiting_for_btn2_long_press = False
btn2_press_start = 0
long_press_handled = False
long_press_detected = False
display_states = ['price', 'graph', 'image']
current_display_state = 0
graph_intervals = ["1d", "7d", "30d"]
current_graph_interval_index = 0
in_menu_mode = False
current_menu_index = 0
display_on = True

try:
    price, change = fetch_crypto_data(current_crypto_index)
    display_crypto(CRYPTO_NAMES[current_crypto_index], price, change)
    last_refresh_time = time.time()

    while True:
        now = time.time()

        if button_pressed(BTN1_PIN):
            if not waiting_for_btn1_long_press:
                btn1_press_start = now
                waiting_for_btn1_long_press = True
                long_press_handled = False
            else:
                if now - btn1_press_start >= LONG_PRESS_DURATION and not long_press_handled:
                    if display_states[current_display_state] == 'graph':
                        current_graph_interval_index = (current_graph_interval_index + 1) % len(graph_intervals)
                        display_graph(current_crypto_index, graph_intervals, current_graph_interval_index)
                        long_press_handled = True
            time.sleep(0.1)
        else:
            if waiting_for_btn1_long_press:
                waiting_for_btn1_long_press = False
                if now - btn1_press_start < LONG_PRESS_DURATION and not long_press_handled:
                    current_display_state = (current_display_state + 1) % len(display_states)
                    state = display_states[current_display_state]
                    if state == 'price':
                        current_graph_interval_index = 0
                        price, change = fetch_crypto_data(current_crypto_index)
                        display_crypto(CRYPTO_NAMES[current_crypto_index], price, change)
                    elif state == 'graph':
                        display_graph(current_crypto_index, graph_intervals, current_graph_interval_index)
                    elif state == 'image':
                        display_logo(current_crypto_index)
                long_press_handled = False

        if button_pressed(BTN2_PIN):
            if not waiting_for_btn2_long_press:
                btn2_press_start = now
                waiting_for_btn2_long_press = True
                long_press_handled = False
            else:
                if now - btn2_press_start >= LONG_PRESS_DURATION and not long_press_handled:
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
                        current_display_state = 0
                        current_graph_interval_index = 0
                        price, change = fetch_crypto_data(current_crypto_index)
                        display_crypto(CRYPTO_NAMES[current_crypto_index], price, change)
                    long_press_handled = True
                    waiting_for_btn2_long_press = True
            time.sleep(0.3)
        else:
            if waiting_for_btn2_long_press:
                waiting_for_btn2_long_press = False
                if now - btn2_press_start < LONG_PRESS_DURATION and not long_press_detected:
                    if not in_menu_mode:
                        in_menu_mode = True
                        current_menu_index = 0
                        current_graph_interval_index = 0
                    else:
                        current_menu_index = (current_menu_index + 1) % len(MENU_ITEMS)
                    display_menu(current_menu_index)
                    time.sleep(0.2)
                long_press_detected = False

        if not in_menu_mode and display_on and (now - last_refresh_time >= REFRESH_INTERVAL):
            last_refresh_time = now
            if display_states[current_display_state] == 'price':
                price, change = fetch_crypto_data(current_crypto_index)
                display_crypto(CRYPTO_NAMES[current_crypto_index], price, change)

        time.sleep(0.05)

except KeyboardInterrupt:
    clear_display()
    import RPi.GPIO as GPIO
    GPIO.cleanup()
    print("Exiting.")