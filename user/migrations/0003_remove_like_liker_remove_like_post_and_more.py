# Generated by Django 4.1.6 on 2023-04-25 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_postview_like_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='liker',
        ),
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='postview',
            name='post',
        ),
        migrations.RemoveField(
            model_name='postview',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='PostView',
        ),
    ]