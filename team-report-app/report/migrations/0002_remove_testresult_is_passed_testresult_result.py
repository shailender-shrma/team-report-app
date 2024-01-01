# Generated by Django 4.2.6 on 2023-11-18 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresult',
            name='is_passed',
        ),
        migrations.AddField(
            model_name='testresult',
            name='result',
            field=models.CharField(choices=[('untested', 'untested'), ('passed', 'passed'), ('failed', 'failed')], default='untested', max_length=90),
        ),
    ]
