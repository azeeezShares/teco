# Generated by Django 5.1.6 on 2025-03-13 20:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_booking_unique_together_booking_branch_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('additional_details', models.TextField(blank=True, null=True)),
                ('receive_special_offers', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='booking',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='booking.client'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('client', 'service', 'branch', 'booking_datetime')},
        ),
        migrations.RemoveField(
            model_name='booking',
            name='user',
        ),
    ]
