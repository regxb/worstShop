from catalog.models import Product


class Cart:

    def __init__(self, request) -> None:
        self.session = request.session
        self.cart = self.session.get('session_key', {})
        if 'session_key' not in self.session:
            self.session['session_key'] = self.cart

    def add(self, product):
        product_id = str(product.id)
        product = Product.objects.get(id=product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'product_title': product.title,
                'product_price': int(product.price),
                'product_image': product.image.url,
                'quantity': 1}
        else:
            qty = int(self.cart[product_id]['quantity']) + 1
            self.cart[product_id] = {
                'product_title': product.title,
                'product_price': int(product.price) * qty,
                'product_image': product.image.url,
                'quantity': qty}
        self.session.modified = True

    def get_products_data(self):
        return self.cart.values()

    def get_total_price(self):
        total_sum = sum(item['product_price'] for item in self.cart.values())
        return '{:,}'.format(total_sum).replace(',', ' ')

    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())
