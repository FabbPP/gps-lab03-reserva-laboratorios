"""
Pruebas unitarias del módulo de disponibilidad (E3).
Ejecutar con: pytest -v
Casos: horario libre, cruce parcial superior, cruce parcial inferior,
inclusión total, laboratorios diferentes y reservas previamente canceladas.
"""
from datetime import datetime

import pytest

from disponibilidad import ESTADO_CONFIRMADA, verificar_disponibilidad


def dt(hora: int, minuto: int = 0) -> datetime:
    return datetime(2026, 9, 28, hora, minuto)


# Escenario base: LAB-01 ocupado de 09:00-11:00 (CONFIRMADA) y de
# 14:00-16:00 (CANCELADA); LAB-02 sin reservas.
RESERVAS = [
    {"lab_id": "LAB-01", "inicio": dt(9, 0), "fin": dt(11, 0), "estado": ESTADO_CONFIRMADA},
    {"lab_id": "LAB-01", "inicio": dt(14, 0), "fin": dt(16, 0), "estado": "CANCELADA"},
]


def test_horario_libre():
    """Horario completamente libre => True."""
    assert verificar_disponibilidad(RESERVAS, "LAB-01", dt(11, 0), dt(13, 0)) is True


def test_cruce_parcial_superior():
    """Inicia antes del fin de la reserva confirmada => False."""
    assert verificar_disponibilidad(RESERVAS, "LAB-01", dt(10, 0), dt(12, 0)) is False


def test_cruce_parcial_inferior():
    """Finaliza después del inicio de la reserva confirmada => False."""
    assert verificar_disponibilidad(RESERVAS, "LAB-01", dt(8, 0), dt(10, 0)) is False


def test_inclusion_total():
    """Intervalo solicitado contenido íntegramente en la reserva => False."""
    assert verificar_disponibilidad(RESERVAS, "LAB-01", dt(9, 30), dt(10, 30)) is False


def test_laboratorios_diferentes():
    """Mismo horario en otro laboratorio físico => True (sin colisión)."""
    assert verificar_disponibilidad(RESERVAS, "LAB-02", dt(9, 0), dt(11, 0)) is True


def test_reservas_previamente_canceladas():
    """Una reserva CANCELADA no bloquea el horario => True."""
    assert verificar_disponibilidad(RESERVAS, "LAB-01", dt(14, 30), dt(15, 30)) is True


def test_intervalo_invalido():
    """Inicio posterior o igual al fin => False (invariante temporal)."""
    assert verificar_disponibilidad(RESERVAS, "LAB-01", dt(13, 0), dt(13, 0)) is False
    assert verificar_disponibilidad(RESERVAS, "LAB-01", dt(13, 0), dt(12, 0)) is False