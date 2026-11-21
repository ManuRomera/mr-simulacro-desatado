#!/usr/bin/env python3
"""Audio del Drive → OGG Opus 96 kbps en bucle sin costura.

Cada pista es un tramo de ≤10 min (Foundry lo carga en búfer) cuyo final se funde con su
principio (crossfade circular qsin), normalizado a −26 LUFS. Nada de fundidos a silencio:
al repetir no hay hueco. `--force` rehace todo.
"""
import subprocess, sys
from pathlib import Path

FUENTES = Path("/Volumes/Datos_Dock/FoundryVTT/Trabajo SIMULACRO/fuentes")
DEST = Path(__file__).resolve().parent.parent / "assets" / "audio"
DEST.mkdir(parents=True, exist_ok=True)
X = 4  # segundos de crossfade circular

# (origen, salida, inicio, fin) en segundos del original
PISTAS = [
    ("Efectos de sonido/Orient Express Train Sounds.mp3", "orient-express-tren.ogg", 60, 420),
    ("Música ambiente/Lovecraftian Detective Ambience.mp3", "ambiente-detective.ogg", 0, 480),
    ("Música escena/Música 1 escena.mp3", "escena-1-embarque.ogg", 0, 480),
    ("Música escena/Música 2 escena.mp3", "escena-2-budapest.ogg", 0, 480),
    ("Música escena/Música 3 escena.mp3", "escena-3-otro-lado.ogg", 0, 480),
    ("Música escena/Música 4 escena.mp3", "escena-4-mezquita.ogg", 0, 480),
]


def bucle(ini, fin, n=X):
    d = fin - ini
    return (f"[0:a]atrim=start={ini}:end={fin},asetpts=PTS-STARTPTS,asplit=3[m][h][t];"
            f"[m]atrim=start={n}:end={d - n},asetpts=PTS-STARTPTS[b];"
            f"[h]atrim=end={n},asetpts=PTS-STARTPTS[head];[t]atrim=start={d - n},asetpts=PTS-STARTPTS[tail];"
            f"[tail][head]acrossfade=d={n}:c1=qsin:c2=qsin[s];"
            "[b][s]concat=n=2:v=0:a=1,loudnorm=I=-26:TP=-4:LRA=6,aresample=48000[a]")


for rel, nombre, ini, fin in PISTAS:
    dst = DEST / nombre
    if dst.exists() and "--force" not in sys.argv:
        print(f"SKIP {nombre}")
        continue
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(FUENTES / rel), "-filter_complex", bucle(ini, fin),
                    "-map", "[a]", "-c:a", "libopus", "-b:a", "96k", "-ac", "2", str(dst)], check=True)
    print(f"OK {nombre}: {dst.stat().st_size / 1e6:.2f} MB")
