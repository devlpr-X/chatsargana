from decimal import Decimal


def cart(request):
    cart_data = request.session.get('cart', {})
    count = sum(item['qty'] for item in cart_data.values())
    total = sum(Decimal(item['price']) * item['qty'] for item in cart_data.values())
    return {
        'cart_count': count,
        'cart_total': total,
    }
