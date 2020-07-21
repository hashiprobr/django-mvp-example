from django.db import models
from django.dispatch import receiver

from example import public_storage, private_storage


class DriveFile(models.Model):
    class Meta:
        abstract = True

    description = models.CharField(max_length=255)


class PublicFile(DriveFile):
    data = models.FileField(storage=public_storage)


class PrivateFile(DriveFile):
    data = models.FileField(storage=private_storage)


@receiver(models.signals.post_delete, sender=PublicFile)
def post_public_file_delete(sender, instance, using, **kwargs):
    sender.data.field.storage.delete(instance.data.name)


@receiver(models.signals.post_delete, sender=PrivateFile)
def post_private_file_delete(sender, instance, using, **kwargs):
    sender.data.field.storage.delete(instance.data.name)
