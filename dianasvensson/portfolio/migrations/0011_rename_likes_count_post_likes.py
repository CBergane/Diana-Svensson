# Generated by Django 4.1.6 on 2023-02-14 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0010_remove_post_excerpt_remove_post_likes_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='likes_count',
            new_name='likes',
        ),
    ]
