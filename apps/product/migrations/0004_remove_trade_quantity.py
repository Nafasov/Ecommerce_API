# Generated by Django 4.2.11 on 2024-05-02 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_category_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='quantity',
        ),
    ]