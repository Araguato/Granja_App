import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:qr_code_scanner/qr_code_scanner.dart';
import 'dart:io';
import 'dart:async';

import '../services/api_service.dart';

class ConnectionConfigScreen extends StatefulWidget {
  const ConnectionConfigScreen({Key? key}) : super(key: key);

  @override
  _ConnectionConfigScreenState createState() => _ConnectionConfigScreenState();
}

class _ConnectionConfigScreenState extends State<ConnectionConfigScreen> {
  final GlobalKey qrKey = GlobalKey(debugLabel: 'QR');
  QRViewController? controller;
  final TextEditingController _urlController = TextEditingController();
  String _connectionStatus = 'No probado';
  bool _isLoading = false;
  bool _isScanning = false;

  @override
  void initState() {
    super.initState();
    _loadCurrentUrl();
  }

  @override
  void dispose() {
    controller?.dispose();
    _urlController.dispose();
    super.dispose();
  }

  // En dispositivos iOS, la cámara necesita ser pausada/reanudada
  @override
  void reassemble() {
    super.reassemble();
    if (Platform.isAndroid) {
      controller!.pauseCamera();
    } else if (Platform.isIOS) {
      controller!.resumeCamera();
    }
  }

  Future<void> _loadCurrentUrl() async {
    final apiService = Provider.of<ApiService>(context, listen: false);
    final currentUrl = await apiService.getBaseUrl();
    setState(() {
      _urlController.text = currentUrl;
    });
  }

  Future<void> _testConnection() async {
    setState(() {
      _isLoading = true;
      _connectionStatus = 'Probando conexión...';
    });

    try {
      final apiService = Provider.of<ApiService>(context, listen: false);
      await apiService.setBaseUrl(_urlController.text);
      
      // Intentar obtener la raíz de la API
      final result = await apiService.get('');
      
      setState(() {
        _isLoading = false;
        _connectionStatus = 'Conexión exitosa';
      });
      
      // Mostrar diálogo de éxito
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Conexión exitosa con el servidor'),
          backgroundColor: Colors.green,
        ),
      );
    } catch (e) {
      setState(() {
        _isLoading = false;
        _connectionStatus = 'Error: ${e.toString()}';
      });
      
      // Mostrar diálogo de error
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error de conexión: ${e.toString()}'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  void _onQRViewCreated(QRViewController controller) {
    this.controller = controller;
    controller.scannedDataStream.listen((scanData) {
      if (scanData.code != null && _isScanning) {
        setState(() {
          _isScanning = false;
          _urlController.text = scanData.code!;
        });
        controller.pauseCamera();
        Navigator.pop(context); // Cerrar el diálogo de escaneo
      }
    });
  }

  void _showQRScanner() {
    setState(() {
      _isScanning = true;
    });
    
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Escanear código QR'),
          content: Container(
            height: 300,
            width: 300,
            child: QRView(
              key: qrKey,
              onQRViewCreated: _onQRViewCreated,
              overlay: QrScannerOverlayShape(
                borderColor: Colors.green,
                borderRadius: 10,
                borderLength: 30,
                borderWidth: 10,
                cutOutSize: 250,
              ),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                setState(() {
                  _isScanning = false;
                });
                controller?.pauseCamera();
                Navigator.pop(context);
              },
              child: const Text('Cancelar'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Configuración de Conexión'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'URL del Servidor',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _urlController,
                    decoration: const InputDecoration(
                      hintText: 'http://192.168.1.100:8000/api/',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.qr_code_scanner),
                  onPressed: _showQRScanner,
                  tooltip: 'Escanear código QR',
                ),
              ],
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _isLoading ? null : _testConnection,
              child: _isLoading
                  ? const CircularProgressIndicator()
                  : const Text('Probar Conexión'),
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: _connectionStatus.contains('exitosa')
                    ? Colors.green.withOpacity(0.1)
                    : _connectionStatus.contains('Error')
                        ? Colors.red.withOpacity(0.1)
                        : Colors.grey.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Estado de la Conexión:',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  Text(_connectionStatus),
                ],
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              'Instrucciones:',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              '1. Ingrese la URL del servidor Django o escanee el código QR generado por la aplicación de Windows.\n'
              '2. Asegúrese de incluir el protocolo (http:// o https://) y el puerto si es necesario.\n'
              '3. La URL debe terminar con /api/\n'
              '4. Presione "Probar Conexión" para verificar que puede conectarse al servidor.',
              style: TextStyle(fontSize: 14),
            ),
          ],
        ),
      ),
    );
  }
}
