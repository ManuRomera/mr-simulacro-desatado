import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { estadoPorDefecto, normalizarEstado, contarPartes, ID } from "../scripts/estado.mjs";

const ROOT = path.resolve(import.meta.dirname, "..");

test("estado puro: normalización y recuento de partes", () => {
  const base = estadoPorDefecto();
  assert.equal(base.dia, 1);
  assert.equal(base.reino, "real");
  assert.equal(contarPartes(base), 0);

  const norm = normalizarEstado({ dia: 99, reino: "invalido", victimas: { roti: true, walters: true } });
  assert.equal(norm.dia, 5);
  assert.equal(norm.reino, "real");
  assert.equal(contarPartes(norm), 2);
});

test("aventura.json: estructura, IDs, macros y rutas de assets", () => {
  const advs = JSON.parse(fs.readFileSync(path.join(ROOT, "_data/aventura.json"), "utf8"));
  assert.equal(advs.length, 1);
  const adv = advs[0];
  assert.equal(adv.actors.length, 17);
  assert.equal(adv.scenes.length, 7);
  assert.equal(adv.journal.length, 8);
  assert.equal(adv.playlists.length, 2);
  assert.equal(adv.tables.length, 1);
  assert.equal(adv.macros.length, 3);

  // Todos los macros llevan author válido no nulo (requisito Foundry v13/v14)
  for (const m of adv.macros) {
    assert.ok(typeof m.author === "string" && m.author.length === 16, `Macro sin author válido: ${m.name}`);
  }

  // Verificar que todos los assets referenciados bajo modules/<ID>/ existen en disco
  const raw = JSON.stringify(adv);
  const prefix = `modules/${ID}/`;
  const re = new RegExp(`${prefix}[^"\\\\<\\s]+`, "g");
  const rutas = [...new Set(raw.match(re) ?? [])];
  assert.ok(rutas.length > 40, `Demasiadas pocas rutas de assets (${rutas.length})`);
  for (const r of rutas) {
    const rel = r.slice(prefix.length);
    const abs = path.join(ROOT, rel);
    assert.ok(fs.existsSync(abs), `Asset faltante: ${rel}`);
  }
});

test("paquete de MR- Dirección: esquema correcto y toda referencia existe en la aventura", async () => {
  const dir = JSON.parse(fs.readFileSync(path.join(ROOT, "content/direccion-es.json"), "utf8"));
  const adv = JSON.parse(fs.readFileSync(path.join(ROOT, "_data/aventura.json"), "utf8"))[0];
  assert.equal(dir.id, ID);

  // Slugs de cada colección (los sonidos viven dentro de las listas)
  const slug = (d) => d.flags?.[ID]?.slug;
  const slugs = new Set([
    ...["scenes", "actors", "journal", "playlists"].flatMap((k) => adv[k].map(slug)),
    ...adv.playlists.flatMap((p) => p.sounds.map(slug)),
  ].filter(Boolean));
  const paginas = new Set(adv.journal.flatMap((j) => j.pages.map((p) => `JournalEntry.${j._id}.JournalEntryPage.${p._id}`)));
  const comprobar = (ref, donde) => {
    if (ref?.flag) assert.ok(slugs.has(ref.flag[2]), `${donde}: slug inexistente «${ref.flag[2]}»`);
    else if (ref?.uuid) assert.ok(paginas.has(ref.uuid), `${donde}: página inexistente ${ref.uuid}`);
    else assert.fail(`${donde}: referencia vacía`);
  };

  const g = dir.settings;
  assert.deepEqual(g.effects, [], "los efectos van por escena, no en la barra global");
  assert.ok(g.markers.milestones.length && g.markers.clocks.length, "hitos y relojes dentro de settings.markers");
  g.motifs.forEach((m) => comprobar(m.music, `motivo ${m.id}`));

  const motivos = new Set(g.motifs.map((m) => m.id));
  assert.deepEqual(new Set(dir.scenes.map((s) => s.ref.flag[2])), new Set(adv.scenes.map(slug)), "todas las escenas configuradas");
  for (const s of dir.scenes) {
    const n = s.ref.flag[2];
    comprobar(s.ref, n); comprobar(s.reading, `${n}.reading`); comprobar(s.music, `${n}.music`);
    s.motifs.forEach((m) => assert.ok(motivos.has(m), `${n}: motivo desconocido ${m}`));
    s.cues.forEach((c) => comprobar(c.sound, `${n}.cue`));
    s.figures.forEach((f) => comprobar(f.ref, `${n}.figura`));
    s.handouts.forEach((h) => comprobar(h.ref, `${n}.ayuda`));
  }

  // Si MR- Dirección está instalado al lado, se usa su propio validador
  const schema = path.join(ROOT, "../mr-direccion/js/core/schema.mjs");
  if (fs.existsSync(schema)) {
    const { validatePack } = await import(schema);
    const r = validatePack(dir);
    assert.deepEqual([r.errors, r.warnings], [[], []]);
  }
});

test("paquete de MR- Pizarra válido", () => {
  const piz = JSON.parse(fs.readFileSync(path.join(ROOT, "content/pizarra-es.json"), "utf8"));
  assert.equal(piz.format, "mr-pizarra-import");
  assert.ok(piz.layers.length === 5);
  assert.ok(piz.items.length >= 12);
});
