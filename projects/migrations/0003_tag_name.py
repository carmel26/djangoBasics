# Generated by Django 4.0.5 on 2022-06-26 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_tag_project_vote_total_review_project_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
