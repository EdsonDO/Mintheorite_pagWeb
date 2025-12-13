from django.db import models
from django.contrib.auth.models import AbstractUser

class Universidad(models.Model):
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Nombre de la Universidad")
    siglas = models.CharField(max_length=20, verbose_name="Siglas (Ej: UDH)")
    logo = models.ImageField(upload_to='universidades/', null=True, blank=True)

    def __str__(self):
        return f"{self.siglas} - {self.nombre}"

class Facultad(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre de la Facultad")
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, related_name='facultades')

    class Meta:
        verbose_name_plural = "Facultades"

    def __str__(self):
        return f"{self.nombre} ({self.universidad.siglas})"

class Carrera(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre de la Carrera")
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name='carreras')

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        ESTUDIANTE = 'ESTUDIANTE', 'Estudiante'
        MENTOR = 'MENTOR', 'Mentor'

    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    first_name = models.CharField(max_length=150, verbose_name="Nombres")
    last_name = models.CharField(max_length=150, verbose_name="Apellidos")

    rol = models.CharField(
        max_length=15, 
        choices=Rol.choices, 
        default=Rol.ESTUDIANTE, 
        verbose_name="Rol"
    )
    codigo_alumno = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True, 
        verbose_name="Código de Alumno / Institucional"
    )
    verificado = models.BooleanField(default=False, verbose_name="Verificado")

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Perfil(models.Model):
    class ObjetivoAcademico(models.TextChoices):
        MEJORAR_PROMEDIO = 'MEJORAR_PROMEDIO', 'Mejorar Ponderado'
        PASAR_CURSO = 'PASAR_CURSO', 'Pasar Cursos'
        MANTENER_PROMEDIO = 'MANTENER_PROMEDIO', 'Mantener Ponderado'
        APRENDER_METODO = 'APRENDER_METODO', 'Aprender Métodos de Estudio'

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono / WhatsApp")
    linkedin = models.URLField(blank=True, null=True, verbose_name="Perfil de LinkedIn")
    portfolio = models.URLField(blank=True, null=True, verbose_name="Portafolio / GitHub")

    carrera = models.ForeignKey(
        Carrera, 
        on_delete=models.PROTECT, 
        related_name='estudiantes',
        verbose_name="Carrera Profesional",
        null=True
    )
    
    ciclo_actual = models.PositiveIntegerField(default=1, verbose_name="Ciclo Actual")
    
    objetivo_academico = models.CharField(
        max_length=30, 
        choices=ObjetivoAcademico.choices, 
        null=True, 
        blank=True
    )
    
    puntos_reputacion = models.IntegerField(default=0, verbose_name="Puntos Meteorite")
    nivel_confianza = models.CharField(max_length=50, default="Novato", verbose_name="Nivel de Confianza (Tier)")
    quizzes_completados = models.PositiveIntegerField(default=0)
    medalla_actual = models.CharField(max_length=50, default="Bit (2^1)", verbose_name="Medalla Actual")
    racha_estudio = models.PositiveIntegerField(default=0, verbose_name="Días en Racha")

    biografia = models.TextField(blank=True, verbose_name="Sobre mí")

    cursos_inscritos = models.ManyToManyField('Curso', blank=True, related_name='estudiantes_inscritos')

    def __str__(self):
        uni = self.carrera.facultad.universidad.siglas if self.carrera else "Sin Asignar"
        return f"{self.usuario.username} - {uni}"

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    ciclo = models.PositiveIntegerField()
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='cursos', null=True) 
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
    
    def __str__(self):
        return f"{self.nombre} (Ciclo {self.ciclo})"

class MaterialEstudio(models.Model):
    class TipoMaterial(models.TextChoices):
        RESUMEN = 'RESUMEN', 'Resumen Sintetizado'
        GUIA = 'GUIA', 'Guía de Estudio'
        METODO = 'METODO', 'Método de Estudio'
        SIMULACRO = 'SIMULACRO', 'Simulacro/Cuestionario'
    
    class Estado(models.TextChoices):
        BORRADOR = 'BORRADOR', 'Borrador'
        EN_REVISION = 'EN_REVISION', 'En Revisión'
        PUBLICADO = 'PUBLICADO', 'Publicado'

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, related_name='materiales')
    subido_por = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_material = models.CharField(max_length=20, choices=TipoMaterial.choices)
    archivo = models.FileField(upload_to='materiales/%Y/%m/')
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.BORRADOR)
    atribucion_derechos = models.CharField(max_length=255, blank=True, verbose_name="Atribución / Copyright")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    conteo_descargas = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Material de Estudio"
        verbose_name_plural = "Materiales de Estudio"

    def __str__(self):
        return self.titulo

class SesionMentoria(models.Model):
    class Estado(models.TextChoices):
        SOLICITADA = 'SOLICITADA', 'Solicitada'
        PROGRAMADA = 'PROGRAMADA', 'Programada'
        REALIZADA = 'REALIZADA', 'Realizada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    mentor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mentorias_impartidas', limit_choices_to={'rol': Usuario.Rol.MENTOR})
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mentorias_tomadas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    tema = models.CharField(max_length=200, verbose_name="Tema Específico")
    fecha_programada = models.DateTimeField()
    enlace_reunion = models.URLField(blank=True, verbose_name="Link de Reunión")
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.SOLICITADA)
    motivo_cancelacion = models.TextField(blank=True, null=True, verbose_name="Motivo de Cancelación/Rechazo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sesión de Mentoría"
        verbose_name_plural = "Sesiones de Mentoría"

    def __str__(self):
        return f"{self.curso.nombre} - {self.fecha_programada}"

class Resena(models.Model):
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    sesion_mentoria = models.ForeignKey(SesionMentoria, on_delete=models.CASCADE, null=True, blank=True, related_name='resenas')
    material = models.ForeignKey(MaterialEstudio, on_delete=models.CASCADE, null=True, blank=True, related_name='resenas')
    puntuacion = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Estrellas (1-5)")
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        target = "Material" if self.material else "Mentoría"
        return f"{self.puntuacion} ★ "

class Quiz(models.Model):
    titulo = models.CharField(max_length=200)
    material_origen = models.ForeignKey(MaterialEstudio, on_delete=models.SET_NULL, null=True, blank=True, related_name='quizzes_derivados')
    creador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='quizzes_creados')
    generado_por_ai = models.BooleanField(default=False, verbose_name="Generado por IA")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"{self.titulo} ({'AI' if self.generado_por_ai else 'Manual'})"

class Pregunta(models.Model):
    class TipoPregunta(models.TextChoices):
        OPCION_MULTIPLE = 'OPCION_MULTIPLE', 'Opción Múltiple (Una correcta)'
        VERDADERO_FALSO = 'VERDADERO_FALSO', 'Verdadero / Falso'
        SELECCION_MULTIPLE = 'SELECCION_MULTIPLE', 'Selección Múltiple (Varias correctas)'

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.TextField(verbose_name="Enunciado de la Pregunta")
    tipo = models.CharField(max_length=20, choices=TipoPregunta.choices, default=TipoPregunta.OPCION_MULTIPLE)
    puntaje = models.PositiveIntegerField(default=10, verbose_name="Puntos por responder bien")

    def __str__(self):
        return self.texto[:50]

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False, verbose_name="¿Es Correcta?")
    retroalimentacion = models.TextField(blank=True, null=True, verbose_name="Explicación / Feedback")

    class Meta:
        verbose_name = "Opción"
        verbose_name_plural = "Opciones"

    def __str__(self):
        return f"{self.texto} {'(Correcta)' if self.es_correcta else ''}"

class IntentoQuiz(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='intentos_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='intentos')
    puntaje_obtenido = models.FloatField(default=0.0)
    aprobado = models.BooleanField(default=False)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Intento de Quiz"
        verbose_name_plural = "Intentos de Quizzes"

    def __str__(self):
        return f"{self.estudiante.username} - {self.quiz.titulo}: {self.puntaje_obtenido}"

class PreguntaForo(models.Model):
    class Estado(models.TextChoices):
        ABIERTA = 'ABIERTA', 'Abierta'
        RESUELTA = 'RESUELTA', 'Resuelta (Mejor Respuesta Seleccionada)'
        CERRADA = 'CERRADA', 'Cerrada por Moderación'

    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='preguntas_foro')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='preguntas_foro')
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ABIERTA)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    
    tags = models.CharField(max_length=200, blank=True, verbose_name="Etiquetas (Tags)")

    class Meta:
        verbose_name = "Pregunta de Foro"
        verbose_name_plural = "Preguntas de Foro"

    def __str__(self):
        return self.titulo

class RespuestaForo(models.Model):
    pregunta = models.ForeignKey(PreguntaForo, on_delete=models.CASCADE, related_name='respuestas')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='respuestas_foro')
    contenido = models.TextField()
    es_mejor_respuesta = models.BooleanField(default=False, verbose_name="Mejor Respuesta (La Corona)")
    puntos_votos = models.IntegerField(default=0, verbose_name="Conteo de Votos (Cache)")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Respuesta de Foro"
        verbose_name_plural = "Respuestas de Foro"

    def __str__(self):
        return f"Respuesta de {self.autor.username} a {self.pregunta.id}"

class Voto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(RespuestaForo, on_delete=models.CASCADE, related_name='votos')
    valor = models.SmallIntegerField(choices=[(1, 'Util (+1)'), (-1, 'No Util (-1)')])
    fecha_voto = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['usuario', 'respuesta']
