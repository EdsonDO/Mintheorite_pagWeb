from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated

from .models import (
    Usuario, Perfil, Universidad, Facultad, Carrera, Curso, MaterialEstudio, SesionMentoria, Resena,
    Quiz, IntentoQuiz, PreguntaForo, RespuestaForo, Voto
)
from .serializers import (
    UsuarioSerializer, PerfilSerializer, UniversidadSerializer, FacultadSerializer, CarreraSerializer, 
    CursoSerializer, MaterialEstudioSerializer, SesionMentoriaSerializer, ResenaSerializer,
    QuizSerializer, IntentoQuizSerializer, PreguntaForoSerializer, RespuestaForoSerializer, VotoSerializer
)

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer

    def get_queryset(self):
        queryset = Usuario.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class UniversidadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Universidad.objects.all()
    serializer_class = UniversidadSerializer
    permission_classes = [AllowAny]

class FacultadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Facultad.objects.all()
    serializer_class = FacultadSerializer
    permission_classes = [AllowAny]

class CarreraViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer
    permission_classes = [AllowAny]

class CursoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [AllowAny]

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = MaterialEstudio.objects.all()
    serializer_class = MaterialEstudioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MentoriaViewSet(viewsets.ModelViewSet):
    queryset = SesionMentoria.objects.all()
    serializer_class = SesionMentoriaSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ResenaViewSet(viewsets.ModelViewSet):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class IntentoQuizViewSet(viewsets.ModelViewSet):
    queryset = IntentoQuiz.objects.all()
    serializer_class = IntentoQuizSerializer

class PreguntaForoViewSet(viewsets.ModelViewSet):
    queryset = PreguntaForo.objects.all().order_by('-fecha_publicacion')
    serializer_class = PreguntaForoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RespuestaForoViewSet(viewsets.ModelViewSet):
    queryset = RespuestaForo.objects.all()
    serializer_class = RespuestaForoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VotoViewSet(viewsets.ModelViewSet):
    queryset = Voto.objects.all()
    serializer_class = VotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
