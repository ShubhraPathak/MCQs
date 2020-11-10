from quiz.views import QuizListAPI, MyQuizListAPI, QuizDetailAPI, QuizQuestionViewAPI, QuizChoiceViewAPI
from rest_framework import routers
from rest_framework_extensions.routers import NestedRouterMixin

router = routers.DefaultRouter()
router.register('quizzes',QuizListAPI)
router.register('questions', QuizQuestionViewAPI)
router.register("quizlist", MyQuizListAPI) #

# localhost:p/api/employee/5
# GET, POST, PUT, DELETE
# list , retrive

class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
	pass

router = NestedDefaultRouter()

quiz_router = router.register('quizzes', QuizListAPI)
quiz_router.register('questions', QuizQuestionViewAPI,
		basename='quiz-questions',
		parents_query_lookups=['quiz']).register('answers',
		QuizChoiceViewAPI, basename='quiz-questions-answers',
		parents_query_lookups=['questions_quiz', 'questions'])