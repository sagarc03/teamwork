from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import Project, Membership, Task
from .serializers import ProjectSerializer, TaskSerializer
from datetime import datetime

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getUser(request):
    print(dir(request.user))
    data = {}
    data['username'] = request.user.username
    data['first_name'] = request.user.first_name
    data['last_name'] = request.user.first_name
    data['email'] = request.user.email
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def projects(request):
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
        project.name = request.data.get('name', project.name)
        project.description = request.data.get(
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

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def project_tasks(request, pk):
    project = Project.objects.filter(pk=pk).first()
    membership = Membership.objects.filter(user=request.user).first()
    if membership.team != project.team:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        task = Task.objects.filter(project=project).all()
        serializer = TaskSerializer(task, many=True)
    elif request.method == 'POST':
        try:
            data = {}
            data['name'] = request.data['name']
            data['description'] = request.data['description'] 
            data['endDate'] = datetime.strptime(
                                        request.data['endDate'],
                                        '%Y-%m-%d'
                                        ).date()
            data['startDate'] = datetime.strptime(
                                        request.data['startDate'],
                                        '%Y-%m-%d'
                                        ).date()
            data['project'] = project
            task =  Task(**data)
            task.save()
            serializer = TaskSerializer(task)
        except Exception as e:
            print(e)
            return Response(
                {"message": "Invalid or Missing fields"},
                status=status.HTTP_400_BAD_REQUEST
                )
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def project_task_view(request, projpk, pk):
    project = Project.objects.filter(pk=projpk).first()
    membership = Membership.objects.filter(user=request.user).first()
    if membership.team != project.team:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    tasks = Task.objects.filter(project=project).all()
    task = get_object_or_404(tasks, pk=pk)

    if request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'PUT' or request.method == 'PATCH':
            task.name = request.data.get('name', task.name)
            task.description = request.data.get(
                                'description', task.description
                                )
            if 'endDate' in request.data:
                task.endDate = datetime.strptime(
                                    request.data['endDate'],
                                    '%Y-%m-%d'
                                    ).date()
            if 'startDate' in request.data:
                task.startDate = datetime.strptime(
                                    request.data['startDate'],
                                    '%Y-%m-%d'
                                    ).date()
            task.save()

    serializer = TaskSerializer(task)
    return Response(data=serializer.data, status=status.HTTP_200_OK)