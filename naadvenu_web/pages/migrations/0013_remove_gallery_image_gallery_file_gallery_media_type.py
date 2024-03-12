# Generated by Django 4.2.10 on 2024-03-06 17:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_alter_student_email_mediacoverage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='image',
        ),
        migrations.AddField(
            model_name='gallery',
            name='file',
            field=models.FileField(default=django.utils.timezone.now, upload_to='uploads/gallery/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gallery',
            name='media_type',
            field=models.CharField(choices=[('image', 'Image'), ('video', 'Video')], default='image', max_length=10),
        ),
    ]
