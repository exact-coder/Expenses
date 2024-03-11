from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Expense(models.Model):
    amount = models.FloatField(_("Amount"))
    date = models.DateField(_("Date"),default=now)
    description = models.TextField(_("Description"))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(_("Category"), max_length=255)

    def __str__(self) -> str:
        return f'{self.category}--{self.amount}'
    
    class Meta:
        ordering=['-date']

class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=255)

    class Meta:
        verbose_name_plural='Categories'

    def __str__(self) -> str:
        return self.name