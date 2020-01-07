from rest_framework import serializers
from .models import Project, Team


class ProjectSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField()

    class Meta:
        model = Project
        fields = (
                'id',
                'name',
                'description',
                'duration',
                'endDate',
                'avatar',
                'team'
                )

    def create(self, validated_data):
        project = Project(
                name=validated_data['name'],
                description=validated_data['description'],
                endDate=validated_data['endDate'],
                team=validated_data['team']
                )
        if validated_data['avatar']:
            project.avatar = validated_data['avatar']

        project.save()
        return project

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
                                    'description', instance.description)
        instance.endDate = validated_data.get('endDate', instance.endDate)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance
