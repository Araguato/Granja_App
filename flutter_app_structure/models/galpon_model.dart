class Galpon {
  final int id;
  final int granjaId;
  final String granjaName;
  final String numeroGalpon;
  final String tipoGalpon;
  final int capacidadAves;
  final double? areaMetrosCuadrados;
  final int? responsableId;

  Galpon({
    required this.id,
    required this.granjaId,
    required this.granjaName,
    required this.numeroGalpon,
    required this.tipoGalpon,
    required this.capacidadAves,
    this.areaMetrosCuadrados,
    this.responsableId,
  });

  factory Galpon.fromJson(Map<String, dynamic> json) {
    return Galpon(
      id: json['id'],
      granjaId: json['granja'],
      granjaName: json['granja_nombre'] ?? '',
      numeroGalpon: json['numero_galpon'],
      tipoGalpon: json['tipo_galpon'],
      capacidadAves: json['capacidad_aves'],
      areaMetrosCuadrados: json['area_metros_cuadrados'] != null 
        ? double.parse(json['area_metros_cuadrados'].toString()) 
        : null,
      responsableId: json['responsable'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'granja': granjaId,
      'numero_galpon': numeroGalpon,
      'tipo_galpon': tipoGalpon,
      'capacidad_aves': capacidadAves,
      'area_metros_cuadrados': areaMetrosCuadrados,
      'responsable': responsableId,
    };
  }
}
