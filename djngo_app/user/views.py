from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializrs import UserSerializer
from rest_framework.response import Response
import grpc
from .some.folder import serveur_pb2_grpc 
from .some.folder import serveur_pb2  
from rest_framework import status
class UserViewSet(viewsets.ViewSet):
    queryset = User_p.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        age = serializer.validated_data.get('age')
        email = serializer.validated_data.get('email')

        channel = grpc.insecure_channel('localhost:50051')
        stub =serveur_pb2_grpc.AgeServiceStub(channel)
        request_grpc = serveur_pb2.UpdateRequest(email=email, age=age)
        response = stub.SendUser(request_grpc)       
        user=User_p.objects.create(username=response.username,first_name=request.data['first_name'],
                    last_name=request.data['last_name'],email=request.data['email'],age=request.data['age'],
                    categore=response.category)
        serializer = self.get_serializer(user)
        return response (serializer.data,status=status.HTTP_201_CREATED)
        
