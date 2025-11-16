# 🚌 SmartBus – Panel Administrativo MVC para Gestión de Pasajeros

![Django](https://img.shields.io/badge/Django-5.2.x-092E20?style=flat&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat&logo=render)

> **SmartBus** es un sistema web desarrollado con Django que implementa un panel administrativo personalizado (MVC) para la gestión de cooperativas de buses, unidades, reservas de pasajeros y monitoreo de ocupación.
El proyecto cumple con requerimientos de validación en back-end, manejo seguro de datos sensibles, uso correcto de llaves foráneas, y elementos dinámicos (dependencias tipo país → provincia → ciudad) mediante AJAX.

🌐 **Demo en producción:**  
👉 [https://administraci-nmvc.onrender.com](https://administraci-nmvc.onrender.com)

---

## Características principales
**✔ Panel Administrativo (Rol staff)**
- CRUD de Cooperativas
- CRUD de Buses
- Panel de Monitoreo de Ocupación
- Listado y gestión de Reservas
- Validación backend de datos sensibles
- Formularios con dropdowns dinámicos cuando hay llaves foráneas 

**✔ Panel de Usuario (Rol normal)**
- Acceso autenticado
- Consulta de reservas
- Creación de reservas

**✔ Funcionalidades técnicas clave**
- Sistema de autenticación personalizado (sin usar el admin nativo de Django).
- API interna con JSON para carga dinámica de buses según cooperativa.
- Plantillas HTML organizadas con herencia Django (base.html / base_public.html).
- Estructura modular mediante carpeta views/ dividida por responsabilidades.
- Validaciones fuertes en ```forms.py```.
- Cálculos en tiempo real de ocupación con annotate().

---

## 🎯 Requerimientos cumplidos
### 🛡️ 1. Validación Back-End de Datos Sensibles
El sistema considera la cédula del pasajero como un dato sensible dentro del contexto del dominio.
Por ello, la validación no se realiza únicamente en el front-end, sino también en back-end, evitando riesgos como modificación del HTML, bypass del JS o envío de valores manuales.

**✔ Implementación realizada**

En ```forms.py``` se valida en servidor:
- Formato del dato
- Evita la duplicación de asientos con la misma cédula
- Controla integridad del asiento y fecha

**Código Incorporado:**

```python
def clean(self):
    cleaned = super().clean()
    bus = cleaned.get('bus')
    fecha = cleaned.get('fecha_viaje')
    asiento = cleaned.get('asiento')

    if bus and fecha and asiento:
        existe = bus.reservas.filter(
            fecha_viaje=fecha,
            asiento=asiento
        ).exists()

        if existe:
            raise forms.ValidationError(
                "Ese asiento ya está reservado para esa fecha."
            )
    return cleaned
```
➡ Esto garantiza que un usuario NO pueda crear reservas inválidas manipulando el HTML o desactivando el JS.

### 🏷️ 2. Manejo adecuado de Llaves Foráneas (Dropdown dependiente)
El sistema cumple el requerimiento de que una llave foránea no puede ser ingresada manualmente por medio de un campo de texto, sino que:
1. Debe seleccionarse desde un dropdown.
2. Si existe dependencia entre entidades, esta debe actualizarse dinámicamente.

**✔ Implementación realizada (Cooperativa → Bus)**

Cuando el usuario selecciona una Cooperativa, el sistema realiza una petición AJAX:
```javascript
fetch(`/panel/api/buses/?cooperativa_id=${coopId}`)
```
Y actualiza automáticamente el dropdown de Buses:
```html
<select name="bus" id="id_bus">
    <option value="">---------</option>
</select>
```
Esto evita por completo que el usuario ingrese manualmente un ID, garantizando integridad referencial.

**✔ Equivalente al ejemplo país → provincia → ciudad**

En este caso, se implementó:
- Cooperativa → Bus
- Bus → Reserva

Cumpliendo exactamente la especificación docente.

---

## 🧩 Arquitectura del Proyecto
### 📁 Estructura de carpetas
```
📦 administraci-nmvc/
 ┣ 📂 administracion/
 ┃ ┣ 📜 admin.py 
 ┃ ┣ 📜 apps.py
 ┃ ┣ 📜 forms.py
 ┃ ┣ 📜 models.py
 ┃ ┣ 📜 views.py
 ┃ ┣ 📜 tests.py
 ┃ ┣ 📂 views/
 ┃ ┃ ┣ 📜 admin_views.py
 ┃ ┃ ┣ 📜 api_views.py
 ┃ ┃ ┣ 📜 auth_views.py
 ┃ ┃ ┗ 📜 usuario_views.py
 ┃ ┗ 📂 templates/
 ┣ 📂 smartbus/
 ┃ ┣ 📜 asgi.py
 ┃ ┣ 📜 settings.py
 ┃ ┣ 📜 urls.py
 ┃ ┗ 📜 wsgi.py
 ┣ 📜 manage.py
 ┣ 📜 procfile.py
 ┣ 📜 db.sqlite3
 ┗ 📜 requirements.txt
```
### 🧱 Capas del sistema

**✔ Equivalente al ejemplo país → provincia → ciudad**
- Cooperativa
- Bus
- Ruta
- Reserva

Incluye integridad referencial y relaciones 1-N entre Cooperativa → Bus → Reserva.

**✔ Vistas (MVC)**
- ```auth_views.py``` → login / logout
- ```admin_views.py``` → administración
- ```usuario_views.py``` → panel usuario
- ```api_views.py``` → endpoints internos JSON

**✔ Templates**
Basados en herencia (```{% extends %}```), menús según rol y formularios Bootstrap-ready.

---

## 🚀 Despliegue en Render (Producción)
El sistema fue desplegado con éxito en Render utilizando:
- **Gunicorn** como servidor WSGI
- **SQLite** como base de datos en producción
- **Whitenoise** para estáticos

🌐 **URL del proyecto desplegado**  
👉 [https://administraci-nmvc.onrender.com](https://administraci-nmvc.onrender.com)

El despliegue incluye:
- Migraciones automatizadas
- Colección de estáticos
- Configuración de seguridad (```DEBUG=False```, ```ALLOWED_HOSTS```)

---

## 🛠️ Tecnologías Utilizadas
- **Python 3.x**
- **Django 5.x**
- **SQLite**
- **Gunicorn**
- **Whitenoise**
- **Render (PaaS)**
- **HTML, CSS, JS (AJAX)**
- **Django Template Engine**

---

## 📦 Instalación local
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Para crear un usuario administrador:
```bash
python manage.py createsuperuser
```

---

## 🎉 Conclusión

Este sistema:
- Implementa validación backend de un dato sensible
- Controla llaves foráneas mediante dropdowns y dependencias dinámicas
- Emplea arquitectura MVC modular
- Fue desplegado con éxito en Render
- Cumple completamente los requerimientos establecidos

---

## 🎥 Video demostrativo
[![Ver demostración breve del proyecto](https://img.youtube.com/vi/GZZM7JoW7Ww/hqdefault.jpg)](https://www.youtube.com/watch?v=GZZM7JoW7Ww)

---

## 👤 Autores

**Víctor A. Suquilanda** | **Roberto F. Guaña**  
📧 Carrera de Ing. Software | Proyecto Administración MVC  
📅 Año: 2025    

---