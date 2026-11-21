// Panel del Guardián (ApplicationV2) · MR- El Simulacro Desatado
import { ID, esc, t, estado, actualizarEstado, estadoPorDefecto, contarPartes, VICTIMAS_BASE, TRAMAS_BASE, RECOMPENSAS_COR } from "./estado.mjs";
import { aplicarModo } from "./compat.mjs";
import { abrirPizarra } from "./integraciones.mjs";

const { ApplicationV2 } = foundry.applications.api;
const STORAGE_KEY = `${ID}:panel-ui`;

const ESCENAS_RAPIDAS = [
  { slug: "portada", label: "00 · Orient Express" },
  { slug: "budapest", label: "01 · Budapest" },
  { slug: "coches-mesa", label: "02 · Coches F y G (Mesa)" },
  { slug: "coches-guardian", label: "03 · Coches F y G (GM)" },
  { slug: "estambul-mesa", label: "04 · Estambul (Mesa)" },
  { slug: "estambul-guardian", label: "05 · Estambul (GM)" },
  { slug: "mezquita", label: "06 · Mezquita Velada" },
];

const AYUDAS_LISTA = [
  { slug: "ayuda-1", label: "Ayuda 1 · Perfil: John Milton" },
  { slug: "ayuda-2", label: "Ayuda 2 · Menú (La Carte)" },
  { slug: "ayuda-3", label: "Ayuda 3 · Itinerario del OE" },
  { slug: "ayuda-4", label: "Ayuda 4 · Carta con recortes" },
  { slug: "ayuda-5", label: "Ayuda 5 · Nota de cita para Chantel" },
  { slug: "ayuda-6", label: "Ayuda 6 · Diario de John Milton" },
];

export class PanelGuardian extends ApplicationV2 {
  static #instancia = null;

  static DEFAULT_OPTIONS = {
    id: "mr-simulacro-panel",
    classes: ["mrsd-panel"],
    tag: "section",
    window: {
      title: "MRSD.Panel.Titulo",
      icon: "fa-solid fa-train",
      resizable: true,
    },
    position: { width: 560, height: 680 },
    actions: {
      tab: PanelGuardian.#cambiarTab,
      dia: PanelGuardian.#fijarDia,
      reino: PanelGuardian.#fijarReino,
      victima: PanelGuardian.#alternarVictima,
      trama: PanelGuardian.#alternarTrama,
      recompensa: PanelGuardian.#lanzarRecompensa,
      escena: PanelGuardian.#activarEscena,
      ayuda: PanelGuardian.#mostrarAyuda,
      guia: PanelGuardian.#abrirGuia,
      actor: PanelGuardian.#abrirActor,
      eco: PanelGuardian.#tirarEco,
      pizarra: PanelGuardian.#abrirPizarra,
      reiniciar: PanelGuardian.#reiniciar,
    },
  };

  constructor(options = {}) {
    let guardado = {};
    try { guardado = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "{}"); } catch {}
    super({ ...options, position: { ...PanelGuardian.DEFAULT_OPTIONS.position, ...(guardado.pos ?? {}) } });
    this._tab = guardado.tab ?? "viaje";
  }

  static abrir() {
    if (!game.user.isGM) return ui.notifications.warn(t("SoloGM"));
    this.#instancia ??= new PanelGuardian();
    this.#instancia.render({ force: true });
    return this.#instancia;
  }

  static refrescar() {
    if (this.#instancia?.rendered) this.#instancia.render();
  }

  _guardarUI() {
    try {
      const { left, top, width, height } = this.position;
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ tab: this._tab, pos: { left, top, width, height } }));
    } catch {}
  }

  setPosition(pos) {
    const res = super.setPosition(pos);
    this._guardarUI();
    return res;
  }

  async _renderHTML() {
    const est = estado();
    const partes = contarPartes(est);
    const tabs = [
      ["viaje", t("Panel.TabViaje"), "fa-compass"],
      ["ayudas", t("Panel.TabAyudas"), "fa-scroll"],
      ["reparto", t("Panel.TabReparto"), "fa-users"],
    ];

    const navHtml = tabs.map(([id, lbl, ico]) => `
      <button type="button" class="mrsd-tab ${this._tab === id ? "activa" : ""}" data-action="tab" data-tab="${id}">
        <i class="fa-solid ${ico}"></i> <span>${esc(lbl)}</span>
      </button>`).join("");

    let cuerpo = "";
    if (this._tab === "viaje") {
      const dias = [1, 2, 3, 4, 5].map((d) =>
        `<button type="button" class="mrsd-pill ${est.dia === d ? "activa" : ""}" data-action="dia" data-dia="${d}">Día ${d}</button>`
      ).join("");
      const reinos = [
        ["real", t("Panel.ReinoReal")],
        ["otro", t("Panel.ReinoOtro")],
        ["mezquita", t("Panel.ReinoMezquita")],
      ].map(([r, lbl]) =>
        `<button type="button" class="mrsd-pill ${est.reino === r ? "activa" : ""}" data-action="reino" data-reino="${r}">${esc(lbl)}</button>`
      ).join("");

      const listaVictimas = VICTIMAS_BASE.map((v) => {
        const marcada = Boolean(est.victimas[v.id]);
        return `
          <button type="button" class="mrsd-check-row ${marcada ? "hecha" : ""}" data-action="victima" data-id="${v.id}">
            <i class="fa-solid ${marcada ? "fa-skull" : "fa-circle"}"></i>
            <span class="mrsd-v-nom"><strong>${v.orden}. ${esc(v.nombre)}</strong> · ${esc(v.parte)}</span>
            <span class="mrsd-v-meta">${esc(v.coche)} · ${esc(v.nicho)}</span>
          </button>`;
      }).join("");

      const escenas = ESCENAS_RAPIDAS.map((e) =>
        `<button type="button" class="mrsd-btn-sec" data-action="escena" data-slug="${e.slug}">${esc(e.label)}</button>`
      ).join("");

      cuerpo = `
        <div class="mrsd-bloque">
          <div class="mrsd-fila-titulo"><span>Cronología del trayecto</span><span class="mrsd-badge">${partes}/6 partes reunidas</span></div>
          <div class="mrsd-pills">${dias}</div>
          <div class="mrsd-pills">${reinos}</div>
        </div>
        <div class="mrsd-bloque">
          <div class="mrsd-fila-titulo"><span>Plan de John Milton · Simulacro de Carne</span></div>
          <div class="mrsd-lista">${listaVictimas}</div>
        </div>
        <div class="mrsd-bloque">
          <div class="mrsd-fila-titulo"><span>Escenas rápidas</span></div>
          <div class="mrsd-grid-2">${escenas}</div>
        </div>`;
    } else if (this._tab === "ayudas") {
      const ayudas = AYUDAS_LISTA.map((a) => `
        <div class="mrsd-ayuda-row">
          <span>${esc(a.label)}</span>
          <button type="button" class="mrsd-btn-mini" data-action="ayuda" data-slug="${a.slug}">
            <i class="fa-solid fa-eye"></i> Mostrar
          </button>
        </div>`).join("");

      const tramas = TRAMAS_BASE.map((x) => {
        const ok = Boolean(est.tramas[x.id]);
        return `
          <button type="button" class="mrsd-check-row ${ok ? "hecha" : ""}" data-action="trama" data-id="${x.id}">
            <i class="fa-solid ${ok ? "fa-square-check" : "fa-square"}"></i>
            <span>${esc(x.label)}</span>
          </button>`;
      }).join("");

      cuerpo = `
        <div class="mrsd-bloque">
          <div class="mrsd-fila-titulo"><span>Ayudas de juego (mostrar a los jugadores)</span></div>
          <div class="mrsd-lista">${ayudas}</div>
        </div>
        <div class="mrsd-bloque">
          <div class="mrsd-fila-titulo"><span>Hitos y pistas descubiertas</span></div>
          <div class="mrsd-lista">${tramas}</div>
        </div>`;
    } else {
      const grupos = [
        ["ganadores", "Ganadores de Lux-Vista"],
        ["pasajeros", "Otros pasajeros"],
        ["personal", "Personal del tren"],
        ["antagonistas", "Antagonistas y amenazas"],
      ];
      const repartoHtml = grupos.map(([cat, tit]) => {
        const acts = game.actors.filter((a) => a.getFlag(ID, "categoria") === cat);
        if (!acts.length) return "";
        const btns = acts.map((a) => `
          <button type="button" class="mrsd-actor-btn" data-action="actor" data-id="${a.id}">
            <img src="${esc(a.prototypeToken?.texture?.src || a.img)}" alt="" />
            <span>${esc(a.name)}</span>
          </button>`).join("");
        return `<div class="mrsd-subtitulo">${esc(tit)}</div><div class="mrsd-grid-2">${btns}</div>`;
      }).join("");

      const recs = RECOMPENSAS_COR.map((r) => {
        const dada = Boolean(est.recompensas[r.id]);
        return `
          <button type="button" class="mrsd-check-row ${dada ? "hecha" : ""}" data-action="recompensa" data-id="${r.id}">
            <i class="fa-solid ${dada ? "fa-check-double" : "fa-dice-d6"}"></i>
            <span><strong>+${r.formula.toUpperCase()} COR</strong> · ${esc(r.label)}</span>
          </button>`;
      }).join("");

      cuerpo = `
        <div class="mrsd-bloque">
          <div class="mrsd-fila-titulo"><span>Dramatis Personae</span></div>
          ${repartoHtml || "<p class='mrsd-vacio'>Importa la aventura al mundo para abrir las fichas directamente desde aquí.</p>"}
        </div>
        <div class="mrsd-bloque">
          <div class="mrsd-fila-titulo"><span>Recompensas de Cordura (tirar al chat)</span></div>
          <div class="mrsd-lista">${recs}</div>
        </div>`;
    }

    const wrap = document.createElement("div");
    wrap.className = "mrsd-wrap";
    wrap.innerHTML = `
      <header class="mrsd-cabecera">
        <div class="mrsd-atajos">
          <button type="button" class="mrsd-btn-prim" data-action="guia"><i class="fa-solid fa-book-open"></i> Guía del Guardián</button>
          <button type="button" class="mrsd-btn-sec" data-action="eco"><i class="fa-solid fa-ghost"></i> Eco del Otro Lado</button>
          <button type="button" class="mrsd-btn-sec" data-action="pizarra"><i class="fa-solid fa-thumbtack"></i> Pizarra</button>
        </div>
        <nav class="mrsd-tabs">${navHtml}</nav>
      </header>
      <div class="mrsd-cuerpo">${cuerpo}</div>
      <footer class="mrsd-pie">
        <span>Horror en el Orient Express · Estambul 2013</span>
        <button type="button" class="mrsd-btn-link" data-action="reiniciar"><i class="fa-solid fa-rotate-left"></i> ${esc(t("Panel.Reiniciar"))}</button>
      </footer>`;
    return wrap;
  }

  _replaceHTML(result, content) {
    content.replaceChildren(result);
  }

  static #cambiarTab(_ev, target) {
    this._tab = target.dataset.tab;
    this._guardarUI();
    this.render();
  }

  static async #fijarDia(_ev, target) {
    const dia = Number(target.dataset.dia);
    await actualizarEstado((e) => ({ ...e, dia }));
  }

  static async #fijarReino(_ev, target) {
    const reino = target.dataset.reino;
    await actualizarEstado((e) => ({ ...e, reino }));
  }

  static async #alternarVictima(_ev, target) {
    const id = target.dataset.id;
    await actualizarEstado((e) => { e.victimas[id] = !e.victimas[id]; return e; });
  }

  static async #alternarTrama(_ev, target) {
    const id = target.dataset.id;
    await actualizarEstado((e) => { e.tramas[id] = !e.tramas[id]; return e; });
  }

  static async #lanzarRecompensa(_ev, target) {
    const rec = RECOMPENSAS_COR.find((r) => r.id === target.dataset.id);
    if (!rec) return;
    await actualizarEstado((e) => { e.recompensas[rec.id] = true; return e; });
    const roll = await new Roll(rec.formula).evaluate();
    const data = aplicarModo({
      speaker: { alias: "El Simulacro desatado · Recompensa de COR" },
      content: `<div class="mrsd-chat-card"><h3>+${roll.total} puntos de Cordura</h3><p>${esc(rec.label)}</p><p class="mrsd-chat-sub">Fórmula: ${rec.formula.toUpperCase()}</p></div>`,
      rolls: [roll],
    });
    await ChatMessage.create(data);
  }

  static async #activarEscena(_ev, target) {
    const sc = game.scenes.find((s) => s.getFlag(ID, "slug") === target.dataset.slug);
    if (!sc) return ui.notifications.warn("Escena no encontrada en el mundo. Importa la aventura primero.");
    await sc.activate();
  }

  static async #mostrarAyuda(_ev, target) {
    await game.modules.get(ID)?.api?.mostrarAyuda(target.dataset.slug);
  }

  static #abrirGuia() {
    const j = game.journal.find((x) => x.getFlag(ID, "guia"));
    if (!j) return ui.notifications.warn("Importa la aventura primero para abrir la Guía del Guardián.");
    j.sheet.render({ force: true });
  }

  static #abrirActor(_ev, target) {
    game.actors.get(target.dataset.id)?.sheet?.render({ force: true });
  }

  static async #tirarEco() {
    await game.modules.get(ID)?.api?.tirarEco();
  }

  static async #abrirPizarra() {
    await abrirPizarra();
  }

  static async #reiniciar() {
    const ok = await foundry.applications.api.DialogV2.confirm({
      window: { title: t("Panel.Reiniciar"), icon: "fa-solid fa-rotate-left" },
      content: `<p>${esc(t("Panel.ConfirmarReinicio"))}</p>`,
      rejectClose: false,
    });
    if (ok) await actualizarEstado(() => estadoPorDefecto());
  }
}
