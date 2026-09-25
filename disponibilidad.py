"""
Módulo de disponibilidad (E3) — Reserva de Laboratorios
========================================================
Lógica formal de no-solapamiento: una reserva es válida si y solo si no
existe intersección temporal con ninguna reserva CONFIRMADA del mismo
laboratorio físico.

Invariante / criterio de aceptación (PMBOK):
    disponibilidad(lab, [inicio, fin))  <=>  ¬∃ r ∈ Reservas(lab):
        r.estado = CONFIRMADA  ∧  max(r.inicio, inicio) < min(r.fin, fin)
"""
from __future__ import annotations

from typing import Iterable, Mapping

ESTADO_CONFIRMADA = "CONFIRMADA"


def verificar_disponibilidad(
    reservas_existentes: Iterable[Mapping[str, object]],
    lab_id: str,
    inicio,
    fin,
) -> bool:
    """Verifica que el intervalo [inicio, fin) esté libre para el laboratorio.

    Args:
        reservas_existentes: lista de reservas registradas (dicts con
            claves ``lab_id``, ``inicio``, ``fin`` y ``estado``).
        lab_id: identificador físico del laboratorio consultado.
        inicio, fin: extremos del intervalo solicitado (objetos datetime
            comparables; se exige inicio < fin).

    Returns:
        ``True`` si el horario está disponible; ``False`` en caso de
        cruce parcial, inclusión total o intervalo inválido.
    """
    if inicio >= fin:
        return False

    for r in reservas_existentes:
        # Solo las reservas CONFIRMADAS del mismo laboratorio restringen
        # la disponibilidad (las canceladas liberan el horario).
        if r["lab_id"] == lab_id and r["estado"] == ESTADO_CONFIRMADA:
            if max(r["inicio"], inicio) < min(r["fin"], fin):
                return False

    return True