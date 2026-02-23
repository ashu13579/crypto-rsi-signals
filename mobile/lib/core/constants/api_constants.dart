class ApiConstants {
  // Base URL - Change this to your backend URL
  static const String baseUrl = 'http://localhost:8000';
  static const String apiVersion = '/api/v1';
  
  // Endpoints
  static const String signals = '/signals';
  static const String market = '/market';
  static const String settings = '/settings';
  static const String paperTrade = '/settings/paper-trade';
  
  // Timeouts
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
  
  // Refresh intervals
  static const Duration autoRefreshInterval = Duration(minutes: 1);
}
