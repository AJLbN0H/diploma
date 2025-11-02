from rest_framework import serializers

from tests.models import Test, Question, Answer, TestResult


class TestSerializer(serializers.ModelSerializer):
    """Serializer модели Test."""

    class Meta:
        model = Test
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer модели Question."""

    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer модели Answer."""

    class Meta:
        model = Answer
        fields = ("text", "question")


class TestResultSerializer(serializers.ModelSerializer):
    """Serializer модели TestResult."""

    test_name = serializers.CharField(source='test.name', read_only=True)
    material_name = serializers.CharField(source='test.material.name', read_only=True)

    class Meta:
        model = TestResult
        fields = [
            'id', 'test_name', 'material_name', 'score', 'total_questions',
            'correct_answers', 'percentage', 'is_passed', 'completed_at'
        ]


class SafeAnswerSerializer(serializers.ModelSerializer):
    """Serializer для безопасной передачи ответа без признака его правильности."""

    class Meta:
        model = Answer
        fields = ['id', 'text']


class SafeQuestionSerializer(serializers.ModelSerializer):
    """Serializer для вывода вопросов с безопасными ответами."""

    answers = SafeAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'name', 'text', 'question_type', 'answers']


class TestDetailSerializer(serializers.ModelSerializer):
    """Serializer для вывода детальной информации по тесту с безопасными вопросами."""

    questions = SafeQuestionSerializer(many=True, read_only=True)
    material_name = serializers.CharField(source='material.name', read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'passing_score', 'material_name', 'questions']


class AnswerSubmissionSerializer(serializers.Serializer):
    """Serializer для отправки ответов студента."""

    question_id = serializers.IntegerField()
    selected_answers = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )
    text_answer = serializers.CharField(required=False, allow_blank=True)


class TestSubmissionSerializer(serializers.Serializer):
    """Serializer для валидации списка ответов на вопросы."""

    answers = AnswerSubmissionSerializer(many=True)



