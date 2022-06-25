# Generated by Django 4.0.5 on 2022-06-25 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pancakes', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='facebook_link',
            field=models.URLField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='instagram_link',
            field=models.URLField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='twitter_link',
            field=models.URLField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='youtube_link',
            field=models.URLField(blank=True, default='', null=True),
        ),
    ]
