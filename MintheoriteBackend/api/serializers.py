from rest_framework import serializers
from .models import (
    Usuario, Perfil, Universidad, Facultad, Carrera, Curso, MaterialEstudio, SesionMentoria, Resena,
    Quiz, Pregunta, Opcion, IntentoQuiz,
    PreguntaForo, RespuestaForo, Voto
)

class UniversidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universidad
        fields = '__all__'

class FacultadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultad
        fields = '__all__'

class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class PerfilSerializer(serializers.ModelSerializer):
    carrera_nombre = serializers.CharField(source='carrera.nombre', read_only=True)
    
    stats_quizzes_aprobados = serializers.SerializerMethodField()
    stats_promedio_global = serializers.SerializerMethodField()
    stats_sesiones_recibidas = serializers.SerializerMethodField()
    stats_aportes_repo = serializers.SerializerMethodField()
    objetivo_display = serializers.CharField(source='get_objetivo_academico_display', read_only=True)
    
    cursos_inscritos_detalles = CursoSerializer(source='cursos_inscritos', many=True, read_only=True)

    class Meta:
        model = Perfil
        fields = '__all__'

    def get_stats_quizzes_aprobados(self, obj):
        return obj.usuario.intentos_quizzes.filter(aprobado=True).count()

    def get_stats_promedio_global(self, obj):
        intentos = obj.usuario.intentos_quizzes.filter(aprobado=True)
        if not intentos.exists():
            return 0
        total = sum(i.puntaje_obtenido for i in intentos)
        return round(total / intentos.count(), 1)

    def get_stats_sesiones_recibidas(self, obj):
        return obj.usuario.mentorias_tomadas.filter(estado='REALIZADA').count()

    def get_stats_aportes_repo(self, obj):
        return MaterialEstudio.objects.filter(subido_por=obj.usuario).count()

class UsuarioSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'rol', 'codigo_alumno', 'verificado', 'perfil']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class MaterialEstudioSerializer(serializers.ModelSerializer):
    autor_nombre = serializers.CharField(source='subido_por.first_name', read_only=True)
    class Meta:
        model = MaterialEstudio
        fields = '__all__'

class SesionMentoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SesionMentoria
        fields = '__all__'

class ResenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resena
        fields = '__all__'

class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = ['id', 'texto', 'es_correcta', 'retroalimentacion']

class PreguntaSerializer(serializers.ModelSerializer):
    opciones = OpcionSerializer(many=True, read_only=True)
    class Meta:
        model = Pregunta
        fields = ['id', 'texto', 'tipo', 'puntaje', 'opciones']

class QuizSerializer(serializers.ModelSerializer):
    preguntas = PreguntaSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = '__all__'

class IntentoQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntentoQuiz
        fields = '__all__'

class RespuestaForoSerializer(serializers.ModelSerializer):
    autor_nombre = serializers.CharField(source='autor.username', read_only=True)
    class Meta:
        model = RespuestaForo
        fields = '__all__'

class PreguntaForoSerializer(serializers.ModelSerializer):
    respuestas = RespuestaForoSerializer(many=True, read_only=True)
    autor_nombre = serializers.CharField(source='autor.username', read_only=True)
    class Meta:
        model = PreguntaForo
        fields = '__all__'

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = '__all__'