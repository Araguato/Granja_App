from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Sum, Avg, Count, F, Q
from django.conf import settings

from .models import ReporteGenerado, PlantillaReporte
from produccion.models import Lote, SeguimientoDiario
from inventario.models import Alimento, Vacuna, Insumo
from ventas.models import Venta, TipoHuevo

import io
import csv
import json
import datetime
import tempfile
from decimal import Decimal

# Intentar importar las bibliotecas para generar PDF y Excel
try:
    import xlsxwriter
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

@login_required
def panel_reportes(request):
    """Vista principal del panel de reportes"""
    reportes_recientes = ReporteGenerado.objects.filter(
        usuario_generador=request.user
    ).order_by('-fecha_generacion')[:5]
    
    plantillas = PlantillaReporte.objects.filter(
        Q(usuario_creador=request.user) | Q(es_predeterminada=True)
    ).order_by('nombre')
    
    context = {
        'reportes_recientes': reportes_recientes,
        'plantillas': plantillas,
        'tipos_reporte': ReporteGenerado.TIPO_REPORTE_CHOICES,
        'formatos_disponibles': ReporteGenerado.FORMATO_CHOICES,
        'excel_disponible': EXCEL_AVAILABLE,
        'pdf_disponible': PDF_AVAILABLE,
    }
    
    return render(request, 'reportes/panel_reportes.html', context)

@login_required
def nuevo_reporte(request):
    """Vista para crear un nuevo reporte"""
    if request.method == 'POST':
        tipo_reporte = request.POST.get('tipo_reporte')
        titulo = request.POST.get('titulo')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        formato = request.POST.get('formato', 'PDF')
        plantilla_id = request.POST.get('plantilla_id')
        
        # Validar datos
        if not all([tipo_reporte, titulo, fecha_inicio, fecha_fin]):
            messages.error(request, 'Todos los campos son obligatorios')
            return redirect('reportes:nuevo_reporte')
        
        try:
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            if fecha_inicio > fecha_fin:
                messages.error(request, 'La fecha de inicio no puede ser posterior a la fecha de fin')
                return redirect('reportes:nuevo_reporte')
        except ValueError:
            messages.error(request, 'Formato de fecha incorrecto')
            return redirect('reportes:nuevo_reporte')
        
        # Crear el reporte
        parametros = {}
        
        # Si se seleccionó una plantilla, usar su configuración
        if plantilla_id:
            try:
                plantilla = PlantillaReporte.objects.get(
                    id=plantilla_id,
                    usuario_creador=request.user
                ) if PlantillaReporte.objects.filter(id=plantilla_id, usuario_creador=request.user).exists() else \
                PlantillaReporte.objects.get(
                    id=plantilla_id,
                    es_predeterminada=True
                )
                parametros = plantilla.configuracion
            except PlantillaReporte.DoesNotExist:
                pass
        
        # Añadir parámetros adicionales del formulario
        for key, value in request.POST.items():
            if key.startswith('param_'):
                parametros[key[6:]] = value
        
        reporte = ReporteGenerado.objects.create(
            titulo=titulo,
            tipo_reporte=tipo_reporte,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            formato=formato,
            usuario_generador=request.user,
            parametros=parametros
        )
        
        # Generar el archivo del reporte
        archivo_generado = generar_archivo_reporte(reporte)
        if archivo_generado:
            messages.success(request, f'Reporte "{titulo}" generado correctamente')
            return redirect('reportes:detalle_reporte', reporte_id=reporte.id)
        else:
            reporte.delete()
            messages.error(request, 'Error al generar el reporte. Verifica que el formato seleccionado esté disponible.')
            return redirect('reportes:nuevo_reporte')
    
    # GET request
    plantillas = PlantillaReporte.objects.filter(
        Q(usuario_creador=request.user) | Q(es_predeterminada=True)
    ).order_by('nombre')
    
    context = {
        'tipos_reporte': ReporteGenerado.TIPO_REPORTE_CHOICES,
        'formatos_disponibles': ReporteGenerado.FORMATO_CHOICES,
        'plantillas': plantillas,
        'fecha_hoy': timezone.now().date().isoformat(),
        'fecha_mes_anterior': (timezone.now().date() - datetime.timedelta(days=30)).isoformat(),
        'excel_disponible': EXCEL_AVAILABLE,
        'pdf_disponible': PDF_AVAILABLE,
    }
    
    return render(request, 'reportes/nuevo_reporte.html', context)

@login_required
def detalle_reporte(request, reporte_id):
    """Vista para ver el detalle de un reporte generado"""
    reporte = get_object_or_404(ReporteGenerado, id=reporte_id, usuario_generador=request.user)
    
    context = {
        'reporte': reporte,
    }
    
    return render(request, 'reportes/detalle_reporte.html', context)

@login_required
@require_POST
def eliminar_reporte(request, reporte_id):
    """Vista para eliminar un reporte"""
    reporte = get_object_or_404(ReporteGenerado, id=reporte_id, usuario_generador=request.user)
    titulo = reporte.titulo
    reporte.delete()
    
    messages.success(request, f'Reporte "{titulo}" eliminado correctamente')
    return redirect('reportes:panel_reportes')

@login_required
def descargar_reporte(request, reporte_id):
    """Vista para descargar un reporte generado"""
    reporte = get_object_or_404(ReporteGenerado, id=reporte_id, usuario_generador=request.user)
    
    if not reporte.archivo:
        # Si el archivo no existe, intentar generarlo nuevamente
        archivo_generado = generar_archivo_reporte(reporte)
        if not archivo_generado:
            messages.error(request, 'No se pudo generar el archivo del reporte')
            return redirect('reportes:detalle_reporte', reporte_id=reporte.id)
    
    # Servir el archivo
    try:
        response = HttpResponse(
            reporte.archivo.read(),
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{reporte.archivo.name.split("/")[-1]}"'
        return response
    except Exception as e:
        messages.error(request, f'Error al descargar el archivo: {str(e)}')
        return redirect('reportes:detalle_reporte', reporte_id=reporte.id)

def generar_archivo_reporte(reporte):
    """Función para generar el archivo del reporte según su tipo y formato"""
    # Obtener los datos según el tipo de reporte
    datos = obtener_datos_reporte(reporte)
    
    if not datos:
        return False
    
    # Generar el archivo según el formato
    if reporte.formato == 'PDF' and PDF_AVAILABLE:
        return generar_pdf(reporte, datos)
    elif reporte.formato == 'EXCEL' and EXCEL_AVAILABLE:
        return generar_excel(reporte, datos)
    elif reporte.formato == 'CSV':
        return generar_csv(reporte, datos)
    
    return False

def obtener_datos_reporte(reporte):
    """Obtiene los datos para el reporte según su tipo"""
    if reporte.tipo_reporte == 'PRODUCCION_DIARIA':
        return obtener_datos_produccion_diaria(reporte)
    elif reporte.tipo_reporte == 'PRODUCCION_SEMANAL':
        return obtener_datos_produccion_semanal(reporte)
    elif reporte.tipo_reporte == 'PRODUCCION_MENSUAL':
        return obtener_datos_produccion_mensual(reporte)
    elif reporte.tipo_reporte == 'MORTALIDAD':
        return obtener_datos_mortalidad(reporte)
    elif reporte.tipo_reporte == 'INVENTARIO':
        return obtener_datos_inventario(reporte)
    elif reporte.tipo_reporte == 'VENTAS':
        return obtener_datos_ventas(reporte)
    elif reporte.tipo_reporte == 'COSTOS':
        return obtener_datos_costos(reporte)
    elif reporte.tipo_reporte == 'RENDIMIENTO':
        return obtener_datos_rendimiento(reporte)
    
    return None

# Funciones para obtener datos específicos según el tipo de reporte
def obtener_datos_produccion_diaria(reporte):
    """Obtiene datos de producción diaria"""
    # Implementación básica - esto se expandiría con la lógica real
    seguimientos = SeguimientoDiario.objects.filter(
        fecha__gte=reporte.fecha_inicio,
        fecha__lte=reporte.fecha_fin
    ).select_related('lote')
    
    datos = {
        'titulo': reporte.titulo,
        'periodo': f"{reporte.fecha_inicio.strftime('%d/%m/%Y')} - {reporte.fecha_fin.strftime('%d/%m/%Y')}",
        'columnas': ['Fecha', 'Lote', 'Huevos Producidos', 'Aves', 'Mortalidad', 'Producción (%)'],
        'filas': []
    }
    
    for seg in seguimientos:
        produccion_porc = 0
        if seg.lote and seg.lote.cantidad_inicial_aves > 0:
            produccion_porc = (seg.huevos_producidos / seg.lote.cantidad_inicial_aves) * 100
        
        datos['filas'].append([
            seg.fecha.strftime('%d/%m/%Y'),
            seg.lote.codigo_lote if hasattr(seg, 'lote') and seg.lote else 'N/A',
            seg.huevos_producidos,
            seg.lote.cantidad_inicial_aves if seg.lote else 0,
            seg.mortalidad,
            f"{produccion_porc:.2f}%"
        ])
    
    return datos

# Implementar las demás funciones de obtención de datos
def obtener_datos_produccion_semanal(reporte):
    """Obtiene datos de producción semanal"""
    # Implementación básica
    return {
        'titulo': reporte.titulo,
        'periodo': f"{reporte.fecha_inicio.strftime('%d/%m/%Y')} - {reporte.fecha_fin.strftime('%d/%m/%Y')}",
        'columnas': ['Semana', 'Huevos Totales', 'Promedio Diario', 'Mortalidad Total', 'Producción (%)'],
        'filas': [
            # Datos de ejemplo
            ['Semana 1', 15000, 2143, 12, '85.7%'],
            ['Semana 2', 15200, 2171, 8, '86.8%'],
        ]
    }

def obtener_datos_produccion_mensual(reporte):
    """Obtiene datos de producción mensual"""
    # Implementación básica
    return {
        'titulo': reporte.titulo,
        'periodo': f"{reporte.fecha_inicio.strftime('%d/%m/%Y')} - {reporte.fecha_fin.strftime('%d/%m/%Y')}",
        'columnas': ['Mes', 'Huevos Totales', 'Promedio Diario', 'Mortalidad Total', 'Producción (%)'],
        'filas': [
            # Datos de ejemplo
            ['Enero 2025', 65000, 2097, 45, '83.9%'],
            ['Febrero 2025', 62000, 2214, 38, '88.6%'],
        ]
    }

def obtener_datos_mortalidad(reporte):
    """Obtiene datos de mortalidad"""
    # Implementación básica
    return {
        'titulo': reporte.titulo,
        'periodo': f"{reporte.fecha_inicio.strftime('%d/%m/%Y')} - {reporte.fecha_fin.strftime('%d/%m/%Y')}",
        'columnas': ['Fecha', 'Lote', 'Mortalidad', 'Causa', 'Tasa Acumulada (%)'],
        'filas': [
            # Datos de ejemplo
            ['01/05/2025', 'L001', 5, 'Enfermedad respiratoria', '0.5%'],
            ['02/05/2025', 'L001', 3, 'Causas naturales', '0.8%'],
        ]
    }

def obtener_datos_inventario(reporte):
    """Obtiene datos de inventario"""
    # Implementación básica
    return {
        'titulo': reporte.titulo,
        'periodo': f"{reporte.fecha_inicio.strftime('%d/%m/%Y')} - {reporte.fecha_fin.strftime('%d/%m/%Y')}",
        'columnas': ['Categoría', 'Ítem', 'Cantidad', 'Unidad', 'Valor Estimado'],
        'filas': [
            # Datos de ejemplo
            ['Alimento', 'Iniciador', 500, 'kg', '$750.00'],
            ['Vacuna', 'Newcastle', 100, 'dosis', '$200.00'],
        ]
    }

def obtener_datos_ventas(reporte):
    """Obtiene datos de ventas"""
    # Implementación básica
    return {
        'titulo': reporte.titulo,
        'periodo': f"{reporte.fecha_inicio.strftime('%d/%m/%Y')} - {reporte.fecha_fin.strftime('%d/%m/%Y')}",
        'columnas': ['Fecha', 'Cliente', 'Producto', 'Cantidad', 'Precio Unitario', 'Total'],
        'filas': [
            # Datos de ejemplo
            ['05/05/2025', 'Supermercado XYZ', 'Huevos Tipo A', 1000, '$0.15', '$150.00'],
            ['06/05/2025', 'Restaurante ABC', 'Huevos Tipo B', 500, '$0.12', '$60.00'],
        ]
    }

def obtener_datos_costos(reporte):
    """Obtiene datos de costos"""
    # Implementación básica
    return {
        'titulo': reporte.titulo,
        'periodo': f"{reporte.fecha_inicio.strftime('%d/%m/%Y')} - {reporte.fecha_fin.strftime('%d/%m/%Y')}",
        'columnas': ['Categoría', 'Concepto', 'Monto', 'Porcentaje del Total'],
        'filas': [
            # Datos de ejemplo
            ['Alimentación', 'Alimento para aves', '$1,200.00', '40%'],
            ['Sanidad', 'Vacunas y medicamentos', '$450.00', '15%'],
        ]
    }

def obtener_datos_rendimiento(reporte):
    """Obtiene datos de rendimiento"""
    # Implementación básica
    return {
        'titulo': reporte.titulo,
        'periodo': f"{reporte.fecha_inicio.strftime('%d/%m/%Y')} - {reporte.fecha_fin.strftime('%d/%m/%Y')}",
        'columnas': ['Lote', 'Edad (semanas)', 'Producción (%)', 'Conversión Alimenticia', 'Viabilidad (%)', 'Índice de Eficiencia'],
        'filas': [
            # Datos de ejemplo
            ['L001', 25, '92.5%', '1.8', '98.2%', '265'],
            ['L002', 18, '85.3%', '2.1', '97.5%', '230'],
        ]
    }

# Funciones para generar archivos en diferentes formatos
def generar_pdf(reporte, datos):
    """Genera un archivo PDF con los datos del reporte"""
    if not PDF_AVAILABLE:
        return False
    
    # Crear un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        # Configurar el documento
        doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Título
        elements.append(Paragraph(datos['titulo'], title_style))
        elements.append(Spacer(1, 12))
        
        # Periodo
        elements.append(Paragraph(f"Periodo: {datos['periodo']}", heading_style))
        elements.append(Spacer(1, 12))
        
        # Tabla de datos
        table_data = [datos['columnas']]
        table_data.extend(datos['filas'])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(table)
        
        # Generar el PDF
        doc.build(elements)
    
    # Guardar el archivo en el modelo
    with open(temp_file.name, 'rb') as f:
        filename = f"{reporte.tipo_reporte.lower()}_{reporte.id}.pdf"
        reporte.archivo.save(filename, f)
    
    return True

def generar_excel(reporte, datos):
    """Genera un archivo Excel con los datos del reporte"""
    if not EXCEL_AVAILABLE:
        return False
    
    # Crear un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        # Crear el libro de trabajo y la hoja
        workbook = xlsxwriter.Workbook(temp_file.name)
        worksheet = workbook.add_worksheet()
        
        # Formatos
        title_format = workbook.add_format({'bold': True, 'font_size': 16})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#CCCCCC', 'border': 1})
        cell_format = workbook.add_format({'border': 1})
        
        # Título y periodo
        worksheet.write(0, 0, datos['titulo'], title_format)
        worksheet.write(1, 0, f"Periodo: {datos['periodo']}")
        
        # Encabezados de columna
        for col, header in enumerate(datos['columnas']):
            worksheet.write(3, col, header, header_format)
        
        # Datos
        for row, fila in enumerate(datos['filas']):
            for col, valor in enumerate(fila):
                worksheet.write(row + 4, col, valor, cell_format)
        
        # Ajustar anchos de columna
        for col in range(len(datos['columnas'])):
            worksheet.set_column(col, col, 15)
        
        workbook.close()
    
    # Guardar el archivo en el modelo
    with open(temp_file.name, 'rb') as f:
        filename = f"{reporte.tipo_reporte.lower()}_{reporte.id}.xlsx"
        reporte.archivo.save(filename, f)
    
    return True

def generar_csv(reporte, datos):
    """Genera un archivo CSV con los datos del reporte"""
    # Crear un buffer en memoria
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Escribir título y periodo
    writer.writerow([datos['titulo']])
    writer.writerow([f"Periodo: {datos['periodo']}"])
    writer.writerow([])  # Línea en blanco
    
    # Escribir encabezados
    writer.writerow(datos['columnas'])
    
    # Escribir datos
    for fila in datos['filas']:
        writer.writerow(fila)
    
    # Guardar el archivo en el modelo
    output.seek(0)
    filename = f"{reporte.tipo_reporte.lower()}_{reporte.id}.csv"
    reporte.archivo.save(filename, io.BytesIO(output.getvalue().encode('utf-8')))
    
    return True
