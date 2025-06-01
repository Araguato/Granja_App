from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from produccion.models import Lote, Galpon, SeguimientoDiario
from .serializers import LoteSerializer, GalponSerializer, SeguimientoDiarioSerializer

class LoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lots to be viewed or edited.
    """
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned lots to active ones,
        by filtering against query parameters in the URL.
        """
        queryset = Lote.objects.all()
        active = self.request.query_params.get('active', None)
        if active is not None:
            queryset = queryset.filter(estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION'])
        return queryset


class GalponViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chicken coops to be viewed or edited.
    """
    queryset = Galpon.objects.all()
    serializer_class = GalponSerializer
    permission_classes = [permissions.IsAuthenticated]


class SeguimientoDiarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows daily tracking to be viewed or edited.
    """
    queryset = SeguimientoDiario.objects.all()
    serializer_class = SeguimientoDiarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filters the returned tracking by lot ID
        """
        queryset = SeguimientoDiario.objects.all()
        lote_id = self.request.query_params.get('lote', None)
        if lote_id is not None:
            queryset = queryset.filter(lote_id=lote_id)
        return queryset.order_by('-fecha_seguimiento')
