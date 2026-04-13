"""
Зураг солих / устгах үед Cloudflare R2-оос хуучин файлыг автоматаар устгах.
"""
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from .models import Product
from .storage import delete_r2_file


# ── Зураг солих үед хуучин зургийг устгах ────────────────────
@receiver(pre_save, sender=Product)
def product_image_replace(sender, instance, **kwargs):
    """
    Product хадгалахаас өмнө:
    DB-д байгаа хуучин зурагтай шинэ зургийг харьцуулж,
    өөр болсон тохиолдолд хуучин зургийг R2-оос устгана.
    """
    if not instance.pk:
        return  # шинэ бүртгэл — устгах юм алга

    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_image = old.image
    new_image = instance.image

    # Зураг хоосон болсон эсвэл өөрчлөгдсөн
    if old_image and old_image != new_image:
        delete_r2_file(str(old_image))


# ── Бүртгэл устгах үед зургийг R2-оос хасах ─────────────────
@receiver(post_delete, sender=Product)
def product_image_delete(sender, instance, **kwargs):
    """Product устгагдсан үед холбогдох зургийг R2-оос устгана."""
    if instance.image:
        delete_r2_file(str(instance.image))
