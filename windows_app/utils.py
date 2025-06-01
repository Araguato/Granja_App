from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize

def load_icon(path, default_icon=None):
    """
    Carga un icono desde una ruta, con manejo de errores.
    Si la carga falla, devuelve un icono predeterminado.
    """
    pixmap = QPixmap(path)
    if pixmap.isNull():
        if default_icon:
            return default_icon
        # Crear un icono vacío como fallback
        return QIcon()
    return QIcon(pixmap)

def scale_pixmap(pixmap, width, height):
    """
    Escala un pixmap con manejo de errores para pixmaps nulos.
    """
    if pixmap.isNull():
        # Crear un pixmap vacío del tamaño solicitado
        empty_pixmap = QPixmap(width, height)
        empty_pixmap.fill()  # Llenar con color transparente
        return empty_pixmap
    return pixmap.scaled(QSize(width, height))
