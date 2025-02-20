# Generated by Django 5.1.6 on 2025-02-20 03:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juez', '0007_problema_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problema',
            name='entradas_prueba',
        ),
        migrations.RemoveField(
            model_name='problema',
            name='salidas_esperadas',
        ),
        migrations.CreateModel(
            name='CasoPrueba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrada', models.TextField()),
                ('salida', models.TextField()),
                ('activo', models.BooleanField(default=False)),
                ('problema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='casos_prueba', to='juez.problema')),
            ],
        ),
    ]
