// Estado persistente de campaña para el Guardián + utilidades puras del módulo.
export const ID = "mr-simulacro-desatado";
export const PACK = `${ID}.aventura`;

export const esc = (s) => foundry.utils.escapeHTML(String(s ?? ""));
export const t = (k, d) => (d ? game.i18n.format(`MRSD.${k}`, d) : game.i18n.localize(`MRSD.${k}`));
export const ruta = (p) => `modules/${ID}/${p}`;
export const soyGM = () => game.user === game.users.activeGM;

export const VICTIMAS_BASE = [
  { id: "roti", orden: 1, nombre: "Giuseppe Roti", parte: "Brazo izquierdo", nicho: "4.º nicho", coche: "Coche G" },
  { id: "walters", orden: 2, nombre: "John Walters", parte: "Brazo derecho", nicho: "2.º nicho", coche: "Coche G" },
  { id: "banuelos", orden: 3, nombre: "Enzo Bañuelos", parte: "Pierna izquierda", nicho: "6.º nicho", coche: "Coche F" },
  { id: "griffin", orden: 4, nombre: "Oscar Griffin", parte: "Pierna derecha", nicho: "5.º nicho", coche: "Coche F" },
  { id: "gonzaga", orden: 5, nombre: "Faustino Gonzaga", parte: "Torso", nicho: "3.º nicho", coche: "Coche F" },
  { id: "descendiente", orden: 6, nombre: "PJ descendiente (o Abella)", parte: "Cabeza", nicho: "1.º nicho", coche: "Coche F" },
];

export const TRAMAS_BASE = [
  { id: "chantel", label: "Chantel Antin pide auxilio (Laberinto de Buda)" },
  { id: "wilson", label: "Mark Wilson se revela como el acosador" },
  { id: "abella", label: "Descubren la identidad de Angelo Minotti" },
  { id: "camisas", label: "Hallan las camisas robadas / ensangrentadas" },
  { id: "tiza", label: "Descubren las marcas de tiza roja bajo las camas" },
  { id: "diario23", label: "Encuentran el diario de 1923 (Museo Británico)" },
  { id: "diarioMilton", label: "Encuentran el diario de John Milton" },
  { id: "portal", label: "Portal a la Mezquita Velada abierto (1D4 h)" },
];

export const RECOMPENSAS_COR = [
  { id: "evitar6", formula: "1d6", label: "Evitar que Milton cometa los seis asesinatos" },
  { id: "evitarSuicidio", formula: "1d6", label: "Evitar que Milton se suicide y complete el Ritual de restauración" },
  { id: "evitarUnion", formula: "1d4", label: "Evitar que las partes del cuerpo se unan en el Simulacro" },
  { id: "capturarMilton", formula: "1d4", label: "Capturar a Milton y entregarlo a las autoridades" },
  { id: "destruirSimulacro", formula: "1d6", label: "Destruir el Simulacro de Carne activado" },
  { id: "salvarChantel", formula: "1d4", label: "Salvar a Chantel Antin de su acosador, Mark Wilson" },
  { id: "entregarMinotti", formula: "1d4", label: "Descubrir a Angelo Minotti y entregarlo a las autoridades" },
];

export function estadoPorDefecto() {
  return {
    dia: 1,
    reino: "real", // real | otro | mezquita
    victimas: Object.fromEntries(VICTIMAS_BASE.map((v) => [v.id, false])),
    tramas: Object.fromEntries(TRAMAS_BASE.map((x) => [x.id, false])),
    recompensas: Object.fromEntries(RECOMPENSAS_COR.map((x) => [x.id, false])),
  };
}

/** Función pura para fusionar estado guardado con el esquema base (testeable con node --test). */
export function normalizarEstado(raw) {
  const base = estadoPorDefecto();
  if (!raw || typeof raw !== "object") return base;
  return {
    dia: Math.min(5, Math.max(1, Number(raw.dia) || 1)),
    reino: ["real", "otro", "mezquita"].includes(raw.reino) ? raw.reino : "real",
    victimas: { ...base.victimas, ...(raw.victimas ?? {}) },
    tramas: { ...base.tramas, ...(raw.tramas ?? {}) },
    recompensas: { ...base.recompensas, ...(raw.recompensas ?? {}) },
  };
}

export function contarPartes(est) {
  const v = est?.victimas ?? {};
  return VICTIMAS_BASE.filter((x) => Boolean(v[x.id])).length;
}

export function estado() {
  return normalizarEstado(game.settings.get(ID, "estado"));
}

export async function actualizarEstado(fn) {
  if (!game.user.isGM) return ui.notifications.warn(t("SoloGM"));
  const next = normalizarEstado(fn(structuredClone(estado())));
  await game.settings.set(ID, "estado", next);
  return next;
}
