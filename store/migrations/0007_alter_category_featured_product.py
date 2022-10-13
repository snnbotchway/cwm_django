# Generated by Django 4.1.2 on 2022-10-13 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_category_options_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='featured_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='store.product'),
        ),
    ]
