# Generated by Django 4.2.9 on 2024-01-14 23:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0010_quiz_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='user2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quizzes_user2', to=settings.AUTH_USER_MODEL),
        ),
    ]
