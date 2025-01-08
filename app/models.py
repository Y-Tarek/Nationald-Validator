from django.db import models
from timestampedmodel import TimestampedModel
import uuid
from django.utils.timezone import now

class Service(TimestampedModel):
    """ Model for storing API Keys for service to service Authentication. """

    public_key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    private_key = models.TextField()
    service_name = models.CharField(max_length=255)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.service_name
    
    @property
    def is_expired(self):
        return self.expires_at and self.expires_at < now()

class CountryCode(models.Model):
    """ This Model will hold Country codes for identity. """
    code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)