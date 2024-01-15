from django import template
from django.contrib.auth.decorators import login_required
import json

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Quiz, Question, Answer, Result


# Create your views here.
def home(request):
    return render(request, "myapp/home.html")


def myquiz(request):
    #
    user_quizzes = Quiz.objects.filter(Q(user=request.user) | Q(user2=request.user))

    return render(request, 'myapp/myquiz.html', {'user_quizzes': user_quizzes})


def addUserToQuizView(request):
    username = request.POST.get('username')
    print(username)
    id = request.POST.get('quizId')
    print(id)


def myprofile(request):
    return render(request, "myapp/myprofile.html")


def createquiz(request):
    return render(request, "myapp/createquiz.html")


def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['pass1']
        password2 = request.POST['pass2']
        if(password2==password):
            myuser = User.objects.create_user(username, email, password)
            myuser.save()
            messages.success(request, "Your account has been successfully created.")
            return redirect('home')
        else:
            messages.success(request, "Password are not the same")

    return render(request, "myapp/signup.html")





@login_required
@csrf_exempt
def addUserToQuizView(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quiz_id = data.get('quiz')
            username = data.get('user')

            quiz = Quiz.objects.get(pk=quiz_id)

            user = User.objects.get(username=username)

            quiz.user2 = user
            quiz.save()

            return JsonResponse({'status': 'success', 'message': 'Użytkownik został dodany do quizu.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Nieprawidłowe żądanie.'})


def signin(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['pass']

        user = authenticate(username=username, password=password)
        user.is_superuser = True
        if user is not None:
            login(request, user)
            return render(request, "myapp/account.html")
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')

    return render(request, "myapp/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out!")
    return render(request, "myapp/home.html")


@login_required
def account(request):
    return render(request, "myapp/account.html")


def back(request, quiz_id):
    return render(request, "myapp/account.html")


def my_quiz_page(request):
    # Pobierz wszystkie quizy z bazy danych
    quizzes = Quiz.objects.all().values('name', 'time', 'pk', 'number_of_question')

    quiz_list = list(quizzes)
    return JsonResponse(quiz_list, safe=False)


def quiz_details(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'myapp/solve_quiz.html', {'quiz': quiz})


def solve_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = []

    for q in quiz.get_questions():
        answer = []
        for a in q.get_answer():
            answer.append(a.text)
        questions.append({str(q): answer})

    return JsonResponse({
        'data': questions,
        'time': quiz.time
    })


@login_required
@csrf_exempt
def save_quiz(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            quiz_title = data.get('quiz-title')

            questions_data = data.get('questions')
            time = data.get('time')
            quiz = Quiz.objects.create(name=quiz_title, user=request.user, time=time)
            for question_data in questions_data:
                question_text = question_data.get('questionText')
                quiz.number_of_question += 1
                answers_data = question_data.get('answersData')

                question = Question.objects.create(text=question_text, quiz=quiz)
                for answer_data in answers_data:
                    answer_text = answer_data.get('answerText')
                    is_correct = answer_data.get('isCorrect')

                    Answer.objects.create(text=answer_text, correct=is_correct, question=question)

            quiz.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
@csrf_exempt
def update_quiz(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            quiz_title = data.get('quiz-title')
            print(quiz_title)
            time=data.get('time')
            questions_data = data.get('questions')

            print(questions_data)

            pk = data.get('quiz')
            print(pk)
            quiz_to_delete = Quiz.objects.get(id=pk)
            user1 = quiz_to_delete.user
            user2 = quiz_to_delete.user2
            quiz_to_delete.delete()

            quiz = Quiz.objects.create(name=quiz_title, user=user1,time=time,user2=user2)
            for question_data in questions_data:
                question_text = question_data.get('questionText')
                quiz.number_of_question += 1
                answers_data = question_data.get('answersData')

                question = Question.objects.create(text=question_text, quiz=quiz)
                for answer_data in answers_data:
                    answer_text = answer_data.get('answerText')
                    is_correct = answer_data.get('isCorrect')

                    Answer.objects.create(text=answer_text, correct=is_correct, question=question)

            quiz.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def save_quiz_view(request, quiz_id):
    if request.method == 'POST':
        csrf_token = request.POST.get('csrfmiddlewaretoken', None)
        selected_answers_str = request.POST.get('selectedAnswers', '{}')
        selected_answers = json.loads(selected_answers_str)
        question_list = []
        question_pk = []
        answer_list = []
        correct_answer_list = []
        processed_answers = {}

        for question, answer in selected_answers.items():
            processed_answers[question] = answer

        result_dict = {question: answer for question, answer in selected_answers.items()}

        for k in processed_answers.keys():
            questions = Question.objects.filter(text=k, quiz=quiz_id)
            question_list.extend(questions)
            for q in questions:
                answer = Answer.objects.filter(question=q, correct=True)
                correct_answer_list.extend(answer)

        print(correct_answer_list)

        for p in question_list:
            for a in processed_answers.values():

                answer = Answer.objects.filter(text=a, question=p)
                if a:
                    answer_list.extend(answer)
        print(answer_list)

        score = 0
        for c in answer_list:
            if c.correct:
                score += 1

        user = request.user
        quiz = Quiz.objects.get(pk=quiz_id)
        print(score)
        multi = 100 / quiz.number_of_question
        result = Result.objects.create(quiz=quiz, user=user, score=score * multi)
        print(result.quiz, result.user, result.score)

        return JsonResponse({
            'quiz_name': result.quiz.name,
            'username': result.user.username,
            'score': result.score,
        })


def get_results(request, quiz_id):
    result_id = request.GET.get('result_id')

    result = get_object_or_404(Result, id=result_id)

    result_data = {
        'quiz_name': result.quiz.name,
        'username': result.user.username,
        'score': result.score,
    }

    return JsonResponse({'results': result_data})


@login_required
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    answers = Answer.objects.filter(question__in=questions)

    return render(request, 'myapp/edit_quiz.html', {'quiz': quiz, 'questions': questions, 'answers': answers})


@login_required
def show_results(request, quiz_id):
    quiz = Quiz.objects.filter(Q(user=request.user) | Q(user2=request.user))
    results = Result.objects.filter(quiz=quiz_id)

    for r in results:
        print(r)
    # Dodaj kod do obsługi wyświetlania wyników
    return render(request, 'myapp/show_results.html', {'quiz': quiz, 'results': results})
