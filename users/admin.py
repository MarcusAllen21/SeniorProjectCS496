from django.contrib import admin
from .models import Profile, Quiz, MCQuestion, Choice, StudentQuizResult

# Register your models here.

class StudentQuizResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'total_questions') 
    list_filter = ('quiz', 'student')
    search_fields = ['student__username', 'quiz__name']

admin.site.register(Profile)
admin.site.register(MCQuestion)
admin.site.register(Choice)
admin.site.register(Quiz)
admin.site.register(StudentQuizResult, StudentQuizResultAdmin)
