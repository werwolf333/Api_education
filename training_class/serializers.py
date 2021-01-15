from django.contrib.auth.models import User, Group
from rest_framework import serializers
from training_class.models import Student, Teacher, Group, Exercise, Solution


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'groupName']


class ExerciseSerializer(serializers.Serializer):
    text = serializers.CharField()
    group_id = serializers.IntegerField()
    teacher_id = serializers.IntegerField()

    def create(self, validated_data):
        return Exercise.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.group_id = validated_data.get('group_id', instance.group_id)
        instance.teacher_id = validated_data.get('teacher_id', instance.teacher_id)
        instance.save()
        return instance


class SolutionSerializer(serializers.Serializer):
    exercise_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    text = serializers.CharField()
    file = serializers.CharField()

    def create(self, validated_data):
        return Solution.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.exercise_id = validated_data.get('exercise_id', instance.exercise_id)
        instance.student_id = validated_data.get('student_id', instance.student_id)
        instance.text = validated_data.get('text', instance.text)
        instance.file = validated_data.get('file', instance.file)
        instance.save()
        return instance
    """
    Example of request:

    ```json
    {
        "exercise": {
            "text":"проверка",
            "group_id":2,
            "teacher_id":1
        }
    }
    ```
    """