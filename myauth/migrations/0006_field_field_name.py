# Generated by Django 4.0.5 on 2023-04-13 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0005_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='field_name',
            field=models.CharField(default=0, max_length=100),
        ),
    ]