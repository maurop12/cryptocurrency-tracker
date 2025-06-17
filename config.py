SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
OLED_I2C_ADDRESS = 0x3C

BTN1_PIN = 17
BTN2_PIN = 27

REFRESH_INTERVAL = 10
LONG_PRESS_DURATION = 0.9

CRYPTO_URLS = [
    "https://rest.coincap.io/v3/assets/bitcoin",
    "https://rest.coincap.io/v3/assets/ethereum",
    "https://rest.coincap.io/v3/assets/solana",
    "https://rest.coincap.io/v3/assets/cardano"
]
CRYPTO_NAMES = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD"]
MENU_ITEMS = ["Bitcoin", "Ethereum", "Solana", "Cardano"]

BITMAP_FILES = [
    "bitmap_imgs/btc1.PNG",
    "bitmap_imgs/eth1.PNG",
    "bitmap_imgs/sol1.PNG",
    "bitmap_imgs/ada.PNG"
]
COINCAP_SYMBOLS = ["bitcoin", "ethereum", "solana", "cardano"]

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'sender@gmail.com'
EMAIL_PASSWORD = 'pass'
TO_EMAIL = 'recipient@gmail.com'

ALERT_CHECK_INTERVAL = 300
ALERT_THRESHOLDS = {
    "bitcoin": 120000,
    "ethereum": 4000,
    "solana": 200,
    "cardano": 2
}

PIN = "0000"