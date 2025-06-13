# Cryptocurrency Tracker

A Raspberry Pi-based cryptocurrency price tracker with OLED display, featuring real-time price monitoring, historical graphs, email alerts, and secure PIN authentication.

## Features

- **Real-time Price Display**: Live cryptocurrency prices for Bitcoin, Ethereum, Solana, and Cardano
- **Interactive Graph Visualization**: Historical price charts with 1-day, 7-day, and 30-day intervals
- **Email Price Alerts**: Automatic notifications when prices cross configured thresholds
- **Secure PIN Authentication**: Terminal-based PIN prompt for secure access
- **Button Controls**: Navigate between cryptocurrencies and display modes using physical buttons
- **OLED Display**: Clear visual interface on SSD1306 128x64 OLED screen

## Hardware Requirements

- Raspberry Pi (any model with GPIO)
- SSD1306 OLED Display (128x64, I2C)
- 2 Push Buttons
- Jumper wires and breadboard
- Internet connection

## Wiring

| Component | Raspberry Pi GPIO |
|-----------|-------------------|
| OLED SDA  | GPIO 2 (SDA)     |
| OLED SCL  | GPIO 3 (SCL)     |
| Button 1  | GPIO 17          |
| Button 2  | GPIO 27          |
| OLED VCC  | 3.3V             |
| OLED GND  | GND              |

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/maurop12/cryptocurrency-tracker.git
cd cryptocurrency-tracker
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```
4. **Enable I2C on Raspberry Pi:**
```bash
sudo raspi-config
# Navigate to Interface Options > I2C > Enable  
```
5. **Configure settings:**
- Edit `config.py` to set your email credentials and alert thresholds
- Update the PIN in `config.py` for secure access

## Usage

1. **Run the application:**
```bash
python main.py
```
2. **Enter your PIN** when prompted for secure access

3. **Button Controls:**
    - Button 1 (Short Press): Cycle through display modes (Price → Graph → Logo)
    - Button 1 (Long Press): Switch graph time intervals (1d → 7d → 30d)
    - Button 2 (Short Press): Enter menu mode and navigate cryptocurrencies
    - Button 2 (Long Press): Toggle display on/off or select cryptocurrency

## Configuration

### Email Alerts
Edit `config.py` to configure email notifications:  
```bash
EMAIL_ADDRESS = 'your-email@gmail.com'  
EMAIL_PASSWORD = 'your-app-password'  
TO_EMAIL = 'recipient@gmail.com'  

ALERT_THRESHOLDS = {  
    "bitcoin": 120000,  
    "ethereum": 4000,  
    "solana": 200,  
    "cardano": 2  
}
```
### PIN Security
Set your secure PIN in `config.py`:
```bash 
  PIN = "1234"  # Change to your preferred PIN
```
## API

This project uses the [CoinCap API](https://coincap.io/) for real-time cryptocurrency data. An API key is included but you can obtain your own at coincap.io.

## Dependencies

- `requests` - HTTP requests for API calls
- `RPi.GPIO` - Raspberry Pi GPIO control
- `Pillow` - Image processing for OLED display
- `luma.oled` - OLED display driver

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Troubleshooting

### Common Issues

- **Display not working**: Check I2C connections and ensure I2C is enabled
- **Button not responding**: Verify GPIO pin connections and pull-up resistors
- **API errors**: Check internet connection and API key validity
- **Email alerts not working**: Verify SMTP settings and app password

### Support

For issues and questions, please open an issue on GitHub.

