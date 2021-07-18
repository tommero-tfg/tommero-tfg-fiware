from django import forms
from django.contrib import admin

from .models import CarModel, ModelReview, CarImage


class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = '__all__'


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    form = CarModelForm
    list_display = ['id', 'name', 'brand', 'fuel', 'transmission', 'motor', 'seats',
                    'average_consumption', 'price', 'base_price']
    readonly_fields = ['guid']


class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = '__all__'


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    form = CarImageForm
    list_display = ['id', 'name', 'image', 'car']


class ModelReviewForm(forms.ModelForm):
    class Meta:
        model = ModelReview
        fields = '__all__'


@admin.register(ModelReview)
class ModelReviewAdmin(admin.ModelAdmin):
    form = ModelReviewForm
    list_display = ['id', 'text', 'user', 'car']
