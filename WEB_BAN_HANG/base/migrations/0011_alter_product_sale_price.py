# Generated by Django 5.0.4 on 2024-05-02 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_suppiler_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True),
        ),
    ]