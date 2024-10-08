# Generated by Django 4.2.1 on 2024-09-18 10:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0062_alter_recipe_recipe_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipe",
            name="recipe_image",
        ),
        migrations.AddField(
            model_name="recipe",
            name="image",
            field=models.ImageField(
                default="asdfasdf",
                upload_to="",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        ["jpg", "jpeg", "png", "webp"]
                    )
                ],
            ),
        ),
    ]
