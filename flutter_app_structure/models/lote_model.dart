class Lote {
  final int id;
  final int galponId;
  final String galponInfo;
  final int razaId;
  final String razaNombre;
  final int? alimentoId;
  final String codigoLote;
  final String fechaInicio;
  final String? fechaIngreso;
  final int cantidadInicialAves;
  final int edadInicialSemanas;
  final int edadSemanas;
  final String estado;

  Lote({
    required this.id,
    required this.galponId,
    required this.galponInfo,
    required this.razaId,
    required this.razaNombre,
    this.alimentoId,
    required this.codigoLote,
    required this.fechaInicio,
    this.fechaIngreso,
    required this.cantidadInicialAves,
    required this.edadInicialSemanas,
    required this.edadSemanas,
    required this.estado,
  });

  factory Lote.fromJson(Map<String, dynamic> json) {
    return Lote(
      id: json['id'],
      galponId: json['galpon'],
      galponInfo: json['galpon_info'] ?? '',
      razaId: json['raza'],
      razaNombre: json['raza_nombre'] ?? '',
      alimentoId: json['alimento'],
      codigoLote: json['codigo_lote'],
      fechaInicio: json['fecha_inicio'],
      fechaIngreso: json['fecha_ingreso'],
      cantidadInicialAves: json['cantidad_inicial_aves'],
      edadInicialSemanas: json['edad_inicial_semanas'],
      edadSemanas: json['edad_semanas'],
      estado: json['estado'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'galpon': galponId,
      'raza': razaId,
      'alimento': alimentoId,
      'codigo_lote': codigoLote,
      'fecha_inicio': fechaInicio,
      'fecha_ingreso': fechaIngreso,
      'cantidad_inicial_aves': cantidadInicialAves,
      'edad_inicial_semanas': edadInicialSemanas,
      'edad_semanas': edadSemanas,
      'estado': estado,
    };
  }
}
