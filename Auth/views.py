
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import (UserSerializer, 
                          UpdateUserSerializer, 
                          ResetPasswordSerializer, 
                          ForgotPasswordSerializer,
                          ActivateUserSerializer,
                          ChangePasswordSerializer,)
from .email import user_create_mail, reset_password_mail
from .tokens import generate_OTP
from .exceptions import OTPNotMatchedException

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from drf_yasg.utils import swagger_auto_schema



class CreateListUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activation_code = generate_OTP() #generate code that will be sent to email

        serializer.save(otp=activation_code)

        # send mail
        email = serializer.validated_data['email']
        user_create_mail(email, activation_code)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    


class CreateSuperUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]

    def perform_create(self, serializer):
        serializer.save(is_superuser=True, is_staff=True)



class  ActivateUser(APIView):

    def patch(self, request, user_id, format=None):
        user = get_object_or_404(User, user_id=user_id)
        serializer = ActivateUserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        new_otp = serializer.validated_data['otp']

        if user.otp != new_otp:
            raise OTPNotMatchedException
        
        serializer.save(is_active=True)
        return Response(status=status.HTTP_200_OK)
        


class RetrieveUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_id'


class UpdateUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAdminUser, IsAuthenticated,]
    lookup_field = 'user_id'


class DeleteUser(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_id'
    permission_classes = [IsAuthenticated,]



class ChangePassword(APIView):
    permission_classes = [IsAuthenticated,]
    
    def patch(self, request, user_id, format=None):
        user = get_object_or_404(User, user_id=user_id)
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        return Response(status=status.HTTP_200_OK)




class ForgotPassword(APIView):

    @swagger_auto_schema(request_body=ForgotPasswordSerializer, responses={200: 'OK'})
    def post(self, request, format=None):
        fp_serializer = ForgotPasswordSerializer(data=request.data)

        if fp_serializer.is_valid():
            email = request.data['email']
            user = get_object_or_404(User, email=email) # check that email exists
            u_serializer= UserSerializer(data=user)

            reset_code = generate_OTP() #generate code that will be sent to email
            u_serializer.save(otp=reset_code) #save otp to database
            reset_password_mail(email, reset_code) #send email

            content = {'email': email,}
            return Response(content, status=status.HTTP_200_OK)



class ResetPassword(APIView):

    @swagger_auto_schema(request_body=ResetPasswordSerializer, responses={200: 'Password updated'})
    def patch(self, request, format=None):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():

            new_otp = serializer.validated_data['otp']
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['password']


            user = get_object_or_404(User, email=email) #get user with email
            if user.otp != new_otp:                     #check if otp  provided matches with database. If not, raise exception.
                raise OTPNotMatchedException

            try:
                user.set_password(new_password)#set new password
            except Exception:
                return Response({'err_msg': 'Could not save Password to database'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response(status=status.HTTP_200_OK) 
    
