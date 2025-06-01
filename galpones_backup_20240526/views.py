from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from .models import Galpon
from .serializers import GalponSerializer
from avicola.models import Empresa

class GalponViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y editar galpones.
    """
    queryset = Galpon.objects.all()
    serializer_class = GalponSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'tipo', 'granja']
    search_fields = ['numero', 'nombre', 'ubicacion', 'observaciones']
    ordering_fields = ['numero', 'nombre', 'fecha_creacion', 'fecha_actualizacion']
    ordering = ['numero']

    def get_queryset(self):
        """
        Filtra los galpones según los permisos del usuario.
        Los superusuarios ven todos los galpones.
        Los usuarios normales solo ven los galpones de sus granjas asignadas.
        """
        queryset = super().get_queryset()
        
        # Si el usuario es superusuario o staff, puede ver todos los galpones
        if self.request.user.is_superuser or self.request.user.is_staff:
            return queryset
            
        # Si el usuario tiene un perfil de granja, solo puede ver los galpones de sus granjas
        if hasattr(self.request.user, 'granja'):
            return queryset.filter(granja=self.request.user.granja)
            
        # Por defecto, no mostrar ningún galpón si el usuario no tiene permisos
        return Galpon.objects.none()

    def perform_create(self, serializer):
        """
        Asigna automáticamente la granja del usuario al crear un nuevo galpón,
        a menos que el usuario sea superusuario o staff.
        """
        if not (self.request.user.is_superuser or self.request.user.is_staff) and hasattr(self.request.user, 'granja'):
            serializer.save(granja=self.request.user.granja)
        else:
            serializer.save()

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Endpoint para obtener estadísticas de los galpones.
        """
        total_galpones = self.get_queryset().count()
        galpones_activos = self.get_queryset().filter(estado='activo').count()
        capacidad_total = sum(galpon.capacidad for galpon in self.get_queryset())
        
        return Response({
            'total_galpones': total_galpones,
            'galpones_activos': galpones_activos,
            'capacidad_total': capacidad_total,
        })
