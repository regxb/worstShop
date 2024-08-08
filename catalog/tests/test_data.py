from django.core.files.uploadedfile import SimpleUploadedFile
from catalog.models import Category, Product


def create_test_data():
    category_1 = Category.objects.create(name='test_1', image='category_image1.png')
    category_2 = Category.objects.create(name='test_2', image='category_image2.png')
    category_3 = Category.objects.create(name='test_3', image='category_image3.png')
    product_1 = Product.objects.create(
        title='title1',
        brand='brand1',
        image='product_image1.png'
    )
    product_1.category.set([category_1])

    product_2 = Product.objects.create(
        title='title2',
        brand='brand2',
        image='product_image2.png'
    )
    product_2.category.set([category_1, category_2])

    product_3 = Product.objects.create(
        title='title3',
        brand='brand3',
        image='product_image3.png'
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
