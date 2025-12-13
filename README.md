# ☄️ Mintheorite
<p align="center">
  <img src="assets/MintheoriteLogoOfficial.png" alt="Mintheorite Logo">
</p>

Bienvenido a **Mintheorite**, la plataforma educativa de próxima generación diseñada para conectar Estudiantes y Mentores en un entorno de aprendizaje dinámico, estético y (Esperemos) gamificado.
---

## 🏗️ Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Angular](https://img.shields.io/badge/angular-%23DD0031.svg?style=for-the-badge&logo=angular&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

Este proyecto está construido sobre cimientos sólidos y modernos:

### 🐍 Backend: Django (Python)
- **Framework**: Django 6.0 (Bleeding Edge)
- **API**: Django Rest Framework (DRF)
- **Seguridad**: Autenticación por Tokens + Variables de Entorno (.env) 🔒
- **Base de Datos**: SQLite3 (Desarrollo) / Postgres (Producción - Ready)

### 🅰️ Frontend: Angular
- **Framework**: Angular 21 (Moderno y Rápido)
- **Estilos**: TailwindCSS v3 + Estilos personalizados Cyber-estéticos 🎨
- **Arquitectura**: Component-based con Módulos Lazy Loaded

---

## 🌟 Características Principales

### 🎓 Para Estudiantes (Mentees)
- **Dashboard Interactivo**: Visualiza tu progreso, mentorías próximas y logros.
- **Búsqueda de Mentores**: Encuentra guías expertos en tus áreas de interés.
- **Gamificación**: Gana insignias y sube de nivel mientras aprendes.

### 🧠 Para Mentores
- **Gestión de Sesiones**: Organiza tu agenda y tus sesiones de mentoría.
- **Perfiles Personalizables**: Muestra tu experiencia y especialidades.
- **Feedback Directo**: Ayuda a tus estudiantes a crecer con retroalimentación precisa.

---

## 🚀 Instalación y Despliegue

### Requisitos Previos
- Python 3.10+
- Node.js 18+
- Angular CLI

### 1️⃣ Backend Setup
```bash
cd MintheoriteBackend
# Crear entorno virtual (opcional pero recomendado)
python -m venv env
source env/bin/activate  # o env\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
# Crea un archivo .env basado en el ejemplo o pide la llave maestra al administrador.

# Migraciones y servidor
python manage.py migrate
python manage.py runserver
```

### 2️⃣ Frontend Setup
```bash
cd MintheoriteFrontend
# Instalar paquetes
npm install

# Iniciar servidor de desarrollo
ng serve
```

Visita `http://localhost:4200/` y listo...

---

## 🛡️ Estructura del Proyecto

```
Mintheorite/
├── 📂 MintheoriteBackend/  # El núcleo lógico (Django)
│   ├── api/                # Endpoints y Lógica de Negocio
│   ├── mintheoriteAPI/     # Configuración del Proyecto
│   └── ...
├── 📂 MintheoriteFrontend/ # La cara visible (Angular)
│   ├── src/app/            # Componentes y Vistas
│   └── ...
└── 📄 README.md            # Tú estás aquí
```

---

## 🤝 Contribución

Este proyecto es privado por ahora. Contacta a **Edson** para acceso.
Si vas a contribuir:
1.  Haz check-out a una nueva rama (`git checkout -b feature/nueva-idea`).
2.  Haz tus cambios y commits descriptivos.
3.  Abre un Pull Request.

---
