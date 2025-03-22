import typer
import os
import zipfile
import datetime
from pathlib import Path

app = typer.Typer()
new_app = typer.Typer()
app.add_typer(new_app, name="new")


class Config:
    """Clase para centralizar la configuración de rutas y directorios"""
    BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATES_DIR = BASE_DIR / "app/templates"
    ROUTES_DIR = BASE_DIR / "app/routes"
    VIEWS_DIR = BASE_DIR / "app/views"
    MAIN_FILE_PATH = BASE_DIR / "app/main.py"
    BASE_TEMPLATE_PATH = TEMPLATES_DIR / "base.html"
    BACKUP_DIR = BASE_DIR / "backup_deleted"
    IGNORED_TEMPLATES = {"base", "home", "widgets"}


class FileManager:
    """Clase para gestionar operaciones de archivos"""
    
    @staticmethod
    def ensure_dir_exists(directory: Path):
        """Asegura que un directorio exista"""
        directory.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def read_file(file_path: Path):
        """Lee un archivo y devuelve su contenido"""
        try:
            return file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"❌ Error al leer {file_path}: {str(e)}")
            return ""
    
    @staticmethod
    def read_lines(file_path: Path):
        """Lee un archivo y devuelve sus líneas"""
        try:
            return file_path.open("r+", encoding="utf-8").readlines()
        except Exception as e:
            print(f"❌ Error al leer {file_path}: {str(e)}")
            return []
    
    @staticmethod
    def write_file(file_path: Path, content: str):
        """Escribe contenido en un archivo"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            return True
        except Exception as e:
            print(f"❌ Error al escribir {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def write_lines(file_path: Path, lines: list):
        """Escribe líneas en un archivo"""
        try:
            with file_path.open("w", encoding="utf-8") as file:
                file.writelines(lines)
            return True
        except Exception as e:
            print(f"❌ Error al escribir {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def create_backup(files: list, backup_dir: Path):
        """Crea un backup de archivos en formato zip"""
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


class ModuleManager:
    """Clase para gestionar los módulos de la aplicación"""
    
    @staticmethod
    def create_route_file(modulo: str, routes_path: Path):
        """Crea el archivo de rutas para un módulo"""
        content = f"""from fastapi import APIRouter, Request
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
        if FileManager.write_file(routes_path, content):
            print(f"✅ Ruta creada: app/routes/{modulo}.py")
            return True
        return False
    
    @staticmethod
    def create_view_file(modulo: str, views_path: Path):
        """Crea el archivo de vistas para un módulo"""
        content = f"""def get_context():
    return {{
        "title": "{modulo.capitalize()}",
        "message": "Este es el módulo {modulo} generado automáticamente."
    }}
"""
        if FileManager.write_file(views_path, content):
            print(f"✅ Vista creada: app/views/{modulo}_data.py")
            return True
        return False
    
    @staticmethod
    def create_template_file(template_path: Path):
        """Crea el archivo de plantilla para un módulo"""
        content = """{% extends 'base.html' %}

{% block content %}
<h1 class="title">{{ title }}</h1>
<p>{{ message }}</p>
{% endblock %}
"""
        if FileManager.write_file(template_path, content):
            print(f"✅ Template creada: {template_path}")
            return True
        return False
    
    @staticmethod
    def update_main_file(modulo: str, main_file_path: Path):
        """Actualiza el archivo main.py para incluir el nuevo módulo"""
        if not main_file_path.exists():
            print("⚠️ No se encontró main.py para actualizar.")
            return False
        
        content = FileManager.read_lines(main_file_path)
        if not content:
            return False
        
        import_line = f"from app.routes import {modulo}\n"
        router_line = f"app.include_router({modulo}.router)\n"
        
        # Verificar si las líneas ya existen
        if import_line not in content:
            # Buscar dónde insertar la importación
            for i, line in enumerate(content):
                if line.startswith("from app.routes import"):
                    content.insert(i + 1, import_line)
                    break
            else:
                content.insert(0, import_line)
        
        if router_line not in content:
            # Buscar dónde insertar el router
            for i, line in enumerate(content):
                if line.startswith("app.include_router("):
                    content.insert(i + 1, router_line)
                    break
            else:
                content.append("\n" + router_line)
        
        return FileManager.write_lines(main_file_path, content)
    
    @staticmethod
    def update_menu(modulo: str, base_template_path: Path):
        """Actualiza el menú en base.html para incluir el nuevo módulo"""
        if not base_template_path.exists():
            print("⚠️ No se encontró base.html para actualizar.")
            return False
        
        lines = FileManager.read_lines(base_template_path)
        if not lines:
            return False
        
        entry = f'        <li><a href="/{modulo}">{modulo.capitalize()}</a></li>\n'
        if entry in lines:
            return True
        
        # Buscar dónde insertar la entrada del menú
        for i, line in enumerate(lines):
            if "</ul>" in line:
                lines.insert(i, entry)
                break
        
        return FileManager.write_lines(base_template_path, lines)


class Commands:
    """Clase para implementar los comandos de la CLI"""
    
    @staticmethod
    @new_app.command("modulo")
    def create_module(modulo: str):
        """Crea un nuevo módulo base (ruta + vista + plantilla) y lo integra en el sistema"""
        routes_path = Config.ROUTES_DIR / f"{modulo}.py"
        views_path = Config.VIEWS_DIR / f"{modulo}_data.py"
        template_path = Config.TEMPLATES_DIR / f"{modulo}.html"
        
        # Asegurar que los directorios existan
        FileManager.ensure_dir_exists(Config.ROUTES_DIR)
        FileManager.ensure_dir_exists(Config.VIEWS_DIR)
        FileManager.ensure_dir_exists(template_path.parent)
        
        # Crear archivos si no existen
        if not routes_path.exists():
            ModuleManager.create_route_file(modulo, routes_path)
        else:
            print("⚠️ Ruta ya existe")
        
        if not views_path.exists():
            ModuleManager.create_view_file(modulo, views_path)
        else:
            print("⚠️ Vista ya existe")
        
        if not template_path.exists():
            ModuleManager.create_template_file(template_path)
        else:
            print("⚠️ Template ya existe")
        
        # Actualizar main.py y menú
        ModuleManager.update_main_file(modulo, Config.MAIN_FILE_PATH)
        ModuleManager.update_menu(modulo, Config.BASE_TEMPLATE_PATH)
    
    @staticmethod
    @app.command()
    def list():
        """Lista todos los módulos registrados en `app/routes/` y verifica su integración"""
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
            print(f"📌 {status} {modulo}")
        
        print("\n✅ Revisión finalizada.")
    
    @staticmethod
    @app.command()
    def clean(delete: bool = False):
        """
        Limpia módulos huérfanos y opcionalmente los elimina con respaldo automático (si se usa --delete)
        """
        print("\n🧹 **Limpieza de Módulos y Archivos Huérfanos**")
        
        existing_modules = {p.stem for p in Config.ROUTES_DIR.glob("*.py") if p.stem != "__init__"}
        templates = {p.stem for p in Config.TEMPLATES_DIR.glob("*.html")}
        views = {p.stem.replace("_data", "") for p in Config.VIEWS_DIR.glob("*_data.py")}
        
        orphan_templates = (templates - existing_modules) - Config.IGNORED_TEMPLATES
        orphan_views = views - existing_modules
        orphan_routes = existing_modules - templates
        
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
        
        # Backup antes de eliminar
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
    app()