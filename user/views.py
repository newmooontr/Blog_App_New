from .serializers import RegisterSerializers
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token


# Create your views here.


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers
    
    
    def create(self, request, *args, **kwargs): # metod override etmek
        response = super().create(request, *args, **kwargs)
        token = Token.objects.create(user_id=response.data['id'])
        response.data['token'] = token.key #gelen dataya token ekleyerek register olan user ı direkt ana sayfaya yönlendirmek.
        # print(response.data)
        return response
