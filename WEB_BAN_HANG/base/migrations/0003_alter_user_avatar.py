# Generated by Django 4.2.5 on 2024-02-15 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='users/avatar.svg', null=True, upload_to='users/'),
        ),
    ]
