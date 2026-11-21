// Integraciones opcionales con MR- Dirección y MR- Pizarra.
import { ID, t, ruta } from "./estado.mjs";

let direccionRegistrada = false;

export async function registrarDireccion(api = game.modules.get("mr-direccion")?.api) {
  if (!api?.registerPack || direccionRegistrada) return;
  try {
    const pack = await (await fetch(ruta("content/direccion-es.json"))).json();
    api.registerPack(pack);
    direccionRegistrada = true;
  } catch (e) {
    console.error(`${ID} | no se pudo registrar el paquete de MR- Dirección`, e);
  }
}

Hooks.on("mrDireccion.ready", (api) => registrarDireccion(api));

const NOMBRE_PIZARRA = () => t("Integ.NombrePizarra");

export async function abrirPizarra() {
  const api = game.modules.get("mr-pizarra")?.api;
  if (!api) return ui.notifications.warn(t("Integ.PizarraNo"));
  const hecha = game.journal.find((j) => j.flags?.["mr-pizarra"]?.board && j.name === NOMBRE_PIZARRA());
  if (hecha) return api.open(hecha);
  const json = await (await fetch(ruta("content/pizarra-es.json"))).text();
  await api.importBoard(null);
  for (let i = 0; i < 40; i++) {
    const area = document.querySelector("#mr-pizarra-import .mrp-paste");
    if (area) {
      area.value = json;
      area.dispatchEvent(new Event("input", { bubbles: true }));
      return ui.notifications.info(t("Integ.PizarraLista"));
    }
    await new Promise((r) => setTimeout(r, 50));
  }
}
