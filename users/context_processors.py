from .models import Wishlist


def wishlist(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        return {'wishlist': wishlist}
    return {'wishlist': []}
