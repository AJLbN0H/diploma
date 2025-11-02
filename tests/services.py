from tests.models import Answer


class TestCalculateService:
    """Сервис для подсчета результатов"""

    @staticmethod
    def calculate_results(self, test, submitted_answers):
        """Логика подсчета результатов теста."""
        questions = test.questions.all()
        total_questions = questions.count()
        correct_answers_count = 0

        for question in questions:
            student_answer = next(
                (
                    answer
                    for answer in submitted_answers
                    if answer["question_id"] == question.id
                ),
                None,
            )

            if student_answer and TestCalculateService._check_answer_correctness(
                question, student_answer
            ):
                correct_answers_count += 1

        percentage = (
            (correct_answers_count / total_questions) * 100
            if total_questions > 0
            else 0
        )
        is_passed = percentage >= test.passing_score

        return {
            "score": correct_answers_count,
            "total_questions": total_questions,
            "correct_answers": correct_answers_count,
            "percentage": round(percentage, 2),
            "is_passed": is_passed,
        }

    @staticmethod
    def _check_answer_correctness(question, student_answer):
        """Проверка правильности ответа на вопрос."""

        if not student_answer:
            return False

        if question.question_type == "single":
            return TestCalculateService._check_single_choice(question, student_answer)
        elif question.question_type == "multiple":
            return TestCalculateService._check_multiple_choice(question, student_answer)
        elif question.question_type == "text":
            return TestCalculateService._check_text_answer(question, student_answer)

        return False

    @staticmethod
    def _check_single_choice(question, student_answer):
        """Проверка одиночного выбора."""

        selected_answers = student_answer.get("selected_answers", [])
        if len(selected_answers) != 1:
            return False

        try:
            selected_answer = Answer.objects.get(
                id=selected_answers[0], question=question
            )
            return selected_answer.is_correct
        except Answer.DoesNotExist:
            return False

    @staticmethod
    def _check_multiple_choice(question, student_answer):
        """Проверка множественного выбора."""

        selected_answers = set(student_answer.get("selected_answers", []))
        if not selected_answers:
            return False

        correct_answers = set(
            question.answers.filter(is_correct=True).values_list("id", flat=True)
        )

        return correct_answers == selected_answers

    @staticmethod
    def _check_text_answer(question, student_answer):
        """Проверка текстового ответа."""

        text_answer = student_answer.get("text_answer", "").strip().lower()
        if not text_answer:
            return False

        correct_texts = [
            answer.text.strip().lower()
            for answer in question.answers.filter(is_correct=True)
        ]

        return text_answer in correct_texts
