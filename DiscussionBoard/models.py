from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.pk})

class Reply(models.Model):
    question = models.ForeignKey(Question, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Reply by {self.author.username} to {self.question.title}'
    
class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, related_name='attachments', null=True, blank=True, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, related_name='attachments', null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.file.name
    
class Visits(models.Model):
    date = models.DateField(auto_now_add=True)
    count = models.PositiveIntegerField(default=0)