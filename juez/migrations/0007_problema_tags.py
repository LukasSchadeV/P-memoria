# Generated by Django 5.1.6 on 2025-02-19 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juez', '0006_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='problema',
            name='tags',
            field=models.ManyToManyField(blank=True, to='juez.tag'),
        ),
    ]
