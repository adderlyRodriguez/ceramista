# Portfolio Ceramista

Web de portfolio para artista ceramista. Permite al admin gestionar proyectos (imágenes y videos) que se muestran públicamente en una galería responsive.

## Tecnologías

- Python / Flask
- SQLite (desarrollo) / PostgreSQL (producción)
- Cloudinary (almacenamiento de media)
- Bootstrap
- Deploy en Render.com

## Requisitos

```bash
pip install -r requirements.txt
```

Crear un archivo `.env` con las variables:

```
SECRET_KEY=...
ADMIN_CODE=...
DATABASE_URL=...
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
MAIL_USERNAME=...
MAIL_PASSWORD=...
```

## Desarrollo

```bash
python app.py
```

## Producción

```bash
gunicorn app:app
```

## Migraciones

```bash
flask db migrate -m "descripción"
flask db upgrade
```

## Arquitectura

Todo el código vive en `app.py` — modelos, rutas y configuración.

**Modelos:** `Category` (categorías del portfolio) y `Project` (obra con título, descripción, URL de media, tipo, fecha y categoría).

**Admin:** Acceso por código (`ADMIN_CODE`) → sesión protegida.

**Media:** Imágenes y videos subidos a Cloudinary; se guarda la URL en la base de datos.

**Vistas públicas:**
- `/` — grilla cronológica de todos los proyectos
- `/inicio` — proyectos agrupados por categoría
