import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import 'alimentos_screen.dart';
import 'vacunas_screen.dart';
import 'seguimientos_screen.dart';
import 'proveedores_screen.dart';
import 'bot_chat_screen.dart';
import 'backups_screen.dart';

class HomeScreen extends StatelessWidget {
  static const routeName = '/';

  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final authProvider = Provider.of<AuthProvider>(context);
    final user = authProvider.currentUser;

    return Scaffold(
      appBar: AppBar(
        title: const Text('App Granja'),
        backgroundColor: Colors.green,
        actions: [
          IconButton(
            icon: const Icon(Icons.exit_to_app),
            onPressed: () async {
              await authProvider.logout();
              if (context.mounted) {
                Navigator.of(context).pushReplacementNamed('/login');
              }
            },
          ),
        ],
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: const BoxDecoration(
                color: Colors.green,
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const CircleAvatar(
                    radius: 30,
                    backgroundColor: Colors.white,
                    child: Icon(
                      Icons.person,
                      size: 40,
                      color: Colors.green,
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    user?.fullName ?? 'Usuario',
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),
                  Text(
                    user?.email ?? '',
                    style: const TextStyle(
                      color: Colors.white70,
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
            ),
            ListTile(
              leading: const Icon(Icons.home),
              title: const Text('Inicio'),
              onTap: () {
                Navigator.pop(context);
              },
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.business),
              title: const Text('Granjas'),
              onTap: () {
                Navigator.pop(context);
                Navigator.of(context).pushNamed('/granjas');
              },
            ),
            ListTile(
              leading: const Icon(Icons.warehouse),
              title: const Text('Galpones'),
              onTap: () {
                Navigator.pop(context);
                Navigator.of(context).pushNamed('/galpones');
              },
            ),
            ListTile(
              leading: const Icon(Icons.pets),
              title: const Text('Razas'),
              onTap: () {
                Navigator.pop(context);
                Navigator.of(context).pushNamed('/razas');
              },
            ),
            ListTile(
              leading: const Icon(Icons.inventory),
              title: const Text('Lotes'),
              onTap: () {
                Navigator.pop(context);
                Navigator.of(context).pushNamed('/lotes');
              },
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.food_bank),
              title: const Text('Alimentos'),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => AlimentosScreen()));
              },
            ),
            ListTile(
              leading: const Icon(Icons.medical_services),
              title: const Text('Vacunas'),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => VacunasScreen()));
              },
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.backup),
              title: const Text('Respaldos'),
              onTap: () {
                Navigator.pop(context);
                Navigator.of(context).pushNamed('/backups');
              },
            ),
            ListTile(
              leading: const Icon(Icons.monitor_heart),
              title: const Text('Seguimientos'),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => SeguimientosScreen()));
              },
            ),
            ListTile(
              leading: const Icon(Icons.people_alt),
              title: const Text('Proveedores'),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => ProveedoresScreen()));
              },
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.book),
              title: const Text('Wiki'),
              onTap: () {
                Navigator.pop(context);
                Navigator.of(context).pushNamed('/wiki');
              },
            ),
            ListTile(
              leading: const Icon(Icons.question_answer),
              title: const Text('FAQ'),
              onTap: () {
                Navigator.pop(context);
                Navigator.of(context).pushNamed('/faq');
              },
            ),
            ListTile(
              leading: const Icon(Icons.chat),
              title: const Text('Asistente Virtual'),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => BotChatScreen()));
              },
            ),
          ],
        ),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(
                Icons.agriculture,
                size: 80,
                color: Colors.green,
              ),
              const SizedBox(height: 24),
              Text(
                'Bienvenido, ${user?.firstName ?? 'Usuario'}',
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              const Text(
                'Sistema de Gestión Avícola',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.grey,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 48),
              // Tarjetas de acceso rápido
              Expanded(
                child: GridView.count(
                  crossAxisCount: 2,
                  crossAxisSpacing: 16,
                  mainAxisSpacing: 16,
                  children: [
                    _buildMenuCard(
                      context,
                      'Granjas',
                      Icons.business,
                      Colors.green.shade700,
                      () => Navigator.of(context).pushNamed('/granjas'),
                    ),
                    _buildMenuCard(
                      context,
                      'Galpones',
                      Icons.warehouse,
                      Colors.orange.shade700,
                      () => Navigator.of(context).pushNamed('/galpones'),
                    ),
                    _buildMenuCard(
                      context,
                      'Razas',
                      Icons.pets,
                      Colors.blue.shade700,
                      () => Navigator.of(context).pushNamed('/razas'),
                    ),
                    _buildMenuCard(
                      context,
                      'Lotes',
                      Icons.inventory,
                      Colors.purple.shade700,
                      () => Navigator.of(context).pushNamed('/lotes'),
                    ),
                    _buildMenuCard(
                      context,
                      'Alimentos',
                      Icons.food_bank,
                      Colors.amber.shade700,
                      () => Navigator.push(context, MaterialPageRoute(builder: (context) => AlimentosScreen())),
                    ),
                    _buildMenuCard(
                      context,
                      'Vacunas',
                      Icons.medical_services,
                      Colors.red.shade700,
                      () => Navigator.push(context, MaterialPageRoute(builder: (context) => VacunasScreen())),
                    ),
                    _buildMenuCard(
                      context,
                      'Seguimientos',
                      Icons.monitor_heart,
                      Colors.teal.shade700,
                      () => Navigator.push(context, MaterialPageRoute(builder: (context) => SeguimientosScreen())),
                    ),
                    _buildMenuCard(
                      context,
                      'Proveedores',
                      Icons.people_alt,
                      Colors.indigo.shade700,
                      () => Navigator.push(context, MaterialPageRoute(builder: (context) => ProveedoresScreen())),
                    ),
                    _buildMenuCard(
                      context,
                      'Asistente Virtual',
                      Icons.chat,
                      Colors.green.shade900,
                      () => Navigator.push(context, MaterialPageRoute(builder: (context) => BotChatScreen())),
                    ),
                    _buildMenuCard(
                      context,
                      'Respaldos',
                      Icons.backup,
                      Colors.deepPurple.shade700,
                      () => Navigator.of(context).pushNamed('/backups'),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMenuCard(
    BuildContext context,
    String title,
    IconData icon,
    Color color,
    VoidCallback onTap,
  ) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircleAvatar(
              radius: 30,
              backgroundColor: color.withOpacity(0.2),
              child: Icon(
                icon,
                size: 30,
                color: color,
              ),
            ),
            const SizedBox(height: 16),
            Text(
              title,
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
