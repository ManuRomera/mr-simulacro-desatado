#!/usr/bin/env python3
"""Genera _data/aventura.json (Adventure completa para CoC7 v8.16 / Foundry v13-v14),
content/direccion-es.json (MR- Dirección) y content/pizarra-es.json (MR- Pizarra).
"""
import hashlib, json, math, os, sys
PADDING = 0.1
from pathlib import Path
import shutil
from PIL import Image

sys.path.insert(0, "/Volumes/Datos_Dock/FoundryVTT/Trabajo LOGO/marca")
import marca  # noqa: E402  (marca MR animada en cada escena)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from datos_actores import ACTORES, HECHIZOS, MOD
from datos_diarios import AYUDAS_DEF, ECOS_OTRO_LADO, paginas_guia

ROOT = Path("/Volumes/Datos_Dock/FoundryVTT/Data/modules/mr-simulacro-desatado")
ASSETS = ROOT / "assets"
DATA_DIR = ROOT / "_data"
CONTENT_DIR = ROOT / "content"
DATA_DIR.mkdir(exist_ok=True)
CONTENT_DIR.mkdir(exist_ok=True)

ALFABETO = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
DUMMY_AUTHOR = "0000000000000000"

def fid(clave: str) -> str:
    """ID determinista de 16 caracteres en base62 (regla de la casa MR-)."""
    n = int(hashlib.sha256(f"{MOD}:{clave}".encode("utf-8")).hexdigest(), 16)
    chars = []
    for _ in range(16):
        n, r = divmod(n, 62)
        chars.append(ALFABETO[r])
    return "".join(chars)

R = lambda rel: f"modules/{MOD}/assets/{rel}"

def img_size(rel):
    with Image.open(ASSETS / rel) as im:
        return im.size

# ---------------- Carpetas ----------------
def hacer_carpetas():
    defs = [
        # Actores
        ("f-act-ganadores", "01 · Ganadores de Lux-Vista", "Actor", "#9c3d32", 10000),
        ("f-act-pasajeros", "02 · Otros pasajeros", "Actor", "#3d5a73", 20000),
        ("f-act-personal", "03 · Personal del tren", "Actor", "#8c6d3b", 30000),
        ("f-act-antagonistas", "04 · Antagonistas y amenazas", "Actor", "#4a1922", 40000),
        # Escenas
        ("f-esc-estampas", "01 · Estampas y mapas", "Scene", "#2c4257", 10000),
        ("f-esc-planos", "02 · Planos de juego", "Scene", "#7a2c24", 20000),
        # Diarios
        ("f-jrn-guia", "01 · Guía del Guardián", "JournalEntry", "#7a2c24", 10000),
        ("f-jrn-ayudas", "02 · Ayudas de juego", "JournalEntry", "#8c6d3b", 20000),
        # Objetos
        ("f-itm-armas", "01 · Armas del escenario", "Item", "#7a2c24", 10000),
        ("f-itm-pistas", "02 · Pistas, tomos y objetos", "Item", "#8c6d3b", 20000),
        ("f-itm-hechizos", "03 · Hechizos de Milton", "Item", "#4a1922", 30000),
        # Listas y macros
        ("f-pl-audio", "El Simulacro desatado", "Playlist", "#2c4257", 10000),
        ("f-mac-util", "MR- El Simulacro Desatado", "Macro", "#7a2c24", 10000),
    ]
    carpetas = []
    mapa = {}
    for clave, nombre, tipo, color, orden in defs:
        cid = fid(clave)
        mapa[clave] = cid
        carpetas.append({
            "_id": cid,
            "name": nombre,
            "type": tipo,
            "folder": None,
            "sorting": "a",
            "sort": orden,
            "color": color,
            "flags": {MOD: {"clave": clave}},
        })
    return carpetas, mapa

# ---------------- Objetos CoC7 ----------------
def item_skill(actor_slug, nombre, valor, esp="", combat=False):
    # Extraer skillName cuando viene en formato "Especialidad (Sub)"
    skill_name = nombre
    spec = esp
    if "(" in nombre and nombre.endswith(")"):
        base_p, sub = nombre.split("(", 1)
        sub = sub[:-1].strip()
        if not spec:
            spec = base_p.strip()
        skill_name = sub
    props = {"push": not combat, "combat": combat, "special": bool(spec)}
    return {
        "_id": fid(f"skill:{actor_slug}:{nombre}"),
        "name": nombre,
        "type": "skill",
        "img": "systems/CoC7/assets/icons/skills/fighting_brawl.svg" if combat else "icons/svg/book.svg",
        "system": {
            "skillName": skill_name,
            "specialization": spec,
            "description": {"value": "", "chat": "", "keeper": ""},
            "base": valor,
            "bonusDice": 0,
            "adjustments": {"personal": None, "occupation": None, "archetype": None, "experience": None},
            "value": valor,
            "attributes": {},
            "properties": props,
            "flags": {},
        },
        "effects": [],
        "folder": None,
        "sort": 0,
        "ownership": {"default": 0},
        "flags": {},
    }

def item_weapon(clave_id, nombre, skill_id, skill_name, dmg, modo, bullets="", rng=0, malf="", folder=None):
    es_rango = (modo == "ranged")
    addb = (modo == "melee_db")
    props = {"rngd": es_rango, "melee": not es_rango, "addb": addb}
    return {
        "_id": fid(clave_id),
        "name": nombre,
        "type": "weapon",
        "img": "systems/CoC7/assets/icons/skills/firearms_handgun.svg" if es_rango else "systems/CoC7/assets/icons/skills/fighting_brawl.svg",
        "system": {
            "description": {"value": "", "chat": "", "special": "", "keeper": ""},
            "wpnType": "",
            "skill": {
                "main": {"name": skill_name, "id": skill_id},
                "alternativ": {"name": "", "id": ""},
            },
            "range": {
                "normal": {"value": rng, "units": "m" if es_rango else "", "damage": dmg},
                "long": {"value": 0, "units": "", "damage": ""},
                "extreme": {"value": 0, "units": "", "damage": ""},
            },
            "usesPerRound": {"normal": 1, "max": 1, "burst": None},
            "bullets": bullets,
            "ammo": bullets if isinstance(bullets, int) else 0,
            "malfunction": malf,
            "blastRadius": None,
            "properties": props,
            "price": {},
        },
        "effects": [],
        "folder": folder,
        "sort": 0,
        "ownership": {"default": 0},
        "flags": {},
    }

def item_spell(slug, owner_prefix="world", folder=None):
    h = HECHIZOS[slug]
    t = {k: False for k in ("bind", "call", "combat", "contact", "dismiss", "enchantment", "gate", "summon")}
    t.update(h.get("type", {}))
    c = h.get("costs", {})
    return {
        "_id": fid(f"spell:{owner_prefix}:{slug}"),
        "name": h["name"],
        "type": "spell",
        "img": "systems/CoC7/assets/icons/pentagram-rose.svg",
        "system": {
            "alternativeNames": [],
            "castingTime": h.get("castingTime", ""),
            "costs": {
                "hitPoints": c.get("hitPoints", 0),
                "magicPoints": c.get("magicPoints", 0),
                "others": c.get("others", ""),
                "sanity": c.get("sanity", ""),
                "power": c.get("power", 0),
            },
            "description": {"chat": "", "value": h["desc"], "keeper": "", "alternativeNames": ""},
            "effects": [],
            "source": "El Simulacro desatado",
            "learned": True,
            "type": t,
        },
        "effects": [],
        "folder": folder,
        "sort": 0,
        "ownership": {"default": 0},
        "flags": {},
    }

def hacer_objetos_mundo(fmap):
    items = []
    # Hechizos en compendio
    for slug in HECHIZOS:
        items.append(item_spell(slug, "world", fmap["f-itm-hechizos"]))

    # Armas clave del escenario
    armas_mundo = [
        ("w-cuchillo-carnicero", "Cuchillo grande de carnicero", "Pelear (Pelea)", "1D8", "melee_db", "", 0, ""),
        ("w-navaja-automatica", "Navaja automática", "Pelear (Pelea)", "1D4", "melee_db", "", 0, ""),
        ("w-pistola-38", "Pistola automática calibre .38", "Armas de fuego (Pistolas)", "1D10", "ranged", 8, 15, 99),
        ("w-derringer-25", "Derringer calibre .25", "Armas de fuego (Pistolas)", "1D6", "ranged", 1, 3, 100),
        ("w-cuchillo-envainado", "Cuchillo envainado", "Pelear (Pelea)", "1D4+2", "melee_db", "", 0, ""),
        ("w-cuchillo-cocina", "Cuchillo de cocina", "Pelear (Pelea)", "1D4+2", "melee_db", "", 0, ""),
        ("w-fusil-22", "Fusil de cerrojo .22", "Armas de fuego (Fusil/Escopeta)", "1D6+1", "ranged", 6, 30, 99),
    ]
    for cid, nom, sk, dmg, modo, bul, rng, malf in armas_mundo:
        items.append(item_weapon(f"world:{cid}", nom, "", sk, dmg, modo, bul, rng, malf, fmap["f-itm-armas"]))

    # Tomo: Diario de John Milton (book)
    items.append({
        "_id": fid("item:diario-milton"),
        "name": "Diario de John Milton",
        "type": "book",
        "img": "icons/sundries/books/book-leather-red.webp",
        "system": {
            "alternativeNames": [],
            "author": "John Milton",
            "content": "",
            "date": "2013",
            "description": {
                "chat": "",
                "value": "<p>Cuaderno con apretada caligrafía que recoge los desvaríos de John Milton, su devoción a Nyarlathotep, su investigación de los hechos de 1923, el rastreo del descendiente y esquemas del Simulacro de Carne. Contiene sus versiones del <em>Ritual de purificación</em>, el <em>Ritual de restauración</em> y <em>Crear portal</em>.</p><p><strong>Lectura:</strong> 1D6+2 horas · <strong>Pérdida de Cordura:</strong> 1D6 · <strong>Mitos de Cthulhu:</strong> +3 %.</p>",
                "keeper": "<p>En la sección «Ritual de restauración» revela que su cuerpo físico debe ser sacrificado para activar el Simulacro de Carne. Para aprender <em>Crear portal</em> hacen falta 1D6+2 horas y una tirada Difícil de INT.</p>",
            },
            "difficultyLevel": "hard",
            "fullStudies": 0,
            "gains": {"cthulhuMythos": {"final": 3, "initial": 3}, "occult": 0, "others": []},
            "initialReading": False,
            "language": "Inglés",
            "mythosRating": 3,
            "sanityLoss": "1D6",
            "spells": [],
            "study": {"necessary": 5, "progress": 0, "units": "CoC7.hours"},
            "type": {"mythos": True, "occult": False, "other": False},
        },
        "effects": [],
        "folder": fmap["f-itm-pistas"],
        "sort": 10000,
        "ownership": {"default": 0},
        "flags": {},
    })

    # Objetos clave (item)
    objetos_clave = [
        ("diario-1923", "Diario de 1923 (Museo Británico)", "icons/sundries/books/book-worn-brown.webp",
         "<p>Antiguo diario desgastado con etiqueta y número de catálogo del Museo Británico en la contraportada. Escrito por uno de los investigadores de 1923; detalla los planes de Mehmet Makryat, el Simulacro de Sedefkar y los Hermanos de la Piel, e incluye dos versiones del <em>Ritual de purificación</em> (la primera anotada al margen como «versión imprecisa»).</p>"),
        ("llave-maestra", "Llave maestra del Orient Express", "icons/sundries/misc/key-brass.webp",
         "<p>Llave maestra de los compartimentos de los coches cama F y G, robada por John Milton a un azafato mediante el hechizo <em>Dominar</em> el Día 3 en Budapest.</p>"),
        ("bol-cobre-tiza", "Bol de cobre ritual, hierbas y tiza roja", "icons/sundries/misc/bowl-wood-brown.webp",
         "<p>Bol de cobre grabado con extraños símbolos (una tirada de <em>Mitos de Cthulhu</em> confirma su origen), un paquete de hierbas pestilentes y un trozo de tiza roja gastada empleada para marcar los somieres de las víctimas.</p>"),
        ("carta-lux-vista", "Carta de bienvenida de Lux-Vista", "icons/sundries/documents/letter-sealed-red.webp",
         "<p>Sobre elegante con el sello de <strong>Lux-Vista.com</strong> que desea unas fabulosas vacaciones a bordo del Orient Express e invita a los doce ganadores a la recepción con John Milton en el coche salón a las 16:30.</p>"),
    ]
    for i, (slug, nom, icono, desc) in enumerate(objetos_clave):
        items.append({
            "_id": fid(f"item:{slug}"),
            "name": nom,
            "type": "item",
            "img": icono,
            "system": {
                "description": {"value": desc, "chat": "", "keeper": ""},
                "quantity": 1,
                "weight": 0,
                "attributes": {},
                "properties": {},
            },
            "effects": [],
            "folder": fmap["f-itm-pistas"],
            "sort": 20000 + i * 1000,
            "ownership": {"default": 0},
            "flags": {},
        })
    return items

# ---------------- Actores CoC7 ----------------
CHAR_META = [
    ("str", "CHARAC.STR", "CHARAC.Strength"),
    ("con", "CHARAC.CON", "CHARAC.Constitution"),
    ("siz", "CHARAC.SIZ", "CHARAC.Size"),
    ("dex", "CHARAC.DEX", "CHARAC.Dexterity"),
    ("app", "CHARAC.APP", "CHARAC.Appearance"),
    ("int", "CHARAC.INT", "CHARAC.Intelligence"),
    ("pow", "CHARAC.POW", "CHARAC.Power"),
    ("edu", "CHARAC.EDU", "CHARAC.Education"),
]

def hacer_actores(fmap):
    folder_map = {
        "ganadores": fmap["f-act-ganadores"],
        "pasajeros": fmap["f-act-pasajeros"],
        "personal": fmap["f-act-personal"],
        "antagonistas": fmap["f-act-antagonistas"],
    }
    actores = []
    uuids = {}
    for idx, a in enumerate(ACTORES):
        aid = fid(f"actor:{a['slug']}")
        uuids[a["slug"]] = aid
        chars = {}
        for k, short, label in CHAR_META:
            chars[k] = {
                "value": a["chars"].get(k),
                "tempValue": None,
                "short": short,
                "label": label,
                "formula": None,
                "bonusDice": 0,
            }

        # Items embebidos: Esquivar + habilidades de combate + armas + habilidades + hechizos
        emb = []
        emb.append(item_skill(a["slug"], "Esquivar", a["dodge"], "", combat=True))

        # Armas y sus habilidades de combate asociadas
        seen_combat_skills = set()
        for c in a.get("combat", []):
            sk_name, val, dmg, modo, wpn_name = c[:5]
            bullets = c[5] if len(c) > 5 else ""
            rng = c[6] if len(c) > 6 else 0
            malf = c[7] if len(c) > 7 else ""
            # Crear habilidad de combate si no existe aún
            if sk_name not in seen_combat_skills:
                sk_item = item_skill(a["slug"], sk_name, val, "Combate", combat=True)
                emb.append(sk_item)
                seen_combat_skills.add(sk_name)
                sk_id = sk_item["_id"]
            else:
                sk_id = fid(f"skill:{a['slug']}:{sk_name}")
            emb.append(item_weapon(f"wpn:{a['slug']}:{wpn_name}", wpn_name, sk_id, sk_name, dmg, modo, bullets, rng, malf))

        for sk_nom, sk_val, sk_esp in a.get("skills", []):
            emb.append(item_skill(a["slug"], sk_nom, sk_val, sk_esp, combat=False))

        for sp_slug in a.get("spells", []):
            emb.append(item_spell(sp_slug, a["slug"]))

        mp_val = a.get("mp", 0)
        mp_max = a.get("mp_max", mp_val)
        san_val = a.get("san")
        is_creature = (a["actor_type"] == "creature")
        san_loss = a.get("san_loss", ("0", "0"))

        infos = {"type": a.get("creature_type", "")} if is_creature else {
            "occupation": a.get("occupation", ""),
            "age": a.get("age", ""),
            "residence": a.get("residence", ""),
            "birthplace": a.get("birthplace", ""),
        }

        doc = {
            "_id": aid,
            "name": a["name"],
            "type": a["actor_type"],
            "img": R(f"actores/retratos/{a['slug']}.webp"),
            "system": {
                "characteristics": chars,
                "attribs": {
                    "hp": {"value": a["hp"], "max": a["hp"], "short": "HP", "label": "Hit points", "auto": False},
                    "mp": {"value": mp_val, "max": mp_max, "short": "MP", "label": "Magic points", "auto": False},
                    "lck": {"value": 50, "short": "LCK", "label": "Luck", "max": 99, "bonusDice": 0},
                    "san": {"value": san_val if san_val is not None else 0, "max": 99, "short": "SAN", "label": "Sanity", "auto": False, "dailyLoss": 0, "bonusDice": 0},
                    "mov": {"value": a["mov"], "max": a["mov"], "short": "MOV", "label": "Movement rate", "auto": False, "type": "walk"},
                    "db": {"value": a["db"], "short": "DB", "label": "Damage bonus", "auto": False},
                    "build": {"current": a["build"], "value": a["build"], "short": "BLD", "label": "Build", "auto": False},
                    "armor": {"value": a.get("armor", 0), "localized": False, "locations": [], "auto": False},
                },
                "infos": infos,
                "special": {
                    "sanLoss": {"checkPassed": san_loss[0], "checkFailled": san_loss[1]},
                    "attacksPerRound": a.get("attacks_per_round", 1),
                    "movement": [],
                    "macros": [],
                },
                "biography": {"personalDescription": {"value": a["desc"]}},
                "description": {"keeper": a["keeper"]},
                "conditions": {},
                "flags": {},
            },
            "prototypeToken": {
                "name": a["name"],
                "displayName": 20,  # HOVER
                "actorLink": not is_creature,
                "texture": {"src": R(f"actores/tokens/{a['slug']}.webp"), "scaleX": 1, "scaleY": 1},
                "width": 1,
                "height": 1,
                "disposition": -1 if a["folder"] == "antagonistas" else 0,
                "ring": {"enabled": False},
            },
            "items": emb,
            "effects": [],
            "folder": folder_map[a["folder"]],
            "sort": (idx + 1) * 10000,
            "ownership": {"default": 0},
            "flags": {MOD: {"slug": a["slug"], "categoria": a["folder"]}},
        }
        actores.append(doc)
    return actores, uuids

# ---------------- Playlists ----------------
def hacer_playlists(fmap):
    pl_musica_id = fid("playlist:musica")
    pl_ambiente_id = fid("playlist:ambiente")

    pistas_musica = [
        ("escena-1", "Escena 1 · Embarque en París", "audio/escena-1-embarque.ogg", 0.55),
        ("escena-2", "Escena 2 · Budapest y el Laberinto", "audio/escena-2-budapest.ogg", 0.55),
        ("escena-3", "Escena 3 · El Otro Lado", "audio/escena-3-otro-lado.ogg", 0.55),
        ("escena-4", "Escena 4 · La Mezquita Velada", "audio/escena-4-mezquita.ogg", 0.60),
        ("ambiente-detective", "Ambiente · Investigación lovecraftiana", "audio/ambiente-detective.ogg", 0.45),
    ]
    sounds_musica = []
    sound_ids = {}
    for i, (slug, nom, path, vol) in enumerate(pistas_musica):
        sid = fid(f"sound:{slug}")
        sound_ids[slug] = sid
        sounds_musica.append({
            "_id": sid,
            "name": nom,
            "path": R(path),
            "playing": False,
            "repeat": True,
            "volume": vol,
            "fade": 2500,
            "sort": (i + 1) * 1000,
            "flags": {MOD: {"slug": slug}},
        })

    sid_tren = fid("sound:tren")
    sound_ids["tren"] = sid_tren
    playlists = [
        {
            "_id": pl_musica_id,
            "name": "El Simulacro desatado · Música de escenas",
            "mode": 0,
            "playing": False,
            "fade": 2500,
            "folder": fmap["f-pl-audio"],
            "sort": 10000,
            "sounds": sounds_musica,
            "ownership": {"default": 0},
            "flags": {MOD: {"slug": "musica"}},
        },
        {
            "_id": pl_ambiente_id,
            "name": "El Simulacro desatado · Sonido del Orient Express",
            "mode": 2,  # Simultaneous / ambient
            "playing": False,
            "fade": 2500,
            "folder": fmap["f-pl-audio"],
            "sort": 20000,
            "sounds": [{
                "_id": sid_tren,
                "name": "Traqueteo continuo del Orient Express",
                "path": R("audio/orient-express-tren.ogg"),
                "playing": False,
                "repeat": True,
                "volume": 0.35,
                "fade": 2500,
                "sort": 1000,
                "flags": {MOD: {"slug": "tren"}},
            }],
            "ownership": {"default": 0},
            "flags": {MOD: {"slug": "ambiente"}},
        },
    ]
    return playlists, {"musica": pl_musica_id, "ambiente": pl_ambiente_id, "sounds": sound_ids}

# ---------------- Escenas ----------------
def muros_mezquita():
    """Muros de 06-mezquita-velada.webp (2101x1581) trazados del propio plano: contorno de la masa
    marrón (sin trazos finos ni marca), roca punteada de la tumba rellena, túnel y puertas a mano."""
    import cv2, numpy as np
    im = cv2.imread(str(ASSETS / "escenas" / "06-mezquita-velada.webp"))
    b, g, r = (im[:, :, i].astype(int) for i in range(3))
    masa = ((r < 190) & (r - b > 45) & (g < 150)).astype(np.uint8) * 255
    masa[1400:, 1700:] = 0  # marca MR
    masa[1140:] = cv2.morphologyEx(masa[1140:], cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8))  # punteado de roca
    masa = cv2.morphologyEx(masa, cv2.MORPH_CLOSE, np.ones((17, 17), np.uint8))
    masa = cv2.morphologyEx(masa, cv2.MORPH_OPEN, np.ones((19, 19), np.uint8))  # quita hojas de puerta y puntos
    contornos, _ = cv2.findContours(masa, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    segs = []
    for c in contornos:
        if cv2.contourArea(c) < 400:
            continue
        pts = cv2.approxPolyDP(c, 4, True)[:, 0].tolist()
        segs += [(*pts[i], *pts[(i + 1) % len(pts)], 0) for i in range(len(pts))]
    # Túnel (trazo fino) y puertas: cerradas en el hueco, en el lado de la bisagra del plano
    linea = lambda *xy: [(*xy[i:i + 2], *xy[i + 2:i + 4], 0) for i in range(0, len(xy) - 2, 2)]
    segs += linea(226, 1491, 226, 1444, 790, 1444, 790, 1358, 923, 1358) + linea(226, 1491, 845, 1491) + linea(925, 1208, 925, 1358)  # roca izquierda de la tumba
    puertas = [(1222, 445, 1300, 445), (1598, 452, 1598, 487), (1713, 490, 1783, 490), (1795, 640, 1795, 695),
               (1932, 640, 1932, 695), (1727, 835, 1793, 835), (1220, 905, 1285, 905), (1367, 905, 1442, 905),
               (912, 1080, 912, 1117), (923, 1358, 923, 1405)]
    segs += [(*d, 1) for d in puertas]
    return [{"_id": fid(f"wall:mez:{i}"), "c": [int(v) for v in s4[:4]], "light": 20, "move": 20, "sight": 20,
             "sound": 20, "dir": 0, "door": s4[4], "ds": 0, "flags": {}} for i, s4 in enumerate(segs)]

def luces_mezquita():
    """Anillo de antorchas parpadeantes en los apliques de hierro de la Mezquita Velada."""
    coords = [
        (690, 520), (690, 770), (540, 645),
        (1060, 430), (1060, 850), (1440, 560), (1440, 750),
    ]
    lights = []
    for i, (x, y) in enumerate(coords):
        lights.append({
            "_id": fid(f"light:mez:{i}"),
            "x": x, "y": y, "rotation": 0, "walls": True, "vision": False, "hidden": False,
            "config": {
                "alpha": 0.45, "angle": 360, "bright": 3.5, "dim": 8, "color": "#ff9d47",
                "coloration": 1, "attenuation": 0.6, "luminosity": 0.45,
                "animation": {"type": "torch", "speed": 4, "intensity": 4, "reverse": False},
            },
            "flags": {},
        })
    return lights

def hacer_escenas(fmap, pl_info):
    (ASSETS / "marca").mkdir(exist_ok=True)
    shutil.copy("/Volumes/Datos_Dock/FoundryVTT/Trabajo LOGO/marca/mr-marca.webm", ASSETS / "marca" / "mr-marca.webm")
    defs = [
        # (slug, name, navName, img_rel, folder, grid_type, grid_size, grid_dist, dark, pl, snd, orden, nav, extra)
        ("portada", "00 · Horror en el Orient Express (Portada)", "Orient Express",
         "escenas/00-orient-express-portada.webp", "f-esc-estampas", 0, 100, 1.5, 0.0,
         pl_info["musica"], pl_info["sounds"]["escena-1"], 0, True, {}),
        ("budapest", "01 · Budapest (Días 2 y 3)", "Budapest",
         "escenas/01-budapest.webp", "f-esc-estampas", 0, 100, 1.5, 0.0,
         pl_info["musica"], pl_info["sounds"]["escena-2"], 1, True, {}),
        ("coches-mesa", "02 · Coches cama F y G (Mesa)", "Coches F y G",
         "escenas/02-coches-cama-mesa.webp", "f-esc-planos", 1, 70, 1.5, 0.0,
         pl_info["musica"], pl_info["sounds"]["escena-3"], 2, True, {"grid_alpha": 0.12}),
        ("coches-guardian", "03 · Coches cama F y G (Guardián)", "Coches (GM)",
         "escenas/03-coches-cama-guardian.webp", "f-esc-planos", 0, 70, 1.5, 0.0,
         pl_info["musica"], pl_info["sounds"]["escena-3"], 3, False, {}),
        ("estambul-mesa", "04 · Estambul en la actualidad (Mesa)", "Estambul",
         "escenas/04-estambul-mesa.webp", "f-esc-estampas", 0, 100, 1.5, 0.0,
         pl_info["musica"], pl_info["sounds"]["ambiente-detective"], 4, True, {}),
        ("estambul-guardian", "05 · Estambul en la actualidad (Guardián)", "Estambul (GM)",
         "escenas/05-estambul-guardian.webp", "f-esc-estampas", 0, 100, 1.5, 0.0,
         pl_info["musica"], pl_info["sounds"]["ambiente-detective"], 5, False, {}),
        ("mezquita", "06 · La Mezquita Velada (Clímax)", "Mezquita Velada",
         "escenas/06-mezquita-velada.webp", "f-esc-planos", 1, 90, 1.5, 0.82,
         pl_info["musica"], pl_info["sounds"]["escena-4"], 6, True, {
             "grid_alpha": 0.18, "tokenVision": True, "fog": True,
             "walls": muros_mezquita(), "lights": luces_mezquita(),
         }),
    ]
    escenas = []
    uuids = {}
    for slug, name, nav_name, img_rel, fkey, gtype, gsize, gdist, dark, pl_id, snd_id, orden, nav, extra in defs:
        sid = fid(f"scene:{slug}")
        uuids[slug] = sid
        w, h = img_size(img_rel)
        # Miniatura 400 px (vista previa del selector de MR- Dirección)
        thumb = f"escenas/thumbs/{slug}.webp"
        (ASSETS / thumb).parent.mkdir(exist_ok=True)
        with Image.open(ASSETS / img_rel) as im:
            im.convert("RGB").resize((400, round(400 * h / w)), Image.LANCZOS).save(ASSETS / thumb, "WEBP", quality=80)
        # Muros y luces se dibujan en píxeles de la imagen; Foundry pone la imagen tras el margen
        # (misma fórmula que SquareGrid.calculateDimensions; el margen va en pasos de 0,05).
        ox = math.ceil(PADDING * w / gsize) * gsize
        oy = math.ceil(PADDING * h / gsize) * gsize
        muros = [{**m, "c": [m["c"][0] + ox, m["c"][1] + oy, m["c"][2] + ox, m["c"][3] + oy]} for m in extra.get("walls", [])]
        luces = [{**l, "x": l["x"] + ox, "y": l["y"] + oy} for l in extra.get("lights", [])]
        mx, my, mw, mh = marca.caja_animada(w, h)
        tile = {"_id": fid(f"tile:{slug}:marca"),
                "texture": {"src": R("marca/mr-marca.webm"), "scaleX": 1, "scaleY": 1, "tint": "#ffffff", "alphaThreshold": 0, "fit": "fill", "anchorX": 0.5, "anchorY": 0.5},
                "x": mx + ox, "y": my + oy, "width": mw, "height": mh, "elevation": 0, "sort": 0, "rotation": 0, "alpha": 1, "hidden": False, "locked": True,
                "restrictions": {"light": False, "weather": False}, "occlusion": {"mode": 0, "alpha": 0},
                "video": {"loop": True, "autoplay": True, "volume": 0}, "flags": {}}
        escenas.append({
            "_id": sid,
            "name": name,
            "navName": nav_name,
            "active": False,
            "navigation": nav,
            "navOrder": orden * 10,
            "background": {"src": R(img_rel), "anchorX": 0, "anchorY": 0, "offsetX": 0, "offsetY": 0, "scaleX": 1, "scaleY": 1},
            "width": w,
            "height": h,
            "padding": PADDING,
            "backgroundColor": "#141012",
            "grid": {
                "type": gtype,
                "size": gsize,
                "style": "solidLines",
                "thickness": 1,
                "color": "#000000",
                "alpha": extra.get("grid_alpha", 0.0),
                "distance": gdist,
                "units": "m",
            },
            "tokenVision": extra.get("tokenVision", False),
            "fog": {"exploration": extra.get("fog", False)},
            "environment": {"darknessLevel": dark},
            "playlist": pl_id,
            "playlistSound": snd_id,
            "walls": muros,
            "lights": luces,
            "tokens": [],
            "notes": [],
            "tiles": [tile],
            "thumb": R(thumb),
            "drawings": [],
            "sounds": [],
            "templates": [],
            "folder": fmap[fkey],
            "sort": (orden + 1) * 10000,
            "ownership": {"default": 0},
            "flags": {MOD: {"slug": slug, "orden": orden}},
        })
    return escenas, uuids

# ---------------- Diarios ----------------
def hacer_diarios(fmap, uuids_actores, uuids_escenas):
    diarios = []
    uuids_ayudas = {}

    # 1) Ayudas de juego (primero para obtener sus UUIDs)
    for idx, a in enumerate(AYUDAS_DEF):
        jid = fid(f"journal:{a['slug']}")
        uuids_ayudas[a["slug"]] = jid
        pages = []
        for p_idx, (ptitle, phtml) in enumerate(a["pages"]):
            pages.append({
                "_id": fid(f"page:{a['slug']}:{p_idx}"),
                "name": ptitle,
                "type": "text",
                "title": {"show": True, "level": 1},
                "text": {"format": 1, "content": phtml.strip()},
                "sort": (p_idx + 1) * 10000,
                "ownership": {"default": -1},
                "flags": {},
            })
        diarios.append({
            "_id": jid,
            "name": a["name"],
            "pages": pages,
            "folder": fmap["f-jrn-ayudas"],
            "sort": (idx + 1) * 10000,
            "ownership": {"default": 0},
            "flags": {MOD: {"slug": a["slug"], "ayuda": True}},
        })

    # 2) Guía del Guardián (10 páginas)
    guia_id = fid("journal:guia-guardian")
    guia_pages = []
    for i, (titulo, html) in enumerate(paginas_guia(uuids_actores, uuids_ayudas, uuids_escenas)):
        guia_pages.append({
            "_id": fid(f"page:guia:{i}"),
            "name": titulo,
            "type": "text",
            "title": {"show": False, "level": 1},
            "text": {"format": 1, "content": html.strip()},
            "sort": (i + 1) * 10000,
            "ownership": {"default": -1},
            "flags": {},
        })
    diarios.append({
        "_id": guia_id,
        "name": "00 · Guía del Guardián: El Simulacro desatado",
        "pages": guia_pages,
        "folder": fmap["f-jrn-guia"],
        "sort": 10000,
        "ownership": {"default": 0},
        "flags": {MOD: {"slug": "guia-guardian", "guia": True}},
    })

    # 3) Dossier rápido de personajes
    filas = []
    for a in ACTORES:
        aid = uuids_actores[a["slug"]]
        rol = a.get("occupation") or a.get("creature_type", "")
        tok_src = R(f"actores/tokens/{a['slug']}.webp")
        filas.append(f'<tr><td><img src="{tok_src}" width="44" height="44" style="border:none;" /></td><td>@UUID[Actor.{aid}]{{{a["name"]}}}</td><td>{rol}</td></tr>')
    dossier_html = f"""
<h1>Dramatis Personae · El Simulacro desatado</h1>
<p>Acceso directo a las 17 fichas jugables de la aventura (100 % fieles a las estadísticas del libro).</p>
<table>
  <thead><tr><th></th><th>Personaje</th><th>Rol / Ocupación</th></tr></thead>
  <tbody>{"".join(filas)}</tbody>
</table>
"""
    diarios.append({
        "_id": fid("journal:dossier-pnj"),
        "name": "01 · Dramatis Personae (Dossier de PNJ)",
        "pages": [{
            "_id": fid("page:dossier:0"),
            "name": "Reparto completo",
            "type": "text",
            "title": {"show": False, "level": 1},
            "text": {"format": 1, "content": dossier_html.strip()},
            "sort": 10000,
            "ownership": {"default": -1},
            "flags": {},
        }],
        "folder": fmap["f-jrn-guia"],
        "sort": 20000,
        "ownership": {"default": 0},
        "flags": {MOD: {"slug": "dossier-pnj"}},
    })

    return diarios, uuids_ayudas

# ---------------- Tabla aleatoria: Ecos del Otro Lado ----------------
def hacer_tablas():
    results = []
    for i, texto in enumerate(ECOS_OTRO_LADO, start=1):
        results.append({
            "_id": fid(f"eco:{i}"),
            "type": "text",
            "text": texto,
            "img": "icons/svg/d20-grey.svg",
            "weight": 1,
            "range": [i, i],
            "drawn": False,
            "flags": {},
        })
    return [{
        "_id": fid("table:ecos-otro-lado"),
        "name": "Ecos del Otro Lado (1D10)",
        "img": "icons/svg/d20-grey.svg",
        "description": "<p>Manifestaciones físicas y recuerdos letales del pasado que duran <strong>1D6 minutos</strong> mientras el Orient Express está atrapado en el Otro Lado (págs. 314–316).</p>",
        "formula": "1d10",
        "replacement": True,
        "displayRoll": True,
        "results": results,
        "folder": None,
        "sort": 10000,
        "ownership": {"default": 0},
        "flags": {MOD: {"slug": "ecos-otro-lado"}},
    }]

# ---------------- Macros (con author ficticio válido para Foundry v13/v14) ----------------
def hacer_macros(fmap):
    defs = [
        ("panel", "El Simulacro · Panel del Guardián", "icons/svg/book.svg",
         f'game.modules.get("{MOD}")?.api?.panel();'),
        ("pizarra", "El Simulacro · Pizarra de investigación", "icons/svg/eye.svg",
         f'game.modules.get("{MOD}")?.api?.abrirPizarra();'),
        ("eco", "El Simulacro · Tirar Eco del Otro Lado", "icons/svg/d20-highlight.svg",
         f'game.modules.get("{MOD}")?.api?.tirarEco();'),
    ]
    macros = []
    for i, (slug, nom, img, cmd) in enumerate(defs):
        macros.append({
            "_id": fid(f"macro:{slug}"),
            "name": nom,
            "type": "script",
            "author": DUMMY_AUTHOR,
            "img": img,
            "scope": "global",
            "command": cmd,
            "folder": fmap["f-mac-util"],
            "sort": (i + 1) * 10000,
            "ownership": {"default": 0},
            "flags": {MOD: {"slug": slug, "macro": True}},
        })
    return macros

# ---------------- Integración MR- Dirección ----------------
# Esquema 1 de MR- Dirección (docs/DISENO.md de mr-direccion). Regla de la casa: cada efecto,
# motivo, figura y ayuda va en la escena donde se usa; en la barra global no hay efectos.
def escribir_direccion():
    F = lambda slug: {"flag": [MOD, "slug", slug]}
    guia = lambda i: {"uuid": f"JournalEntry.{fid('journal:guia-guardian')}.JournalEntryPage.{fid(f'page:guia:{i}')}"}
    ayudas = lambda *ns: [{"ref": F(f"ayuda-{n}"), "label": ""} for n in ns]
    figuras = lambda *slugs: [{"ref": F(s), "label": ""} for s in slugs]
    tren = [{"label": "Traqueteo del tren", "icon": "train", "sound": F("tren")}]
    ganadores = ("giuseppe-roti", "john-walters", "enzo-banuelos", "oscar-griffin", "faustino-gonzaga", "antonio-abella")
    plano = {"mode": "none"}  # planos cenitales: sin perspectiva

    def escena(slug, orden, nombre, lectura, musica, motivos, notas, cues=(), fig=(), hand=(), stage=None):
        return {"ref": F(slug), "order": orden, "name": nombre, "reading": guia(lectura), "music": F(musica),
                "motifs": list(motivos), "cues": list(cues), "ambient": None, "figures": list(fig),
                "handouts": list(hand), "notes": notas, "thumb": "", **({"stage": stage} if stage else {})}

    # Figuras solo en las ilustraciones; en los planos cenitales se usan fichas normales.
    coches = dict(lectura=7, musica="escena-3", motivos=("otro-lado", "investigacion"), cues=tren,
                  hand=ayudas(5, 6), stage=plano,
                  notas="Días 1 a 4 a bordo. Milton se mueve con la llave maestra; los asesinatos empiezan el lunes.")
    estambul = dict(lectura=8, musica="ambiente-detective", motivos=("investigacion", "mezquita"),
                    hand=ayudas(6), stage=plano,
                    notas="Día 5. El diario de Milton señala la Mezquita Velada.")
    pack = {
        "schema": 1,
        "id": MOD,
        "title": "MR- El Simulacro Desatado",
        "version": "1.0.0",
        "author": "Manu Romera",
        "license": "Uso personal · Aventura original © Chaosium / Edge",
        "settings": {
            "fade": 3,
            "motifs": [
                {"id": "embarque", "label": "Embarque", "icon": "train", "music": F("escena-1")},
                {"id": "budapest", "label": "Budapest", "icon": "landmark", "music": F("escena-2")},
                {"id": "otro-lado", "label": "El Otro Lado", "icon": "smog", "music": F("escena-3")},
                {"id": "mezquita", "label": "Mezquita Velada", "icon": "fire", "music": F("escena-4")},
                {"id": "investigacion", "label": "Investigación", "icon": "magnifying-glass", "music": F("ambiente-detective")},
            ],
            "effects": [],
            "markers": {
                "milestones": [
                    {"id": "d1", "label": "Día 1 · Recepción de Lux-Vista en París", "public": True},
                    {"id": "d2", "label": "Día 2 · Escándalo de Gonzaga y cena en Budapest", "public": True},
                    {"id": "d3", "label": "Día 3 · Laberinto de Buda y el Ritual de purificación", "public": True},
                    {"id": "d4", "label": "Día 4 · El Otro Lado, asesinatos y diario de 1923", "public": True},
                    {"id": "d5", "label": "Día 5 · El portal y la Mezquita Velada", "public": True},
                ],
                "clocks": [
                    {"id": "simulacro", "label": "El Simulacro de Carne", "segments": 6, "public": False, "announce": False,
                     "phrases": ["Brazo izquierdo", "Brazo derecho", "Pierna izquierda", "Pierna derecha", "Torso", "Cabeza: el descendiente"]},
                ],
            },
        },
        "scenes": [
            escena("portada", 0, "Embarque en París", 3, "escena-1", ("embarque", "investigacion"),
                   "Día 1. Recepción de Lux-Vista y presentación de los ganadores.",
                   cues=tren, fig=figuras(*ganadores), hand=ayudas(1, 2, 3)),
            escena("budapest", 1, "Budapest y el Laberinto", 4, "escena-2", ("budapest", "investigacion"),
                   "Días 2 y 3. Escándalo de Gonzaga, tour opcional y el Laberinto de Buda.",
                   fig=figuras("faustino-gonzaga", "chantel-antin", "henri-guillemette", "john-milton"), hand=ayudas(4)),
            escena("coches-mesa", 2, "Coches cama F y G", **coches),
            escena("coches-guardian", 3, "Coches cama F y G (Guardián)", **coches),
            escena("estambul-mesa", 4, "Estambul 2013", **estambul),
            escena("estambul-guardian", 5, "Estambul 2013 (Guardián)", **estambul),
            escena("mezquita", 6, "La Mezquita Velada", 8, "escena-4", ("mezquita",),
                   "Clímax. Milton, los soldados sin rostro y el Simulacro.", stage=plano),
        ],
    }
    (CONTENT_DIR / "direccion-es.json").write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("content/direccion-es.json OK")

# ---------------- Integración MR- Pizarra ----------------
def escribir_pizarra():
    pizarra = {
        "format": "mr-pizarra-import",
        "version": 1,
        "mode": "board",
        "title": "El Simulacro desatado · Pizarra de investigación",
        "background": "corcho-claro",
        "pinPreset": {"pin": "auto", "color": "", "layout": "auto"},
        "layers": [
            {"ref": "ganadores", "name": "Ganadores de Lux-Vista", "revealed": True},
            {"ref": "pasajeros", "name": "Otros pasajeros y personal", "revealed": True},
            {"ref": "acosador", "name": "El acosador de Chantel", "revealed": False},
            {"ref": "asesinatos", "name": "Los asesinatos del Otro Lado", "revealed": False},
            {"ref": "milton", "name": "La verdad de John Milton", "revealed": False},
        ],
        "items": [
            # Fila 1: Ganadores de Lux-Vista
            {"ref": "roti", "type": "entity", "name": "Giuseppe Roti", "kind": "Actor", "frame": "polaroid", "showToAll": True, "layer": "ganadores", "x": 220, "y": 220, "w": 200, "rot": -3},
            {"ref": "walters", "type": "entity", "name": "John Walters", "kind": "Actor", "frame": "polaroid", "showToAll": True, "layer": "ganadores", "x": 480, "y": 220, "w": 200, "rot": 2},
            {"ref": "banuelos", "type": "entity", "name": "Enzo Bañuelos", "kind": "Actor", "frame": "polaroid", "showToAll": True, "layer": "ganadores", "x": 740, "y": 220, "w": 200, "rot": -2},
            {"ref": "griffin", "type": "entity", "name": "Oscar Griffin", "kind": "Actor", "frame": "polaroid", "showToAll": True, "layer": "ganadores", "x": 1000, "y": 220, "w": 200, "rot": 3},
            {"ref": "gonzaga", "type": "entity", "name": "Faustino Gonzaga", "kind": "Actor", "frame": "polaroid", "showToAll": True, "layer": "ganadores", "x": 1260, "y": 220, "w": 200, "rot": -4},
            {"ref": "abella", "type": "entity", "name": "Antonio Abella (Angelo Minotti)", "kind": "Actor", "frame": "polaroid", "showToAll": True, "layer": "ganadores", "x": 1520, "y": 220, "w": 200, "rot": 2},
            # Fila 2: Otros pasajeros
            {"ref": "chantel", "type": "entity", "name": "Chantel Antin", "kind": "Actor", "frame": "polaroid", "showToAll": True, "layer": "pasajeros", "x": 220, "y": 540, "w": 200, "rot": 2},
            {"ref": "guillemette", "type": "entity", "name": "Henri Guillemette", "kind": "Actor", "frame": "polaroid", "showToAll": True, "layer": "pasajeros", "x": 480, "y": 540, "w": 200, "rot": -2},
            {"ref": "wilson", "type": "entity", "name": "Mark Wilson", "kind": "Actor", "frame": "polaroid", "showToAll": True, "layer": "pasajeros", "x": 740, "y": 540, "w": 200, "rot": 3},
            {"ref": "wyss", "type": "entity", "name": "Fabian Wyss", "kind": "Actor", "frame": "polaroid", "showToAll": True, "layer": "pasajeros", "x": 1000, "y": 540, "w": 200, "rot": -3},
            {"ref": "farber", "type": "entity", "name": "Lars Färber", "kind": "Actor", "frame": "polaroid", "showToAll": True, "layer": "pasajeros", "x": 1260, "y": 540, "w": 200, "rot": 2},
            {"ref": "milton-card", "type": "entity", "name": "John Milton", "kind": "Actor", "frame": "polaroid", "showToAll": True, "layer": "ganadores", "x": 1520, "y": 540, "w": 210, "rot": -1},
            # Capa acosador
            {"ref": "nota-acosador", "type": "note", "title": "«El amor de TU vida»", "text": "Cartas con recortes a Chantel Antin.\nEn la cabina de Mark Wilson hay recortes, pegamento y un diario obsesivo.", "color": "amber", "layer": "acosador", "x": 480, "y": 840, "w": 280, "rot": -2},
            # Capa asesinatos
            {"ref": "nota-tiza", "type": "note", "title": "Marcas de tiza roja", "text": "Bajo el somier de cada víctima hay dibujada con tiza roja la parte del cuerpo amputada post mortem.", "color": "crimson", "layer": "asesinatos", "x": 920, "y": 840, "w": 280, "rot": 1},
            {"ref": "nota-diario-23", "type": "note", "title": "Diario de 1923", "text": "Propiedad del Museo Británico. Aparece junto al 5.º cadáver: Hermanos de la Piel, Simulacro de Sedefkar y Ritual de purificación.", "color": "parchment", "layer": "asesinatos", "x": 1240, "y": 840, "w": 280, "rot": -2},
            # Capa verdad de Milton
            {"ref": "nota-simulacro", "type": "note", "title": "El Simulacro de Carne", "text": "6 partes en los nichos de la Mezquita Velada (Estambul).\nMilton necesita morir en el círculo de sangre para poseerlo.", "color": "crimson", "layer": "milton", "x": 1560, "y": 840, "w": 300, "rot": 2},
        ],
        "connections": [
            {"from": "chantel", "to": "nota-acosador", "color": "#b45309", "layer": "acosador"},
            {"from": "wilson", "to": "nota-acosador", "color": "#b45309", "layer": "acosador"},
            {"from": "roti", "to": "nota-tiza", "color": "#991b1b", "layer": "asesinatos"},
            {"from": "walters", "to": "nota-tiza", "color": "#991b1b", "layer": "asesinatos"},
            {"from": "gonzaga", "to": "nota-diario-23", "color": "#991b1b", "layer": "asesinatos"},
            {"from": "milton-card", "to": "nota-simulacro", "color": "#7f1d1d", "layer": "milton"},
        ],
    }
    (CONTENT_DIR / "pizarra-es.json").write_text(json.dumps(pizarra, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("content/pizarra-es.json OK")

# ---------------- Principal ----------------
def main():
    carpetas, fmap = hacer_carpetas()
    items = hacer_objetos_mundo(fmap)
    actores, uuids_actores = hacer_actores(fmap)
    playlists, pl_info = hacer_playlists(fmap)
    escenas, uuids_escenas = hacer_escenas(fmap, pl_info)
    diarios, uuids_ayudas = hacer_diarios(fmap, uuids_actores, uuids_escenas)
    tablas = hacer_tablas()
    macros = hacer_macros(fmap)

    aventura = {
        "_id": fid("adventure:principal"),
        "name": "MR- El Simulacro Desatado (Horror en el Orient Express · 2013)",
        "img": R("escenas/00-orient-express-portada.webp"),
        "caption": "Estambul, 2013 · Epílogo contemporáneo de Horror en el Orient Express para La llamada de Cthulhu 7.ª ed.",
        "description": (
            "<p><strong>El Simulacro desatado</strong> (Mike Mason y Penelope Love) preparado al completo para dirigir en Foundry VTT "
            "con el sistema <em>Call of Cthulhu 7th Edition</em>.</p>"
            "<ul>"
            f"<li><strong>{len(actores)} actores jugables</strong> con todas sus características, habilidades, armas, hechizos, retratos y tokens circulares.</li>"
            f"<li><strong>{len(escenas)} escenas</strong> (portada 4K, Budapest, Coches cama F y G versión mesa y Guardián, Estambul mesa y Guardián, y La Mezquita Velada con muros y antorchas).</li>"
            f"<li><strong>{len(diarios)} diarios</strong>: Guía completa del Guardián en 10 páginas, Dramatis Personae y las 6 Ayudas de juego listas para mostrar a los jugadores.</li>"
            f"<li><strong>{len(playlists)} listas de audio</strong> (música para las 4 escenas, ambiente detectivesco y sonido continuo del Orient Express).</li>"
            f"<li><strong>Tabla de Ecos del Otro Lado</strong>, <strong>Panel del Guardián</strong> e integración con <em>MR- Dirección</em> y <em>MR- Pizarra</em>.</li>"
            "</ul>"
        ),
        "actors": actores,
        "items": items,
        "scenes": escenas,
        "journal": diarios,
        "playlists": playlists,
        "tables": tablas,
        "macros": macros,
        "cards": [],
        "combats": [],
        "folders": carpetas,
        "sort": 0,
        "flags": {MOD: {"version": "1.0.0"}},
    }

    out_path = DATA_DIR / "aventura.json"
    out_path.write_text(json.dumps([aventura], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"_data/aventura.json OK: {len(actores)} actores, {len(items)} objetos, {len(escenas)} escenas, {len(diarios)} diarios, {len(playlists)} playlists, {len(tablas)} tablas, {len(macros)} macros")

    escribir_direccion()
    escribir_pizarra()

if __name__ == "__main__":
    main()
