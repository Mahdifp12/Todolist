# Generated by Django 4.2.3 on 2023-07-16 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_remove_itemtodo_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemtodo',
            options={'verbose_name': 'آیتم تودو', 'verbose_name_plural': 'آیتم های تودو'},
        ),
    ]