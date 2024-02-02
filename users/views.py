from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import ChoiceForm, ChoiceFormSet, MCQuestionFormSet, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Quiz, QuizAttempt, MCQuestion, Choice, StudentQuizResult
from django.views.generic import DetailView
from .forms import QuizForm, MCQuestion, MCQuestionFormSet, MCQuestionForm


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            teacher = form.cleaned_data.get('is_teacher')
            messages.success(request, f'Account created for {username}!, are they a teacher? {teacher}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated successfully!')
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)

# Working with quizzes

class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz_detail.html'
    context_object_name = 'quiz'

def submit_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    existing_attempt = QuizAttempt.objects.filter(student=request.user, quiz=quiz).exists()
    
    if existing_attempt:
        messages.info(request, 'You have already attempted this quiz.')
        return redirect('quiz-list')

    if request.method == 'POST':
        correct_answers = 0
        selected_choices = []

        for question in quiz.questions.all():
            submitted_answer_pk = request.POST.get(str(question.pk))

            print("Submitted Answer PK:", submitted_answer_pk)
            
            if submitted_answer_pk:
                choice = get_object_or_404(Choice, pk=submitted_answer_pk)
                print("Is Choice Correct?", choice.is_correct)
                selected_choices.append(choice)
                
                if choice.is_correct:
                    correct_answers += 1

        score = (correct_answers / len(quiz.questions.all())) * 100

        attempt = QuizAttempt(student=request.user, quiz=quiz)
        attempt.save()
        attempt.selected_choices.set(selected_choices)

        StudentQuizResult.objects.create(
            student=request.user, 
            quiz=quiz, 
            score=score,
            total_questions=quiz.questions.count()
        )

        return redirect('quiz-list')
    return redirect('quiz-detail', pk=quiz.pk)

def quiz_list(request):
    quizzes = Quiz.objects.all()

    context = {
        'quizzes': quizzes,
        'is_teacher': request.user.is_authenticated and request.user.profile.is_teacher
    }
    
    return render(request, 'users/quiz_list.html', context)


def quiz_detail(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'users/quiz_detail.html', {'quiz': quiz})

@login_required
def create_quiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = request.user
            quiz.save()
            return redirect('create_questions', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'users/create_quiz.html', {'form': form})

def teacher_report(request):
    quizzes = Quiz.objects.all()
    data = []

    for quiz in quizzes:
        quiz_data = {
            "quiz": quiz.title,
            "results": [],
            "average": 0,
            "highest": 0,
            "lowest": 100  # Assuming score is out of 100
        }

        results = StudentQuizResult.objects.filter(quiz=quiz)
        
        for result in results:
            quiz_data["results"].append({
                "student": result.student.username,
                "score": result.score
            })

            # Update highest, lowest, and accumulate for average
            if result.score > quiz_data["highest"]:
                quiz_data["highest"] = result.score
            if result.score < quiz_data["lowest"]:
                quiz_data["lowest"] = result.score
            quiz_data["average"] += result.score

        if results:
            quiz_data["average"] /= len(results)

        data.append(quiz_data)

    return render(request, "users/teacher_report.html", {"quizzes": data})

@login_required
def student_report(request):
    student_results = StudentQuizResult.objects.filter(student=request.user)
    
    context = {
        'student_results': student_results
    }
    return render(request, 'users/student_report.html', context)

def create_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == "POST":
        form = MCQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('add_choices', question_id=question.id)
    else:
        form = MCQuestionForm()
    return render(request, 'users/create_question.html', {'form': form})



def add_choices(request, question_id):
    question = get_object_or_404(MCQuestion, pk=question_id)
    if request.method == "POST":
        formset = ChoiceFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            # Redirect to create another question or some other page
            return redirect('create_questions', quiz_id=question.quiz.id)
    else:
        formset = ChoiceFormSet(instance=question)
    return render(request, 'users/add_choices.html', {'formset': formset})


