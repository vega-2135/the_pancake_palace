# Generated by Django 4.2.1 on 2024-07-05 10:36

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0044_alter_recipe_recipe_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="recipe_image",
            field=cloudinary.models.CloudinaryField(
                default="placeholder", max_length=255, verbose_name="image"
            ),
        ),
    ]
