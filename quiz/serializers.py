
from quiz.models import Quiz, QuizTaker, Question, Choice, UsersAnswer
from rest_framework import serializers


class ChoiceSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	class Meta:
		model = Choice
		fields = ['id', 'choice', 'is_correct', 'question']
		read_only_fields = ['question',]


class QuestionSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	choices = ChoiceSerializer(many=True)

	class Meta:
		model = Question
		fields = ['id', 'question', 'choices', 'quiz']
		read_only_fields = ['quiz', ]

	''' explicitly creating/updating question within a existing quiz does not support yet.
	FIXME: Not sure if create method of Question will work as update as quiz
	instance is required here. Implimentation taking more time than expected, droping it.
	same can be done for Choices feild as well.
	May be will try with urls.
	'''

	# connenting out code for now.

	_ = '''
	def create(self, validated_data):
		choices = validated_data.pop('choices')
		quiz_instance = Quiz.objects.filter(id=1)
		question = Question.objects.create(**validated_data, quiz=quiz_instance)
		for choice in choices:
			Answer.objects.create(**choice, question=question)
		# question.tags.set(tags)
		return question

	def update(self, instance, validated_data):
		choices = validated_data.pop('choices')
		# quiz = validated_data.pop('quiz')
		instance.question = validated_data.get("question", instance.question)
		print(instance.question)
		instance.save()
		keep_choices = []
		for choice in choices:
			if "id" in choice.keys():
				if Answer.objects.filter(id=choice["id"]).exists():
					c = Choice.objects.get(id=choice["id"])
					c.text = choice.get('text', c.text)
					c.save()
					keep_choices.append(c.id)
				else:
					continue
			else:
				print(instance, "\n")
				c = Answer.objects.create(**choice, question=instance)
				keep_choices.append(c.id)

		for choice in instance.choices:
			if choice.id not in keep_choices:
				choice.delete()

		return instance
	'''


class QuizListSerializer(serializers.ModelSerializer):
	# update, create, delete, retrive. tested with postman. works fine.
	id = serializers.IntegerField(required=False)
	questions_count = serializers.SerializerMethodField()	
	questions = QuestionSerializer(many=True)

	class Meta:
		model = Quiz
		fields = ["id", "name", "description", "questions_count", "questions"]
		read_only_fields = ["questions_count", 'id',]
		# fields = "__all__"

	def get_questions_count(self, obj):
		return obj.question_set.all().count()

	def create(self, validated_data):
		choices = validated_data.pop('choices')
		questions = validated_data.pop('questions')
		quiz = Quiz.objects.create(**validated_data)
		for question in questions:
			for choice in choices:
				Choice.objects.create(**choice, question=question)
			Question.objects.create(**question, quiz=quiz)
		return quiz

	def update(self, instance, validated_data):
		questions = validated_data.pop('questions')
		instance.name = validated_data.get("name", instance.name)
		instance.save()
		keep_choices = []
		keep_questions = []
		for question in questions:
			choices = question.pop('choices')
			if "id" in question.keys():
				if Question.objects.filter(id=question['id']).exists():
					q = Question.objects.filter(id=question["id"])
					q.text = question.get('text', q.text)
					q.save()
					keep_questions.append(q.id)
				else:
					continue
			else:
				q = Question.objects.create(**question, quiz=instance)
				keep_questions.append(q.id)

			for choice in choices:
				if "id" in choice.keys():
					if Choice.objects.filter(id=choice["id"]).exists():
						c = Choice.objects.get(id=choice["id"])
						c.text = choice.get('text', c.text)
						c.save()
						keep_choices.append(c.id)
					else:
						continue
				else:
					c = Choice.objects.create(**choice, question=q)
					keep_choices.append(c.id)
			
			for choice in q.choices:
				if choice.id not in keep_choices:
					choice.delete()
		for question in questions:
			if question.get('id') not in keep_questions:
				dict(question).clear()

		return instance

class UsersAnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = UsersAnswer
		fields = "__all__"


class MyQuizListSerializer(serializers.ModelSerializer):
	completed = serializers.SerializerMethodField()
	progress = serializers.SerializerMethodField()
	questions_count = serializers.SerializerMethodField()
	score = serializers.SerializerMethodField()

	class Meta:
		model = Quiz
		fields = ["id", "name", "description", "questions_count", "completed", "score", "progress"]
		read_only_fields = ["questions_count", "completed", "progress"]

	def get_completed(self, obj):
		try:
			quiztaker = QuizTaker.objects.get(user=self.context['request'].user.id, quiz=obj)
			return quiztaker.completed
		except QuizTaker.DoesNotExist:
			return None

	def get_progress(self, obj):
		try:
			quiztaker = QuizTaker.objects.get(user=self.context['request'].user.id, quiz=obj)
			if quiztaker.completed == False:
				questions_answered = UsersAnswer.objects.filter(quiz_taker=quiztaker, answer__isnull=False).count()
				total_questions = obj.question_set.all().count()
				return int(questions_answered / total_questions)
			return None
		except QuizTaker.DoesNotExist:
			return None

	def get_questions_count(self, obj):
		return obj.question_set.all().count()

	def get_score(self, obj):
		try:
			quiztaker = QuizTaker.objects.get(user=self.context['request'].user.id, quiz=obj)
			if quiztaker.completed == True:
				return quiztaker.score
			return None
		except QuizTaker.DoesNotExist:
			return None


class QuizTakerSerializer(serializers.ModelSerializer):
	usersanswer_set = UsersAnswerSerializer(many=True)

	class Meta:
		model = QuizTaker
		fields = "__all__"


class QuizDetailSerializer(serializers.ModelSerializer):
	quiztakers_set = serializers.SerializerMethodField()
	question_set = QuestionSerializer(many=True)

	class Meta:
		model = Quiz
		fields = "__all__"

	def get_quiztakers_set(self, obj):
		try:
			quiz_taker = QuizTaker.objects.get(user=self.context['request'].user.id, quiz=obj)
			serializer = QuizTakerSerializer(quiz_taker)
			return serializer.data
		except QuizTaker.DoesNotExist:
			return None


class QuizResultSerializer(serializers.ModelSerializer):
	quiztaker_set = serializers.SerializerMethodField()
	question_set = QuestionSerializer(many=True)

	class Meta:
		model = Quiz
		fields = "__all__"

	def get_quiztaker_set(self, obj):
		try:
			quiztaker = QuizTaker.objects.get(user=self.context['request'].user.id, quiz=obj)
			serializer = QuizTakerSerializer(quiztaker)
			return serializer.data

		except QuizTaker.DoesNotExist:
			return None 