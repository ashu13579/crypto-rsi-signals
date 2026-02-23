import 'package:flutter/material.dart';
import '../../widgets/coin_card.dart';
import '../../../core/constants/app_strings.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(AppStrings.appName),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              // TODO: Implement refresh
            },
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              // TODO: Navigate to settings
            },
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          // TODO: Implement pull to refresh
        },
        child: ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: 10, // TODO: Replace with actual data
          itemBuilder: (context, index) => const CoinCard(
            symbol: 'BTC/USDT',
            price: 43250.00,
            rsi: 45.2,
            signal: 'HOLD',
            change24h: 2.5,
          ),
        ),
      ),
    );
  }
}
