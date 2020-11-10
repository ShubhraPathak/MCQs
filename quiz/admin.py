from django.contrib import admin
import nested_admin
from .models import Quiz, Question, Choice


class ChoiceInLine(nested_admin.NestedTabularInline):
	model = Choice
	extra = 3
	max_choices_per_question = 3


class QuestionInLine(nested_admin.NestedTabularInline):
	model = Question
	inlines = [ChoiceInLine,]
	extra = 5
	max_question_per_quiz = 20


class QuizAdmin(nested_admin.NestedModelAdmin):
	inlines = [QuestionInLine,]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(Choice)
# admin.site.register(FeedBack)
