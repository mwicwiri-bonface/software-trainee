# Generated by Django 3.2.3 on 2021-05-21 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0002_alter_joballocation_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postjob',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='applicant.job'),
        ),
    ]
