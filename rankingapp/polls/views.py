from django.http import HttpResponse
from django.shortcuts import render

from .models import Question


def index(request):
    latest_question_list = Question.objects.all()
    return render(request, "polls/index.html", {
        "latest_question_list": latest_question_list
    })


def detail(request, question_id):
    return HttpResponse(f"You are now looking at the question #{question_id}")


def results(request, question_id):
    return HttpResponse(f"You are now looking at the results of the question #{question_id}")


def vote(request, question_id):
    return HttpResponse(f"You are now voting for the question #{question_id}")
