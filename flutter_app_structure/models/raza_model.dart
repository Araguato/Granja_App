class Raza {
  final int id;
  final String nombre;
  final String tipoRaza;
  final String descripcion;

  Raza({
    required this.id,
    required this.nombre,
    required this.tipoRaza,
    required this.descripcion,
  });

  factory Raza.fromJson(Map<String, dynamic> json) {
    return Raza(
      id: json['id'],
      nombre: json['nombre'],
      tipoRaza: json['tipo_raza'],
      descripcion: json['descripcion'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'nombre': nombre,
      'tipo_raza': tipoRaza,
      'descripcion': descripcion,
    };
  }
}
