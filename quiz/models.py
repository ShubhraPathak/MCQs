
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class Quiz(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=70)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['timestamp',]
		verbose_name_plural = "Quizzes"

	def __str__(self):
		return self.name

	@property
	def questions(self):
		return self.question_set.all()

class Question(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	question = models.CharField(max_length=100)
	order = models.IntegerField(default=0)

	def __str__(self):
		return self.question

	@property
	def choices(self):
		return self.choice_set.all()

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice = models.CharField(max_length=100)
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return self.choice


class QuizTaker(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	score = models.IntegerField(default=0)
	completed = models.BooleanField(default=False)
	date_finished = models.DateTimeField(null=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.email


class UsersAnswer(models.Model):
	quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.question.question


@receiver(pre_save, sender=Quiz)
def slugify_name(sender, instance, *args, **kwargs):
	instance.slug = slugify(instance.name)


# class FeedBack(models.Model):
# 	"""docstring for  FeedBack"""
# 	name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Name")
# 	email = models.EmailField(max_length=120, blank=True, null=True, verbose_name="Email")
# 	message = models.TextField(max_length=5000, blank=True, null=True, verbose_name="Message")
# 	creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")

# 	class Meta:
# 		ordering = ['-creation_date']
# 		verbose_name_plural = "Feed Backs"

# 	def __str__(self):
# 		if self.name:
# 			return '{0} - {1}'.format(self.creation_date, self.name)
# 		elif self.email:
# 			return '{0} - {1}'.format(self.creation_date, self.email)
# 		return '{0}'.format(self.creation_date)
