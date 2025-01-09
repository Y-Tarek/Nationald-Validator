from django.db import models
from timestampedmodel import TimestampedModel
from .utility import generate_key_pair 
from django.utils.timezone import now
from app.constants import (
    SUCCESSFUL,
    STATUS_CHOICES
)

class Service(TimestampedModel):
    """ Model for storing API Keys for service to service Authentication. """

    public_key = models.TextField(unique=True, blank=True)
    private_key = models.TextField(blank=True)
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
            self.public_key, self.private_key = generate_key_pair()
        super().save(*args, **kwargs)

class Transaction(TimestampedModel):
    """ This Model will hold service transactions. """
    service = models.ForeignKey(
        Service,
        on_delete= models.CASCADE,
        related_name="service_transactions"
    )
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=SUCCESSFUL)