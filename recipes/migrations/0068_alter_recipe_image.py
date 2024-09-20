# Generated by Django 4.2.1 on 2024-09-18 12:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0067_alter_recipe_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="image",
            field=models.ImageField(
                upload_to="",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        ["jpg", "jpeg", "png", "webp"]
                    )
                ],
                verbose_name="image",
            ),
        ),
    ]