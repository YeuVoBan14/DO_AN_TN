# Generated by Django 4.2.5 on 2024-03-02 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_category_updated_suppiler_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='old_cart',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]