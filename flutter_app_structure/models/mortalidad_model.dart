class MortalidadDiaria {
  final int id;
  final int loteId;
  final String loteCode;
  final String fecha;
  final int cantidad;
  final String? causa;
  final String? observaciones;

  MortalidadDiaria({
    required this.id,
    required this.loteId,
    required this.loteCode,
    required this.fecha,
    required this.cantidad,
    this.causa,
    this.observaciones,
  });

  factory MortalidadDiaria.fromJson(Map<String, dynamic> json) {
    return MortalidadDiaria(
      id: json['id'],
      loteId: json['lote'],
      loteCode: json['lote_codigo'] ?? '',
      fecha: json['fecha'],
      cantidad: json['cantidad'],
      causa: json['causa'],
      observaciones: json['observaciones'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'lote': loteId,
      'fecha': fecha,
      'cantidad': cantidad,
      'causa': causa,
      'observaciones': observaciones,
    };
  }
}

class MortalidadSemanal {
  final int id;
  final int loteId;
  final String loteCode;
  final String semana;
  final String fechaInicio;
  final String fechaFin;
  final int cantidad;
  final double porcentaje;
  final int avesIniciales;
  final int avesFinal;

  MortalidadSemanal({
    required this.id,
    required this.loteId,
    required this.loteCode,
    required this.semana,
    required this.fechaInicio,
    required this.fechaFin,
    required this.cantidad,
    required this.porcentaje,
    required this.avesIniciales,
    required this.avesFinal,
  });

  factory MortalidadSemanal.fromJson(Map<String, dynamic> json) {
    return MortalidadSemanal(
      id: json['id'],
      loteId: json['lote'],
      loteCode: json['lote_codigo'] ?? '',
      semana: json['semana'],
      fechaInicio: json['fecha_inicio'],
      fechaFin: json['fecha_fin'],
      cantidad: json['cantidad'],
      porcentaje: json['porcentaje'] != null 
          ? double.parse(json['porcentaje'].toString()) 
          : 0.0,
      avesIniciales: json['aves_iniciales'],
      avesFinal: json['aves_final'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'lote': loteId,
      'semana': semana,
      'fecha_inicio': fechaInicio,
      'fecha_fin': fechaFin,
      'cantidad': cantidad,
      'porcentaje': porcentaje,
      'aves_iniciales': avesIniciales,
      'aves_final': avesFinal,
    };
  }
}
