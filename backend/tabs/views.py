from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Tab, Comment, Favorite
from .serializers import (
    TabSerializer, CommentSerializer,
    FavoriteSerializer, RegisterSerializer, UserSerializer
)


# Auth

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# Tabs

class TabListCreateView(generics.ListCreateAPIView):
    serializer_class = TabSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Tab.objects.all().order_by('-created_at')
        search = self.request.query_params.get('search')
        difficulty = self.request.query_params.get('difficulty')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(artist__icontains=search) |
                Q(song__icontains=search)
            )
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TabDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TabSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Tab.objects.all()

    def update(self, request, *args, **kwargs):
        tab = self.get_object()
        if tab.author != request.user:
            return Response({'error': 'You can only edit your own tabs'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        tab = self.get_object()
        if tab.author != request.user:
            return Response({'error': 'You can only delete your own tabs'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


# Comments

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        tab = Tab.objects.get(pk=self.kwargs['tab_id'])
        serializer.save(author=self.request.user, tab=tab)


class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


# Favorites

class FavoriteToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, tab_id):
        tab = Tab.objects.get(pk=tab_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, tab=tab)
        if not created:
            favorite.delete()
            return Response({'status': 'unfavorited'})
        return Response({'status': 'favorited'})


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)