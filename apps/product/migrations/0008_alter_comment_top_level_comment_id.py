# Generated by Django 4.2.11 on 2024-05-02 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_comment_top_level_comment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='top_level_comment_id',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]
