// Botones rápidos del módulo y crédito discreto MR- en la pestaña de Ajustes de Foundry.
import { ID, t } from "./estado.mjs";
import { abrirPizarra } from "./integraciones.mjs";

export function registrarAjustesUI(api) {
  Hooks.on("renderSettings", (_app, html) => {
    if (!game.user.isGM) return;
    const root = html instanceof HTMLElement ? html : html[0];
    if (!root || root.querySelector(".mrsd-settings-box")) return;

    const sec = document.createElement("section");
    sec.className = "mrsd-settings-box";
    sec.innerHTML = `
      <h4 class="divider">MR- El Simulacro Desatado</h4>
      <div class="mrsd-settings-btns">
        <button type="button" data-mrsd="panel"><i class="fa-solid fa-train"></i> ${t("Ajustes.BotonPanel")}</button>
        <button type="button" data-mrsd="pizarra"><i class="fa-solid fa-thumbtack"></i> ${t("Ajustes.BotonPizarra")}</button>
        <button type="button" data-mrsd="reimportar"><i class="fa-solid fa-file-import"></i> ${t("Ajustes.BotonReimportar")}</button>
      </div>
      <p class="mrsd-credit">Módulo preparado por <strong>Manu Romera</strong> (serie <code>MR-</code>).</p>`;

    sec.querySelector('[data-mrsd="panel"]')?.addEventListener("click", () => api.panel());
    sec.querySelector('[data-mrsd="pizarra"]')?.addEventListener("click", () => abrirPizarra());
    sec.querySelector('[data-mrsd="reimportar"]')?.addEventListener("click", () => api.importarAventura({ confirmar: true }));

    const destino = root.querySelector(".settings-sidebar, #settings-game") ?? root;
    destino.appendChild(sec);
  });
}
