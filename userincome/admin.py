from django.contrib import admin
from userincome.models import UserIncome,Source

# Register your models here.
@admin.register(UserIncome)
class UserIncomeAdmin(admin.ModelAdmin):
    list_display=['amount', 'date','owner' ,'source']
    list_display_links=['amount','owner']
    ordering=['-date']

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display=['id','name']