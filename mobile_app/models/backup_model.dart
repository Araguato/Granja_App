class Backup {
  final int id;
  final String name;
  final String filePath;
  final String backupType;
  final String status;
  final double size;
  final DateTime createdAt;
  final DateTime? completedAt;
  final bool isAuto;
  final String? notes;
  final bool fileExists;
  final String? createdBy;

  Backup({
    required this.id,
    required this.name,
    required this.filePath,
    required this.backupType,
    required this.status,
    required this.size,
    required this.createdAt,
    this.completedAt,
    required this.isAuto,
    this.notes,
    required this.fileExists,
    this.createdBy,
  });

  // Getter para obtener el tamaño en MB
  double get sizeInMb => size / (1024 * 1024);

  // Getter para obtener el nombre del archivo
  String get fileName {
    final parts = filePath.split('/');
    return parts.isNotEmpty ? parts.last : '';
  }

  // Getter para obtener el texto de estado
  String get statusText {
    switch (status) {
      case 'PENDING':
        return 'Pendiente';
      case 'IN_PROGRESS':
        return 'En Progreso';
      case 'COMPLETED':
        return 'Completado';
      case 'FAILED':
        return 'Fallido';
      default:
        return status;
    }
  }

  // Getter para obtener el texto del tipo de respaldo
  String get backupTypeText {
    switch (backupType) {
      case 'FULL':
        return 'Completo';
      case 'DB':
        return 'Base de Datos';
      case 'MEDIA':
        return 'Archivos de Medios';
      default:
        return backupType;
    }
  }

  // Getter para obtener el color del estado
  String get statusColor {
    switch (status) {
      case 'PENDING':
        return '#FFC107'; // Amarillo
      case 'IN_PROGRESS':
        return '#17A2B8'; // Azul
      case 'COMPLETED':
        return '#28A745'; // Verde
      case 'FAILED':
        return '#DC3545'; // Rojo
      default:
        return '#6C757D'; // Gris
    }
  }

  factory Backup.fromJson(Map<String, dynamic> json) {
    return Backup(
      id: json['id'],
      name: json['name'],
      filePath: json['file_path'],
      backupType: json['backup_type'],
      status: json['status'],
      size: json['size'].toDouble(),
      createdAt: DateTime.parse(json['created_at']),
      completedAt: json['completed_at'] != null ? DateTime.parse(json['completed_at']) : null,
      isAuto: json['is_auto'] ?? false,
      notes: json['notes'],
      fileExists: json['file_exists'] ?? false,
      createdBy: json['created_by'] != null ? json['created_by']['username'] : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'file_path': filePath,
      'backup_type': backupType,
      'status': status,
      'size': size,
      'created_at': createdAt.toIso8601String(),
      'completed_at': completedAt?.toIso8601String(),
      'is_auto': isAuto,
      'notes': notes,
      'file_exists': fileExists,
    };
  }
}
