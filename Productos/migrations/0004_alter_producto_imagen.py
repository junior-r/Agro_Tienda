# Generated by Django 4.0.5 on 2022-06-19 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0003_producto_recomendar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='productos/<django.db.models.fields.CharField>_<built-in function id>/'),
        ),
    ]
