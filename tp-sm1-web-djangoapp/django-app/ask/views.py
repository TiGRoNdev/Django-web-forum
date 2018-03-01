from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.http import HttpResponseRedirect, QueryDict
from django.contrib.auth import login as log_in
from django.contrib.auth import logout
from django import forms
from ask.models import *
from ask.paginator import paginate
from ask.forms import AskForm, AnswerForm, LoginForm, SignUpForm


@require_GET
def signout(request):
    if request.user is not None:
        logout(request)
    return HttpResponseRedirect('/')


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            log_in(request, user)
            return HttpResponseRedirect("/")
    else:
        form = LoginForm()
    return render(request, 'ask/login.html', {'form': form, 'username': request.user.username})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            log_in(request, user)
            return HttpResponseRedirect("/")
    else:
        form = SignUpForm()
    return render(request, 'ask/signup.html', {'form': form, 'username': request.user.username})


def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if request.user.is_anonymous:
            form.add_error("author", forms.ValidationError("You must be an authenticated user, please Sign In or Register"))
        else:
            if form.is_valid():
                ask = form.save(user=request.user)
                url = ask.get_absolute_url()
                return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask/ask.html', {'form': form, 'username': request.user.username})


def question(request, question_number):
    question = get_object_or_404(Question, id=question_number)
    since = request.GET.get('since')
    answers, since = Answer.objects.main(since, question)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            if request.user.is_anonymous:
                answer = form.save(question_id=question_number)
            else:
                answer = form.save(user=request.user, question_id=question_number)
            question = answer.question
            return HttpResponseRedirect("/question/{}/".format(question.id))
    else:
        form = AnswerForm()
    return render(request, 'ask/question.html',
                  {
                      'answers': answers,
                      'question': question,
                      'since': since,
                      'form': form,
                      'username': request.user.username
                  })


@require_GET
def popular(request):
    questions = Question.objects.popular()
    tags = Tag.objects.popular()
    page = paginate(request, questions)
    return render(request, 'ask/popular.html',
                  {
                      'questions': page.object_list,
                      'tags': tags,
                      'page': page,
                      'username': request.user.username
                  })


@require_GET
def home(request):
    questions = Question.objects.new()
    tags = Tag.objects.popular()
    page = paginate(request, questions)
    return render(request, 'ask/home.html',
                  {
                      'questions': page.object_list,
                      'tags': tags,
                      'page': page,
                      'username': request.user.username
                  })


@require_GET
def questions_by_tag(request):
    tag_id = request.GET.get('tag')
    questions = Question.objects.get_by_tag(tag_id)
    tags = Tag.objects.popular()
    page = paginate(request, questions)
    return render(request, 'ask/home.html',
                  {
                      'questions': page.object_list,
                      'tags': tags,
                      'page': page,
                      'username': request.user.username
                  })
