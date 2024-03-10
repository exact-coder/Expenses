from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.

class UserPreference(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    currency = models.CharField(_("Currency"), max_length=225,blank=True,null=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s preferences"