# Generated by Django 5.1.2 on 2024-10-09 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0004_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default='credit', max_length=6),
        ),
    ]
