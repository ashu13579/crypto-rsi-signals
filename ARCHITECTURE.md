# 🏗️ Architecture Documentation

## System Overview

```
┌─────────────────┐
│  Flutter App    │
│  (Mobile)       │
└────────┬────────┘
         │ REST API
         ▼
┌─────────────────┐
│  FastAPI        │
│  Backend        │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────┐
│ SQLite │ │ CCXT │
│   DB   │ │Binance│
└────────┘ └──────┘
```

---

## Backend Architecture

### Layers

1. **API Layer** (`app/api/`)
   - REST endpoints
   - Request/response handling
   - Input validation

2. **Service Layer** (`app/services/`)
   - Business logic
   - Market data fetching
   - RSI calculation
   - Signal detection

3. **Data Layer** (`app/models/`)
   - Database models
   - ORM (SQLAlchemy)

4. **Background Tasks** (`app/tasks/`)
   - Signal scanner (60s interval)
   - Async processing

### Core Components

#### MarketDataService
```python
- fetch_ohlcv(symbol, timeframe) → DataFrame
- fetch_ticker(symbol) → Dict
- fetch_multiple_tickers(symbols) → List[Dict]
```

#### RSICalculator
```python
- calculate(df, period=14) → Series
- get_current_rsi(df) → float
- get_previous_rsi(df) → float
```

#### SignalDetector
```python
- detect_signal(df) → (SignalType, float)
- is_oversold(rsi) → bool
- is_overbought(rsi) → bool
```

#### SignalScanner
```python
- scan_symbol(symbol) → Signal
- scan_all_symbols() → List[Signal]
- start() → continuous scanning
```

---

## Frontend Architecture (Flutter)

### Structure

```
lib/
├── core/
│   ├── constants/      # App-wide constants
│   ├── network/        # API client, Dio setup
│   └── storage/        # Secure storage, cache
├── data/
│   ├── models/         # Data models
│   └── repositories/   # API repositories
├── providers/          # Riverpod state management
└── presentation/
    ├── screens/        # App screens
    └── widgets/        # Reusable widgets
```

### State Management

**Riverpod Providers:**
- `signalProvider` - Signal data
- `marketProvider` - Market data
- `settingsProvider` - User settings

### Screens

1. **Dashboard** - Coin list with signals
2. **Coin Detail** - Chart, RSI, signal history
3. **Signal History** - Filterable signal log
4. **Settings** - RSI config, API keys
5. **Alerts** - Push notification log

---

## Data Flow

### Signal Detection Flow

```
1. Scanner triggers every 60s
2. For each symbol:
   a. Fetch OHLCV from Binance (CCXT)
   b. Calculate RSI(14)
   c. Detect crossover:
      - BUY: RSI crosses above 30
      - SELL: RSI crosses below 70
      - HOLD: No crossover
   d. Store signal in database
3. Mobile app polls /api/v1/signals
4. Display signals with color coding
```

### API Request Flow

```
Mobile App → Dio Client → FastAPI → Service Layer → CCXT/Database → Response
```

---

## Database Schema

### Signal Table
```sql
CREATE TABLE signals (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR NOT NULL,
    signal_type ENUM('BUY', 'SELL', 'HOLD'),
    rsi_value FLOAT NOT NULL,
    price FLOAT NOT NULL,
    timeframe VARCHAR DEFAULT '1h',
    timestamp DATETIME NOT NULL,
    created_at DATETIME DEFAULT NOW()
);
```

### UserSettings Table
```sql
CREATE TABLE user_settings (
    id INTEGER PRIMARY KEY,
    user_id VARCHAR UNIQUE NOT NULL,
    rsi_period INTEGER DEFAULT 14,
    rsi_oversold INTEGER DEFAULT 30,
    rsi_overbought INTEGER DEFAULT 70,
    timeframe VARCHAR DEFAULT '1h',
    notifications_enabled BOOLEAN DEFAULT TRUE,
    exchange_api_key VARCHAR,
    exchange_api_secret VARCHAR,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME
);
```

---

## API Endpoints

### Signals
- `GET /api/v1/signals` - List signals (paginated)
- `GET /api/v1/signals/{symbol}` - Symbol history
- `GET /api/v1/signals/active` - Active signals only

### Market
- `GET /api/v1/market/{symbol}` - Price + RSI + Signal
- `GET /api/v1/market/overview/all` - All symbols

### Settings
- `GET /api/v1/settings` - Get user settings
- `POST /api/v1/settings` - Update settings
- `POST /api/v1/settings/paper-trade` - Paper trade

---

## Signal Strategy

### RSI Indicator
- **Period**: 14 (configurable)
- **Oversold**: 30 (configurable)
- **Overbought**: 70 (configurable)

### Signal Logic
```python
if previous_rsi <= 30 and current_rsi > 30:
    return BUY  # Oversold → Normal

if previous_rsi >= 70 and current_rsi < 70:
    return SELL  # Overbought → Normal

return HOLD  # No crossover
```

---

## Security

### Backend
- Environment variables for secrets
- CORS configuration
- Input validation (Pydantic)
- Rate limiting ready
- HTTPS in production

### Mobile
- Flutter Secure Storage for API keys
- Certificate pinning (optional)
- Code obfuscation in release
- No hardcoded secrets

---

## Scalability

### Current Capacity
- 20+ symbols
- 60s scan interval
- SQLite (dev) / PostgreSQL (prod)

### Future Enhancements
- WebSocket for real-time updates
- Redis caching
- Horizontal scaling with load balancer
- Multi-exchange support
- Microservices architecture

---

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn/Gunicorn
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Exchange**: CCXT
- **Analysis**: Pandas, TA
- **Async**: asyncio

### Frontend
- **Framework**: Flutter
- **State**: Riverpod
- **Network**: Dio
- **Storage**: Hive, Secure Storage
- **Notifications**: Firebase
- **UI**: Material 3, Google Fonts

---

## Performance

### Backend
- Async I/O for concurrent requests
- Connection pooling
- Background task isolation
- Rate limiting to exchanges

### Mobile
- Offline caching
- Lazy loading
- Image caching
- Pagination

---

**Clean, modular, production-ready architecture** ✨
