// Compila _data/aventura.json a packs/aventura (LevelDB, Adventure) y empaqueta dist/mr-simulacro-desatado.zip
import fs from "node:fs/promises";
import { createWriteStream } from "node:fs";
import { ClassicLevel } from "classic-level";
import archiver from "archiver";

const manifest = JSON.parse(await fs.readFile("module.json"));
manifest.download = `${manifest.url}/releases/download/v${manifest.version}/${manifest.id}.zip`;
await fs.writeFile("module.json", JSON.stringify(manifest, null, 2) + "\n");

for (const pack of manifest.packs ?? []) {
  await fs.rm(pack.path, { recursive: true, force: true });
  const db = new ClassicLevel(pack.path, { valueEncoding: "json" });
  const docs = JSON.parse(await fs.readFile(`_data/${pack.name}.json`));
  for (const d of docs) await db.put(`!adventures!${d._id}`, d);
  await db.close();
  console.log(`pack ${pack.name}: ${docs.length} aventura(s)`);
}

await fs.mkdir("dist", { recursive: true });
const zipPath = `dist/${manifest.id}.zip`;
const out = createWriteStream(zipPath);
const zip = archiver("zip", { zlib: { level: 9 } });
zip.pipe(out);
const done = new Promise((res, rej) => {
  out.on("close", res);
  out.on("error", rej);
  zip.on("error", rej);
});

for (const p of ["module.json", "scripts", "styles", "lang", "packs", "assets", "content", "README.md", "CHANGELOG.md", "NOTICE.md"]) {
  try {
    const st = await fs.stat(p);
    if (st.isDirectory()) zip.directory(p, p);
    else zip.file(p, { name: p });
  } catch { /* opcional */ }
}

await zip.finalize();
await done;
await fs.copyFile("module.json", "dist/module.json");
const st = await fs.stat(zipPath);
console.log(`${zipPath} (${(st.size / 1e6).toFixed(2)} MB)`);
