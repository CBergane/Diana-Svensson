# Generated by Django 4.1.6 on 2023-02-12 01:39

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_like_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_summernote.fields.SummernoteTextField(),
        ),
    ]
