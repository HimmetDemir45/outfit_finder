from rest_framework import serializers
from .models import Category, StyleTag, ClothingItem, ItemLink, Outfit

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class StyleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleTag
        fields = ['id', 'name', 'slug']

class ItemLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemLink
        fields = ['id', 'clothing_item', 'store_name', 'url', 'price', 'is_affiliate', 'last_updated']

class ClothingItemSerializer(serializers.ModelSerializer):
    # Bir kıyafeti çektiğimizde, altındaki mağaza linklerini de JSON içinde otomatik görebilmek için:
    links = ItemLinkSerializer(many=True, read_only=True)
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = ClothingItem
        fields = ['id', 'name', 'category', 'category_name', 'image', 'tags', 'links', 'added_by', 'created_at']
        # Güvenlik önlemi: Kimin eklediğini dışarıdan gelen veriye güvenerek değil,
        # doğrudan giriş yapmış kullanıcının token/oturum bilgisinden alacağız.
        read_only_fields = ['added_by']

class OutfitSerializer(serializers.ModelSerializer):
    # Kombinleri çekerken, içindeki kıyafetlerin sadece ID'sini değil, tüm detaylarını getirmesi için:
    items_detail = ClothingItemSerializer(source='items', many=True, read_only=True)
    tags_detail = StyleTagSerializer(source='tags', many=True, read_only=True)
    creator_name = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Outfit
        fields = [
            'id', 'name', 'image', 'description',
            'items', 'items_detail',
            'tags', 'tags_detail',
            'creator', 'creator_name',
            'is_published', 'created_at'
        ]
        read_only_fields = ['creator']
