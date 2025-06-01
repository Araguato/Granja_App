from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    """Categorías para organizar los artículos de la Wiki"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Descripción")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='subcategories', verbose_name="Categoría Padre")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    """Artículos de la Wiki"""
    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=220, unique=True, verbose_name="Slug")
    summary = models.TextField(max_length=500, blank=True, verbose_name="Resumen")
    content = models.TextField(verbose_name="Contenido")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles',
                                verbose_name="Categoría")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                              related_name='wiki_articles', verbose_name="Autor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    is_published = models.BooleanField(default=True, verbose_name="Publicado")
    views = models.PositiveIntegerField(default=0, verbose_name="Vistas")
    
    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Attachment(models.Model):
    """Archivos adjuntos para los artículos"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='attachments',
                               verbose_name="Artículo")
    file = models.FileField(upload_to='wiki/attachments/', verbose_name="Archivo")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.CharField(max_length=255, blank=True, verbose_name="Descripción")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Subida")
    
    class Meta:
        verbose_name = "Archivo Adjunto"
        verbose_name_plural = "Archivos Adjuntos"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.article.title})"
