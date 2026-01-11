"""
Agente Remediador Mínimo para Week 01 - CIED

Este módulo implementa un sistema de remediación determinístico basado en
patrones de error identificados. No utiliza LLMs ni dependencias externas.
"""

from enum import Enum
from typing import Dict, Optional


class RemediationAction(Enum):
    """Acciones de remediación disponibles para errores pedagógicos."""
    REINFORCE = "reinforce"  # Reforzar conceptos básicos
    RETRY = "retry"        # Permitir reintento inmediato
    HALT = "halt"          # Detener y requerir intervención


def remediate(error_id: str, context: Optional[Dict] = None) -> Dict:
    """
    Determina la acción de remediación apropiada para un error específico.

    Esta función implementa una lógica determinística basada en patrones
    identificados en los errores de Week 01. No requiere acceso a bases
    de datos externas ni LLMs.

    Args:
        error_id: Identificador único del error cometido
        context: Contexto adicional (opcional, no utilizado en esta versión)

    Returns:
        Dict con las claves:
        - "action": RemediationAction (REINFORCE, RETRY, o HALT)
        - "reason": Explicación de por qué se eligió esta acción
    """
    # Lógica determinística basada en patrones de error
    if "innecesaria" in error_id.lower():
        return {
            "action": RemediationAction.REINFORCE,
            "reason": "Error indica falta de comprensión conceptual básica. Se requiere reforzar fundamentos antes de continuar."
        }

    if "antiderivada" in error_id.lower() or "derivada" in error_id.lower():
        return {
            "action": RemediationAction.RETRY,
            "reason": "Error en cálculo algebraico o aplicación de reglas. Permitir reintento inmediato con explicación específica."
        }

    # Caso por defecto: errores críticos o no clasificados
    return {
        "action": RemediationAction.HALT,
        "reason": "Error requiere análisis pedagógico detallado. Se detiene el progreso hasta revisión del docente."
    }