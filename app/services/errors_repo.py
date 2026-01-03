"""
Servicio para acceso a datos de errores
Implementa carga perezosa y cache simple para archivos JSON
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
#from functools import lru_cache


logger = logging.getLogger(__name__)


class ErrorsRepository:
    """
    Repositorio para manejar datos de errores desde archivos JSON
    """

    def __init__(self, errors_dir: Path):
        """
        Inicializa el repositorio con el directorio de errores

        Args:
            errors_dir: Path al directorio que contiene los archivos JSON de errores
        """
        self.errors_dir = errors_dir
        self._cache: Optional[Dict[str, Dict[str, Any]]] = None

    def _load_error_from_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Carga un error desde un archivo JSON con manejo de errores robusto

        Args:
            file_path: Path al archivo JSON

        Returns:
            Dict con datos del error o None si hay error
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validar que tenga id
            if 'id' not in data:
                logger.warning(f"Archivo {file_path} no tiene campo 'id', omitiendo")
                return None

            return data

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON en {file_path}: {e}")
            return None
        except FileNotFoundError:
            logger.error(f"Archivo no encontrado: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado cargando {file_path}: {e}")
            return None

    def _load_all_errors_uncached(self) -> Dict[str, Dict[str, Any]]:
        """
        Carga todos los errores desde archivos JSON sin usar cache

        Returns:
            Dict con todos los errores indexados por id
        """
        errors = {}

        if not self.errors_dir.exists():
            logger.warning(f"Directorio de errores no existe: {self.errors_dir}")
            return errors

        # Buscar archivos JSON
        for json_file in self.errors_dir.glob('*.json'):
            error_data = self._load_error_from_file(json_file)
            if error_data:
                error_id = error_data['id']
                errors[error_id] = error_data
                logger.debug(f"Cargado error: {error_id}")

        logger.info(f"Cargados {len(errors)} errores desde {self.errors_dir}")
        return errors

    @property
    def all_errors(self) -> Dict[str, Dict[str, Any]]:
        """
        Propiedad que carga y cachea todos los errores

        Returns:
            Dict con todos los errores
        """
        if self._cache is None:
            self._cache = self._load_all_errors_uncached()
        return self._cache

    def load_all_errors(self) -> List[Dict[str, Any]]:
        """
        Carga todos los errores

        Returns:
            Lista de todos los errores
        """
        return list(self.all_errors.values())

    def get_error_by_id(self, error_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un error específico por su ID

        Args:
            error_id: ID del error a buscar

        Returns:
            Dict con datos del error o None si no existe
        """
        return self.all_errors.get(error_id)

    def search_errors(self, query: str) -> List[Dict[str, Any]]:
        """
        Busca errores por título, tags o descripción

        Args:
            query: Término de búsqueda (case insensitive)

        Returns:
            Lista de errores que coinciden con la búsqueda
        """
        if not query:
            return self.load_all_errors()

        query_lower = query.lower()
        results = []

        for error in self.all_errors.values():
            # Buscar en título
            if 'titulo' in error and query_lower in error['titulo'].lower():
                results.append(error)
                continue

            # Buscar en tags
            if 'metadata' in error and 'tags' in error['metadata']:
                tags = error['metadata']['tags']
                if any(query_lower in tag.lower() for tag in tags):
                    results.append(error)
                    continue

            # Buscar en descripción corta
            if 'descripcion_corta' in error and query_lower in error['descripcion_corta'].lower():
                results.append(error)
                continue

            # Buscar en curso, tema, subtema
            searchable_fields = ['curso', 'tema', 'subtema']
            for field in searchable_fields:
                if field in error and query_lower in str(error[field]).lower():
                    results.append(error)
                    break

        return results

    def clear_cache(self):
        """
        Limpia el cache para forzar recarga en la próxima consulta
        """
        self._cache = None
        logger.info("Cache de errores limpiado")


# Instancia global del repositorio (se inicializará en la aplicación)
_errors_repo: Optional[ErrorsRepository] = None


def get_errors_repo() -> ErrorsRepository:
    """
    Obtiene la instancia global del repositorio de errores
    Debe inicializarse con init_errors_repo() primero

    Returns:
        Instancia del repositorio

    Raises:
        RuntimeError: Si el repositorio no ha sido inicializado
    """
    if _errors_repo is None:
        raise RuntimeError("Errors repository not initialized. Call init_errors_repo() first.")
    return _errors_repo


def init_errors_repo(errors_dir: Path) -> ErrorsRepository:
    """
    Inicializa el repositorio global de errores

    Args:
        errors_dir: Path al directorio de errores

    Returns:
        Instancia inicializada del repositorio
    """
    global _errors_repo
    _errors_repo = ErrorsRepository(errors_dir)
    logger.info(f"Repositorio de errores inicializado con directorio: {errors_dir}")
    return _errors_repo
