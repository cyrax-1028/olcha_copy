# Generated by Django 5.1.6 on 2025-03-09 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
