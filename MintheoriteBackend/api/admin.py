from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Perfil, Universidad, Facultad, Carrera, Curso, MaterialEstudio, SesionMentoria, Resena

class CustomUserAdmin(UserAdmin):
    model = Usuario
    list_display = ['username', 'email', 'rol', 'codigo_alumno', 'verificado']
    fieldsets = UserAdmin.fieldsets + (
        ('Información Académica', {'fields': ('rol', 'codigo_alumno', 'verificado')}),
    )

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Perfil)
admin.site.register(Universidad)
admin.site.register(Facultad)
admin.site.register(Carrera)
admin.site.register(Curso)
admin.site.register(MaterialEstudio)
admin.site.register(SesionMentoria)
admin.site.register(Resena)