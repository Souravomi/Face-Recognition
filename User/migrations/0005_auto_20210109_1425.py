# Generated by Django 3.0.8 on 2021-01-09 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_attandance_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='Mobile',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
