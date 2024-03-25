from django.db import migrations, models
import json

def convert_text_to_json(apps, schema_editor):
    Recipe = apps.get_model('recipes', 'Recipe')
    for recipe in Recipe.objects.all():
        try:
            ingredients_json = json.loads(recipe.ingredients)
            recipe.ingredients_json_field = ingredients_json
            recipe.save()
        except json.JSONDecodeError:
            # Handle invalid JSON data if necessary
            pass

class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(convert_text_to_json),
    ]