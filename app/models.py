from django.db import models
from timestampedmodel import TimestampedModel
from .utility import generate_key_pair 
from django.utils.timezone import now

class Service(TimestampedModel):
    """ Model for storing API Keys for service to service Authentication. """

    public_key = models.TextField(unique=True)
    private_key = models.TextField()
    service_name = models.CharField(max_length=255)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.service_name
    
    @property
    def is_authenticated(self):
        return self.is_active and (not self.expires_at or self.expires_at >= now())
    
    @property
    def is_expired(self):
        return self.expires_at and self.expires_at < now()
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.public_key, self.private_key = self.generate_key_pair()
        super().save(*args, **kwargs)

class CountryCode(models.Model):
    """ This Model will hold Country codes for identity. """
    code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)