import 'package:flutter/material.dart';
import '../../core/constants/app_colors.dart';

class SignalBadge extends StatelessWidget {
  final String signal;

  const SignalBadge({super.key, required this.signal});

  Color get _color {
    switch (signal.toUpperCase()) {
      case 'BUY':
        return AppColors.buyGreen;
      case 'SELL':
        return AppColors.sellRed;
      default:
        return AppColors.holdGray;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: _color.withOpacity(0.2),
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: _color, width: 1),
      ),
      child: Text(
        signal.toUpperCase(),
        style: TextStyle(
          color: _color,
          fontWeight: FontWeight.bold,
          fontSize: 12,
        ),
      ),
    );
  }
}
