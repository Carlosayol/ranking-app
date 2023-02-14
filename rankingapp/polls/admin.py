from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fields = ["question_text"]
    inlines = [ChoiceInline]
    list_display = ("question_text", "created_at", "was_created_recently")
    list_filter = ["created_at"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
