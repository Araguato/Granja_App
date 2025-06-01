class Proveedor {
  final int id;
  final String rif;
  final String nombre;
  final String contactoPrincipal;
  final String telefono;
  final String email;
  final String direccion;

  Proveedor({
    required this.id,
    required this.rif,
    required this.nombre,
    required this.contactoPrincipal,
    required this.telefono,
    required this.email,
    required this.direccion,
  });

  factory Proveedor.fromJson(Map<String, dynamic> json) {
    return Proveedor(
      id: json['id'],
      rif: json['rif'],
      nombre: json['nombre'],
      contactoPrincipal: json['contacto_principal'] ?? '',
      telefono: json['telefono'] ?? '',
      email: json['email'] ?? '',
      direccion: json['direccion'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'rif': rif,
      'nombre': nombre,
      'contacto_principal': contactoPrincipal,
      'telefono': telefono,
      'email': email,
      'direccion': direccion,
    };
  }
}
