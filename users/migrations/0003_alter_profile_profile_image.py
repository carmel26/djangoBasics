# Generated by Django 4.0.5 on 2022-07-03 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profiles/user-default.jpg', null=True, upload_to='profiles/'),
        ),
    ]
