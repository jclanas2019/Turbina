## 💻 Generación de Plantillas

Turbina genera automáticamente plantillas HTML con Jinja2 según el tipo de módulo:

- **Básico**: Página simple con estructura mínima
- **Formulario**: Formulario completo con validación
- **CRUD**: Interfaz con tablas, formularios y operaciones CRUD
- **Dashboard**: Panel con widgets, gráficos y estadísticas

Las plantillas generadas:
- Extienden el layout base
- Utilizan TailwindCSS para estilos responsivos
- Incorporan componentes reutilizables de `widgets.html`
- Incluyen animaciones y transiciones adecuadas
- Están optimizadas para dispositivos móviles y de escritorio## 🧩 Widgets y Componentes Reutilizables

Turbina2 incluye una biblioteca completa de widgets y componentes UI reutilizables implementados como macros de Jinja2:

- **Widgets de datos**: `widget_card`, `reporte_card`, `data_table`
- **Widgets interactivos**: `login_modal`, `search_bar`, `form_input`, `toggle_switch`
- **Widgets de navegación**: `breadcrumb`, `accordion_item`
- **Widgets de visualización**: `chart_widget`, `calendar_widget`, `countdown_timer`
- **Componentes UI**: `notification_card`, `timeline_event`, `testimonial_card`, `team_member_card`
- **Componentes de marketing**: `pricing_card`, `feature_box`, `contact_form`, `faq_item`
- **Componentes de panel**: `dashboard_panel`

Todos los widgets se adaptan al esquema de color de tu aplicación y están diseñados para funcionar perfectamente con TailwindCSS.

### Uso de widgets

```html
{% import "widgets.html" as widgets %}

<!-- Tarjeta informativa -->
{{ widgets.widget_card(icon="📈", title="Ventas", value="$12,458", color="blue") }}

<!-- Tabla de datos -->
{{ widgets.data_table(headers=["ID", "Nombre", "Precio"], rows=productos, color="indigo") }}

<!-- Panel de dashboard -->
{{ widgets.dashboard_panel(title="Estadísticas", icon="📊", content=stats_content, color="green") }}
```# <img src="static/img/logo.jpg" alt="Logo Turbina" width="40" height="40" style="vertical-align: middle;"> Turbina

Un generador avanzado de módulos para aplicaciones FastAPI que acelera el desarrollo con scaffolding inteligente y generación de código asistida por IA.

## 🚀 Características
- Frontend liviano sin build
- Componentes Alpine.js (contador + formulario)
- Estilos responsivos con TailwindCSS (CDN)
- Backend rápido con FastAPI
- Generación de código con IA (mediante Ollama)
- Creación automatizada de módulos con diferentes patrones
- Componentes reutilizables con macros Jinja2
- Gestión completa del ciclo de vida de módulos

## 📋 Tipos de Módulos Soportados

Turbina2 permite crear diferentes tipos de módulos según tus necesidades:

- **Básico**: Módulo sencillo con un solo endpoint GET
- **Formulario**: Módulo con formulario y procesamiento POST
- **CRUD**: Módulo completo con operaciones API REST (Create, Read, Update, Delete)
- **Dashboard**: Panel de control con estadísticas y gráficos

## ▶️ Cómo correr

1. Instala dependencias:
```bash
pip install -r requirements.txt
```

2. Asegúrate de tener Ollama instalado y ejecutándose (opcional, para generación con IA):
```bash
# Instalar Ollama - visita https://ollama.com/
# Ejecutar el modelo gemma3
ollama run gemma3
```

3. Crea tu aplicación FastAPI inicial o usa una existente

4. Coloca turbina.py en la raíz de tu proyecto

5. Ejecuta turbina para ver las opciones disponibles:
```bash
python turbina.py --help
```

## 🛠️ Comandos Principales

### Crear un nuevo módulo
```bash
# Sintaxis básica
python turbina.py new modulo NOMBRE_MODULO --tipo TIPO --descripcion "Descripción del módulo"

# Ejemplos:
# Módulo básico
python turbina.py new modulo usuarios

# Módulo CRUD con modelo
python turbina.py new modulo productos --tipo crud --descripcion "Gestión de productos" --model

# Módulo de dashboard
python turbina.py new modulo estadisticas --tipo dashboard --descripcion "Panel de métricas"
```

### Listar módulos existentes
```bash
python turbina.py list
```

### Ver tipos de módulos disponibles
```bash
python turbina.py module-types
```

### Limpiar archivos huérfanos
```bash
# Detectar archivos huérfanos sin eliminar
python turbina.py clean

# Detectar y eliminar archivos huérfanos (con respaldo)
python turbina.py clean --delete
```

## 🗃️ Estructura de Proyecto Generada

Al crear un nuevo módulo, Turbina2 genera y actualiza los siguientes componentes:

- **Rutas**: `app/routes/NOMBRE_MODULO.py`
- **Vista/Lógica**: `app/views/NOMBRE_MODULO_data.py`
- **Plantilla**: `app/templates/NOMBRE_MODULO.html`
- **Modelo** (opcional): `app/models/NOMBRE_MODULO.py`
- **Widgets**: Acceso a todos los componentes definidos en `widgets.html`

Además, actualiza automáticamente:
- **main.py**: Registra las nuevas rutas
- **base.html**: Añade entradas al menú de navegación

## 🤖 Generación con IA

Turbina2 utiliza Ollama con el modelo Gemma3 para generar código inteligente basado en el tipo de módulo y la descripción proporcionada. La generación incluye:

- Rutas FastAPI con endpoints apropiados según el tipo
- Vistas con lógica de negocio
- Plantillas HTML con Jinja2
- Modelos SQLAlchemy con campos relevantes

Si Ollama no está disponible, se utilizarán plantillas básicas predefinidas.

## 🔄 Integración con FastAPI

El código generado sigue las mejores prácticas para FastAPI:
- Rutas organizadas con APIRouter
- Templating con Jinja2
- Modelado de datos con SQLAlchemy (opcional)
- Respuesta HTML y JSON según el tipo de módulo

## 🧹 Mantenimiento de Proyecto

Turbina2.py ofrece herramientas para mantener limpio tu proyecto:
- Detección de archivos huérfanos (templates, vistas, modelos sin rutas asociadas)
- Respaldo automático antes de eliminar
- Verificación de integridad entre rutas, vistas y plantillas

## ⚙️ Configuración

La configuración principal se encuentra en la clase `Config` dentro de turbina2.py. Puedes modificar:

- Rutas de directorios
- Modelo de IA utilizado
- URL base de Ollama
- Plantillas ignoradas
- Tipos de módulos disponibles

## 📚 Dependencias

- FastAPI
- Typer (para la CLI)
- Ollama (opcional, para generación con IA)
- Langchain (para interacción con LLM)
- SQLAlchemy (para modelos)
- Jinja2 (para plantillas)
- TailwindCSS (para estilos)

## 📝 Licencia

MIT

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para sugerencias, correcciones o mejoras.

---

Desarrollado con ❤️ para acelerar el desarrollo de aplicaciones FastAPI.