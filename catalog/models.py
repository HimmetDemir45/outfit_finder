from django.db import models
from django.conf import settings

class Category(models.Model):
    """Tişört, Pantolon, Ayakkabı gibi temel kategoriler"""
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class StyleTag(models.Model):
    """Arama ve filtreleme için etiketler (Örn: Casual, Kıvanç Tatlıtuğ, Sokak Tarzı)"""
    name = models.CharField(max_length=100, verbose_name="Etiket/Tarz")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class ClothingItem(models.Model):
    """Kombinleri oluşturan tekil kıyafet parçaları"""
    name = models.CharField(max_length=200, verbose_name="Kıyafet Adı")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='clothing_images/', verbose_name="Fotoğraf")
    tags = models.ManyToManyField(StyleTag, blank=True, related_name='clothes')

    # İleride kullanıcılar eklediğinde kimin eklediğini bilmek için
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class ItemLink(models.Model):
    """Aynı ürünün farklı mağazalardaki fiyatları ve affiliate linkleri"""
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name='links')
    store_name = models.CharField(max_length=100, verbose_name="Mağaza Adı (Trendyol, Zara vb.)")
    url = models.URLField(max_length=500, verbose_name="Ürün Linki")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")
    is_affiliate = models.BooleanField(default=True, verbose_name="Affiliate Linki mi?")

    # İleride bot (scraper) yazdığımızda bu alanı otomatik güncelleyeceğiz
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Son Fiyat Güncellemesi")

    class Meta:
        ordering = ['price'] # En ucuzdan en pahalıya otomatik sıralama yapar

    def __str__(self):
        return f"{self.store_name} - {self.price} TL"

class Outfit(models.Model):
    """Kıyafetlerin birleşimiyle oluşan nihai kombinler"""
    name = models.CharField(max_length=200, verbose_name="Kombin Adı")
    image = models.ImageField(upload_to='outfit_images/', verbose_name="Kombin Fotoğrafı")
    description = models.TextField(blank=True, verbose_name="Açıklama")

    items = models.ManyToManyField(ClothingItem, related_name='outfits', verbose_name="Kullanılan Kıyafetler")
    tags = models.ManyToManyField(StyleTag, blank=True, related_name='outfits')

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_outfits')

    # Kullanıcılar kombin eklemeye başladığında, onaylamadan sitede görünmemesi için
    is_published = models.BooleanField(default=True, verbose_name="Yayında mı?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
