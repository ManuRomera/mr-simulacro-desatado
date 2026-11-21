#!/usr/bin/env python3
"""Pipeline gráfico de MR- El Simulacro Desatado:
- Retratos (webp con marca MR en esquina) y tokens circulares (generados ANTES de la marca MR) de los 17 actores.
- Ayudas de juego recortadas limpiamente de Ayudas de juego.pdf.
- Escenas y mapas (mesa y Guardián) sin cabeceras ni números de página, componiendo smask sobre pergamino.
"""
import os, sys, shutil
from pathlib import Path
import fitz
from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, "/Volumes/Datos_Dock/FoundryVTT/Trabajo LOGO/marca")
import marca

FUENTES = Path("/Volumes/Datos_Dock/FoundryVTT/Trabajo SIMULACRO/fuentes")
BRAIN = Path("/Users/mromera/.gemini/antigravity/brain/f58d6b0b-c09e-403b-8761-4668fb11ae0e")
MOD = Path("/Volumes/Datos_Dock/FoundryVTT/Data/modules/mr-simulacro-desatado")
ASSETS = MOD / "assets"
RETRATOS = ASSETS / "actores" / "retratos"
TOKENS = ASSETS / "actores" / "tokens"
AYUDAS = ASSETS / "ayudas"
ESCENAS = ASSETS / "escenas"
DIARIO = ASSETS / "diario"

for d in (RETRATOS, TOKENS, AYUDAS, ESCENAS, DIARIO):
    d.mkdir(parents=True, exist_ok=True)

# 14 retratos del Drive + 3 generados por el módulo
ACTORES_IMG = {
    "antonio-abella": FUENTES / "Imángenes PNJ" / "Antonio Abella.png",
    "chantel-antin": FUENTES / "Imángenes PNJ" / "Chantel Antin.png",
    "enzo-banuelos": FUENTES / "Imángenes PNJ" / "Enzo Bañuelos.png",
    "fabian-wyss": FUENTES / "Imángenes PNJ" / "Fabian Wyss.png",
    "faustino-gonzaga": FUENTES / "Imángenes PNJ" / "Faustino Gonzaga.png",
    "giuseppe-roti": FUENTES / "Imángenes PNJ" / "Giuseppe Roti.png",
    "henri-guillemette": FUENTES / "Imángenes PNJ" / "Henri Guillemette.png",
    "john-walters": FUENTES / "Imángenes PNJ" / "John Walters.png",
    "lars-farber": FUENTES / "Imángenes PNJ" / "Lars Färber.png",
    "marisa-ocana": FUENTES / "Imángenes PNJ" / "Marisa Ocaña.png",
    "mark-wilson": FUENTES / "Imángenes PNJ" / "Mark Wilson.png",
    "oscar-griffin": FUENTES / "Imángenes PNJ" / "Oscar Griffin.png",
    "rene-violet": FUENTES / "Imángenes PNJ" / "René Violet.png",
    "wanda-zeigler": FUENTES / "Imángenes PNJ" / "Wanda Zeigler.png",
    "john-milton": BRAIN / "john_milton_1795299864627.jpg",
    "soldado-sin-rostro": BRAIN / "soldado_sin_rostro_1795299836592.jpg",
    "simulacro-de-carne": BRAIN / "simulacro_de_carne_1795299846405.jpg",
}

def hacer_token(im: Image.Image, tam: int = 512, borde=(198, 158, 92)) -> Image.Image:
    """Recorta centrado en la cabeza/busto superior, aplica máscara circular y aro art déco Orient Express."""
    w, h = im.size
    lado = min(w, h)
    # Enfocar ligeramente hacia arriba (retrato vertical 2:3 -> cara en el tercio superior)
    top = int((h - lado) * 0.22)
    left = (w - lado) // 2
    cuadro = im.crop((left, top, left + lado, top + lado)).resize((tam, tam), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (tam, tam), 0)
    ImageDraw.Draw(mask).ellipse((10, 10, tam - 10, tam - 10), fill=255)
    out = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    out.paste(cuadro, (0, 0), mask)
    draw = ImageDraw.Draw(out)
    # Doble aro elegante: exterior oscuro, interior latón dorado
    draw.ellipse((4, 4, tam - 4, tam - 4), outline=(28, 22, 18, 255), width=10)
    draw.ellipse((10, 10, tam - 10, tam - 10), outline=borde + (255,), width=7)
    draw.ellipse((18, 18, tam - 18, tam - 18), outline=(245, 232, 200, 170), width=2)
    return out

def procesar_actores():
    for slug, src in ACTORES_IMG.items():
        im = Image.open(src).convert("RGB")
        # 1) Token circular ANTES de estampar la marca de esquina (regla de la casa)
        borde = (158, 42, 42) if slug in ("john-milton", "soldado-sin-rostro", "simulacro-de-carne") else (198, 158, 92)
        tok = hacer_token(im, 512, borde=borde)
        tok.save(TOKENS / f"{slug}.webp", "WEBP", quality=88)
        # 2) Retrato redimensionado a 768 de ancho máx + marca MR en esquina
        im.thumbnail((768, 1200), Image.LANCZOS)
        ret = marca.esquina(im)
        ret.save(RETRATOS / f"{slug}.webp", "WEBP", quality=86)
        print(f"Actor OK: {slug}")

def render_recorte(doc, page_idx, rect_frac, dst, dpi=220, max_w=2400, estampar=True):
    """Recorta una fracción (x0, y0, x1, y1) de una página PDF a alta resolución."""
    page = doc[page_idx]
    r = page.rect
    clip = fitz.Rect(r.width * rect_frac[0], r.height * rect_frac[1], r.width * rect_frac[2], r.height * rect_frac[3])
    pix = page.get_pixmap(clip=clip, dpi=dpi, alpha=False)
    im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    if im.width > max_w:
        im.thumbnail((max_w, int(max_w * 1.5)), Image.LANCZOS)
    if estampar:
        im = marca.esquina(im)
    im.save(dst, "WEBP", quality=88)
    print(f"Recorte OK: {dst.name} ({im.width}x{im.height})")
    return im.size

def extraer_con_smask(doc, xref, smask, fondo_rgb=(241, 234, 220)):
    """Extrae una imagen PDF con smask componiendo RGBA sobre el color de papel ANTES de convertir a RGB."""
    pix = fitz.Pixmap(doc, xref)
    if pix.n - pix.alpha >= 4:  # CMYK -> RGB
        pix = fitz.Pixmap(fitz.csRGB, pix)
    if smask:
        m = fitz.Pixmap(doc, smask)
        pix = fitz.Pixmap(pix, m)
        im = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
        fondo = Image.new("RGBA", im.size, fondo_rgb + (255,))
        im = Image.alpha_composite(fondo, im).convert("RGB")
    else:
        im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return im

def procesar_ayudas():
    doc = fitz.open(FUENTES / "Ayudas de juego.pdf")
    # p.1: Perfil John Milton (navegador)
    render_recorte(doc, 0, (0.095, 0.100, 0.945, 0.465), AYUDAS / "actualidad-1-milton.webp", dpi=220, max_w=1600)
    # p.2 izq: Menú La Carte
    render_recorte(doc, 1, (0.055, 0.120, 0.495, 0.710), AYUDAS / "actualidad-2-menu.webp", dpi=220, max_w=1200)
    # p.2 der: Itinerario del Orient Express
    render_recorte(doc, 1, (0.530, 0.100, 0.945, 0.675), AYUDAS / "actualidad-3-itinerario.webp", dpi=220, max_w=1200)
    # p.3 izq: Carta recortes «Adorable Chantel»
    render_recorte(doc, 2, (0.050, 0.095, 0.498, 0.358), AYUDAS / "actualidad-4-carta-recortes.webp", dpi=240, max_w=1200)
    # p.3 der: Nota manuscrita «Queridísima Chantel»
    render_recorte(doc, 2, (0.518, 0.100, 0.948, 0.352), AYUDAS / "actualidad-5-nota-cita.webp", dpi=240, max_w=1200)
    # p.4: Diario de John Milton (3 fragmentos separados + completo)
    render_recorte(doc, 3, (0.052, 0.098, 0.915, 0.460), AYUDAS / "actualidad-6-fragmento-1.webp", dpi=220, max_w=1600)
    render_recorte(doc, 3, (0.062, 0.445, 0.480, 0.895), AYUDAS / "actualidad-6-fragmento-2.webp", dpi=220, max_w=1200)
    render_recorte(doc, 3, (0.495, 0.405, 0.968, 0.905), AYUDAS / "actualidad-6-fragmento-3.webp", dpi=220, max_w=1200)
    render_recorte(doc, 3, (0.050, 0.098, 0.968, 0.905), AYUDAS / "actualidad-6-diario-completo.webp", dpi=200, max_w=1800)

def procesar_escenas():
    # 00: Portada Orient Express Escena.png (3840x2160 -> 2560x1440)
    im = Image.open(FUENTES / "Orient Express Escena.png").convert("RGB")
    im = im.resize((2560, 1440), Image.LANCZOS)
    marca.esquina(im).save(ESCENAS / "00-orient-express-portada.webp", "WEBP", quality=88)
    print("Escena OK: 00-orient-express-portada.webp (2560x1440)")

    # 01: Budapest (foto p.4 del PDF de aventura, xref=396) + foto Laberinto de Buda (p.18, xref=441)
    adv = fitz.open(FUENTES / "Aventura El simulacro desatado.pdf")
    buda = extraer_con_smask(adv, 396, 0)
    buda = buda.resize((1920, 1440), Image.LANCZOS)
    marca.esquina(buda).save(ESCENAS / "01-budapest.webp", "WEBP", quality=88)
    print("Escena OK: 01-budapest.webp (1920x1440)")

    lab = extraer_con_smask(adv, 441, 0)
    lab = lab.resize((998, 780), Image.LANCZOS)
    marca.esquina(lab).save(DIARIO / "laberinto-buda.webp", "WEBP", quality=88)
    print("Diario OK: laberinto-buda.webp (998x780)")

    # 02: Coches cama F y G (Mesa - SIN spoilers, componiendo xref=28 y xref=29 con sus smasks sobre pergamino limpio!)
    kdoc = fitz.open(FUENTES / "Keepers-Maps.pdf")
    coche_f = extraer_con_smask(kdoc, 28, 45, fondo_rgb=(241, 234, 220))
    coche_g = extraer_con_smask(kdoc, 29, 47, fondo_rgb=(241, 234, 220))
    W, H = 2400, 1320
    lienzo = Image.new("RGB", (W, H), (241, 234, 220))
    # Añadir sutil marco art déco Orient Express
    draw = ImageDraw.Draw(lienzo)
    draw.rectangle((28, 28, W - 28, H - 28), outline=(145, 58, 45), width=3)
    draw.rectangle((38, 38, W - 38, H - 38), outline=(182, 148, 92), width=2)
    cf = coche_f.resize((2200, round(2200 * coche_f.height / coche_f.width)), Image.LANCZOS)
    cg = coche_g.resize((2200, round(2200 * coche_g.height / coche_g.width)), Image.LANCZOS)
    lienzo.paste(cf, (100, 120))
    lienzo.paste(cg, (100, 720))
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 40)
    except Exception:
        font = ImageFont.load_default()
    draw.text((W // 2, 625), "Coche cama F", fill=(42, 32, 26), font=font, anchor="mm")
    draw.text((W // 2, 1225), "Coche cama G", fill=(42, 32, 26), font=font, anchor="mm")
    marca.esquina(lienzo).save(ESCENAS / "02-coches-cama-mesa.webp", "WEBP", quality=88)
    print(f"Escena OK: 02-coches-cama-mesa.webp ({W}x{H})")

    # 03: Coches cama F y G (Guardián - con etiquetas de ocupantes de p.2 de Keepers-Maps.pdf)
    render_recorte(kdoc, 1, (0.045, 0.080, 0.955, 0.515), ESCENAS / "03-coches-cama-guardian.webp", dpi=260, max_w=2400)

    # 04: Estambul en la actualidad (Mesa - sin Mezquita Velada)
    idoc = fitz.open(FUENTES / "Investigators-Maps.pdf")
    render_recorte(idoc, 0, (0.050, 0.080, 0.955, 0.922), ESCENAS / "04-estambul-mesa.webp", dpi=240, max_w=2200)

    # 05: Estambul en la actualidad (Guardián - con #11 La Mezquita Velada)
    render_recorte(kdoc, 0, (0.050, 0.080, 0.955, 0.922), ESCENAS / "05-estambul-guardian.webp", dpi=240, max_w=2200)

    # 06: La Mezquita Velada (plano táctico limpio de p.3 de Keepers-Maps.pdf)
    render_recorte(kdoc, 2, (0.075, 0.222, 0.922, 0.712), ESCENAS / "06-mezquita-velada.webp", dpi=300, max_w=2400)

if __name__ == "__main__":
    procesar_actores()
    procesar_ayudas()
    procesar_escenas()
    print("¡Todo el arte procesado!")
