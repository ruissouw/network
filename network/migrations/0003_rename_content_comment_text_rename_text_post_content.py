# Generated by Django 5.0.6 on 2024-08-08 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_user_followers_user_following_post_comment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="content",
            new_name="text",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="text",
            new_name="content",
        ),
    ]
