# Generated by Django 5.1.6 on 2025-04-04 12:34

import froala_editor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', froala_editor.fields.FroalaField()),
            ],
        ),
    ]
