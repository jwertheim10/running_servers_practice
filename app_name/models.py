from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.db import models
import re

# Create your models here.
class Tasks(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Accounts (AbstractUser):
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z-]{2,}$',  # Allows only letters and hyphens
                message="Name must be at least 2 characters and can only contain uppercase, lowercase, and hyphens"
            )
        ]
    )
    email = models.EmailField(max_length=255)

    def normalize_phone_number(self):
        phone = str(self.phone).strip()
        digits_only = re.sub(r'\D', '', phone)

        if len(digits_only) == 10:
            return f"{digits_only[:3]}-{digits_only[3:6]}-{digits_only[6:]}"
        elif len(digits_only) == 11:
            return f"{digits_only[1:4]}-{digits_only[4:7]}-{digits_only[7:]}"
        else:
            raise ValueError("Invalid phone number format. Phone number should contain 10 or 11 digits.")

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = self.normalize_phone_number()
        if self.pk is None and self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
