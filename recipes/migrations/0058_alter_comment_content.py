# Generated by Django 4.2.1 on 2024-09-16 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0057_alter_comment_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=models.TextField(),
        ),
    ]
