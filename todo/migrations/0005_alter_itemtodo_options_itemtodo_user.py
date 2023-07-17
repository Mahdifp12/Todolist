# Generated by Django 4.2.3 on 2023-07-16 22:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0004_alter_itemtodo_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemtodo',
            options={'ordering': ['created_date'], 'verbose_name': 'آیتم تودو', 'verbose_name_plural': 'آیتم های تودو'},
        ),
        migrations.AddField(
            model_name='itemtodo',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]