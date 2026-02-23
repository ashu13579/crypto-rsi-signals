# 🚀 Crypto RSI Signals - Production Ready

## Overview
Production-ready mobile application for real-time cryptocurrency trading signals based on RSI (Relative Strength Index) strategy.

**Architecture**: Flutter Frontend + Python FastAPI Backend

---

## 📁 Project Structure

```
crypto-rsi-signals/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py            # FastAPI app entry
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # Database setup
│   │   ├── models/
│   │   │   ├── signal.py      # Signal model
│   │   │   └── user.py        # User settings model
│   │   ├── schemas/
│   │   │   ├── signal.py      # Pydantic schemas
│   │   │   └── settings.py
│   │   ├── services/
│   │   │   ├── market_data.py # CCXT integration
│   │   │   ├── rsi_calculator.py
│   │   │   └── signal_detector.py
│   │   ├── api/
│   │   │   ├── signals.py     # Signal endpoints
│   │   │   ├── market.py      # Market data endpoints
│   │   │   └── settings.py    # Settings endpoints
│   │   └── tasks/
│   │       └── scanner.py     # Background scanner
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── mobile/                     # Flutter Mobile App
│   ├── lib/
│   │   ├── main.dart
│   │   ├── core/
│   │   │   ├── constants/
│   │   │   ├── network/
│   │   │   └── storage/
│   │   ├── data/
│   │   │   ├── models/
│   │   │   └── repositories/
│   │   ├── providers/
│   │   └── presentation/
│   │       ├── screens/
│   │       │   ├── dashboard/
│   │       │   ├── coin_detail/
│   │       │   ├── signal_history/
│   │       │   ├── settings/
│   │       │   └── alerts/
│   │       └── widgets/
│   └── pubspec.yaml
│
└── docker-compose.yml
```

---

## 🔧 Backend Setup

### Prerequisites
- Python 3.9+
- pip
- virtualenv

### Installation

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

### Run Locally

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**API Documentation**: http://localhost:8000/docs

---

## 📱 Flutter App Setup

### Prerequisites
- Flutter SDK 3.0+
- Dart 3.0+
- Android Studio / Xcode
- Firebase project configured

### Installation

```bash
cd mobile

# Get dependencies
flutter pub get

# Run code generation
flutter pub run build_runner build --delete-conflicting-outputs
```

### Firebase Setup

1. Create Firebase project at https://console.firebase.google.com
2. Add Android/iOS apps
3. Download `google-services.json` (Android) and `GoogleService-Info.plist` (iOS)
4. Install FlutterFire CLI:
   ```bash
   dart pub global activate flutterfire_cli
   flutterfire configure
   ```

### Run App

```bash
# Run on connected device/emulator
flutter run

# Build APK
flutter build apk --release

# Build iOS
flutter build ios --release
```

---

## 🚀 Deployment

### Backend Deployment (VPS - Ubuntu)

```bash
# SSH into your VPS
ssh user@your-vps-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.9 python3-pip python3-venv nginx -y

# Clone repository
git clone https://github.com/ashu13579/crypto-rsi-signals.git
cd crypto-rsi-signals/backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
nano .env  # Edit with production values

# Create systemd service
sudo nano /etc/systemd/system/crypto-rsi.service
```

**Service file content:**
```ini
[Unit]
Description=Crypto RSI Signals API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/crypto-rsi-signals/backend
Environment="PATH=/path/to/crypto-rsi-signals/backend/venv/bin"
EnvironmentFile=/path/to/crypto-rsi-signals/backend/.env
ExecStart=/path/to/crypto-rsi-signals/backend/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl start crypto-rsi
sudo systemctl enable crypto-rsi
sudo systemctl status crypto-rsi
```

**Nginx Configuration:**
```bash
sudo nano /etc/nginx/sites-available/crypto-rsi
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/crypto-rsi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Docker Deployment

```bash
# On VPS or local
git clone https://github.com/ashu13579/crypto-rsi-signals.git
cd crypto-rsi-signals

# Build and run with docker-compose
docker-compose up -d
```

---

## 📊 API Endpoints

### Signals
- `GET /api/v1/signals` - Get latest signals
- `GET /api/v1/signals/{symbol}` - Get signal history for symbol
- `GET /api/v1/signals/active` - Get active signals only

### Market Data
- `GET /api/v1/market/{symbol}` - Get latest price + RSI
- `GET /api/v1/market/overview/all` - Get all symbols overview

### Settings
- `POST /api/v1/settings` - Update user strategy settings
- `GET /api/v1/settings` - Get current settings

### Paper Trading
- `POST /api/v1/settings/paper-trade` - Simulate trade
- `GET /api/v1/settings/paper-trade/history` - Get paper trade history

### Health
- `GET /health` - Health check
- `GET /` - API info

---

## 🎯 Features

### Backend
✅ Multi-symbol scanning (20+ symbols)  
✅ RSI calculation (14 period)  
✅ Signal detection (BUY/SELL/HOLD)  
✅ Background scanner (60s interval)  
✅ REST API with FastAPI  
✅ SQLite/PostgreSQL support  
✅ Auto-generated API docs  
✅ CORS enabled  
✅ Rate limiting ready  

### Mobile App
✅ Dashboard with live signals  
✅ Coin detail with RSI chart  
✅ Signal history with filters  
✅ Settings (RSI thresholds)  
✅ Push notifications (Firebase)  
✅ Dark trading theme (Binance-inspired)  
✅ Auto-refresh (1 min)  
✅ Offline caching  
✅ Loading skeletons  
✅ Paper trading  
✅ Secure API key storage  

---

## 🎨 UI/UX Features

- ✅ Dark trading theme (Binance-inspired)
- ✅ Color-coded signals (Green BUY, Red SELL, Gray HOLD)
- ✅ Auto-refresh every 1 minute
- ✅ Offline caching
- ✅ Loading skeletons
- ✅ Pull-to-refresh
- ✅ Error handling with retry
- ✅ Push notifications

---

## 🔐 Security Best Practices

### Backend
- ✅ Use environment variables for secrets
- ✅ Implement rate limiting
- ✅ Add CORS configuration
- ✅ Use HTTPS in production
- ✅ Validate all inputs
- ✅ Implement authentication (JWT recommended)

### Mobile App
- ✅ Store API keys in Flutter Secure Storage
- ✅ Use certificate pinning for API calls
- ✅ Obfuscate code in release builds
- ✅ Never commit API keys to version control

---

## 📈 Signal Strategy

**BUY Signal**: RSI crosses above 30 (oversold → normal)  
**SELL Signal**: RSI crosses below 70 (overbought → normal)  
**HOLD**: No crossover detected

---

## 🔄 Background Scanner

The scanner runs continuously:
- Scans 20+ symbols every 60 seconds
- Calculates RSI for each
- Detects and stores signals
- Can be extended to WebSocket for real-time updates

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Flutter Tests
```bash
cd mobile
flutter test
flutter test --coverage
```

---

## 📈 Monitoring & Logging

### Backend Logging
- Logs stored in `backend/logs/`
- Use `tail -f logs/app.log` to monitor

### Production Monitoring
- Consider: Sentry, DataDog, or New Relic
- Setup health check endpoints
- Monitor API response times

---

## 🚧 Future Enhancements

- [ ] WebSocket support for real-time updates
- [ ] Multiple RSI strategies (custom periods)
- [ ] Backtesting module
- [ ] Live trading integration
- [ ] Multi-exchange support
- [ ] Advanced charting (candlesticks)
- [ ] Portfolio tracking
- [ ] Social features (share signals)

---

## 📄 License

MIT License

---

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

---

**Built with ❤️ for crypto traders**
