# Generated by Django 5.0.7 on 2024-08-28 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BunyanApp', '0010_remove_choice_created_at_remove_choice_points_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='points',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]
