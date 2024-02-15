from .serializers import NewsletterSerializer, CustomUserSerializer,UserAuthenticationSerializer,NewsletterSubscriberSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
import utils
from .models import CustomUser,Newsletter
from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication

#===========================================
class UserRegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():           
            serializer.save()
            email = serializer.validated_data["email"]
            user = CustomUser.objects.get(email=email)
            active_code = utils.create_random_code(6)
            utils.send_email("confirmation code", f"your active code is {active_code}", [email])
            user.active_code = active_code
            user.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#===========================================
class UserActivationAPIView(APIView):
    def post(self, request):
        serializer = UserAuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            active_code = serializer.validated_data["active_code"]
            try:
                user = CustomUser.objects.get(email=email, active_code=active_code, is_active=False)
            except CustomUser.DoesNotExist:
                return Response({'message': 'Invalid email or activation token or user is already active.'}, status=status.HTTP_400_BAD_REQUEST)

            if not user.is_active:
                user.is_active = True
                user.active_code = utils.create_random_code(6)
                user.save()
                return Response({'message': 'Your account is active'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Your account is already active.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#===========================================
    
class SubscribeNewsletterAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        data = request.data
        ser_data = NewsletterSubscriberSerializer(data=data)
        if ser_data.is_valid():
            email = ser_data.validated_data["email"]
            user = CustomUser.objects.get(email=email)
            user.subscribed_newletter = True
            user.save()
            return Response("You are subscribed")
        return Response(status=status.HTTP_400_BAD_REQUEST)
#===========================================
class UnsubscribeNewsletterAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, ):
        email = request.data.get('email')
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                user.subscribed_newletter = False
                user.save()
                return Response({'message': 'Unsubscribed successfully'}, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Email not found'}, status=status.HTTP_400_BAD_REQUEST)
#===========================================

class NewsletterAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def post(self,request):
        ser_data = NewsletterSerializer(data=request.data)
        if ser_data.is_valid():
            subject = ser_data['subject']
            content = ser_data['content']
            newsletter = Newsletter.objects.create(
                subject=subject,
                content=content,
            )
            newsletter.save()
            return Response(status=status.HTTP_200_OK)

#===========================================

class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                token, create = Token.objects.get_or_create(user=user)
                return Response({'message': 'login successful', 'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#===========================================

class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        request.auth.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    






