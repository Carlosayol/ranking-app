from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("You are now in the main page")


def detail(request, question_id):
    return HttpResponse(f"You are now looking at the question #{question_id}")


def results(request, question_id):
    return HttpResponse(f"You are now looking at the results of the question #{question_id}")


def vote(request, question_id):
    return HttpResponse(f"You are now voting for the question #{question_id}")
