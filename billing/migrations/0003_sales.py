# Generated by Django 4.2.6 on 2024-07-07 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_cart_data_cart_product_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_name', models.CharField(max_length=100)),
                ('sales_total', models.IntegerField(max_length=100)),
            ],
        ),
    ]