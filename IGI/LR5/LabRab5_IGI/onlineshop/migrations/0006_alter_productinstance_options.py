# Generated by Django 5.0.2 on 2024-05-16 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineshop', '0005_remove_productinstance_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productinstance',
            options={'permissions': (('can_mark_issued', 'Set product as issued'),)},
        ),
    ]
