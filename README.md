# WiFi Credential Manager

A web application for managing and displaying WiFi credentials with QR code support.

## Features
- Display WiFi SSID and password
- Generate QR code for easy WiFi connection
- Dark/Light theme support
- Password-protected edit functionality
- Auto-refresh every 10 minutes
- SQLite database storage

## Installation

1. Clone the repository
```bash
git clone [your-repository-url]
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python main.py
```

5. Access the application at `http://127.0.0.1:8001`

## Default Credentials
- Admin Password: 0422
- Default SSID: DefaultSSID
- Default Password: DefaultPassword

## Stack
- FastAPI
- Jinja2
- SQLAlchemy
- QR Code Generator
