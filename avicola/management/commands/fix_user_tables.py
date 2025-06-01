from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Crea las tablas faltantes para UserProfile'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Crear tabla para la relación UserProfile-Groups
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS "avicola_userprofile_groups" (
                "id" bigserial NOT NULL PRIMARY KEY,
                "userprofile_id" bigint NOT NULL,
                "group_id" integer NOT NULL,
                CONSTRAINT "avicola_userprofile_groups_userprofile_id_group_id_key" UNIQUE ("userprofile_id", "group_id"),
                CONSTRAINT "avicola_userprofile_groups_userprofile_id_fkey" FOREIGN KEY ("userprofile_id") REFERENCES "avicola_userprofile" ("id") DEFERRABLE INITIALLY DEFERRED,
                CONSTRAINT "avicola_userprofile_groups_group_id_fkey" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED
            );
            CREATE INDEX IF NOT EXISTS "avicola_userprofile_groups_userprofile_id_idx" ON "avicola_userprofile_groups" ("userprofile_id");
            CREATE INDEX IF NOT EXISTS "avicola_userprofile_groups_group_id_idx" ON "avicola_userprofile_groups" ("group_id");
            """)
            
            # Crear tabla para la relación UserProfile-Permissions
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS "avicola_userprofile_user_permissions" (
                "id" bigserial NOT NULL PRIMARY KEY,
                "userprofile_id" bigint NOT NULL,
                "permission_id" integer NOT NULL,
                CONSTRAINT "avicola_userprofile_user_permissions_userprofile_id_permission_id_key" UNIQUE ("userprofile_id", "permission_id"),
                CONSTRAINT "avicola_userprofile_user_permissions_userprofile_id_fkey" FOREIGN KEY ("userprofile_id") REFERENCES "avicola_userprofile" ("id") DEFERRABLE INITIALLY DEFERRED,
                CONSTRAINT "avicola_userprofile_user_permissions_permission_id_fkey" FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
            );
            CREATE INDEX IF NOT EXISTS "avicola_userprofile_user_permissions_userprofile_id_idx" ON "avicola_userprofile_user_permissions" ("userprofile_id");
            CREATE INDEX IF NOT EXISTS "avicola_userprofile_user_permissions_permission_id_idx" ON "avicola_userprofile_user_permissions" ("permission_id");
            """)
            
            self.stdout.write(self.style.SUCCESS('Tablas creadas exitosamente'))
