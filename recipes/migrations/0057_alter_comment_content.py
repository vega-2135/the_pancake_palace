# Generated by Django 4.2.1 on 2024-09-12 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0056_alter_recipe_servings"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=models.TextField(
                help_text="Remember to rate the recipe before submitting a comment."
            ),
        ),
    ]