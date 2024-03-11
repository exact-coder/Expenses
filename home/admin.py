from django.contrib import admin
from home.models import Expense,Category


# Register your models here.
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display=['amount', 'date','owner' ,'category']
    list_display_links=['amount','owner']
    ordering=['-date']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name']