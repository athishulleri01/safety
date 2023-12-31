# Generated by Django 4.2.5 on 2023-09-16 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_product_image1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='original_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='selling_prince',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('original_price', models.FloatField()),
                ('selling_price', models.FloatField()),
                ('stock', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='product.product')),
            ],
        ),
    ]
