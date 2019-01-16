# Generated by Django 2.1.4 on 2019-01-16 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_server', '0003_question_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('answer', models.TextField()),
                ('question_id', models.IntegerField()),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]