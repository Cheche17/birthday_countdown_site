# Generated by Django 4.2.11 on 2024-11-04 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_user_giftcountdown_recipient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcountdown',
            name='gift_description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='giftcountdown',
            name='gift_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]