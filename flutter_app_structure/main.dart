import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/auth_provider.dart';
import 'providers/granja_provider.dart';
import 'providers/galpon_provider.dart';
import 'providers/raza_provider.dart';
import 'providers/lote_provider.dart';
import 'providers/backup_provider.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';
import 'screens/granjas_screen.dart';
import 'screens/backups_screen.dart';
import 'screens/backup_details_screen.dart';
import 'screens/backup_config_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => GranjaProvider()),
        ChangeNotifierProvider(create: (_) => GalponProvider()),
        ChangeNotifierProvider(create: (_) => RazaProvider()),
        ChangeNotifierProvider(create: (_) => LoteProvider()),
        ChangeNotifierProvider(create: (_) => BackupProvider()),
      ],
      child: Consumer<AuthProvider>(
        builder: (ctx, authProvider, _) {
          return MaterialApp(
            title: 'App Granja',
            theme: ThemeData(
              primarySwatch: Colors.green,
              visualDensity: VisualDensity.adaptivePlatformDensity,
              fontFamily: 'Roboto',
              appBarTheme: const AppBarTheme(
                backgroundColor: Colors.green,
                foregroundColor: Colors.white,
              ),
            ),
            home: authProvider.isAuthenticated 
                ? const HomeScreen() 
                : const LoginScreen(),
            routes: {
              HomeScreen.routeName: (ctx) => const HomeScreen(),
              LoginScreen.routeName: (ctx) => const LoginScreen(),
              GranjasScreen.routeName: (ctx) => const GranjasScreen(),
              BackupsScreen.routeName: (ctx) => const BackupsScreen(),
              BackupDetailsScreen.routeName: (ctx) => const BackupDetailsScreen(),
              BackupConfigScreen.routeName: (ctx) => const BackupConfigScreen(),
              // Aquí se agregarían las rutas para las demás pantallas
            },
            onGenerateRoute: (settings) {
              // Manejo de rutas dinámicas
              return null;
            },
            onUnknownRoute: (settings) {
              // Manejo de rutas desconocidas
              return MaterialPageRoute(
                builder: (ctx) => const HomeScreen(),
              );
            },
          );
        },
      ),
    );
  }
}
