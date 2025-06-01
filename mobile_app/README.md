# App Granja - Aplicación Móvil

Esta es la aplicación móvil para el sistema de gestión avícola App Granja, desarrollada con Flutter.

## Características

- **Autenticación de usuarios**: Inicio de sesión seguro con tokens JWT
- **Dashboard interactivo**: Visualización de estadísticas clave del sistema
- **Gestión de granjas**: Administración de granjas y sus propiedades
- **Gestión de galpones**: Control de galpones y su capacidad
- **Gestión de lotes**: Seguimiento de lotes de aves
- **Gestión de razas**: Información sobre razas y sus características
- **Sistema de respaldos**: Creación, restauración y gestión de respaldos del sistema
- **Asistente virtual**: Chatbot para resolver dudas y proporcionar ayuda
- **Seguimientos**: Registro y monitoreo de seguimientos diarios
- **Gestión de alimentos**: Control de inventario y consumo de alimentos
- **Gestión de vacunas**: Programación y registro de vacunaciones

## Estructura del proyecto

```
lib/
├── models/            # Modelos de datos
├── providers/         # Gestores de estado con Provider
├── screens/           # Pantallas de la aplicación
├── services/          # Servicios para comunicación con API
└── widgets/           # Widgets reutilizables
```

## Requisitos

- Flutter SDK (versión 3.0.0 o superior)
- Dart (versión 3.0.0 o superior)
- Conexión a internet para comunicarse con el servidor
- Servidor Django de App Granja en ejecución

## Configuración

1. Asegúrese de tener Flutter instalado en su sistema
2. Clone este repositorio
3. Ejecute `flutter pub get` para instalar las dependencias
4. Configure la URL de la API en `lib/services/api_service.dart`
5. Ejecute la aplicación con `flutter run`

## Conexión con el servidor

La aplicación se conecta con el servidor Django de App Granja a través de una API REST. Por defecto, la aplicación está configurada para conectarse a:

- `http://10.0.2.2:8000/api/` para emuladores Android
- `http://localhost:8000/api/` para Windows/Web

Si necesita cambiar esta configuración, edite el archivo `lib/services/api_service.dart`.

## Compilación

Para compilar la aplicación para diferentes plataformas:

### Android
```
flutter build apk --release
```

### iOS
```
flutter build ios --release
```

### Windows
```
flutter build windows --release
```

## Dependencias principales

- **provider**: Para gestión del estado
- **http**: Para comunicación con la API
- **flutter_secure_storage**: Para almacenamiento seguro de tokens
- **intl**: Para formateo de fechas y números
- **shared_preferences**: Para almacenamiento local de configuraciones

## Generación de la aplicación

Para generar la aplicación completa a partir de esta estructura, utilice el script `build_flutter_app.bat` ubicado en la raíz del proyecto App_Granja:

```
cd C:\App_Granja
build_flutter_app.bat
```

Este script creará una nueva aplicación Flutter y copiará todos los archivos necesarios de la estructura actual.
