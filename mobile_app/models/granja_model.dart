class Granja {
  final int id;
  final String codigoGranja;
  final String nombre;
  final String direccion;
  final String ubicacionGeografica;
  final String telefono;
  final int? encargadoId;
  final int capacidadTotalAves;
  final String estado;
  final int empresaId;

  Granja({
    required this.id,
    required this.codigoGranja,
    required this.nombre,
    required this.direccion,
    required this.ubicacionGeografica,
    required this.telefono,
    this.encargadoId,
    required this.capacidadTotalAves,
    required this.estado,
    required this.empresaId,
  });

  factory Granja.fromJson(Map<String, dynamic> json) {
    return Granja(
      id: json['id'],
      codigoGranja: json['codigo_granja'],
      nombre: json['nombre'],
      direccion: json['direccion'],
      ubicacionGeografica: json['ubicacion_geografica'] ?? '',
      telefono: json['telefono'] ?? '',
      encargadoId: json['encargado'],
      capacidadTotalAves: json['capacidad_total_aves'],
      estado: json['estado'],
      empresaId: json['empresa'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'codigo_granja': codigoGranja,
      'nombre': nombre,
      'direccion': direccion,
      'ubicacion_geografica': ubicacionGeografica,
      'telefono': telefono,
      'encargado': encargadoId,
      'capacidad_total_aves': capacidadTotalAves,
      'estado': estado,
      'empresa': empresaId,
    };
  }
}
