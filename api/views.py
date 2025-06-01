from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView

from avicola.models import UserProfile
from produccion.models import Granja, Galpon, Lote, SeguimientoDiario, MortalidadDiaria, MortalidadSemanal
from inventario.models import Proveedor, Raza, Alimento, Vacuna, Insumo, GuiaDesempenoRaza
from wiki.models import Category, Article, Attachment
from faq.models import FAQCategory, FAQ
from bot.models import BotIntent, BotConversation, BotMessage

# Importar serializadores de usuario
from .serializers import UserSerializer

# Importar serializadores de producción
from .serializers_produccion import (
    GranjaSerializer, GalponSerializer, LoteSerializer,
    SeguimientoDiarioSerializer, MortalidadDiariaSerializer, MortalidadSemanalSerializer
)

# Importar serializadores de inventario
from .serializers_inventario import (
    ProveedorSerializer, RazaSerializer, AlimentoSerializer,
    VacunaSerializer, InsumoSerializer, GuiaDesempenoRazaSerializer
)

# Importar serializadores de módulos adicionales
from .serializers_wiki import CategorySerializer, ArticleListSerializer, ArticleDetailSerializer, AttachmentSerializer
from .serializers_faq import FAQCategorySerializer, FAQSerializer
from .serializers_bot import BotConversationSerializer, BotMessageSerializer, BotMessageCreateSerializer
from .serializers_estadisticas import EstadisticasSerializer

# Importar funciones de estadísticas
from core.estadisticas import obtener_estadisticas_dashboard, obtener_estadisticas_produccion, obtener_estadisticas_mortalidad, obtener_estadisticas_ventas, obtener_distribucion_tipos_huevo, obtener_resumen_inventario

# Importaciones adicionales para comparación de razas
import json
import os
from django.conf import settings


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar usuarios.
    """
    queryset = UserProfile.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']


class RazaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar razas de aves.
    """
    queryset = Raza.objects.all()
    serializer_class = RazaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'tipo_raza', 'descripcion']
    filterset_fields = ['tipo_raza']
    ordering_fields = ['nombre']


class AlimentoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar alimentos.
    """
    queryset = Alimento.objects.all()
    serializer_class = AlimentoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'descripcion', 'tipo_alimento']
    filterset_fields = ['etapa', 'tipo_alimento']
    ordering_fields = ['nombre']


class GranjaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar granjas.
    """
    queryset = Granja.objects.all()
    serializer_class = GranjaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'codigo_granja', 'direccion']
    filterset_fields = ['estado']
    ordering_fields = ['nombre', 'codigo_granja']


class GalponViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar galpones.
    """
    queryset = Galpon.objects.all()
    serializer_class = GalponSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['numero_galpon']
    filterset_fields = ['granja', 'tipo_galpon']
    ordering_fields = ['granja', 'numero_galpon']


class LoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar lotes.
    """
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['codigo_lote']
    filterset_fields = ['galpon', 'raza', 'estado']
    ordering_fields = ['fecha_ingreso', 'codigo_lote']


class SeguimientoDiarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar seguimientos diarios.
    """
    queryset = SeguimientoDiario.objects.all()
    serializer_class = SeguimientoDiarioSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lote', 'fecha_seguimiento', 'tipo_seguimiento']
    ordering_fields = ['fecha_seguimiento']


# Vistas para Wiki
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar categorías de la Wiki.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'name']
    lookup_field = 'slug'


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar artículos de la Wiki.
    """
    queryset = Article.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['category', 'is_published']
    ordering_fields = ['updated_at', 'title']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Incrementar contador de vistas
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# Vistas para FAQ
class FAQCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar categorías de FAQ.
    """
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'name']
    lookup_field = 'slug'


class FAQViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar preguntas frecuentes.
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['question', 'answer']
    filterset_fields = ['category', 'is_published']
    ordering_fields = ['order', 'question']
    
    def get_queryset(self):
        # Solo mostrar FAQs publicadas para usuarios no administradores
        if self.request.user.is_staff:
            return FAQ.objects.all()
        return FAQ.objects.filter(is_published=True)


# Vistas para Bot
class BotConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar conversaciones con el bot.
    """
    serializer_class = BotConversationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['start_time']
    
    def get_queryset(self):
        # Los usuarios solo pueden ver sus propias conversaciones
        if self.request.user.is_staff:
            return BotConversation.objects.all()
        return BotConversation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Asignar el usuario actual como propietario de la conversación
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        serializer = BotMessageCreateSerializer(data={
            'conversation': conversation.id,
            'text': request.data.get('text', '')
        })
        
        if serializer.is_valid():
            serializer.save()
            # Devolver la conversación actualizada con todos los mensajes
            return Response(
                BotConversationSerializer(conversation, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def end_conversation(self, request, pk=None):
        conversation = self.get_object()
        from django.utils import timezone
        conversation.end_time = timezone.now()
        conversation.feedback_rating = request.data.get('rating')
        conversation.save()
        return Response({'status': 'conversation ended'})


# ViewSets adicionales para Inventario
class ProveedorViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar proveedores.
    """
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'rif', 'contacto_principal']
    ordering_fields = ['nombre']


class VacunaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar vacunas.
    """
    queryset = Vacuna.objects.all()
    serializer_class = VacunaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre_comercial', 'enfermedad_objetivo']
    filterset_fields = ['proveedor']
    ordering_fields = ['nombre_comercial']


class InsumoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar insumos.
    """
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    filterset_fields = ['tipo_insumo', 'proveedor']
    ordering_fields = ['nombre']


class GuiaDesempenoRazaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar guías de desempeño por raza.
    """
    queryset = GuiaDesempenoRaza.objects.all()
    serializer_class = GuiaDesempenoRazaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['raza', 'dia_edad']
    ordering_fields = ['raza', 'dia_edad']


# ViewSets adicionales para Producción
class MortalidadDiariaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar registros de mortalidad diaria.
    """
    queryset = MortalidadDiaria.objects.all()
    serializer_class = MortalidadDiariaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lote', 'fecha']
    ordering_fields = ['-fecha']


class MortalidadSemanalViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar y editar registros de mortalidad semanal.
    """
    queryset = MortalidadSemanal.objects.all()
    serializer_class = MortalidadSemanalSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lote', 'semana', 'anio']
    ordering_fields = ['-anio', '-semana']


# ViewSet para Estadísticas
class EstadisticasViewSet(viewsets.ViewSet):
    """
    API endpoint para obtener estadísticas del sistema.
    """
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Obtiene todas las estadísticas para el dashboard.
        """
        stats = obtener_estadisticas_dashboard()
        
        # Formatear los datos para el serializador
        data = {
            'produccion_labels': stats['produccion']['labels'],
            'produccion_datos': stats['produccion']['datos'],
            'mortalidad_labels': stats['mortalidad']['labels'],
            'mortalidad_datos': stats['mortalidad']['datos'],
            'ventas_labels': stats['ventas']['labels'],
            'ventas_datos': stats['ventas']['datos'],
            'tipos_huevo_labels': stats['tipos_huevo']['labels'],
            'tipos_huevo_datos': stats['tipos_huevo']['datos'],
            'lotes_totales': stats['inventario']['total_lotes'],
            'lotes_activos': stats['inventario']['lotes_activos'],
            'alimentos_count': stats['inventario']['total_alimentos'],
            'vacunas_count': stats['inventario']['total_vacunas'],
            'engorde_labels': stats['engorde']['labels'],
            'engorde_peso': stats['engorde']['datos_peso'],
            'engorde_ganancia': stats['engorde']['datos_ganancia'],
            'engorde_conversion': stats['engorde']['datos_conversion'],
            'galpon_labels': stats['por_galpon']['labels'],
            'galpon_peso': stats['por_galpon']['datos_peso'],
            'galpon_mortalidad': stats['por_galpon']['datos_mortalidad'],
        }
        
        serializer = EstadisticasSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def produccion(self, request):
        """
        Obtiene estadísticas de producción (huevos).
        """
        periodo = request.query_params.get('periodo', 'semana')
        stats = obtener_estadisticas_produccion(periodo)
        
        data = {
            'produccion_labels': stats['labels'],
            'produccion_datos': stats['datos']
        }
        
        serializer = EstadisticasSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mortalidad(self, request):
        """
        Obtiene estadísticas de mortalidad.
        """
        periodo = request.query_params.get('periodo', 'semana')
        stats = obtener_estadisticas_mortalidad(periodo)
        
        data = {
            'mortalidad_labels': stats['labels'],
            'mortalidad_datos': stats['datos']
        }
        
        serializer = EstadisticasSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def ventas(self, request):
        """
        Obtiene estadísticas de ventas.
        """
        periodo = request.query_params.get('periodo', 'mes')
        stats = obtener_estadisticas_ventas(periodo)
        
        data = {
            'ventas_labels': stats['labels'],
            'ventas_datos': stats['datos']
        }
        
        serializer = EstadisticasSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def tipos_huevo(self, request):
        """
        Obtiene la distribución de tipos de huevo.
        """
        stats = obtener_distribucion_tipos_huevo()
        
        data = {
            'tipos_huevo_labels': stats['labels'],
            'tipos_huevo_datos': stats['datos']
        }
        
        serializer = EstadisticasSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inventario(self, request):
        """
        Obtiene un resumen del inventario.
        """
        stats = obtener_resumen_inventario()
        
        serializer = EstadisticasSerializer(stats)
        return Response(serializer.data)


# Vista para Comparación de Razas
class ComparacionRazasView(APIView):
    """
    Vista API para obtener datos de comparación entre razas nominales y datos reales de lotes
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, raza_id=None, lote_id=None):
        """
        Obtiene datos para comparar una raza nominal con los datos reales de un lote
        """
        try:
            # Si no se especifican IDs, devolver la lista de razas y lotes disponibles
            if not raza_id or not lote_id:
                return self._get_razas_lotes_disponibles()
            
            # Intentar cargar datos desde el archivo JSON
            json_path = os.path.join(settings.BASE_DIR, 'windows_app', 'datos_comparacion_razas.json')
            
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                # Obtener datos de la raza especificada
                if raza_id == '1':
                    datos_raza = datos.get('raza1', {})
                elif raza_id == '2':
                    datos_raza = datos.get('raza2', {})
                else:
                    return Response(
                        {"error": f"Raza con ID {raza_id} no encontrada"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # Calcular diferencias y porcentajes
                resultado = self._calcular_diferencias(datos_raza)
                
                return Response(resultado)
            else:
                return Response(
                    {"error": "Archivo de datos no encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"error": f"Error al obtener datos de comparación: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _get_razas_lotes_disponibles(self):
        """
        Obtiene la lista de razas y lotes disponibles para comparación
        """
        try:
            # Cargar datos desde el archivo JSON
            json_path = os.path.join(settings.BASE_DIR, 'windows_app', 'datos_comparacion_razas.json')
            
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                # Extraer información de razas y lotes
                razas = []
                lotes = []
                
                for key, value in datos.items():
                    if key.startswith('raza'):
                        raza_id = key.replace('raza', '')
                        razas.append({
                            'id': raza_id,
                            'nombre': value.get('nombre', f'Raza {raza_id}')
                        })
                    
                    # Extraer información de lotes
                    actual = value.get('actual', {})
                    if 'lote_id' in actual and 'nombre_lote' in actual:
                        lote = {
                            'id': actual['lote_id'],
                            'nombre': actual['nombre_lote']
                        }
                        if lote not in lotes:
                            lotes.append(lote)
                
                return Response({
                    'razas': razas,
                    'lotes': lotes
                })
            else:
                return Response(
                    {"error": "Archivo de datos no encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"error": f"Error al obtener razas y lotes disponibles: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _calcular_diferencias(self, datos_raza):
        """
        Calcula las diferencias entre valores nominales y reales
        """
        resultado = {
            'nombre_raza': datos_raza.get('nombre', 'Raza desconocida'),
            'nombre_lote': datos_raza.get('actual', {}).get('nombre_lote', 'Lote desconocido'),
            'metricas': []
        }
        
        # Mapeo de nombres de métricas
        nombres_metricas = {
            'produccion': 'Producción',
            'peso': 'Peso (g)',
            'mortalidad': 'Mortalidad (%)',
            'consumo_alimento': 'Consumo de alimento (g)',
            'conversion': 'Conversión alimenticia'
        }
        
        # Calcular diferencias para cada métrica
        nominal = datos_raza.get('nominal', {})
        actual = datos_raza.get('actual', {})
        
        for key_base in ['produccion', 'peso', 'mortalidad', 'consumo_alimento', 'conversion']:
            key_nominal = f'{key_base}_esperado'
            key_actual = f'{key_base}_actual'
            
            if key_nominal in nominal and key_actual in actual:
                valor_nominal = nominal[key_nominal]
                valor_actual = actual[key_actual]
                diferencia = valor_actual - valor_nominal
                
                # Calcular porcentaje de diferencia
                if valor_nominal != 0:
                    porcentaje = (diferencia / valor_nominal) * 100
                else:
                    porcentaje = 0
                
                # Determinar si la diferencia es positiva o negativa
                # Para mortalidad y conversión, menor es mejor
                if key_base in ['mortalidad', 'conversion', 'consumo_alimento']:
                    estado = 'positivo' if diferencia <= 0 else 'negativo'
                else:
                    estado = 'positivo' if diferencia >= 0 else 'negativo'
                
                resultado['metricas'].append({
                    'nombre': nombres_metricas.get(key_base, key_base),
                    'valor_nominal': valor_nominal,
                    'valor_actual': valor_actual,
                    'diferencia': diferencia,
                    'porcentaje': round(porcentaje, 2),
                    'estado': estado
                })
        
        return resultado
