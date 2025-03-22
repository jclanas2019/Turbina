#!/usr/bin/env python3
import typer
import os
import zipfile
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import re
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import OllamaLLM

app = typer.Typer()
new_app = typer.Typer()
app.add_typer(new_app, name="new")

class Config:
    BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATES_DIR = BASE_DIR / "app/templates"
    ROUTES_DIR = BASE_DIR / "app/routes"
    VIEWS_DIR = BASE_DIR / "app/views"
    MODELS_DIR = BASE_DIR / "app/models"
    MAIN_FILE_PATH = BASE_DIR / "app/main.py"
    BASE_TEMPLATE_PATH = TEMPLATES_DIR / "base.html"
    BACKUP_DIR = BASE_DIR / "backup_deleted"
    IGNORED_TEMPLATES = {"base", "home", "widgets"}
    OLLAMA_MODEL = "gemma3"
    OLLAMA_BASE_URL = "http://localhost:11434"
    MODULE_TYPES = {
        "basic": "Módulo básico con un solo endpoint GET",
        "form": "Módulo con formulario y procesamiento POST",
        "crud": "Módulo CRUD completo con API REST",
        "dashboard": "Panel de control con estadísticas y gráficos"
    }

class FileManager:
    @staticmethod
    def ensure_dir_exists(directory: Path):
        directory.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def read_file(file_path: Path):
        try:
            return file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"❌ Error al leer {file_path}: {str(e)}")
            return ""
    
    @staticmethod
    def read_lines(file_path: Path):
        try:
            return file_path.open("r+", encoding="utf-8").readlines()
        except Exception as e:
            print(f"❌ Error al leer {file_path}: {str(e)}")
            return []
    
    @staticmethod
    def write_file(file_path: Path, content: str):
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            return True
        except Exception as e:
            print(f"❌ Error al escribir {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def write_lines(file_path: Path, lines: list):
        try:
            with file_path.open("w", encoding="utf-8") as file:
                file.writelines(lines)
            return True
        except Exception as e:
            print(f"❌ Error al escribir {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def create_backup(files: list, backup_dir: Path):
        backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = backup_dir / f"backup_clean_{timestamp}.zip"
        try:
            with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file in files:
                    arcname = file.relative_to(Config.BASE_DIR)
                    zipf.write(file, arcname)
            print(f"\n🗂 Archivos respaldados en: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ Error al crear backup: {str(e)}")
            return False

class CodeCleaner:
    @staticmethod
    def clean_markdown_code_blocks(content):
        content = re.sub(r'```\w*\n', '', content)
        content = re.sub(r'```', '', content)
        content = re.sub(r'`{1,3}', '', content)
        return content.strip()
    
    @staticmethod
    def verify_no_markdown(content):
        if '```' in content or '`python' in content or '`html' in content:
            return CodeCleaner.clean_markdown_code_blocks(content)
        return content
    
    @staticmethod
    def verify_router(content: str) -> str:
        if "router = APIRouter()" not in content:
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if line.startswith("from ") or line.startswith("import "):
                    continue
                lines.insert(i + 1, "router = APIRouter()\n")
                break
            else:
                lines.insert(0, "from fastapi import APIRouter\nrouter = APIRouter()\n")
            content = "\n".join(lines)
        return content
    
    @staticmethod
    def fix_imports(content: str, modulo: str) -> str:
        invalid_import = re.compile(r'from\s*\.\s*import\s*app\.views\.' + re.escape(modulo) + r'_data')
        if invalid_import.search(content):
            content = invalid_import.sub(f'from app.views import {modulo}_data', content)
        if f'from app.views import {modulo}_data' not in content:
            lines = content.splitlines()
            lines.insert(0, f'from app.views import {modulo}_data\n')
            content = "\n".join(lines)
        return content
    
    @staticmethod
    def fix_jinja2templates(content: str) -> str:
        content = re.sub(r'Jinja2Templates\(directory_path=', 'Jinja2Templates(directory=', content)
        return content
    
    @staticmethod
    def fix_template_response(content: str, modulo: str) -> str:
        content = re.sub(r'TemplateResponse\("[^"]+"', f'TemplateResponse("{modulo}.html"', content)
        return content
    
    @staticmethod
    def validate_python_content(content: str, modulo: str) -> str:
        if not content or "def get_context()" not in content or modulo not in content:
            return f"""def get_context():
    return {{
        "title": "{modulo.capitalize()}",
        "message": "Este es el módulo {modulo} generado automáticamente."
    }}
"""
        return content

class LLMGenerator:
    def __init__(self):
        try:
            self.llm = OllamaLLM(model=Config.OLLAMA_MODEL, base_url=Config.OLLAMA_BASE_URL)
            self.parser = JsonOutputParser()
        except Exception as e:
            print(f"⚠️ Error al inicializar Ollama: {e}")
            print("⚠️ Se usarán plantillas básicas en su lugar.")
            self.llm = None
    
    def _generate_content(self, prompt_text):
        if not self.llm:
            return None
        try:
            response = self.llm.invoke(prompt_text)
            cleaned_response = CodeCleaner.verify_no_markdown(response)
            return cleaned_response
        except Exception as e:
            print(f"⚠️ Error al generar con LLM: {e}")
            return None
    
    def generate_routes(self, modulo: str, module_type: str, description: str) -> str:
        prompt = f"""
        Genera el código Python para un archivo de rutas FastAPI.
        Detalles del módulo:
        - Nombre: {modulo}
        - Tipo: {module_type}
        - Descripción: {description}
        Requisitos:
        - Debe ser compatible con FastAPI
        - DEBE importar las vistas EXACTAMENTE como 'from app.views import {modulo}_data' (NO usar otras formas)
        - Debe usar Jinja2Templates con 'directory=TEMPLATES_DIR' (NO usar 'directory_path')
        - Debe definir un router con 'router = APIRouter()'
        - Debe incluir un endpoint GET en la ruta '/{modulo}' que renderice '{modulo}.html' usando TemplateResponse
        - El endpoint debe pasar el contexto desde '{modulo}_data.get_context()' y agregar 'request' al contexto
        - Para tipos CRUD debe incluir endpoints GET, POST, PUT, DELETE
        - Para tipos form debe incluir manejo de formularios POST
        - El nombre del módulo {modulo} debe conservar el nombre original del usuario que es {modulo}
        MUY IMPORTANTE: No incluyas marcadores de código como ```python o ``` en tu respuesta.
        Devuelve solo el código Python puro sin ningún tipo de formato markdown.
        Código Python:
        """
        response = self._generate_content(prompt)
        if not response:
            return None
        response = CodeCleaner.verify_no_markdown(response)
        response = CodeCleaner.verify_router(response)
        response = CodeCleaner.fix_imports(response, modulo)
        response = CodeCleaner.fix_jinja2templates(response)
        response = CodeCleaner.fix_template_response(response, modulo)
        return response
    
    def generate_views(self, modulo: str, module_type: str, description: str) -> str:
        prompt = f"""
        Genera el código Python para un archivo de vistas/datos usado por FastAPI.
        Detalles del módulo:
        - Nombre: {modulo}
        - Tipo: {module_type}
        - Descripción: {description}
        Requisitos:
        - El nombre del archivo será {modulo}_data.py
        - Debe contener al menos la función get_context() que devuelve un diccionario
        - Para tipo CRUD, incluir funciones create_item, update_item, delete_item, get_items
        - Para tipo dashboard, incluir funciones que generen datos para gráficos y estadísticas
        - Para tipo form, incluir funciones para procesar formularios
        - El nombre del módulo {modulo} debe conservar el nombre original del usuario que es {modulo}
        MUY IMPORTANTE: No incluyas marcadores de código como ```python o ``` en tu respuesta.
        Devuelve solo el código Python puro sin ningún tipo de formato markdown.
        Código Python:
        """
        response = self._generate_content(prompt)
        if not response or "def get_context()" not in response:
            return None
        response = CodeCleaner.verify_no_markdown(response)
        response = CodeCleaner.validate_python_content(response, modulo)
        return response
    
    def generate_template(self, modulo: str, module_type: str, description: str) -> str:
        prompt = f"""
        Genera el código HTML para una plantilla Jinja2 de FastAPI.
        Detalles del módulo:
        - Nombre: {modulo}
        - Tipo: {module_type}
        - Descripción: {description}
        Requisitos:
        - Debe extender de 'base.html' usando la sintaxis: {{% extends 'base.html' %}}
        - Debe usar el bloque content: {{% block content %}} ... {{% endblock %}}
        - Debe mostrar las variables 'title' y 'message' del contexto si están presentes
        - Para tipo CRUD, incluir tabla y formularios para crear/editar/eliminar
        - Para tipo dashboard, incluir elementos para gráficos y estadísticas
        - Para tipo form, incluir un formulario con validación del lado del cliente
        - Usar bulma.min.css para los estilos
        MUY IMPORTANTE: No incluyas marcadores de código como ```html o ``` en tu respuesta.
        Devuelve solo el código HTML puro sin ningún tipo de formato markdown.
        Código HTML:
        """
        response = self._generate_content(prompt)
        if not response:
            return None
        if response:
            response = response.replace('{{% ', '{% ').replace(' %}}', ' %}')
            response = CodeCleaner.verify_no_markdown(response)
        return response
    
    def generate_model(self, modulo: str, description: str) -> str:
        prompt = f"""
        Genera el código Python para un modelo SQLAlchemy basado en esta descripción.
        Detalles del módulo:
        - Nombre: {modulo}
        - Descripción: {description}
        Requisitos:
        - Debe ser compatible con SQLAlchemy y FastAPI
        - Debe tener al menos 3-5 campos relevantes para el modelo
        - Debe incluir tipos de datos apropiados
        - Debe incluir relaciones si son pertinentes
        - Debe incluir campos de fecha de creación y actualización
        MUY IMPORTANTE: No incluyas marcadores de código como ```python o ``` en tu respuesta.
        Devuelve solo el código Python puro sin ningún tipo de formato markdown.
        Código Python:
        """
        response = self._generate_content(prompt)
        if not response:
            return None
        return CodeCleaner.verify_no_markdown(response)

class ModuleManager:
    def __init__(self):
        self.llm_generator = LLMGenerator()
    
    def create_route_file(self, modulo: str, routes_path: Path, module_type: str, description: str):
        try:
            content = self.llm_generator.generate_routes(modulo, module_type, description)
            if content and FileManager.write_file(routes_path, content):
                print(f"✅ Ruta creada: app/routes/{modulo}.py")
                return True
            else:
                raise Exception("No se pudo generar contenido con LLM")
        except Exception as e:
            print(f"❌ Error al generar rutas: {str(e)}")
            content = self._create_basic_route(modulo)
            if FileManager.write_file(routes_path, content):
                print(f"⚠️ Usada plantilla básica para ruta: app/routes/{modulo}.py")
                return True
            return False
    
    def create_view_file(self, modulo: str, views_path: Path, module_type: str, description: str):
        try:
            content = self.llm_generator.generate_views(modulo, module_type, description)
            if content and FileManager.write_file(views_path, content):
                print(f"✅ Vista creada: app/views/{modulo}_data.py")
                return True
            else:
                raise Exception("No se pudo generar contenido válido con LLM")
        except Exception as e:
            print(f"❌ Error al generar vistas: {str(e)}")
            content = self._create_basic_view(modulo)
            if FileManager.write_file(views_path, content):
                print(f"⚠️ Usada plantilla básica para vista: app/views/{modulo}_data.py")
                return True
            return False
    
    def create_template_file(self, modulo: str, template_path: Path, module_type: str, description: str):
        try:
            content = self.llm_generator.generate_template(modulo, module_type, description)
            if content and FileManager.write_file(template_path, content):
                print(f"✅ Template creada: {template_path}")
                return True
            else:
                raise Exception("No se pudo generar contenido con LLM")
        except Exception as e:
            print(f"❌ Error al generar template: {str(e)}")
            content = self._create_basic_template()
            if FileManager.write_file(template_path, content):
                print(f"⚠️ Usada plantilla básica para template: {template_path}")
                return True
            return False
    
    def create_model_file(self, modulo: str, model_path: Path, description: str):
        try:
            content = self.llm_generator.generate_model(modulo, description)
            if content and FileManager.write_file(model_path, content):
                print(f"✅ Modelo creado: app/models/{modulo}.py")
                return True
            else:
                raise Exception("No se pudo generar contenido con LLM")
        except Exception as e:
            print(f"❌ Error al generar modelo: {str(e)}")
            content = self._create_basic_model(modulo)
            if FileManager.write_file(model_path, content):
                print(f"⚠️ Usada plantilla básica para modelo: app/models/{modulo}.py")
                return True
            return False
    
    def update_main_file(self, modulo: str, main_file_path: Path):
        if not main_file_path.exists():
            print("⚠️ No se encontró main.py para actualizar.")
            return False
        content = FileManager.read_lines(main_file_path)
        if not content:
            return False
        import_line = f"from app.routes import {modulo}\n"
        router_line = f"app.include_router({modulo}.router)\n"
        if import_line not in content:
            for i, line in enumerate(content):
                if line.startswith("from app.routes import"):
                    content.insert(i + 1, import_line)
                    break
            else:
                content.insert(0, import_line)
        if router_line not in content:
            for i, line in enumerate(content):
                if line.startswith("app.include_router("):
                    content.insert(i + 1, router_line)
                    break
            else:
                content.append("\n" + router_line)
        # Eliminar duplicados de app.include_router
        seen = set()
        new_content = []
        for line in content:
            if line.startswith("app.include_router(") and line in seen:
                continue
            seen.add(line)
            new_content.append(line)
        return FileManager.write_lines(main_file_path, new_content)
    
    def update_menu(self, modulo: str, base_template_path: Path):
        if not base_template_path.exists():
            print("⚠️ No se encontró base.html para actualizar.")
            return False
        lines = FileManager.read_lines(base_template_path)
        if not lines:
            return False
        entry = f'        <li><a href="/{modulo}">{modulo.capitalize()}</a></li>\n'
        if entry in lines:
            return True
        for i, line in enumerate(lines):
            if "</ul>" in line:
                lines.insert(i, entry)
                break
        # Corregir la ruta de bulma.min.css
        for i, line in enumerate(lines):
            if 'href="bulma.min.css"' in line:
                lines[i] = line.replace('href="bulma.min.css"', 'href="/static/css/bulma.min.css"')
                break
        return FileManager.write_lines(base_template_path, lines)
    
    def _create_basic_route(self, modulo: str) -> str:
        return f"""from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.views import {modulo}_data
import os

router = APIRouter()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/{modulo}", response_class=HTMLResponse)
async def {modulo}_view(request: Request):
    context = {modulo}_data.get_context()
    context["request"] = request
    return templates.TemplateResponse("{modulo}.html", context)
"""
    
    def _create_basic_view(self, modulo: str) -> str:
        return f"""def get_context():
    return {{
        "title": "{modulo.capitalize()}",
        "message": "Este es el módulo {modulo} generado automáticamente."
    }}
"""
    
    def _create_basic_template(self) -> str:
        return """{% extends 'base.html' %}

{% block content %}
<div class="container">
    <h1 class="title">{{ title }}</h1>
    <p class="subtitle">{{ message }}</p>
</div>
{% endblock %}
"""
    
    def _create_basic_model(self, modulo: str) -> str:
        return f"""from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class {modulo.capitalize()}(Base):
    __tablename__ = "{modulo}"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<{modulo.capitalize()}(id={{self.id}}, nombre={{self.nombre}})>"
"""

class Commands:
    @staticmethod
    @app.command()
    def module_types():
        print("\n📊 **Tipos de Módulos Disponibles**")
        for type_key, description in Config.MODULE_TYPES.items():
            print(f"📌 {type_key}: {description}")
    
    @staticmethod
    @new_app.command("modulo")
    def create_module(
        modulo: str, 
        tipo: str = typer.Option("basic", help="Tipo de módulo a crear"),
        descripcion: str = typer.Option("", help="Descripción del módulo"),
        model: bool = typer.Option(False, help="Crear modelo SQLAlchemy")
    ):
        if tipo not in Config.MODULE_TYPES:
            print(f"❌ Tipo de módulo '{tipo}' no válido. Usa el comando 'module-types' para ver los disponibles.")
            return
        routes_path = Config.ROUTES_DIR / f"{modulo}.py"
        views_path = Config.VIEWS_DIR / f"{modulo}_data.py"
        template_path = Config.TEMPLATES_DIR / f"{modulo}.html"
        model_path = Config.MODELS_DIR / f"{modulo}.py"
        if not descripcion:
            descripcion = f"Módulo {tipo} para gestionar {modulo}"
        FileManager.ensure_dir_exists(Config.ROUTES_DIR)
        FileManager.ensure_dir_exists(Config.VIEWS_DIR)
        FileManager.ensure_dir_exists(template_path.parent)
        if model:
            FileManager.ensure_dir_exists(Config.MODELS_DIR)
        module_manager = ModuleManager()
        if not routes_path.exists():
            module_manager.create_route_file(modulo, routes_path, tipo, descripcion)
        else:
            print("⚠️ Ruta ya existe")
        if not views_path.exists():
            module_manager.create_view_file(modulo, views_path, tipo, descripcion)
        else:
            print("⚠️ Vista ya existe")
        if not template_path.exists():
            module_manager.create_template_file(modulo, template_path, tipo, descripcion)
        else:
            print("⚠️ Template ya existe")
        if model and not model_path.exists():
            module_manager.create_model_file(modulo, model_path, descripcion)
        module_manager.update_main_file(modulo, Config.MAIN_FILE_PATH)
        module_manager.update_menu(modulo, Config.BASE_TEMPLATE_PATH)
    
    @staticmethod
    @app.command()
    def list():
        print("\n📂 **Listado de Módulos Registrados**")
        if not Config.ROUTES_DIR.exists():
            print("❌ No se encontró la carpeta de rutas.")
            return
        existing_modules = {p.stem for p in Config.ROUTES_DIR.glob("*.py") if p.stem != "__init__"}
        if not existing_modules:
            print("⚠️ No hay módulos registrados.")
            return
        main_content = FileManager.read_file(Config.MAIN_FILE_PATH)
        base_content = FileManager.read_file(Config.BASE_TEMPLATE_PATH)
        for modulo in sorted(existing_modules):
            status = "✅"
            if f"from app.routes import {modulo}" not in main_content or f"app.include_router({modulo}.router)" not in main_content:
                status = "⚠️ Falta en main.py"
            if f'<a href="/{modulo}">' not in base_content:
                status = "⚠️ Falta en menú"
            model_path = Config.MODELS_DIR / f"{modulo}.py"
            model_status = "Con modelo" if model_path.exists() else "Sin modelo"
            print(f"📌 {status} {modulo} ({model_status})")
        print("\n✅ Revisión finalizada.")
    
    @staticmethod
    @app.command()
    def clean(delete: bool = False):
        print("\n🧹 **Limpieza de Módulos y Archivos Huérfanos**")
        existing_modules = {p.stem for p in Config.ROUTES_DIR.glob("*.py") if p.stem != "__init__"}
        templates = {p.stem for p in Config.TEMPLATES_DIR.glob("*.html")}
        views = {p.stem.replace("_data", "") for p in Config.VIEWS_DIR.glob("*_data.py")}
        models = {p.stem for p in Config.MODELS_DIR.glob("*.py") if p.stem != "__init__"}
        orphan_templates = (templates - existing_modules) - Config.IGNORED_TEMPLATES
        orphan_views = views - existing_modules
        orphan_routes = existing_modules - templates
        orphan_models = models - existing_modules
        files_to_delete = []
        if orphan_templates:
            print("\n⚠️ Templates huérfanos:")
            for name in orphan_templates:
                print(f"   - {name}.html")
                files_to_delete.append(Config.TEMPLATES_DIR / f"{name}.html")
        if orphan_views:
            print("\n⚠️ Vistas huérfanas:")
            for name in orphan_views:
                print(f"   - {name}_data.py")
                files_to_delete.append(Config.VIEWS_DIR / f"{name}_data.py")
        if orphan_routes:
            print("\n⚠️ Rutas sin template correspondiente:")
            for name in orphan_routes:
                print(f"   - {name}.py")
                files_to_delete.append(Config.ROUTES_DIR / f"{name}.py")
        if orphan_models:
            print("\n⚠️ Modelos huérfanos:")
            for name in orphan_models:
                print(f"   - {name}.py")
                files_to_delete.append(Config.MODELS_DIR / f"{name}.py")
        if delete and files_to_delete:
            if FileManager.create_backup(files_to_delete, Config.BACKUP_DIR):
                for file in files_to_delete:
                    try:
                        file.unlink()
                        print(f"   ✅ Eliminado: {file.relative_to(Config.BASE_DIR)}")
                    except Exception as e:
                        print(f"   ❌ Error al eliminar {file}: {str(e)}")
        if not files_to_delete:
            print("\n✅ Sin elementos huérfanos. Todo está limpio.")
        else:
            if delete:
                print("\n🗑 Limpieza completada. Archivos eliminados tras respaldo.")
            else:
                print("\n⚠️ Limpieza completada con advertencias. Usa --delete para limpiar y respaldar.")

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║                                                        ║
    ║  TURBINA2 - Generador avanzado de módulos para FastAPI ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
    """)
    app()