from django import forms
from django.utils.translation import gettext_lazy as _
from .models import BackupConfiguration, Backup


class BackupConfigurationForm(forms.ModelForm):
    """Formulario para configurar el sistema de respaldos"""
    
    class Meta:
        model = BackupConfiguration
        fields = [
            'max_backups',
            'auto_backup_enabled',
            'auto_backup_frequency',
            'include_database',
            'include_media',
            'compress_backup',
            'encrypt_backup',
            'notification_email',
            'backup_directory',
        ]
        widgets = {
            'backup_directory': forms.TextInput(attrs={'class': 'form-control'}),
            'notification_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'max_backups': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'auto_backup_frequency': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 168}),
        }
    
    def clean_backup_directory(self):
        """Validar que el directorio de respaldos sea válido"""
        directory = self.cleaned_data['backup_directory']
        
        # Verificar que no contenga caracteres inválidos
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        for char in invalid_chars:
            if char in directory:
                raise forms.ValidationError(
                    _('El directorio no puede contener los siguientes caracteres: < > : " | ? *')
                )
        
        return directory


class CreateBackupForm(forms.Form):
    """Formulario para crear un nuevo respaldo"""
    backup_type = forms.ChoiceField(
        choices=Backup.BACKUP_TYPES,
        label=_('Tipo de Respaldo'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label=_('Notas'),
        required=False
    )
