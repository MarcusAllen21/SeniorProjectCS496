from django.shortcuts import render
from .models import Question, Reply, Attachment, Visits
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.db import models

# Create your views here.

def home(request):
    context = {
        'posts': Question.objects.all()
    }
    return render(request, 'DiscussionBoard/home.html', context)

class QuestionListView(ListView):
    model = Question
    template_name = 'DiscussionBoard/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        post_count = Question.objects.count()
        visit_count = Visits.objects.aggregate(total_visits=models.Sum('count'))['total_visits']
        
        context['post_count'] = post_count
        context['visit_count'] = visit_count
        
        return context

class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['replies'] = self.object.replies.all().order_by('-date_posted')
        return context

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        for file in self.request.FILES.getlist('files'):
            Attachment.objects.create(file=file, question=self.object)

        return response

    
class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = ['title', 'content', 'file_upload']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Reply
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question = Question.objects.get(pk=self.kwargs['pk'])
        response = super().form_valid(form)
        for file in self.request.FILES.getlist('files'):
            Attachment.objects.create(file=file, reply=self.object)
            
        return response

    def get_success_url(self):
        return reverse_lazy('question-detail', kwargs={'pk': self.object.question.pk})

    
def about(request):
    return render(request, 'DiscussionBoard/about.html', {'title': "About"})


