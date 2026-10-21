# Medusa — La Sede

Presets y config del WLED que maneja la medusa de La Sede: una cabeza y 6 tentáculos, 3600 LEDs.

## Controlador

- WLED 0.15.1, ESP32, 8 salidas WS281x, 3600 LEDs, AudioReactive apagado.
- Red: STA en **LaSedeFA**, IP fija `192.168.68.55/22`, gateway `192.168.68.1`, mDNS `medusa.local`.
- Respaldo: si no conecta a LaSedeFA, abre la red **Medusa-AP** (abierta, sin clave) en `4.3.2.1`.
- Al bootear: preset 72 "Booteo" → 10 s de "Setup" (un color por pin) → playlist 70 "Medusa 50".

## Layout

| Pin | Parte | LEDs | Color en "Setup" |
|---|---|---|---|
| P16 | Cabeza A | 0–600 | rojo |
| P18 | Cabeza B | 600–1200 | verde |
| P17 | Tentáculo 1 | 1200–1800 | azul |
| P26 | Tentáculo 2 | 1800–2100 | ámbar |
| P23 | Tentáculo 3 | 2100–2400 | cian |
| P22 | Tentáculo 4 | 2400–3000 | magenta |
| P25 | Tentáculo 5 | 3000–3300 | blanco |
| P33 | Tentáculo 6 | 3300–3600 | naranja |

En los presets la cabeza (0–1200) es un solo segmento con espejo (`mi`). Cada tentáculo tiene su propio segmento. Se asume que los datos de cada tentáculo entran desde la cabeza: con `rev=false` los efectos fluyen hacia afuera.

## Presets

- **1–19**: originales (backup en `backups/2026-10-20/wled_presets.json`).
- **20–69**: 50 efectos generados por `gen.py`:
  - 20–29 océano / bioluminiscencia
  - 30–39 movimiento de tentáculos
  - 40–49 fuego / tóxico
  - 50–59 psicodelia
  - 60–69 chispas / eventos
- **70** "Medusa 50": playlist aleatoria de 20–69, 1 min cada uno.
- **71** "Setup": color sólido por pin, para chequear el cableado.
- **72** "Booteo": 71 durante 10 s, y al terminar pasa a 70 (preset de arranque).

## Regenerar y subir

```sh
python gen.py backups/2026-10-20/wled_presets.json presets_new.json
curl -F "data=@presets_new.json;filename=/presets.json" http://medusa.local/upload
# WLED cachea presets.json: aplicar otro preset antes de probar el editado
curl -X POST -H 'Content-Type: application/json' -d '{"ps":72}' http://medusa.local/json/state
```

## Carpetas

- `backups/2026-10-20/`: config y presets tal como estaban antes de tocar nada (red vieja "Medusa").
- `actual/`: snapshot de la config, los presets y la info actuales.

Los `cfg.json` de WLED no incluyen las claves de wifi, solo su largo (`pskl`).
