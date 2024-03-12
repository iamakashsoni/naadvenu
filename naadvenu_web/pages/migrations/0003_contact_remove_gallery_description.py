# Generated by Django 4.2.10 on 2024-02-23 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_remove_student_country_remove_student_pincode_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('phone_number_1', models.CharField(max_length=15)),
                ('phone_number_2', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='description',
        ),
    ]
