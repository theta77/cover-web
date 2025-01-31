# Generated by Django 5.0.6 on 2024-08-15 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coverweb', '0003_remove_video_filename_video_thumbnail_video_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='like',
            field=models.CharField(max_length=100000),
        ),
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.FileField(blank=True, upload_to='video/'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(blank=True, upload_to='video/'),
        ),
    ]
