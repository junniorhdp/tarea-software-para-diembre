# Pañalera Junior- Evidencia de Calidad SENA(Instructor Javier)

## 1. Propósito y Estándares de Calidad

Este proyecto, desarrollado para el módulo de Aplicación de Calidad del SENA, busca demostrar la Fiabilidad, Usabilidad y Mantenibilidad del software.

Característica de Calidad

Evidencia de Cumplimiento

Fiabilidad

Usabilidad

Diseño 100% responsivo implementado con Tailwind CSS. Experiencia de usuario consistente.

Mantenibilidad

Código modular (HTML/Python separados).

Seguridad

Autenticación con Firebase Auth y prevención de inyección mediante la serialización de datos.

## 2. Tecnologías Clave

Frontend: HTML, JavaScript, Tailwind CSS (para estilización y responsive design).

Backend: Python (Django) - Estructura MVC para separación de lógica.

Base de Datos: Firebase Firestore - Sincronización de datos en tiempo real.

## 3. Proceso de Aseguramiento de la Calidad (QA)

Se aplicó un riguroso proceso de pruebas para validar el cumplimiento de los requisitos:

### A. Pruebas de Integración y Funcionales

Se validó la comunicación correcta de los datos (CRUD) entre el frontend y Firestore, asegurando que:

La visualización del catálogo público es correcta para todos los usuarios.

Solo el administrador puede ejecutar acciones de registro de ventas o modificación de productos.

### B. Pruebas de Usabilidad (Diseño Responsivo)

La interfaz fue probada en distintos viewports (sm:, md:, lg: de Tailwind) para garantizar la correcta visualización y funcionamiento en dispositivos móviles, tabletas y escritorio, cumpliendo con los estándares de accesibilidad y experiencia de usuario.

### C. Análisis de Código

Se realizó una revisión de código enfocada en limpieza y legibilidad.

Se eliminaron dependencias obsoletas y se optimizaron las consultas a la base de datos para asegurar el rendimiento.

## 4. Uso y Despliegue

## 4.1 Instalación (Entorno Django)

Clonar el repositorio: git clone [https://github.com/junniorhdp/tarea-software-para-diembre]

Instalar dependencias: pip install -r requirements.txt

Aplicar migraciones: python manage.py migrate

## 4.2 Ejecución

Iniciar el servidor de desarrollo: python manage.py runserver
