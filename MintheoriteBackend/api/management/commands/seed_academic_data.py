from django.core.management.base import BaseCommand
from api.models import Universidad, Facultad, Carrera, Curso

class Command(BaseCommand):
    help = 'Seeds the database with initial academic data (UDH, UNHEVAL)'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        odh, _ = Universidad.objects.get_or_create(nombre='Universidad de Huánuco', siglas='UDH')
        unheval, _ = Universidad.objects.get_or_create(nombre='Universidad Nacional Hermilio Valdizán', siglas='UNHEVAL')

        fac_ing_udh, _ = Facultad.objects.get_or_create(nombre='Facultad de Ingeniería', universidad=odh)
        
        carrera_sistemas, _ = Carrera.objects.get_or_create(nombre='Ingeniería de Sistemas e Informática', facultad=fac_ing_udh)

        cursos_data = [
            ('Introducción a la Ingeniería', 1),
            ('Matemática I', 1),
            ('Lenguaje y Comunicación', 1),
            ('Metodología del Estudio', 1),
            ('Matemática II', 2),
            ('Algoritmos y Estructura de Datos I', 2),
            ('Física I', 2),
            ('Matemática III', 3),
            ('Algoritmos y Estructura de Datos II', 3),
            ('Estadística y Probabilidades', 3),
            ('Arquitectura de Computadoras', 3),
        ]

        for nombre, ciclo in cursos_data:
            Curso.objects.get_or_create(
                codigo=f"SIS-{nombre[:3].upper()}-{ciclo}0",
                defaults={
                    'nombre': nombre,
                    'ciclo': ciclo,
                    'carrera': carrera_sistemas
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded academic data!'))
