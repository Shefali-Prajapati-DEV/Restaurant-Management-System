from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category
from .serializers import CategorySerializer
from .serializers import RegisterSerializer
from.serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

 
class CategoryAPIView(APIView):



    def get_permissions(self):

        if self.request.method == "GET":

            return[AllowAny()]
        return[IsAdminUser()]

    def post(self, request):

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
 

    def get(self, request, id=None):


        if id is None:

            categories = Category.objects.all()

            serializer = CategorySerializer(categories, many=True)

            return Response(serializer.data)

        category = get_object_or_404(Category, id=id)

        serializer = CategorySerializer(category)

        return Response(serializer.data)
    
    
    
    def put(self, request, id):

        category = get_object_or_404(Category, id=id)
        
        serializer = CategorySerializer(category, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    

    def delete(self, request, id):

        category = get_object_or_404(Category, id=id)

        category.delete()

        return Response(
            {"message": "Category Deleted Successfully"},
            status=status.HTTP_200_OK
        )
    
class RegisterAPIView(APIView):

    def post(slef, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {"message": "User Registered Successfully"},
                status=status.HTTP_201_CREATED

            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST

        )
    
class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data = request.data)

        if serializer.is_valid():

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(
                username=username,
                password=password
            )
             
            if user is not None:
                
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                     "message":"Login Successfully",
                     "refresh": str(refresh),
                     "access": str(refresh.access_token)
                     },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    "error":"Invalid Username or Password"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )