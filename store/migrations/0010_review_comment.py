# Generated by Django 4.1.2 on 2022-10-15 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_rename_reviews_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
