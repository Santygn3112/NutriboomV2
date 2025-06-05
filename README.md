# NutriBoom

NutriBoom es una aplicación web de seguimiento nutricional desarrollada con **Flask** y **MySQL**. Permite a los usuarios llevar un control detallado de su dieta y de su progreso a lo largo del tiempo.

## ¿Qué incluye?

- **Autenticación de usuarios** con recuperación de contraseña vía correo electrónico.
- Formulario para introducir **datos personales** (edad, altura, calorías objetivo, etc.).
- Registro diario de **peso, grasa corporal** e índice de masa corporal.
- Gestor de **platos e ingredientes** para planificar las comidas.
- **Calendario de dieta** donde añadir los platos de cada día y ver un resumen porcentual de calorías.
- Sección de **estadísticas** con gráficos interactivos (ECharts) para visualizar la evolución del peso, calorías y otros indicadores.
- **Panel de administración** (solo para usuarios con `is_admin`) desde el que se pueden crear, editar y eliminar ingredientes o platos de forma paginada.

La aplicación se organiza en:

- `app.py`: punto de entrada donde se inicializa Flask y se registran todas las rutas.
- `backend/Modelos`: modelos de base de datos con SQLAlchemy.
- `routes/`: vistas y lógica de negocio.
- `templates/` y `static/`: archivos HTML, hojas de estilo y scripts del frontend.

## Requisitos
- Python 3.10 o superior.
- Un servidor MySQL accesible.

Instala las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

Copia el archivo `.env.example` a `.env` y completa los siguientes valores:

- `SECRET_KEY`: clave para las sesiones de Flask.
- Parámetros de tu servidor de correo (`MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`).
- Credenciales de MySQL (`MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`).

## Puesta en marcha
1. Inicia tu servicio MySQL con la configuración indicada en el `.env`.
2. Ejecuta la aplicación:

```bash
python app.py
```

En el primer arranque se creará automáticamente la base de datos y se poblará con algunos datos de ejemplo. A continuación podrás acceder en `http://localhost:5000`.



