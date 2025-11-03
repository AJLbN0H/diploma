from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from tests.models import Test, Question, Answer, TestResult
from materials.models import Material
from tests.serializer import (
    TestSerializer,
    QuestionSerializer,
    AnswerSerializer,
    TestResultSerializer,
    SafeAnswerSerializer,
    SafeQuestionSerializer,
    TestDetailSerializer,
    AnswerSubmissionSerializer,
    TestSubmissionSerializer,
)
from tests.services import TestCalculateService

User = get_user_model()


class TestModelTestCase(APITestCase):
    """Тесты для модели Test."""

    def setUp(self):
        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()

        self.material = Material.objects.create(
            name="Test Material", description="Test Description", owner=self.user
        )
        self.test = Test.objects.create(
            name="Test Exam",
            description="Test Description",
            material=self.material,
            owner=self.user,
            passing_score=70,
        )

    def test_test_creation(self):
        """Тестирует корректное создание объекта Test."""

        self.assertEqual(self.test.name, "Test Exam")
        self.assertEqual(self.test.passing_score, 70)
        self.assertEqual(self.test.owner, self.user)

    def test_test_str_representation(self):
        """Тестирует строковое представление объекта Test."""

        expected_str = f"\nНазвание теста:Test Exam\nМинимальный бал для зачета: 70\n"
        self.assertEqual(str(self.test), expected_str)


class QuestionModelTestCase(APITestCase):
    """Тесты для модели Question."""

    def setUp(self):
        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()

        self.test = Test.objects.create(
            name="Test Exam", owner=self.user, passing_score=70
        )
        self.question = Question.objects.create(
            name="Test Question",
            text="What is Django?",
            test=self.test,
            question_type="single",
            owner=self.user,
        )

    def test_question_creation(self):
        """Тестирует корректное создание объекта Question."""

        self.assertEqual(self.question.name, "Test Question")
        self.assertEqual(self.question.question_type, "single")
        self.assertEqual(self.question.owner, self.user)


class AnswerModelTestCase(APITestCase):
    """Тесты для модели Answer."""

    def setUp(self):
        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()

        self.test = Test.objects.create(
            name="Test Exam", owner=self.user, passing_score=70
        )
        self.question = Question.objects.create(
            name="Test Question",
            text="What is Django?",
            test=self.test,
            owner=self.user,
        )
        self.answer = Answer.objects.create(
            text="A web framework", question=self.question, is_correct=True
        )

    def test_answer_creation(self):
        """Тестирует корректное создание объекта Answer."""

        self.assertEqual(self.answer.text, "A web framework")
        self.assertTrue(self.answer.is_correct)
        self.assertEqual(self.answer.question, self.question)


class TestResultModelTestCase(APITestCase):
    """Тесты для модели TestResult."""

    def setUp(self):
        self.student = User.objects.create(email="student@test.com", role="student")
        self.student.set_password("student123")
        self.student.save()

        self.teacher = User.objects.create(email="teacher@test.com", role="teacher")
        self.teacher.set_password("teacher123")
        self.teacher.save()

        self.test = Test.objects.create(
            name="Test Exam", owner=self.teacher, passing_score=70
        )
        self.test_result = TestResult.objects.create(
            student=self.student,
            test=self.test,
            score=80,
            total_questions=10,
            correct_answers=8,
            percentage=80.0,
            is_passed=True,
        )

    def test_test_result_creation(self):
        """Тестирует корректное создание объекта TestResult."""

        self.assertEqual(self.test_result.student, self.student)
        self.assertEqual(self.test_result.test, self.test)
        self.assertEqual(self.test_result.score, 80)
        self.assertEqual(self.test_result.total_questions, 10)
        self.assertEqual(self.test_result.correct_answers, 8)
        self.assertEqual(self.test_result.percentage, 80.0)
        self.assertTrue(self.test_result.is_passed)


class TestSerializerTestCase(APITestCase):
    """Тесты для TestSerializer."""

    def setUp(self):
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")

        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()
        self.user.groups.add(self.teacher_group)

        self.material = Material.objects.create(
            name="Test Material", description="Test Description", owner=self.user
        )

        self.test_data = {
            "name": "Serializer Test",
            "description": "Test Description",
            "passing_score": 70,
            "material": self.material.id,
            "owner": self.user.id,
        }

    def test_test_serializer_valid_data(self):
        """Тестирует валидацию TestSerializer с корректными данными."""

        serializer = TestSerializer(data=self.test_data)
        self.assertTrue(serializer.is_valid())

    def test_test_serializer_invalid_data(self):
        """Тестирует валидацию TestSerializer с некорректными данными."""

        invalid_data = self.test_data.copy()
        invalid_data["passing_score"] = -5  # Невалидный балл
        serializer = TestSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("passing_score", serializer.errors)

    def test_test_serializer_create(self):
        """Тестирует создание объекта Test через сериализатор."""

        serializer = TestSerializer(data=self.test_data)
        self.assertTrue(serializer.is_valid())
        test = serializer.save()
        self.assertEqual(test.name, "Serializer Test")
        self.assertEqual(test.owner, self.user)


class QuestionSerializerTestCase(APITestCase):
    """Тесты для QuestionSerializer."""

    def setUp(self):
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")

        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()
        self.user.groups.add(self.teacher_group)

        self.test = Test.objects.create(
            name="Test Exam", owner=self.user, passing_score=70
        )

        self.question_data = {
            "name": "Serializer Question",
            "text": "Question text",
            "test": self.test.id,
            "question_type": "single",
            "owner": self.user.id,
        }

    def test_question_serializer_valid_data(self):
        """Тестирует валидацию QuestionSerializer с корректными данными."""

        serializer = QuestionSerializer(data=self.question_data)
        self.assertTrue(serializer.is_valid())

    def test_question_serializer_invalid_question_type(self):
        """Тестирует валидацию QuestionSerializer с некорректным типом вопроса."""

        invalid_data = self.question_data.copy()
        invalid_data["question_type"] = "invalid_type"
        serializer = QuestionSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("question_type", serializer.errors)

    def test_question_serializer_create(self):
        """Тестирует создание объекта Question через сериализатор."""

        serializer = QuestionSerializer(data=self.question_data)
        self.assertTrue(serializer.is_valid())
        question = serializer.save()
        self.assertEqual(question.name, "Serializer Question")
        self.assertEqual(question.question_type, "single")


class AnswerSerializerTestCase(APITestCase):
    """Тесты для AnswerSerializer."""

    def setUp(self):
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")

        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()
        self.user.groups.add(self.teacher_group)

        self.test = Test.objects.create(
            name="Test Exam", owner=self.user, passing_score=70
        )

        self.question = Question.objects.create(
            name="Test Question", text="Question text", test=self.test, owner=self.user
        )

        self.answer_data = {
            "text": "Serializer Answer",
            "question": self.question.id,
            "is_correct": True,
        }

    def test_answer_serializer_valid_data(self):
        """Тестирует валидацию AnswerSerializer с корректными данными."""

        serializer = AnswerSerializer(data=self.answer_data)
        self.assertTrue(serializer.is_valid())

    def test_answer_serializer_create(self):
        """Тестирует создание объекта Answer через сериализатор."""

        serializer = AnswerSerializer(data=self.answer_data)
        self.assertTrue(serializer.is_valid())
        answer = serializer.save()
        self.assertEqual(answer.text, "Serializer Answer")
        self.assertTrue(answer.is_correct)


class TestResultSerializerTestCase(APITestCase):
    """Тесты для TestResultSerializer."""

    def setUp(self):
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")
        self.student_group, _ = Group.objects.get_or_create(name="Студенты")

        self.student = User.objects.create(email="student@test.com", role="student")
        self.student.set_password("student123")
        self.student.save()
        self.student.groups.add(self.student_group)

        self.teacher = User.objects.create(email="teacher@test.com", role="teacher")
        self.teacher.set_password("teacher123")
        self.teacher.save()
        self.teacher.groups.add(self.teacher_group)

        self.test = Test.objects.create(
            name="Test Exam", owner=self.teacher, passing_score=70
        )

        self.test_result = TestResult.objects.create(
            student=self.student,
            test=self.test,
            score=80,
            total_questions=10,
            correct_answers=8,
            percentage=80.0,
            is_passed=True,
        )

        self.test_result_data = {
            "student": self.student.id,
            "test": self.test.id,
            "score": 85,
            "total_questions": 10,
            "correct_answers": 9,
            "percentage": 85.0,
            "is_passed": True,
        }

    def test_test_result_serializer_valid_data(self):
        """Тестирует валидацию TestResultSerializer с корректными данными."""

        serializer = TestResultSerializer(data=self.test_result_data)
        self.assertTrue(serializer.is_valid())

    def test_test_result_serializer_read_only_fields(self):
        """Тестирует, что test_name является read_only полем."""

        serializer = TestResultSerializer(self.test_result)
        self.assertIn("test_name", serializer.data)
        self.assertEqual(serializer.data["test_name"], "Test Exam")


class SafeAnswerSerializerTestCase(APITestCase):
    """Тесты для SafeAnswerSerializer."""

    def setUp(self):
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")

        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()
        self.user.groups.add(self.teacher_group)

        self.test = Test.objects.create(
            name="Test Exam", owner=self.user, passing_score=70
        )

        self.question = Question.objects.create(
            name="Test Question", text="Question text", test=self.test, owner=self.user
        )

        self.answer = Answer.objects.create(
            text="Safe answer", question=self.question, is_correct=True
        )

    def test_safe_answer_serializer_hides_is_correct(self):
        """Тестирует, что SafeAnswerSerializer скрывает поле is_correct."""

        serializer = SafeAnswerSerializer(self.answer)
        data = serializer.data

        self.assertIn("id", data)
        self.assertIn("text", data)
        self.assertEqual(data["text"], "Safe answer")

        self.assertNotIn("is_correct", data)


class SafeQuestionSerializerTestCase(APITestCase):
    """Тесты для SafeQuestionSerializer."""

    def setUp(self):
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")

        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()
        self.user.groups.add(self.teacher_group)

        self.test = Test.objects.create(
            name="Test Exam", owner=self.user, passing_score=70
        )

        self.question = Question.objects.create(
            name="Safe Question",
            text="Question text",
            test=self.test,
            question_type="single",
            owner=self.user,
        )

        self.answer1 = Answer.objects.create(
            text="Answer 1", question=self.question, is_correct=True
        )
        self.answer2 = Answer.objects.create(
            text="Answer 2", question=self.question, is_correct=False
        )

    def test_safe_question_serializer_includes_safe_answers(self):
        """Тестирует, что SafeQuestionSerializer включает безопасные ответы."""

        serializer = SafeQuestionSerializer(self.question)
        data = serializer.data

        self.assertIn("id", data)
        self.assertIn("name", data)
        self.assertIn("text", data)
        self.assertIn("question_type", data)
        self.assertIn("answers", data)

        self.assertEqual(len(data["answers"]), 2)

        for answer in data["answers"]:
            self.assertIn("id", answer)
            self.assertIn("text", answer)
            self.assertNotIn("is_correct", answer)


class TestDetailSerializerTestCase(APITestCase):
    """Тесты для TestDetailSerializer."""

    def setUp(self):
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")

        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()
        self.user.groups.add(self.teacher_group)

        self.material = Material.objects.create(
            name="Test Material", description="Test Description", owner=self.user
        )

        self.test = Test.objects.create(
            name="Detail Test",
            description="Test Description",
            material=self.material,
            owner=self.user,
            passing_score=70,
        )

        self.question1 = Question.objects.create(
            name="Question 1",
            text="First question",
            test=self.test,
            question_type="single",
            owner=self.user,
        )

        self.question2 = Question.objects.create(
            name="Question 2",
            text="Second question",
            test=self.test,
            question_type="multiple",
            owner=self.user,
        )

        self.answer1 = Answer.objects.create(
            text="Answer 1-1", question=self.question1, is_correct=True
        )
        self.answer2 = Answer.objects.create(
            text="Answer 1-2", question=self.question1, is_correct=False
        )

    def test_test_detail_serializer_includes_material_name(self):
        """Тестирует, что TestDetailSerializer включает название материала."""

        serializer = TestDetailSerializer(self.test)
        data = serializer.data

        self.assertIn("material_name", data)
        self.assertEqual(data["material_name"], "Test Material")

    def test_test_detail_serializer_includes_safe_questions(self):
        """Тестирует, что TestDetailSerializer включает безопасные вопросы."""

        serializer = TestDetailSerializer(self.test)
        data = serializer.data

        self.assertIn("questions", data)
        self.assertEqual(len(data["questions"]), 2)

        for question in data["questions"]:
            self.assertIn("answers", question)
            for answer in question["answers"]:
                self.assertNotIn("is_correct", answer)


class AnswerSubmissionSerializerTestCase(APITestCase):
    """Тесты для AnswerSubmissionSerializer."""

    def test_answer_submission_serializer_single_choice(self):
        """Тестирует валидацию AnswerSubmissionSerializer для одиночного выбора."""

        data = {"question_id": 1, "selected_answers": [1]}
        serializer = AnswerSubmissionSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_answer_submission_serializer_multiple_choice(self):
        """Тестирует валидацию AnswerSubmissionSerializer для множественного выбора."""

        data = {"question_id": 1, "selected_answers": [1, 2, 3]}
        serializer = AnswerSubmissionSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_answer_submission_serializer_text_answer(self):
        """Тестирует валидацию AnswerSubmissionSerializer для текстового ответа."""

        data = {"question_id": 1, "text_answer": "Text response"}
        serializer = AnswerSubmissionSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_answer_submission_serializer_empty_selected_answers(self):
        """Тестирует валидацию AnswerSubmissionSerializer с пустым selected_answers."""

        data = {"question_id": 1, "selected_answers": []}
        serializer = AnswerSubmissionSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_answer_submission_serializer_missing_fields(self):
        """Тестирует валидацию AnswerSubmissionSerializer с отсутствующими полями."""

        data = {"question_id": 1}
        serializer = AnswerSubmissionSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class TestSubmissionSerializerTestCase(APITestCase):
    """Тесты для TestSubmissionSerializer."""

    def test_test_submission_serializer_valid_data(self):
        """Тестирует валидацию TestSubmissionSerializer с корректными данными."""

        data = {
            "answers": [
                {"question_id": 1, "selected_answers": [1, 2]},
                {"question_id": 2, "text_answer": "Text response"},
            ]
        }
        serializer = TestSubmissionSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_test_submission_serializer_empty_answers(self):
        """Тестирует валидацию TestSubmissionSerializer с пустым списком ответов."""

        data = {"answers": []}
        serializer = TestSubmissionSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_test_submission_serializer_missing_answers(self):
        """Тестирует валидацию TestSubmissionSerializer без поля answers."""

        data = {}
        serializer = TestSubmissionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("answers", serializer.errors)

    def test_test_submission_serializer_invalid_answers(self):
        """Тестирует валидацию TestSubmissionSerializer с невалидными ответами."""

        data = {
            "answers": [{"question_id": "invalid_id", "selected_answers": "not_a_list"}]
        }
        serializer = TestSubmissionSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class TestCalculateServiceTestCase(APITestCase):
    """Тесты для сервиса подсчета результатов TestCalculateService."""

    def setUp(self):
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")

        self.teacher = User.objects.create(email="teacher@test.com", role="teacher")
        self.teacher.set_password("teacher123")
        self.teacher.save()
        self.teacher.groups.add(self.teacher_group)

        self.student = User.objects.create(email="student@test.com", role="student")
        self.student.set_password("student123")
        self.student.save()

        self.test = Test.objects.create(
            name="Calculation Test", owner=self.teacher, passing_score=50
        )

        self.single_question = Question.objects.create(
            name="Single Choice",
            text="Select correct answer",
            test=self.test,
            question_type="single",
            owner=self.teacher,
        )
        self.correct_single_answer = Answer.objects.create(
            text="Correct", question=self.single_question, is_correct=True
        )
        self.wrong_single_answer = Answer.objects.create(
            text="Wrong", question=self.single_question, is_correct=False
        )

        self.multiple_question = Question.objects.create(
            name="Multiple Choice",
            text="Select all correct answers",
            test=self.test,
            question_type="multiple",
            owner=self.teacher,
        )
        self.correct_multiple_answer1 = Answer.objects.create(
            text="Correct 1", question=self.multiple_question, is_correct=True
        )
        self.correct_multiple_answer2 = Answer.objects.create(
            text="Correct 2", question=self.multiple_question, is_correct=True
        )
        self.wrong_multiple_answer = Answer.objects.create(
            text="Wrong", question=self.multiple_question, is_correct=False
        )

        self.text_question = Question.objects.create(
            name="Text Question",
            text="Write the answer",
            test=self.test,
            question_type="text",
            owner=self.teacher,
        )
        self.correct_text_answer = Answer.objects.create(
            text="correct answer", question=self.text_question, is_correct=True
        )

    def test_calculate_results_all_correct(self):
        """Тестирует подсчет результатов когда все ответы правильные."""

        submitted_answers = [
            {
                "question_id": self.single_question.id,
                "selected_answers": [self.correct_single_answer.id],
            },
            {
                "question_id": self.multiple_question.id,
                "selected_answers": [
                    self.correct_multiple_answer1.id,
                    self.correct_multiple_answer2.id,
                ],
            },
            {"question_id": self.text_question.id, "text_answer": "correct answer"},
        ]

        results = TestCalculateService.calculate_results(
            self, self.test, submitted_answers
        )

        self.assertEqual(results["score"], 3)
        self.assertEqual(results["total_questions"], 3)
        self.assertEqual(results["correct_answers"], 3)
        self.assertEqual(results["percentage"], 100.0)
        self.assertTrue(results["is_passed"])

    def test_calculate_results_partial_correct(self):
        """Тестирует подсчет результатов когда часть ответов правильные."""

        submitted_answers = [
            {
                "question_id": self.single_question.id,
                "selected_answers": [self.correct_single_answer.id],
            },
            {
                "question_id": self.multiple_question.id,
                "selected_answers": [self.correct_multiple_answer1.id],
            },
            {"question_id": self.text_question.id, "text_answer": "wrong answer"},
        ]

        results = TestCalculateService.calculate_results(
            self, self.test, submitted_answers
        )

        self.assertEqual(results["score"], 1)
        self.assertEqual(results["total_questions"], 3)
        self.assertEqual(results["correct_answers"], 1)
        self.assertAlmostEqual(results["percentage"], 33.33, places=2)
        self.assertFalse(results["is_passed"])

    def test_check_single_choice_correct(self):
        """Тестирует проверку правильного ответа на вопрос с одиночным выбором."""

        student_answer = {"selected_answers": [self.correct_single_answer.id]}
        result = TestCalculateService._check_single_choice(
            self.single_question, student_answer
        )
        self.assertTrue(result)

    def test_check_single_choice_wrong(self):
        """Тестирует проверку неправильного ответа на вопрос с одиночным выбором."""

        student_answer = {"selected_answers": [self.wrong_single_answer.id]}
        result = TestCalculateService._check_single_choice(
            self.single_question, student_answer
        )
        self.assertFalse(result)

    def test_check_multiple_choice_correct(self):
        """Тестирует проверку правильного ответа на вопрос с множественным выбором."""

        student_answer = {
            "selected_answers": [
                self.correct_multiple_answer1.id,
                self.correct_multiple_answer2.id,
            ]
        }
        result = TestCalculateService._check_multiple_choice(
            self.multiple_question, student_answer
        )
        self.assertTrue(result)

    def test_check_text_answer_correct(self):
        """Тестирует проверку правильного текстового ответа."""

        student_answer = {"text_answer": "CORRECT ANSWER"}
        result = TestCalculateService._check_text_answer(
            self.text_question, student_answer
        )
        self.assertTrue(result)


class TestViewSetTestCase(APITestCase):
    """Тесты для ViewSet модели Test."""

    def setUp(self):
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")
        self.student_group, _ = Group.objects.get_or_create(name="Студенты")
        self.admin_group, _ = Group.objects.get_or_create(name="Администраторы")

        self.teacher_user = User.objects.create(
            email="teacher@test.com", role="teacher"
        )
        self.teacher_user.set_password("teacher123")
        self.teacher_user.save()
        self.teacher_user.groups.add(self.teacher_group)

        self.student_user = User.objects.create(
            email="student@test.com", role="student"
        )
        self.student_user.set_password("student123")
        self.student_user.save()
        self.student_user.groups.add(self.student_group)

        self.admin_user = User.objects.create(email="admin@test.com", role="admin")
        self.admin_user.set_password("admin123")
        self.admin_user.save()
        self.admin_user.groups.add(self.admin_group)

        self.material = Material.objects.create(
            name="Test Material",
            description="Test Description",
            owner=self.teacher_user,
        )

        self.test_data = {
            "name": "API Test",
            "description": "Test Description",
            "passing_score": 70,
            "material": self.material.id,
        }

        self.test = Test.objects.create(
            name="Existing Test",
            description="Existing Description",
            material=self.material,
            owner=self.teacher_user,
            passing_score=60,
        )

    def test_create_test_as_teacher(self):
        """Тестирует создание теста преподавателем HTTP_201_CREATED."""

        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.post(reverse("tests:test-list"), self.test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Test.objects.count(), 2)

    def test_create_test_as_student_should_fail(self):
        """Тестирует попытку создания теста студентом HTTP_403_FORBIDDEN."""

        self.client.force_authenticate(user=self.student_user)
        response = self.client.post(reverse("tests:test-list"), self.test_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_tests_as_teacher(self):
        """Тестирует получение списка тестов преподавателем HTTP_200_OK."""

        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(reverse("tests:test-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_test_detail(self):
        """Тестирует получение детальной информации о тесте HTTP_200_OK."""

        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(
            reverse("tests:test_detail", kwargs={"pk": self.test.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSubmitViewTestCase(APITestCase):
    """Тесты для представления отправки ответов на тест."""

    def setUp(self):
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")
        self.student_group, _ = Group.objects.get_or_create(name="Студенты")

        self.student_user = User.objects.create(
            email="student@test.com", role="student"
        )
        self.student_user.set_password("student123")
        self.student_user.save()
        self.student_user.groups.add(self.student_group)

        self.teacher_user = User.objects.create(
            email="teacher@test.com", role="teacher"
        )
        self.teacher_user.set_password("teacher123")
        self.teacher_user.save()
        self.teacher_user.groups.add(self.teacher_group)

        self.material = Material.objects.create(
            name="Test Material",
            description="Test Description",
            owner=self.teacher_user,
        )

        self.test = Test.objects.create(
            name="Submission Test",
            owner=self.teacher_user,
            passing_score=50,
            material=self.material,
        )

        self.question = Question.objects.create(
            name="Test Question",
            text="Question text",
            test=self.test,
            question_type="single",
            owner=self.teacher_user,
        )

        self.correct_answer = Answer.objects.create(
            text="Correct", question=self.question, is_correct=True
        )

        self.submission_data = {
            "answers": [
                {
                    "question_id": self.question.id,
                    "selected_answers": [self.correct_answer.id],
                }
            ]
        }

    def test_test_submission(self):
        """Тестирует успешную отправку ответов на тест студентом HTTP_201_CREATED."""

        self.client.force_authenticate(user=self.student_user)
        response = self.client.post(
            reverse("tests:test_submit", kwargs={"test_id": self.test.id}),
            self.submission_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TestResult.objects.filter(student=self.student_user).exists())

    def test_test_submission_unauthenticated(self):
        """Тестирует попытку отправки теста без аутентификации HTTP_401_UNAUTHORIZED."""

        response = self.client.post(
            reverse("tests:test_submit", kwargs={"test_id": self.test.id}),
            self.submission_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestResultViewTestCase(APITestCase):
    """Тесты для представлений работы с результатами тестов."""

    def setUp(self):
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")
        self.student_group, _ = Group.objects.get_or_create(name="Студенты")

        self.student_user = User.objects.create(
            email="student@test.com", role="student"
        )
        self.student_user.set_password("student123")
        self.student_user.save()
        self.student_user.groups.add(self.student_group)

        self.teacher_user = User.objects.create(
            email="teacher@test.com", role="teacher"
        )
        self.teacher_user.set_password("teacher123")
        self.teacher_user.save()
        self.teacher_user.groups.add(self.teacher_group)

        self.material = Material.objects.create(
            name="Test Material",
            description="Test Description",
            owner=self.teacher_user,
        )

        self.test = Test.objects.create(
            name="Result Test",
            owner=self.teacher_user,
            passing_score=50,
            material=self.material,
        )

        self.test_result = TestResult.objects.create(
            student=self.student_user,
            test=self.test,
            score=80,
            total_questions=10,
            correct_answers=8,
            percentage=80.0,
            is_passed=True,
        )

    def test_list_results_as_student(self):
        """Тестирует получение списка результатов тестов студентом HTTP_200_OK."""

        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(reverse("tests:test_results"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_own_result(self):
        """Тестирует получение детальной информации о своем результате теста HTTP_200_OK."""

        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(
            reverse("tests:test_result_detail", kwargs={"pk": self.test_result.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
