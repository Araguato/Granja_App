class Vacuna {
  final int id;
  final String nombreComercial;
  final String enfermedadObjetivo;
  final String? descripcion;
  final String? laboratorio;
  final String? numeroLote;
  final String? fechaVencimiento;
  final int? proveedorId;
  final String proveedorNombre;

  Vacuna({
    required this.id,
    required this.nombreComercial,
    required this.enfermedadObjetivo,
    this.descripcion,
    this.laboratorio,
    this.numeroLote,
    this.fechaVencimiento,
    this.proveedorId,
    required this.proveedorNombre,
  });

  factory Vacuna.fromJson(Map<String, dynamic> json) {
    return Vacuna(
      id: json['id'],
      nombreComercial: json['nombre_comercial'],
      enfermedadObjetivo: json['enfermedad_objetivo'],
      descripcion: json['descripcion'],
      laboratorio: json['laboratorio'],
      numeroLote: json['numero_lote'],
      fechaVencimiento: json['fecha_vencimiento'],
      proveedorId: json['proveedor'],
      proveedorNombre: json['proveedor_nombre'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'nombre_comercial': nombreComercial,
      'enfermedad_objetivo': enfermedadObjetivo,
      'descripcion': descripcion,
      'laboratorio': laboratorio,
      'numero_lote': numeroLote,
      'fecha_vencimiento': fechaVencimiento,
      'proveedor': proveedorId,
    };
  }
}
