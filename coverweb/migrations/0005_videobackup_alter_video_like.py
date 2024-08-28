# Generated by Django 5.0.6 on 2024-08-15 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coverweb', '0004_alter_video_like_alter_video_thumbnail_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoBackUp',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('sub', models.CharField(max_length=100)),
                ('info', models.CharField(blank=True, max_length=10000)),
                ('view', models.IntegerField(default=0)),
                ('like', models.CharField(blank=True, max_length=100000)),
                ('date', models.DateField(auto_now_add=True)),
                ('thumbnail', models.FileField(blank=True, upload_to='video/')),
                ('video', models.FileField(blank=True, upload_to='video/')),
                ('genre', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='video',
            name='like',
            field=models.CharField(blank=True, max_length=100000),
        ),
    ]
