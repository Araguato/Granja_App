class Alimento {
  final int id;
  final String nombre;
  final String descripcion;
  final String tipoAlimento;
  final String etapa;
  final double? contenidoProteina;
  final double? energiaMetabolizable;
  final double? grasaCruda;
  final double? fibraCruda;
  final double? calcio;
  final double? fosforo;
  final int? proveedorId;
  final String proveedorNombre;

  Alimento({
    required this.id,
    required this.nombre,
    required this.descripcion,
    required this.tipoAlimento,
    required this.etapa,
    this.contenidoProteina,
    this.energiaMetabolizable,
    this.grasaCruda,
    this.fibraCruda,
    this.calcio,
    this.fosforo,
    this.proveedorId,
    required this.proveedorNombre,
  });

  factory Alimento.fromJson(Map<String, dynamic> json) {
    return Alimento(
      id: json['id'],
      nombre: json['nombre'],
      descripcion: json['descripcion'] ?? '',
      tipoAlimento: json['tipo_alimento'],
      etapa: json['etapa'],
      contenidoProteina: json['contenido_proteina'] != null 
          ? double.parse(json['contenido_proteina'].toString()) 
          : null,
      energiaMetabolizable: json['energia_metabolizable'] != null 
          ? double.parse(json['energia_metabolizable'].toString()) 
          : null,
      grasaCruda: json['grasa_cruda'] != null 
          ? double.parse(json['grasa_cruda'].toString()) 
          : null,
      fibraCruda: json['fibra_cruda'] != null 
          ? double.parse(json['fibra_cruda'].toString()) 
          : null,
      calcio: json['calcio'] != null 
          ? double.parse(json['calcio'].toString()) 
          : null,
      fosforo: json['fosforo'] != null 
          ? double.parse(json['fosforo'].toString()) 
          : null,
      proveedorId: json['proveedor'],
      proveedorNombre: json['proveedor_nombre'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'nombre': nombre,
      'descripcion': descripcion,
      'tipo_alimento': tipoAlimento,
      'etapa': etapa,
      'contenido_proteina': contenidoProteina,
      'energia_metabolizable': energiaMetabolizable,
      'grasa_cruda': grasaCruda,
      'fibra_cruda': fibraCruda,
      'calcio': calcio,
      'fosforo': fosforo,
      'proveedor': proveedorId,
    };
  }
}
