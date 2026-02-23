# ⚡ Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Backend Setup

```bash
# 1. Clone repository
git clone https://github.com/ashu13579/crypto-rsi-signals.git
cd crypto-rsi-signals/backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env

# 5. Run backend
uvicorn app.main:app --reload
```

✅ **Backend running at:** http://localhost:8000  
📚 **API Docs:** http://localhost:8000/docs

---

### Flutter App Setup

```bash
# 1. Navigate to mobile directory
cd mobile

# 2. Get dependencies
flutter pub get

# 3. Run app
flutter run
```

✅ **App running on your device/emulator**

---

### Docker Setup (Easiest)

```bash
# 1. Clone repository
git clone https://github.com/ashu13579/crypto-rsi-signals.git
cd crypto-rsi-signals

# 2. Run with Docker
docker-compose up -d
```

✅ **Everything running!**  
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

---

## 🧪 Test the API

### Get Market Data
```bash
curl http://localhost:8000/api/v1/market/BTC/USDT
```

### Get Signals
```bash
curl http://localhost:8000/api/v1/signals
```

### Health Check
```bash
curl http://localhost:8000/health
```

---

## 📱 Configure Mobile App

Edit `mobile/lib/core/constants/api_constants.dart`:

```dart
static const String baseUrl = 'http://YOUR_IP:8000';  // Change to your backend URL
```

For Android emulator: `http://10.0.2.2:8000`  
For iOS simulator: `http://localhost:8000`  
For physical device: `http://YOUR_COMPUTER_IP:8000`

---

## 🎯 What's Next?

1. **Customize RSI Settings** - Edit `.env` file
2. **Add More Symbols** - Update `DEFAULT_SYMBOLS` in `.env`
3. **Setup Firebase** - For push notifications
4. **Deploy to Production** - See [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🆘 Common Issues

### Backend won't start
```bash
# Check Python version (need 3.9+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Flutter errors
```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter run
```

### Can't connect to backend from mobile
- Check firewall settings
- Use correct IP address
- Ensure backend is running

---

**Happy Trading!** 📈
