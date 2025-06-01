/**
 * Script para cambiar el idioma de la aplicación
 */
function changeLanguage(languageCode) {
    // Crear una cookie con el idioma seleccionado
    document.cookie = `django_language=${languageCode}; path=/; max-age=31536000`;
    
    // Recargar la página para aplicar el cambio de idioma
    window.location.reload();
}
