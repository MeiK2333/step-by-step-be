from rest_framework import serializers

from source.models import Problem, Solution, Source, SourceUser


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = ["name"]


class SourceUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SourceUser
        fields = ["user", "source", "username"]


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem
        fields = ["source", "title", "link"]


class SolutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Solution
        fields = [
            "source_user",
            "problem",
            "result",
            "language",
            "time_used",
            "memory_used",
            "length",
            "submitted_at",
        ]

