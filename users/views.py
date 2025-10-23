from rest_framework import generics
from .serialaizer import RegisterSerializer

# контроллер для авторизации
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
