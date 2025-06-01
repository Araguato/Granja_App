import 'package:flutter/material.dart';

class ErrorDialog extends StatelessWidget {
  final String message;
  final String title;
  final VoidCallback? onRetry;

  const ErrorDialog({
    Key? key,
    required this.message,
    this.title = 'Error',
    this.onRetry,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text(title),
      content: Text(message),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Cerrar'),
        ),
        if (onRetry != null)
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              onRetry!();
            },
            child: const Text('Reintentar'),
          ),
      ],
    );
  }
}
