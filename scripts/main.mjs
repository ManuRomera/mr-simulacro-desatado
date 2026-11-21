// MR- El Simulacro Desatado · Arranque, importación, barra de herramientas, API y macros.
import { ID, PACK, esc, t, soyGM } from "./estado.mjs";
import { aplicarModo } from "./compat.mjs";
import { PanelGuardian } from "./panel.mjs";
import { registrarDireccion, abrirPizarra } from "./integraciones.mjs";
import { registrarAjustesUI } from "./mr-credits.mjs";

Hooks.once("init", () => {
  game.settings.register(ID, "estado", {
    scope: "world",
    config: false,
    type: Object,
    default: {},
    onChange: () => PanelGuardian.refrescar(),
  });
  game.settings.register(ID, "modoMundo", {
    scope: "world",
    config: false,
    type: String,
    default: "", // "" | "todo" | "compendios"
  });
});

function mundoVacio() {
  const sinDocs = ["actors", "items", "journal", "playlists", "macros", "tables", "cards"].every((c) => !game[c]?.size);
  return sinDocs && game.scenes.contents.every((s) => s.background?.src?.startsWith("nue/") && !s.tokens.size);
}

async function asignarMacrosBarra() {
  const macros = game.macros.filter((m) => m.getFlag(ID, "macro"));
  for (const m of macros) {
    if (!game.users.has(m.author?.id)) await m.update({ author: game.user.id });
  }
  // Colocar las macros del módulo en huecos libres de la barra rápida del Guardián
  const hotbar = game.user.hotbar ?? {};
  const yaPuestas = new Set(Object.values(hotbar));
  let slot = 1;
  for (const m of macros) {
    if (yaPuestas.has(m.id)) continue;
    while (hotbar[slot] && slot <= 10) slot++;
    if (slot <= 10) {
      await game.user.assignHotbarMacro(m, slot);
      slot++;
    }
  }
}

export async function importarAventura({ confirmar = true } = {}) {
  if (!game.user.isGM) return ui.notifications.warn(t("SoloGM"));
  const pack = game.packs.get(PACK);
  if (!pack) return ui.notifications.error(t("Importar.SinPack"));
  if (confirmar && !mundoVacio()) {
    const ok = await foundry.applications.api.DialogV2.confirm({
      window: { title: t("Importar.Titulo"), icon: "fa-solid fa-file-import" },
      content: `<p>${esc(t("Importar.Aviso"))}</p>`,
      yes: { label: t("Importar.Si"), icon: "fa-solid fa-file-import" },
      no: { label: t("Cancelar") },
      rejectClose: false,
    });
    if (!ok) return;
  }
  ui.notifications.info(t("Importar.Empieza"));
  const adv = (await pack.getDocuments())[0];
  await adv.import({ dialog: false });
  await game.settings.set(ID, "modoMundo", "todo");
  await asignarMacrosBarra();
  await registrarDireccion();
  // Con MR- Dirección, que active ella: así su música manda y la nativa no queda sonando debajo.
  const portada = game.scenes.find((s) => s.getFlag(ID, "orden") === 0);
  const dir = game.modules.get("mr-direccion")?.active && game.modules.get("mr-direccion").api;
  if (portada) await (dir?.dispatch ? dir.dispatch("activate", portada.id) : portada.activate());
  ui.notifications.info(t("Importar.Hecho"));
  game.journal.find((j) => j.getFlag(ID, "guia"))?.sheet.render({ force: true });
}

export async function mostrarAyuda(slug) {
  if (!game.user.isGM) return ui.notifications.warn(t("SoloGM"));
  const j = game.journal.find((x) => x.getFlag(ID, "slug") === slug);
  if (!j) return ui.notifications.warn("Ayuda de juego no encontrada en el mundo. Importa la aventura primero.");
  await j.sheet.render({ force: true });
  await Journal.show(j, { force: true });
}

export async function tirarEco() {
  if (!game.user.isGM) return ui.notifications.warn(t("SoloGM"));
  const tabla = game.tables.find((x) => x.getFlag(ID, "slug") === "ecos-otro-lado");
  if (!tabla) return ui.notifications.warn("Tabla de Ecos del Otro Lado no encontrada. Importa la aventura primero.");
  const res = await tabla.draw({ displayChat: false });
  const txt = res.results?.[0]?.text ?? "";
  const data = aplicarModo({
    speaker: { alias: "El Otro Lado · Eco del pasado" },
    whisper: ChatMessage.getWhisperRecipients("GM"),
    content: `<div class="mrsd-chat-card"><h3>Eco del Otro Lado (1D6 min)</h3><p>${esc(txt)}</p></div>`,
    rolls: res.roll ? [res.roll] : [],
  });
  await ChatMessage.create(data);
}

const API = {
  importarAventura,
  panel: () => PanelGuardian.abrir(),
  mostrarAyuda,
  tirarEco,
  abrirPizarra,
};

Hooks.once("ready", async () => {
  game.modules.get(ID).api = API;
  registrarDireccion();
  registrarAjustesUI(API);

  if (!game.user.isGM) return;
  await asignarMacrosBarra();

  if (soyGM() && !game.settings.get(ID, "modoMundo") && mundoVacio()) {
    const eleccion = await foundry.applications.api.DialogV2.wait({
      window: { title: t("Importar.Titulo"), icon: "fa-solid fa-train" },
      content: `<p>${esc(t("Importar.Pregunta"))}</p>`,
      buttons: [
        { action: "todo", label: t("Importar.Todo"), icon: "fa-solid fa-file-import", default: true },
        { action: "compendios", label: t("Importar.Compendios"), icon: "fa-solid fa-box-archive" },
      ],
      rejectClose: false,
    });
    if (eleccion === "todo") {
      await importarAventura({ confirmar: false });
    } else if (eleccion === "compendios") {
      await game.settings.set(ID, "modoMundo", "compendios");
    }
  }
});

Hooks.on("getSceneControlButtons", (controls) => {
  if (!game.user.isGM) return;
  const herr = (name, title, icon, fn) => ({ name, title, icon, button: true, visible: true, onChange: () => fn() });
  const tools = [
    herr("panel", "MRSD.Barra.Panel", "fa-solid fa-book-open", API.panel),
    herr("eco", "MRSD.Barra.Eco", "fa-solid fa-ghost", API.tirarEco),
    herr("pizarra", "MRSD.Barra.Pizarra", "fa-solid fa-thumbtack", API.abrirPizarra),
  ];
  controls.mrsd = {
    name: "mrsd",
    title: "MRSD.Barra.Titulo",
    icon: "fa-solid fa-train",
    order: 92,
    visible: true,
    activeTool: "",
    tools: Object.fromEntries(tools.map((x, i) => [x.name, { ...x, order: i }])),
  };
});
