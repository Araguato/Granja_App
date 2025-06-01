from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

def register_cache_signals(model_name, cache_prefix=None):
    \"\"\"Register cache invalidation signals for a model.\"\"\"
    if cache_prefix is None:
        cache_prefix = model_name.lower()

    def invalidate_cache(sender, instance, **kwargs):
        # Invalidate list cache
        cache.delete(f\"{cache_prefix}_list\")
        # Invalidate detail cache
        cache.delete(f\"{cache_prefix}_{instance.id}\")
        # Invalidate any related caches
        if hasattr(instance, 'get_related_cache_keys'):
            for key in instance.get_related_cache_keys():
                cache.delete(key)

    # Connect signals
    post_save.connect(invalidate_cache, sender=model_name)
    post_delete.connect(invalidate_cache, sender=model_name)
