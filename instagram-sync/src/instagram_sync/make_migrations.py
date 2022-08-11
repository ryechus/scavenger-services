import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagram_sync.migration_settings")
    from django.core import management

    # args = sys.argv + ["makemigrations", "instagram_sync.contrib.django"]
    management.call_command("makemigrations", "contrib.django")
