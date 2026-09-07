from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
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
    # queryset ve serializer_class ayarların...

    # Ziyaretçiler okuyabilir, giriş yapanlar oluşturabilir,
    # SADECE objenin sahibi güncelleyip silebilir.
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Güvenlik: Kombini oluşturan kişiyi otomatik olarak arka planda atar.
        serializer.save(creator=self.request.user)
