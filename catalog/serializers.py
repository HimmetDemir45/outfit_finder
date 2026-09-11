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
        fields = '__all__'

class ClothingItemSerializer(serializers.ModelSerializer):
    # Fiyatları sıralamak için alanımızı dinamik bir metoda çeviriyoruz
    links = serializers.SerializerMethodField()

    class Meta:
        model = ClothingItem
        # Senin modelinden aldığımız tüm alanlar ve güvenliği sağlayan 'creator' alanı
        fields = ['id', 'name', 'category', 'image', 'tags', 'links', 'creator']

    def get_links(self, obj):
        # Modelinde related_name='links' yazdığın için burada obj.links kullanıyoruz
        # Fiyatları ucuzdan pahalıya sırala
        ordered_links = obj.links.all().order_by('price')

        # Sıralı veriyi dönüştür ve JSON'a ekle
        return ItemLinkSerializer(ordered_links, many=True).data

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
