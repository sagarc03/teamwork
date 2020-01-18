from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import Project, Membership, Task, SubTask
from .serializers import ProjectSerializer, TaskSerializer, SubTaskSerializer
from datetime import datetime

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def projects_view(request):
    membership = Membership.objects.filter(user=request.user).first()
    if request.method == 'GET':
        projects = Project.objects.filter(team=membership.team).all()
        serializer = ProjectSerializer(projects, many=True)
    elif request.method == 'POST':
        data = {}
        try:
            data['name'] = request.data['name']
            data['description'] = request.data['description']
            data['endDate'] = datetime.strptime(
                                        request.data['endDate'],
                                        '%Y-%m-%d'
                                        ).date()
            data['team'] = membership.team
            if 'avatar' not in request.data:
                data['avatar'] = None
            else:
                data['avatar'] = request.data['avatar']
        except Exception as e:
            print(e)
            return Response(
                {"message": "Invalid or Missing fields"},
                status=status.HTTP_400_BAD_REQUEST
                )

        project = Project(**data)
        project.save()
        serializer = ProjectSerializer(project)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def project_view(request, pk=None):
    membership = Membership.objects.filter(user=request.user).first()
    projects = Project.objects.filter(team=membership.team).all()
    project = get_object_or_404(projects, pk=pk)

    if request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PATCH' or request.method == 'PUT':
        project.name = request.data.getitem('name', project.name)
        project.description = request.data.getItem(
                                    'description', project.description
                                    )
        if 'endDate' in request.data:
            project.endDate = datetime.strptime(
                    request.data['endDate'],
                    '%Y-%m-%d'
                    ).date()
        project.save()

    serializer = ProjectSerializer(project)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


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


class SubTaskViewSet(viewsets.ViewSet):
    queryset = SubTask.objects.all()

    def list(self, request):
        task = self.validate_and_retrive_task(request)

        if isinstance(task, Response):
            return task

        subtask = SubTask.objects.filter(task=task).all()
        serializer = SubTaskSerializer(subtask, many=True)
        return Response(data=serializer.data)

    def create(self, request):
        task = self.validate_and_retrive_task(request)
        if isinstance(task, Response):
            return task

        validated_data = request.data
        validated_data['endDate'] = datetime.strptime(
                                        validated_data['endDate'],
                                        '%Y-%m-%d'
                                        ).date()
        validated_data['startDate'] = datetime.strptime(
                                        validated_data['startDate'],
                                        '%Y-%m-%d'
                                        ).date()
        validated_data['task'] = task

        serializer = SubTaskSerializer()
        newInstance = serializer.create(validated_data)
        serializer = SubTaskSerializer(newInstance)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        instance = self.get_instance(request, pk=pk)
        serializer = SubTaskSerializer(instance)
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
        serializer = SubTaskSerializer()
        newInstance = serializer.update(instance, validated_data)
        serializer = SubTaskSerializer(newInstance)
        return Response(data=serializer.data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        instance = self.get_instance(request, pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def validate_and_retrive_task(self, request):
        if 'task' not in request.headers and 'task' not in request.data:
            return Response(
                        data={'message': 'task id missing from the header'},
                        status=status.HTTP_400_BAD_REQUEST
                        )

        membership = Membership.objects.filter(user=request.user).first()
        if 'task' in request.data:
            pk = request.data['task']
        else:
            pk = request.headers['task']

        task = Task.objects.filter(pk=pk).first()

        if membership.team != task.project.team:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return task

    def get_instance(self, request, pk=None):
        task = self.validate_and_retrive_task(request)
        if isinstance(task, Response):
            return task
        subtask = SubTask.objects.filter(task=task).all()
        return get_object_or_404(subtask, pk=pk)
