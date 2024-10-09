# Generated by Django 5.1.2 on 2024-10-09 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_transaction_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='airline',
            name='date_formed',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='airline',
            name='parent_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='players.airline'),
        ),
    ]
