from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse, reverse_lazy

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_teacher = models.BooleanField(verbose_name="Teacher", default=False)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('quiz-detail', kwargs={'pk': self.pk})

    
class MCQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField(null=True)

    def __str__(self):
        return self.text if self.text else "Unnamed Question"

class Choice(models.Model):
    question = models.ForeignKey(MCQuestion, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    selected_choices = models.ManyToManyField(Choice)
    date_attempted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}'s attempt on {self.quiz.title}"
    
class StudentQuizResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_results")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'quiz')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} - {self.score}/{self.total_questions}"