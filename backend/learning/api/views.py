import random

from django.core.paginator import EmptyPage, Paginator
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.models import HSKLevel, Vocabulary
from learning.quiz import generate_question
from learning.quiz.validators import (
    validate_quiz_type,
    validate_vocabulary,
)

from .serializers import (
    HSKLevelSerializer,
    QuizAnswerSerializer,
    QuizBatchAnswerSerializer,
    QuizQuestionSerializer,
    StudyWordSerializer,
)


def get_question_data(vocabulary, quiz_type):
    """Generate a question and return its public response data."""
    validate_vocabulary(vocabulary, quiz_type)
    question = generate_question(vocabulary, quiz_type)

    # Never send the correct answer in the question response.
    if (
        len(question.options) != 4
        or len(set(question.options)) != 4
        or question.correct_answer not in question.options
    ):
        return None

    return {
        "id": question.id,
        "quiz_type": question.quiz_type.value,
        "vocabulary_id": question.vocabulary_id,
        "prompt": question.prompt,
        "options": question.options,
    }


def choose_question(vocabulary_queryset, quiz_type):
    """Try several vocabulary items until a valid question is generated."""
    candidate_ids = list(
        vocabulary_queryset.values_list("id", flat=True)
    )

    if not candidate_ids:
        return None

    random.shuffle(candidate_ids)

    for vocabulary_id in candidate_ids[:20]:
        vocabulary = vocabulary_queryset.model.objects.get(
            pk=vocabulary_id
        )

        try:
            data = get_question_data(vocabulary, quiz_type)
        except ValueError:
            continue

        if data is not None:
            return data

    return None


class HSKLevelListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        levels = HSKLevel.objects.all()
        data = [
            {
                "id": level.id,
                "name": level.name,
                "order": level.order,
                "description": level.description,
            }
            for level in levels
        ]

        serializer = HSKLevelSerializer(data, many=True)
        return Response(serializer.data)


class StudyWordListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            level_order = int(
                request.query_params.get("hsk_level", "1")
            )
            page_number = int(
                request.query_params.get("page", "1")
            )
            page_size = int(
                request.query_params.get("page_size", "50")
            )
        except (TypeError, ValueError):
            return Response(
                {"detail": "Invalid pagination or HSK level value."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not 1 <= level_order <= 7:
            return Response(
                {"detail": "HSK level must be between 1 and 7."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if page_number < 1:
            return Response(
                {"detail": "Page number must be at least 1."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not 1 <= page_size <= 50:
            return Response(
                {"detail": "Page size must be between 1 and 50."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            level = HSKLevel.objects.get(order=level_order)
        except HSKLevel.DoesNotExist:
            return Response(
                {"detail": "HSK level not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        words = Vocabulary.objects.filter(
            hsk_level=level
        ).order_by("frequency", "simplified")

        paginator = Paginator(words, page_size)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            return Response(
                {"detail": "Page not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = [
            {
                "id": word.id,
                "simplified": word.simplified,
                "pinyin": word.pinyin,
                "meaning": word.meanings[0] if word.meanings else "",
            }
            for word in page.object_list
        ]

        serializer = StudyWordSerializer(data, many=True)

        return Response({
            "count": paginator.count,
            "page": page.number,
            "page_size": page_size,
            "total_pages": paginator.num_pages,
            "next_page": (
                page.next_page_number() if page.has_next() else None
            ),
            "previous_page": (
                page.previous_page_number()
                if page.has_previous()
                else None
            ),
            "results": serializer.data,
        })


class QuizQuestionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        level, quiz_type, error = get_quiz_parameters(request)

        if error:
            return error

        data = choose_question(
            Vocabulary.objects.filter(hsk_level=level),
            quiz_type,
        )

        if data is None:
            return Response(
                {"detail": "Could not generate a valid question."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(data)


class QuizQuestionListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        level, quiz_type, error = get_quiz_parameters(request)

        if error:
            return error

        queryset = Vocabulary.objects.filter(hsk_level=level)
        candidate_ids = list(queryset.values_list("id", flat=True))

        if not candidate_ids:
            return Response(
                {"detail": "No vocabulary is available for this level."},
                status=status.HTTP_404_NOT_FOUND,
            )

        questions = []
        selected_ids = set()

        # Avoid repeating words where possible.
        random.shuffle(candidate_ids)

        for vocabulary_id in candidate_ids:
            if len(questions) == 10:
                break

            vocabulary = Vocabulary.objects.get(pk=vocabulary_id)

            try:
                data = get_question_data(vocabulary, quiz_type)
            except ValueError:
                continue

            if data is None:
                continue

            if vocabulary_id in selected_ids:
                continue

            questions.append(data)
            selected_ids.add(vocabulary_id)

        if len(questions) < 10:
            return Response(
                {
                    "detail": (
                        "Not enough valid questions are available "
                        "to build a 10-question quiz."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({"questions": questions})


class QuizAnswerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = QuizAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question_id = serializer.validated_data["question_id"]
        answer = serializer.validated_data["answer"]

        try:
            vocabulary_id_text, quiz_type_value = question_id.split("-", 1)
            vocabulary_id = int(vocabulary_id_text)
            quiz_type = validate_quiz_type(quiz_type_value)
        except (ValueError, TypeError):
            return Response(
                {"detail": "Invalid question ID or quiz type."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            vocabulary = Vocabulary.objects.get(pk=vocabulary_id)
        except Vocabulary.DoesNotExist:
            return Response(
                {"detail": "Question not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            validate_vocabulary(vocabulary, quiz_type)
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        correct_answer = get_correct_answer(vocabulary, quiz_type)

        return Response({
            "question_id": question_id,
            "correct": answer == correct_answer,
            "correct_answer": correct_answer,
        })


def get_quiz_parameters(request):
    """Validate the requested HSK level and quiz type."""
    try:
        level_order = int(
            request.query_params.get("hsk_level", "1")
        )
    except (TypeError, ValueError):
        return None, None, Response(
            {"detail": "Invalid HSK level."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not 1 <= level_order <= 7:
        return None, None, Response(
            {"detail": "HSK level must be between 1 and 7."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        level = HSKLevel.objects.get(order=level_order)
    except HSKLevel.DoesNotExist:
        return None, None, Response(
            {"detail": "HSK level not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        quiz_type = validate_quiz_type(
            request.query_params.get(
                "quiz_type",
                "hanzi_to_meaning",
            )
        )
    except ValueError as exc:
        return None, None, Response(
            {"detail": str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return level, quiz_type, None


def get_correct_answer(vocabulary, quiz_type):
    """Return the correct answer without regenerating random options."""
    from learning.quiz import QuizType

    if quiz_type == QuizType.HANZI_TO_MEANING:
        return vocabulary.meanings[0]

    if quiz_type == QuizType.MEANING_TO_HANZI:
        return vocabulary.simplified

    if quiz_type == QuizType.HANZI_TO_PINYIN:
        return vocabulary.pinyin

    if quiz_type == QuizType.PINYIN_TO_HANZI:
        return vocabulary.simplified

    raise ValueError(f"Unsupported quiz type: {quiz_type}")




class QuizBatchAnswerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = QuizBatchAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submitted_answers = serializer.validated_data["answers"]

        # Keep batch requests within a reasonable size.
        if len(submitted_answers) > 50:
            return Response(
                {"detail": "A maximum of 50 answers is allowed per request."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Reject duplicate question IDs in the same submission.
        question_ids = [
            item["question_id"] for item in submitted_answers
        ]

        if len(question_ids) != len(set(question_ids)):
            return Response(
                {"detail": "Duplicate question IDs are not allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results = []

        for item in submitted_answers:
            question_id = item["question_id"]
            answer = item["answer"]

            try:
                vocabulary_id_text, quiz_type_value = question_id.split("-", 1)
                vocabulary_id = int(vocabulary_id_text)
                quiz_type = validate_quiz_type(quiz_type_value)
            except (ValueError, TypeError):
                return Response(
                    {"detail": f"Invalid question ID: {question_id}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                vocabulary = Vocabulary.objects.get(pk=vocabulary_id)
            except Vocabulary.DoesNotExist:
                return Response(
                    {"detail": f"Question not found: {question_id}"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            try:
                validate_vocabulary(vocabulary, quiz_type)
                correct_answer = get_correct_answer(vocabulary, quiz_type)
            except ValueError as exc:
                return Response(
                    {"detail": str(exc)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            results.append({
                "question_id": question_id,
                "correct": answer == correct_answer,
                "correct_answer": correct_answer,
            })

        correct_count = sum(
            1 for result in results if result["correct"]
        )

        return Response({
            "total_questions": len(results),
            "correct_count": correct_count,
            "score_percentage": round(
                correct_count / len(results) * 100, 2
            ),
            "results": results,
        })
