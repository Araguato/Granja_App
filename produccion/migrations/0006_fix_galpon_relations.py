from django.db import migrations

def fix_galpon_relations(apps, schema_editor):
    """
    Fix broken relationships between Lote and Galpon models.
    This will help identify and fix any broken references.
    """
    Lote = apps.get_model('produccion', 'Lote')
    Galpon = apps.get_model('produccion', 'Galpon')
    
    # Find all Lotes that reference non-existent Galpones
    broken_lotes = []
    for lote in Lote.objects.all():
        try:
            # This will raise Galpon.DoesNotExist if the galpon doesn't exist
            lote.galpon
        except Galpon.DoesNotExist:
            broken_lotes.append(lote)
    
    if not broken_lotes:
        print("No broken Lote-Galpon relationships found.")
        return
    
    print(f"Found {len(broken_lotes)} Lotes with broken Galpon references.")
    print("Please run the following SQL commands to fix the relationships:")
    print("------------------------------------------------------------")
    
    # Generate SQL to fix the relationships
    for lote in broken_lotes:
        # Find a suitable Galpon to assign (you'll need to adjust this logic)
        # For now, we'll just print the broken references
        print(f"-- Lote ID: {lote.id}, Codigo: {lote.codigo_lote}")
        print(f"-- Current Galpon ID: {lote.galpon_id} (does not exist)")
        print("-- Run these commands after updating the Galpon ID:")
        print(f"-- UPDATE produccion_lote SET galpon_id = [NEW_GALPON_ID] WHERE id = {lote.id};\n")
    
    print("\nAfter running the above commands, run:\n")
    print("python manage.py check")
    print("\nTo verify there are no more broken relationships.")


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0005_add_audit_fields_to_galpon'),
    ]

    operations = [
        migrations.RunPython(fix_galpon_relations, migrations.RunPython.noop),
    ]
