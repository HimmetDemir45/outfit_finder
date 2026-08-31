from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, StyleTagViewSet, ClothingItemViewSet,
    ItemLinkViewSet, OutfitViewSet
)

app_name = "catalog"

# DefaultRouter, ViewSet'lerimiz için standart GET, POST, PUT, DELETE rotalarını otomatik oluşturur.
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', StyleTagViewSet)
router.register(r'clothes', ClothingItemViewSet)
router.register(r'links', ItemLinkViewSet)
router.register(r'outfits', OutfitViewSet, basename='outfit')

urlpatterns = [
    path('', include(router.urls)),
]
