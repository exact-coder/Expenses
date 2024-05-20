from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# Create your models here.

class UserIncome(models.Model):
    amount = models.FloatField(_("Amount"))
    date = models.DateField(_("Date"),default=now)
    description = models.TextField(_("Description"))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(_("Source"), max_length=255)

    def __str__(self) -> str:
        return f'{self.source}--{self.amount}'
    
    class Meta:
        ordering=['-date']

class Source(models.Model):
    name = models.CharField(_("Category Name"), max_length=255)

    def __str__(self) -> str:
        return self.name