"""Genera 50 presets para la MEDUSA (cabeza 0-1200 mirrored + 6 tentaculos por pin)."""
import json, sys

orig = json.load(open(sys.argv[1]))
out = sys.argv[2]

# layout fisico (de preset 3 "Debug")
TENT = [("Tentaculo 1 (P17)", 1200, 1800), ("Tentaculo 2 (P26)", 1800, 2100),
        ("Tentaculo 3 (P23)", 2100, 2400), ("Tentaculo 4 (P22)", 2400, 3000),
        ("Tentaculo 5 (P25)", 3000, 3300), ("Tentaculo 6 (P33)", 3300, 3600)]

# colores
MAG, CYA, BLU, VIO, PUR = [255, 0, 200], [0, 255, 255], [0, 40, 255], [140, 0, 255], [90, 0, 200]
PNK, RED, ORA, AMB, GRN = [255, 0, 90], [255, 0, 0], [255, 60, 0], [255, 150, 0], [0, 255, 60]
TEAL, LIM, WHT, OFF = [0, 255, 140], [150, 255, 0], [255, 255, 255], [0, 0, 0]


def seg(i, name, start, stop, fx, sx=128, ix=128, pal=0, col=(MAG, OFF, OFF), bri=255,
        rev=False, mi=False, c1=128, c2=128, c3=16, o1=False, o2=False, o3=False, of=0):
    return {"id": i, "start": start, "stop": stop, "grp": 1, "spc": 0, "of": of, "on": True,
            "frz": False, "bri": bri, "cct": 127, "set": 0, "n": name,
            "col": [list(c) for c in col], "fx": fx, "sx": max(0, min(255, sx)),
            "ix": max(0, min(255, ix)), "pal": pal, "c1": c1, "c2": c2, "c3": c3,
            "sel": i == 0, "rev": rev, "mi": mi, "o1": o1, "o2": o2, "o3": o3, "si": 0, "m12": 0}


def preset(name, head, tent, bri=60, jitter=0, revs=None, per=None):
    """head/tent: dicts de params. jitter: variacion de sx por tentaculo (organico).
    revs: lista de rev por tentaculo. per: lista de dicts que pisan params por tentaculo."""
    segs = [seg(0, "Cabeza", 0, 1200, mi=True, **head)]
    for k, (n, a, b) in enumerate(TENT):
        p = dict(tent)
        if jitter:
            p["sx"] = p.get("sx", 128) + (k * 7 % 5 - 2) * jitter
        if revs:
            p["rev"] = revs[k]
        if per:
            p.update(per[k])
        segs.append(seg(k + 1, n, a, b, **p))
    segs += [{"id": i, "stop": 0} for i in range(7, 16)]
    return {"on": True, "bri": bri, "transition": 7, "mainseg": 0, "n": name, "seg": segs}


ALT = [False, True] * 3
P = []
add = lambda *a, **k: P.append(preset(*a, **k))

# --- 1-10: oceano / bioluminiscencia
add("Latido Abisal", dict(fx=100, sx=60, ix=200, col=(MAG, OFF, OFF)),
    dict(fx=15, sx=40, ix=40, col=(VIO, OFF, OFF), bri=200), jitter=6)
add("Bioluminiscencia", dict(fx=101, sx=60, ix=128, pal=9),
    dict(fx=80, sx=90, ix=160, pal=37, bri=220))
add("Pulso Cian", dict(fx=2, sx=90, col=(CYA, BLU, OFF), pal=3),
    dict(fx=76, sx=150, ix=200, pal=37, bri=230), jitter=10)
add("Corriente Marina", dict(fx=110, sx=20, ix=4, pal=51),
    dict(fx=110, sx=40, ix=10, pal=51, bri=210), jitter=5)
add("Pacifica", dict(fx=101, sx=80, ix=100), dict(fx=101, sx=100, ix=160, bri=220), jitter=8)
add("Lago Violeta", dict(fx=75, sx=60, pal=46), dict(fx=75, sx=90, pal=46, bri=210), jitter=6)
add("Plancton", dict(fx=74, sx=40, ix=60, pal=63),
    dict(fx=74, sx=60, ix=120, pal=63, bri=220))
add("Medusa Fantasma", dict(fx=12, sx=40, col=(PUR, OFF, OFF)),
    dict(fx=77, sx=60, ix=230, col=(CYA, OFF, OFF), pal=0, bri=200), jitter=8)
add("Aguas Profundas", dict(fx=107, sx=30, ix=60, pal=60),
    dict(fx=107, sx=50, ix=120, pal=60, bri=220), jitter=5)
add("Aurora Boreal", dict(fx=38, sx=40, ix=128, pal=50), dict(fx=38, sx=70, ix=160, pal=50, bri=220))

# --- 11-20: movimiento de tentaculos
add("Ondas Hacia Afuera", dict(fx=2, sx=120, col=(BLU, OFF, OFF)),
    dict(fx=15, sx=120, ix=80, col=(CYA, BLU, OFF), bri=220))
add("Absorcion", dict(fx=100, sx=80, ix=180, col=(PNK, OFF, OFF)),
    dict(fx=15, sx=110, ix=80, col=(MAG, OFF, OFF), rev=True, bri=220))
add("Cometas", dict(fx=105, sx=60, ix=160, pal=40),
    dict(fx=59, sx=140, ix=220, col=(CYA, MAG, VIO), bri=230), jitter=12)
add("Gotas Descendentes", dict(fx=2, sx=50, col=(TEAL, OFF, OFF)),
    dict(fx=96, sx=128, ix=140, col=(CYA, OFF, OFF), bri=230), jitter=10)
add("Serpientes", dict(fx=67, sx=70, ix=128, pal=45),
    dict(fx=92, sx=110, ix=210, pal=45, bri=230), jitter=14)
add("Latigazo", dict(fx=12, sx=150, col=(VIO, OFF, OFF)),
    dict(fx=3, sx=180, ix=128, col=(MAG, CYA, OFF), bri=220), revs=ALT)
add("Danza Sinusoidal", dict(fx=108, sx=60, ix=40, pal=40),
    dict(fx=108, sx=90, ix=80, pal=37, bri=220), jitter=12)
add("Meteoros Magenta", dict(fx=2, sx=80, col=(PUR, OFF, OFF)),
    dict(fx=76, sx=180, ix=180, col=(MAG, OFF, OFF), pal=0, bri=240), jitter=12)
add("Ola Viajera", dict(fx=105, sx=80, ix=120, pal=9),
    dict(fx=52, sx=80, ix=60, col=(BLU, CYA, OFF), bri=220), jitter=6)
add("Ecolocalizacion", dict(fx=79, sx=110, ix=60, col=(CYA, OFF, OFF)),
    dict(fx=40, sx=120, ix=150, col=(CYA, OFF, OFF), bri=230), jitter=10)

# --- 21-30: fuego / toxico / colores calidos
add("Medusa de Fuego", dict(fx=66, sx=80, ix=160, pal=35),
    dict(fx=66, sx=70, ix=120, pal=35, bri=230))
add("Lava Viva", dict(fx=107, sx=50, ix=100, pal=8), dict(fx=110, sx=40, ix=8, pal=8, bri=220), jitter=6)
add("Marea Roja", dict(fx=100, sx=70, ix=200, col=(RED, OFF, OFF)),
    dict(fx=77, sx=120, ix=200, pal=69, bri=230), jitter=10)
add("Toxica", dict(fx=69, sx=60, pal=58), dict(fx=76, sx=150, ix=200, pal=58, bri=230), jitter=10)
add("Radiactiva", dict(fx=2, sx=110, col=(LIM, OFF, OFF)),
    dict(fx=15, sx=100, ix=60, col=(GRN, LIM, OFF), bri=220), jitter=8)
add("Brasas", dict(fx=45, sx=100, ix=160, col=(ORA, OFF, OFF)),
    dict(fx=88, sx=90, ix=200, col=(AMB, OFF, OFF), bri=220))
add("Ambar", dict(fx=101, sx=60, ix=128, pal=47), dict(fx=74, sx=60, ix=100, pal=47, bri=210))
add("Atardecer Coral", dict(fx=67, sx=50, ix=100, pal=13),
    dict(fx=110, sx=40, ix=6, pal=21, bri=220), jitter=6)
add("Icefire", dict(fx=107, sx=50, ix=80, pal=36), dict(fx=92, sx=100, ix=200, pal=36, bri=230), jitter=12)
add("Magma y Hielo", dict(fx=66, sx=80, ix=140, pal=35),
    dict(fx=76, sx=150, ix=200, col=(CYA, OFF, OFF), bri=230), jitter=10)

# --- 31-40: psicodelia
add("Caleidoscopio", dict(fx=97, sx=60, ix=128, pal=6),
    dict(fx=65, sx=60, ix=128, pal=6, bri=200, o1=True))
add("Arcoiris Lento", dict(fx=9, sx=30, ix=128), dict(fx=9, sx=60, ix=200, bri=200), jitter=8)
add("Candy", dict(fx=105, sx=90, ix=140, pal=57), dict(fx=110, sx=60, ix=12, pal=57, bri=210), jitter=8)
add("Neon Tiamat", dict(fx=109, sx=60, ix=128, pal=45),
    dict(fx=109, sx=80, ix=160, pal=45, bri=220), jitter=8)
add("Plasma", dict(fx=97, sx=80, ix=128, pal=41), dict(fx=97, sx=100, ix=160, pal=41, bri=220))
add("Sombras Danzantes", dict(fx=112, sx=60, ix=128, pal=40),
    dict(fx=112, sx=90, ix=128, pal=37, bri=220), jitter=8)
add("Rotacion Psico", dict(fx=114, sx=40, ix=128, pal=55),
    dict(fx=33, sx=90, ix=100, bri=180), jitter=10)
add("Blends", dict(fx=115, sx=60, ix=128, pal=61), dict(fx=115, sx=80, ix=128, pal=61, bri=210))
add("Colorloop Suave", dict(fx=8, sx=40, ix=255), dict(fx=67, sx=80, ix=128, pal=11, bri=200), jitter=8)
add("Rueda Magenta", dict(fx=113, sx=40, ix=128, pal=40),
    dict(fx=37, sx=120, ix=60, col=(MAG, VIO, OFF), bri=220), jitter=8)

# --- 41-50: chispas / eventos / ritmo
add("Chispas Electricas", dict(fx=2, sx=60, col=(PUR, OFF, OFF)),
    dict(fx=22, sx=100, ix=60, col=(PUR, CYA, OFF), bri=230))
add("Tormenta", dict(fx=57, sx=128, ix=80, col=(WHT, OFF, OFF), bri=180),
    dict(fx=57, sx=110, ix=60, col=(CYA, OFF, OFF), bri=230))
add("Luciernagas", dict(fx=49, sx=60, ix=100, col=(AMB, LIM, OFF)),
    dict(fx=51, sx=60, ix=120, col=(LIM, AMB, OFF), bri=220))
add("Estrellas del Fondo", dict(fx=81, sx=60, ix=100, pal=46),
    dict(fx=80, sx=60, ix=140, pal=46, bri=220))
add("Fuegos Marinos", dict(fx=89, sx=128, ix=80, pal=37),
    dict(fx=90, sx=100, ix=128, pal=37, bri=220))
add("Lluvia", dict(fx=2, sx=60, col=(BLU, OFF, OFF)),
    dict(fx=43, sx=120, ix=100, col=(CYA, BLU, OFF), bri=230), jitter=10)
add("Rebote", dict(fx=105, sx=60, ix=128, pal=37),
    dict(fx=91, sx=128, ix=80, col=(CYA, MAG, VIO), bri=230))
add("Pochoclo", dict(fx=74, sx=80, ix=100, pal=40),
    dict(fx=95, sx=128, ix=100, col=(MAG, CYA, OFF), bri=230))
add("Bpm Medusa", dict(fx=68, sx=80, pal=40), dict(fx=68, sx=100, pal=40, bri=220), jitter=6)
add("Juggle", dict(fx=64, sx=80, ix=100), dict(fx=64, sx=90, ix=160, bri=230), jitter=10)

assert len(P) == 50, len(P)
res = dict(orig)
for i, p in enumerate(P):
    res[str(20 + i)] = p
res["70"] = {"n": "Medusa 50", "on": True, "playlist": {
    "ps": list(range(20, 70)), "dur": [600] * 50, "transition": [7] * 50,
    "repeat": 0, "end": 0, "r": 1}}
# 71 Setup: un color fijo por pin (para chequear cableado al bootear)
PINS = [("Cabeza A (P16)", 0, 600, RED), ("Cabeza B (P18)", 600, 1200, GRN),
        ("Tentaculo 1 (P17)", 1200, 1800, BLU), ("Tentaculo 2 (P26)", 1800, 2100, AMB),
        ("Tentaculo 3 (P23)", 2100, 2400, CYA), ("Tentaculo 4 (P22)", 2400, 3000, MAG),
        ("Tentaculo 5 (P25)", 3000, 3300, WHT), ("Tentaculo 6 (P33)", 3300, 3600, ORA)]
res["71"] = {"on": True, "bri": 40, "transition": 0, "mainseg": 0, "n": "Setup",
             "seg": [seg(i, n, a, b, 0, col=(c, OFF, OFF)) for i, (n, a, b, c) in enumerate(PINS)]
             + [{"id": i, "stop": 0} for i in range(8, 16)]}
# 72 Booteo: Setup 10 s y despues la playlist 70
res["72"] = {"n": "Booteo", "on": True, "playlist": {
    "ps": [71], "dur": [100], "transition": [0], "repeat": 1, "end": 70, "r": 0}}
json.dump(res, open(out, "w"), separators=(",", ":"))
print("ok", len(res), "presets,", len(json.dumps(res)), "bytes")
