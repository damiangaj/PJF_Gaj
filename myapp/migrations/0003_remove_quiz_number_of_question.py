# Generated by Django 4.2.9 on 2024-01-10 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_quiz_time_alter_answer_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='number_of_question',
        ),
    ]
