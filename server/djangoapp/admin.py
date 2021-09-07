from django.contrib import admin
from .models import CarMake, CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['maker', 'name','modeltype','engine','year']

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name','description']
    inlines = [CarModelInline]

# Register your models here.
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
