# Generated by Django 5.0.4 on 2024-11-18 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineshop', '0043_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinfo',
            name='banner3',
            field=models.ImageField(blank=True, null=True, upload_to='company_info/'),
        ),
    ]
