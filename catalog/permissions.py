from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Sadece objenin sahibine düzenleme (PUT/PATCH) ve silme (DELETE) izni verir.
    Hem 'creator' hem de 'added_by' alanlarını dinamik olarak destekler.
    """
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS gibi veri değiştirmeyen isteklere her zaman izin ver
        if request.method in permissions.SAFE_METHODS:
            return True

        # Objenin sahibini bul ('creator' alanı varsa onu al, yoksa None dön)
        owner = getattr(obj, 'creator', None)

        # Eğer 'creator' yoksa, bu sefer 'added_by' alanına bak
        if owner is None:
            owner = getattr(obj, 'added_by', None)

        # Eğer iki alan da modelde yoksa, işi şansa bırakma ve güvenli tarafta kal (False dön)
        if owner is None:
            return False

        # Son olarak objenin sahibi ile isteği atan kullanıcıyı karşılaştır
        return owner == request.user
