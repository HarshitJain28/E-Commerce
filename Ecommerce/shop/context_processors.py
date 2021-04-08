from .models import Cart


def cart_processor(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, cart_status=False)
        if cart.exists():
            total_items = 0
            for item in cart:
                total_items += item.quantity
            return {
                'total_items': total_items
            }
        else:
            return {
                'total_items': 0
            }
    else:
        return {
            'total_items': 0
        }
