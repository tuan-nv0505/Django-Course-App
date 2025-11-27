from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    avatar = CloudinaryField(default='https://res.cloudinary.com/dt1pa28g2/image/upload/v1764153082/sbcf-default-avatar_tgyi8q.webp')


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Course(BaseModel):
    subject = models.CharField(max_length=255)
    description = models.TextField(null=True)
    image = CloudinaryField(null=True) #models.ImageField(upload_to='courses/%Y/%m', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

class Lesson(BaseModel):
    subject = models.CharField(max_length=255)
    content = RichTextField()
    image = CloudinaryField(null=True) #models.ImageField(upload_to='lessons/%Y/%m', null=True)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.subject

    class Meta:
        unique_together = ('subject', 'course')

class Tag(BaseModel):
    name =models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Comment(Interaction):
    content = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.content

class Like(Interaction):
    class Meta:
        unique_together = ('user', 'lesson')
