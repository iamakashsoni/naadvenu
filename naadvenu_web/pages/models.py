from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField
from django.utils.text import slugify


class Student(models.Model):
    LEVEL_CHOICES = [
        ('level1', 'Level 1'),
        ('level2', 'Level 2'),
        ('level3', 'Level 3'),
        ('level4', 'Level 4'),
        ('level5', 'Level 5'),
        ('level6', 'Level 6'),
    ]
    ACCOUNT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=200)
    address = models.TextField()
    occupation = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='uploads/student_photos/', null=True, blank=True)
    date_of_registration = models.DateField(default=timezone.now)
    account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS_CHOICES, default='inactive')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='level1')

    def __str__(self):
        return self.user.username

class Gallery(models.Model):
    MEDIA_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    title = models.CharField(max_length=100)
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, default='image')
    file = models.FileField(upload_to='uploads/gallery/')
    date_of_event = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    share_count = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)

    @property
    def like_count(self):
        return self.users_liked.count()

    users_liked = models.ManyToManyField(User, blank=True,  related_name='liked_posts')
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{timezone.now().strftime('%d-%m-%Y-%H-%M')}")
        super().save(*args, **kwargs)
        
class MediaCoverage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/media-coverage/')
    date_of_event = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    share_count = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)

    @property
    def like_count(self):
        return self.users_liked.count()

    users_liked = models.ManyToManyField(User, blank=True,  related_name='liked_media_posts')
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{timezone.now().strftime('%d-%m-%Y-%H-%M')}")
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Testimonial by {self.student.user.username}'

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = HTMLField()
    date = models.DateField()
    images = models.ImageField(upload_to='uploads/event_images/', blank=True)
    like_count = models.IntegerField(default=0)  # New field for like count
    share_count = models.IntegerField(default=0)  # New field for share count

    def __str__(self):
        return self.title
        
class Contact(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    alt_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return self.email