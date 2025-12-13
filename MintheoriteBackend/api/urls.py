from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UsuarioViewSet, UniversidadViewSet, FacultadViewSet, CarreraViewSet,
    CursoViewSet, MaterialViewSet, MentoriaViewSet, ResenaViewSet, PerfilViewSet,
    QuizViewSet, IntentoQuizViewSet, PreguntaForoViewSet, RespuestaForoViewSet, VotoViewSet
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'universidades', UniversidadViewSet)
router.register(r'facultades', FacultadViewSet)
router.register(r'carreras', CarreraViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'materiales', MaterialViewSet)
router.register(r'mentorias', MentoriaViewSet)
router.register(r'perfiles', PerfilViewSet, basename='perfil')
router.register(r'resenas', ResenaViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'intentos', IntentoQuizViewSet)
router.register(r'foro-preguntas', PreguntaForoViewSet)
router.register(r'foro-respuestas', RespuestaForoViewSet)
router.register(r'votos', VotoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]