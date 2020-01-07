from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Project, Membership, Task
from .serializers import ProjectSerializer, TaskSerializer
from datetime import datetime
# Create your views here.


class ProjectViewSet(viewsets.ViewSet):
    queryset = Project.objects.all()

    def list(self, request):
        projects = self.get_team_projects(request)
        serializer = ProjectSerializer(projects, many=True)
        return Response(data=serializer.data)

    def create(self, request):
        validated_data = request.data
        membership = Membership.objects.filter(user=request.user).first()
        validated_data['team'] = membership.team
        validated_data['endDate'] = datetime.strptime(
                                        validated_data['endDate'],
                                        '%Y-%m-%d'
                                        ).date()
        if 'avatar' not in validated_data:
            validated_data['avatar'] = None

        serializer = ProjectSerializer()
        newInstance = serializer.create(validated_data)
        serializer = ProjectSerializer(newInstance)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        instance = self.get_instance(request, pk=pk)
        serializer = ProjectSerializer(instance)
        return Response(data=serializer.data)

    def update(self, request, pk=None):
        validated_data = request.data
        instance = self.get_instance(request, pk=pk)
        if 'endDate' in validated_data:
            validated_data['endDate'] = datetime.strptime(
                                        validated_data['endDate'],
                                        '%Y-%m-%d'
                                        ).date()
        serializer = ProjectSerializer()
        newInstance = serializer.update(instance, validated_data)
        serializer = ProjectSerializer(newInstance)
        return Response(data=serializer.data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        instance = self.get_instance(request, pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_team_projects(self, request):
        membership = Membership.objects.filter(user=request.user).first()
        return Project.objects.filter(team=membership.team).all()

    def get_instance(self, request, pk=None):
        projects = self.get_team_projects(request)
        return get_object_or_404(projects, pk=pk)


class TaskViewSet(viewsets.ViewSet):
    queryset = Task.objects.all()

    def list(self, request):
        project = self.validate_and_retrive_project(request)

        if isinstance(project, Response):
            return project

        task = Task.objects.filter(project=project).all()
        serializer = TaskSerializer(task, many=True)
        return Response(data=serializer.data)

    def create(self, request):
        project = self.validate_and_retrive_project(request)

        if isinstance(project, Response):
            return project

        validated_data = request.data
        validated_data['endDate'] = datetime.strptime(
                                        validated_data['endDate'],
                                        '%Y-%m-%d'
                                        ).date()
        validated_data['startDate'] = datetime.strptime(
                                        validated_data['startDate'],
                                        '%Y-%m-%d'
                                        ).date()
        validated_data['project'] = project

        serializer = TaskSerializer()
        newInstance = serializer.create(validated_data)
        serializer = TaskSerializer(newInstance)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        instance = self.get_instance(request, pk=pk)
        serializer = TaskSerializer(instance)
        return Response(data=serializer.data)

    def update(self, request, pk=None):
        validated_data = request.data
        instance = self.get_instance(request, pk=pk)
        if 'endDate' in validated_data:
            validated_data['endDate'] = datetime.strptime(
                                        validated_data['endDate'],
                                        '%Y-%m-%d'
                                        ).date()
        if 'startDate' in validated_data:
            validated_data['startDate'] = datetime.strptime(
                                        validated_data['startDate'],
                                        '%Y-%m-%d'
                                        ).date()
        serializer = TaskSerializer()
        newInstance = serializer.update(instance, validated_data)
        serializer = TaskSerializer(newInstance)
        return Response(data=serializer.data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        instance = self.get_instance(request, pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def validate_and_retrive_project(self, request):
        if 'project' not in request.headers and 'project' not in request.data:
            return Response(
                        data={'message': 'project id missing from the header'},
                        status=status.HTTP_400_BAD_REQUEST
                        )

        membership = Membership.objects.filter(user=request.user).first()
        if 'project' in request.data:
            pk = request.data['project']
        else:
            pk = request.headers['project']

        project = Project.objects.filter(pk=pk).first()

        if membership.team != project.team:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return project

    def get_instance(self, request, pk=None):
        project = self.validate_and_retrive_project(request)

        if isinstance(project, Response):
            return project

        task = Task.objects.filter(project=project).all()
        return get_object_or_404(task, pk=pk)
