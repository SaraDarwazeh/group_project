# Generated by Django 5.0.7 on 2024-08-26 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BunyanApp', '0004_language_user_country_alter_appointment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
