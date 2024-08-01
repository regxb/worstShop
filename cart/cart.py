from decimal import Decimal

from catalog.models import Product, ProductProxy


class Cart:

    def __init__(self, request) -> None:
        self.session = request.session
        self.cart = self.session.get('session_key', {})
        if 'session_key' not in self.session:
            self.session['session_key'] = self.cart

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = ProductProxy.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['product_price'] = Decimal(item['product_price'])
            item['total_price'] = item['product_price'] * item['quantity']
            yield item

    def add(self, product):
        product_id = str(product.id)
        product = Product.objects.get(id=product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'product_price': int(product.price),
                'quantity': 1}
        else:
            self.cart[product_id]['quantity'] += 1
        self.session.modified = True

    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] == 1:
                del self.cart[product_id]
            else:
                self.cart[product_id]['quantity'] -= 1
            self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def get_total_price(self):
        return sum((Decimal(item['product_price']) * item['quantity']) for item in self.cart.values())

    def get_product_quantity(self, product_id):
        item = self.cart.get(product_id, {})
        return item.get('quantity', 0)

    def get_product_price(self, product_id):
        item = self.cart.get(product_id, {})
        return Decimal(item.get('product_price', 0)) * item.get('quantity', 0)
