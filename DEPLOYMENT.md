# 🚀 Deployment Guide

## VPS Deployment (Ubuntu Server)

### 1. Server Setup

```bash
# SSH into your VPS
ssh user@your-vps-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3.9 python3-pip python3-venv nginx git -y
```

### 2. Clone Repository

```bash
git clone https://github.com/ashu13579/crypto-rsi-signals.git
cd crypto-rsi-signals/backend
```

### 3. Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
# Copy environment file
cp .env.example .env

# Edit with production values
nano .env
```

**Important settings to change:**
- `SECRET_KEY` - Generate a strong secret key
- `DATABASE_URL` - Use PostgreSQL in production
- `ALLOWED_ORIGINS` - Add your frontend domain
- `DEBUG=False`

### 5. Create Systemd Service

```bash
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
WorkingDirectory=/home/user/crypto-rsi-signals/backend
Environment="PATH=/home/user/crypto-rsi-signals/backend/venv/bin"
EnvironmentFile=/home/user/crypto-rsi-signals/backend/.env
ExecStart=/home/user/crypto-rsi-signals/backend/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start and enable service
sudo systemctl daemon-reload
sudo systemctl start crypto-rsi
sudo systemctl enable crypto-rsi
sudo systemctl status crypto-rsi
```

### 6. Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/crypto-rsi
```

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

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
```

### 7. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d api.yourdomain.com
```

### 8. PostgreSQL Setup (Production)

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Create database
sudo -u postgres psql

CREATE DATABASE crypto_rsi;
CREATE USER crypto_user WITH PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE crypto_rsi TO crypto_user;
\q
```

Update `.env`:
```
DATABASE_URL=postgresql://crypto_user:strong_password_here@localhost/crypto_rsi
```

```bash
# Restart service
sudo systemctl restart crypto-rsi
```

---

## Docker Deployment

### Quick Start

```bash
# Clone repository
git clone https://github.com/ashu13579/crypto-rsi-signals.git
cd crypto-rsi-signals

# Build and run
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop
docker-compose down
```

---

## Mobile App Deployment

### Android

```bash
cd mobile

# Build APK
flutter build apk --release

# APK location: build/app/outputs/flutter-apk/app-release.apk
```

### iOS

```bash
# Build iOS
flutter build ios --release

# Open Xcode and archive for App Store
```

### Update API URL

Edit `mobile/lib/core/constants/api_constants.dart`:
```dart
static const String baseUrl = 'https://api.yourdomain.com';
```

---

## Monitoring

### View Logs

```bash
# Application logs
tail -f backend/logs/app.log

# Systemd logs
sudo journalctl -u crypto-rsi -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Check

```bash
curl https://api.yourdomain.com/health
```

---

## Maintenance

### Update Code

```bash
cd crypto-rsi-signals
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart crypto-rsi
```

### Database Backup

```bash
# PostgreSQL backup
pg_dump crypto_rsi > backup_$(date +%Y%m%d).sql

# Restore
psql crypto_rsi < backup_20240101.sql
```

---

## Security Checklist

- [ ] Change default `SECRET_KEY` in `.env`
- [ ] Use strong database passwords
- [ ] Enable firewall (ufw)
- [ ] Setup fail2ban
- [ ] Regular security updates
- [ ] Monitor logs
- [ ] Backup database regularly
- [ ] Use HTTPS only
- [ ] Implement rate limiting
- [ ] Secure API keys

---

## Troubleshooting

### Service won't start

```bash
# Check logs
sudo journalctl -u crypto-rsi -n 50

# Check permissions
ls -la /home/user/crypto-rsi-signals/backend

# Test manually
cd /home/user/crypto-rsi-signals/backend
source venv/bin/activate
python -m app.main
```

### Database connection issues

```bash
# Test PostgreSQL connection
psql -U crypto_user -d crypto_rsi -h localhost

# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL
```

---

**Production Ready!** 🎉
