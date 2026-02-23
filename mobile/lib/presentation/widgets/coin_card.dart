import 'package:flutter/material.dart';
import '../../core/constants/app_colors.dart';
import 'signal_badge.dart';

class CoinCard extends StatelessWidget {
  final String symbol;
  final double price;
  final double rsi;
  final String signal;
  final double? change24h;

  const CoinCard({
    super.key,
    required this.symbol,
    required this.price,
    required this.rsi,
    required this.signal,
    this.change24h,
  });

  @override
  Widget build(BuildContext context) {
    final isPositive = (change24h ?? 0) >= 0;
    
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        onTap: () {
          // TODO: Navigate to coin detail
        },
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              // Symbol and RSI
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      symbol,
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: AppColors.textPrimary,
                          ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'RSI: ${rsi.toStringAsFixed(1)}',
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                            color: AppColors.textSecondary,
                          ),
                    ),
                  ],
                ),
              ),
              
              // Price and Change
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(
                    '\$${price.toStringAsFixed(2)}',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                          color: AppColors.textPrimary,
                        ),
                  ),
                  if (change24h != null) ...[
                    const SizedBox(height: 4),
                    Text(
                      '${isPositive ? '+' : ''}${change24h!.toStringAsFixed(2)}%',
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                            color: isPositive ? AppColors.buyGreen : AppColors.sellRed,
                            fontWeight: FontWeight.w600,
                          ),
                    ),
                  ],
                  const SizedBox(height: 8),
                  SignalBadge(signal: signal),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
