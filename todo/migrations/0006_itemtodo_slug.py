# Generated by Django 4.2.3 on 2023-07-17 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_alter_itemtodo_options_itemtodo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtodo',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=200, unique=True, verbose_name='عنوان در url'),
        ),
    ]
