from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Category, StyleTag, ClothingItem, ItemLink, Outfit
from .serializers import (
    CategorySerializer, StyleTagSerializer, ClothingItemSerializer,
    ItemLinkSerializer, OutfitSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class StyleTagViewSet(viewsets.ModelViewSet):
    queryset = StyleTag.objects.all()
    serializer_class = StyleTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ClothingItemViewSet(viewsets.ModelViewSet):
    queryset = ClothingItem.objects.all()
    serializer_class = ClothingItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Güvenlik: Kıyafeti ekleyen kişiyi dışarıdan gelen veriye göre değil,
        # o an sisteme giriş yapmış (istek atan) kullanıcıya göre otomatik belirler.
        serializer.save(added_by=self.request.user)

class ItemLinkViewSet(viewsets.ModelViewSet):
    queryset = ItemLink.objects.all()
    serializer_class = ItemLinkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OutfitViewSet(viewsets.ModelViewSet):
    serializer_class = OutfitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Ziyaretçiler sadece onaylanmış (is_published=True) kombinleri görür.
        # Giriş yapmış kullanıcılar ise hem onaylanmış kombinleri hem de kendi oluşturdukları taslakları görebilir.
        if self.request.user.is_authenticated:
            return Outfit.objects.filter(Q(is_published=True) | Q(creator=self.request.user))
        return Outfit.objects.filter(is_published=True)

    def perform_create(self, serializer):
        # Güvenlik: Kombini oluşturan kişiyi otomatik olarak arka planda atar.
        serializer.save(creator=self.request.user)
