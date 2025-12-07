from rest_framework import serializers
from .models import Menu, Category, Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id','name','description','image','is_available']

class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()  # اضافه کردن فیلد URL تصویر

    class Meta:
        model = Category
        fields = ['id','name','order','items','image','image_url']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class MenuSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ['id','name','description','categories']
