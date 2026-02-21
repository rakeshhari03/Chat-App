from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        # Reset all users to offline status when app starts
        # (but keep their last_seen timestamp intact)
        from accounts.models import CustomUser
        
        CustomUser.objects.update(is_online=False)
