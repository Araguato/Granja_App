from django.db import migrations

def migrate_galpones_data(apps, schema_editor):
    """
    Migrate data from galpones_galpon to produccion_galpon if needed.
    This is a safety check to ensure no data is lost.
    """
    try:
        # Get the models
        GalponOld = apps.get_model('galpones', 'Galpon')
        GalponNew = apps.get_model('produccion', 'Galpon')
        
        # Check if there's any data to migrate
        if GalponOld.objects.exists() and not GalponNew.objects.exists():
            print("Migrating data from galpones_galpon to produccion_galpon...")
            for old_galpon in GalponOld.objects.all():
                # Create new galpon with the same data
                GalponNew.objects.create(
                    numero_galpon=old_galpon.numero,
                    # Add other fields as needed
                    # ...
                )
    except LookupError:
        # galpones app is not installed, nothing to migrate
        pass

class Migration(migrations.Migration):
    dependencies = [
        ('produccion', '0006_fix_galpon_relations'),  # Using the latest migration
    ]

    operations = [
        migrations.RunPython(migrate_galpones_data, migrations.RunPython.noop),
    ]
