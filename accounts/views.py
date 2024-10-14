from rest_framework import views, generics, status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from django.utils import timezone

from accounts import serializers, models


class RegisterApiView(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyApiView(generics.GenericAPIView):
    serializer_class = serializers.RegisterVerifySerializer
    queryset = models.Confirmation.objects.all()

    def post(self, request):
        serializer = serializers.RegisterVerifySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = serializer.data['code']
            try:
                otp_code = models.Confirmation.objects.filter(code=code).first()
                user = models.User.objects.filter(id=otp_code.user.id).first()
            except:
                return Response({'message': 'Invalid code'}, status=status.HTTP_404_NOT_FOUND)
            if otp_code.is_used:
                return Response({'message': 'Code is used'}, status.HTTP_400_BAD_REQUEST)
            if otp_code.expires < timezone.now():
                return Response({'message': 'Code is not available'})
            otp_code.is_used = True
            user.is_active = True
            otp_code.save()
            user.save()
            token = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(token),
                'access': str(token.access_token),
            }
            return Response({'success': True, 'message': 'Muvaffaqiyatli royxatdan otdingiz', 'tokens': tokens}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeApiView(generics.GenericAPIView):
    serializer_class = serializers.ResendVerifyCodeSerializer

    def post(self, request):
        serializer = serializers.ResendVerifyCodeSerializer(data=request.data)
        serializer.is_valid()
        phone_number = serializer.data['phone_number']
        user = models.User.objects.filter(phone_number=phone_number).first()
        if not user:
            return Response({'message': 'This phone number is not valid or not found'}, status=status.HTTP_404_NOT_FOUND)
        code = user.create_verify_code()
        return Response({'new_code': code}, status=status.HTTP_201_CREATED)
