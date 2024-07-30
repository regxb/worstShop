from django.core.files.uploadedfile import SimpleUploadedFile
from catalog.models import Category, Product


def create_test_data():
    test_image = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded_file = SimpleUploadedFile('test.jpg', test_image, content_type='image/jpeg')

    category_1 = Category.objects.create(name='test_1', image=uploaded_file)
    category_2 = Category.objects.create(name='test_2', image=uploaded_file)
    category_3 = Category.objects.create(name='test_3', image=uploaded_file)
    product_1 = Product.objects.create(
        title='title1',
        brand='brand1',
        image=uploaded_file
    )
    product_1.category.set([category_1])

    product_2 = Product.objects.create(
        title='title2',
        brand='brand2',
        image=uploaded_file
    )
    product_2.category.set([category_1, category_2])

    product_3 = Product.objects.create(
        title='title3',
        brand='brand3',
        image=uploaded_file
    )
    product_3.category.set([category_3])

    return {
        'categories': {
            'category_1': category_1,
            'category_2': category_2,
            'category_3': category_3,
        },
        'products': {
            'product_1': product_1,
            'product_2': product_2,
            'product_3': product_3
        }
    }
