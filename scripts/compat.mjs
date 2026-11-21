// Capa de compatibilidad Foundry VTT v13 / v14 (regla de la casa MR-)

/** Devuelve el modo de mensaje/tirada activo sin lanzar error en v13. */
export function modoMensaje() {
  for (const k of ["messageMode", "rollMode"]) {
    try { return game.settings.get("core", k); } catch { /* clave no registrada en esta versión */ }
  }
  return CONST.DICE_ROLL_MODES?.PUBLIC ?? "publicroll";
}

/** Aplica el modo de mensaje/tirada al objeto ChatMessage compatible con v13 y v14. */
export function aplicarModo(data, modo = modoMensaje()) {
  if (typeof ChatMessage.applyMode === "function") return ChatMessage.applyMode(data, modo);
  if (typeof ChatMessage.applyRollMode === "function") return ChatMessage.applyRollMode(data, modo);
  return data;
}
