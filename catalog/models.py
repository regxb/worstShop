import random
import string

import stripe
from django.conf import settings
from django.db import models
from django.urls import reverse
from slugify import slugify

stripe.api_key = settings.STRIPE_SECRET_KEY


class Category(models.Model):
    name = models.CharField('Категория', max_length=250)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    slug = models.SlugField('URL', max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField('Время создания', auto_now_add=True)
    image = models.ImageField('Изображение', upload_to='category', null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        unique_together = (['slug', 'parent'])

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('catalog:products', args=[self.slug])

    @staticmethod
    def _rand_slug():
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    title = models.CharField('Название', max_length=250)
    brand = models.CharField('Бренд', max_length=250)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField('URL', max_length=250)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=0, default=99)
    image = models.ImageField('Изображение', upload_to='products')
    available = models.BooleanField('Наличие', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)
    stripe_price = models.CharField(blank=True, null=True, max_length=128)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.stripe_price:
            stripe_price_id = self.get_stripe_product_price_id()
            self.stripe_price = stripe_price_id
        super(Product, self).save(*args, **kwargs)

    def get_stripe_product_price_id(self):
        product = stripe.Product.create(name=self.title)
        price = stripe.Price.create(
            currency="rub",
            unit_amount=round(self.price*100),
            product=product['id'],
        )
        return price['id']

    def get_absolute_url(self):
        return reverse("catalog:product_detail", args=[str(self.slug)])

    def get_average_rating(self):
        reviews = self.reviews.all()
        total_rating = sum([review.rating for review in reviews])
        return round(total_rating / reviews.count(), 1) if reviews.exists() else 0


class ProductManager(models.Manager):

    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    objects = ProductManager()

    class Meta:
        proxy = True


class Review(models.Model):
    from users.models import User

    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(max_length=1000)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user.username}: {self.comment}'
