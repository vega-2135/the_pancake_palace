# Generated by Django 4.2.1 on 2024-07-22 20:24

import cloudinary.models
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0053_alter_recipe_recipe_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="recipe_image",
            field=cloudinary.models.CloudinaryField(
                max_length=255,
                validators=[
                    django.core.validators.FileExtensionValidator(
                        ["jpg", "jpeg", "png", "webp"]
                    )
                ],
                verbose_name="image",
            ),
        ),
    ]
