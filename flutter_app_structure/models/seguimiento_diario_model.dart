class SeguimientoDiario {
  final int id;
  final int loteId;
  final String loteCode;
  final String fechaSeguimiento;
  final String tipoSeguimiento;
  final String tipoSeguimientoDisplay;
  final int? mortalidad;
  final double? pesoPromedioAve;
  final double? consumoAlimentoKg;
  final int? huevosA;
  final int? huevosB;
  final int? huevosC;
  final int? huevosSucios;
  final int? huevosRotos;
  final int avesPresentes;
  final int mortalidadDia;
  final int huevosTotal;

  SeguimientoDiario({
    required this.id,
    required this.loteId,
    required this.loteCode,
    required this.fechaSeguimiento,
    required this.tipoSeguimiento,
    required this.tipoSeguimientoDisplay,
    this.mortalidad,
    this.pesoPromedioAve,
    this.consumoAlimentoKg,
    this.huevosA,
    this.huevosB,
    this.huevosC,
    this.huevosSucios,
    this.huevosRotos,
    required this.avesPresentes,
    required this.mortalidadDia,
    required this.huevosTotal,
  });

  factory SeguimientoDiario.fromJson(Map<String, dynamic> json) {
    return SeguimientoDiario(
      id: json['id'],
      loteId: json['lote'],
      loteCode: json['lote_codigo'] ?? '',
      fechaSeguimiento: json['fecha_seguimiento'],
      tipoSeguimiento: json['tipo_seguimiento'],
      tipoSeguimientoDisplay: json['tipo_seguimiento_display'] ?? '',
      mortalidad: json['mortalidad'],
      pesoPromedioAve: json['peso_promedio_ave'] != null 
          ? double.parse(json['peso_promedio_ave'].toString()) 
          : null,
      consumoAlimentoKg: json['consumo_alimento_kg'] != null 
          ? double.parse(json['consumo_alimento_kg'].toString()) 
          : null,
      huevosA: json['huevos_a'],
      huevosB: json['huevos_b'],
      huevosC: json['huevos_c'],
      huevosSucios: json['huevos_sucios'],
      huevosRotos: json['huevos_rotos'],
      avesPresentes: json['aves_presentes_count'] ?? 0,
      mortalidadDia: json['mortalidad_dia'] ?? 0,
      huevosTotal: json['huevos_total'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'lote': loteId,
      'fecha_seguimiento': fechaSeguimiento,
      'tipo_seguimiento': tipoSeguimiento,
      'mortalidad': mortalidad,
      'peso_promedio_ave': pesoPromedioAve,
      'consumo_alimento_kg': consumoAlimentoKg,
      'huevos_a': huevosA,
      'huevos_b': huevosB,
      'huevos_c': huevosC,
      'huevos_sucios': huevosSucios,
      'huevos_rotos': huevosRotos,
    };
  }
}
