from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Cart, CartItem, Category, Menu
from .serializers import CartSerializer, CategorySerializer
from .serializers import RegisterSerializer
from.serializers import LoginSerializer
from.serializers import MenuSerializer
from.serializers import CartItemSerializer
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

class MenuAPIView(APIView):

    def get(self, request):

        menus = Menu.objects.all()

        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Request se data lena
        menu_id = request.data.get('menu_id')
        quantity = request.data.get('quantity', 1)

        # Menu item find karna
        menu = get_object_or_404(Menu, id=menu_id)

        # Logged-in user ka cart get ya create karna
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        # Check karna ki item already cart mein hai ya nahi
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu=menu,
            defaults={'quantity': quantity}
        )

        # Agar item already cart mein tha
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # Response return karna
        serializer = CartItemSerializer(cart_item)

        return Response(
            {
                'message': 'Item added to cart successfully',
                'item': serializer.data
            },
            status=status.HTTP_200_OK
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):

        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):

        cart_item = get_object_or_404(CartItem, id = id, cart__user=request.user)
        quantity = request.data.get('quantity')
        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id = None):
        if id:
            #specific item delet
            cart_item = get_object_or_404(CartItem, id = id, cart__user=request.user)
            cart_item.delete()
            return Response({'message': 'Item removed from cart successfully'}, status=status.HTTP_200_OK)
        else:
            # complete cart delete
            cart = get_object_or_404(Cart, user=request.user)
            cart.cartitem_set.all().delete()
            return Response({'message': 'Cart cleared successfully'}, status=status.HTTP_200_OK)

