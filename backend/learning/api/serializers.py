from rest_framework import serializers


class HSKLevelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    order = serializers.IntegerField()
    description = serializers.CharField()


class StudyWordSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    simplified = serializers.CharField()
    pinyin = serializers.CharField()
    meaning = serializers.CharField()


class QuizQuestionSerializer(serializers.Serializer):
    id = serializers.CharField()
    quiz_type = serializers.CharField()
    vocabulary_id = serializers.IntegerField()
    prompt = serializers.CharField()
    options = serializers.ListField(
        child=serializers.CharField(),
    )


class QuizAnswerSerializer(serializers.Serializer):
    question_id = serializers.CharField()
    answer = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )



class QuizAnswerItemSerializer(serializers.Serializer):
    question_id = serializers.CharField()
    answer = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )


class QuizBatchAnswerSerializer(serializers.Serializer):
    answers = QuizAnswerItemSerializer(
        many=True,
        allow_empty=False,
    )
