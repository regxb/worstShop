# Generated by Django 5.0.7 on 2024-07-31 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_remove_product_category_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/products/%Y/%m/%d', verbose_name='Изображение'),
        ),
    ]