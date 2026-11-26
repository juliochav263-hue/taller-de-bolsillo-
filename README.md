# Taller de Bolsillo

Sitio para emprendedores y feriantes de San Luis: agenda de ferias, Caja de feria y cuentas simples.
En vivo: https://taller-de-bolsillo-ar-26.web.app/

## Qué hay acá

| Carpeta | Qué es |
|---|---|
| `dist/` | El sitio tal cual se publica en Firebase Hosting (proyecto `taller-de-bolsillo-ar-26`). |
| `firebase.json` | Configuración del hosting, con las redirecciones de las herramientas que se sacaron. |
| `herramientas/agenda-ferias/` | `ferias.json`, con los datos verificados, y `generar.py`, que arma `dist/ferias-san-luis.html`. |
| `herramientas/caja-de-feria/` | `generar_caja.py`, que arma la prueba gratis (`dist/muestras/caja-de-feria.html`) y el kit pago (`kit/`). |
| `OBJETIVO.md` | Objetivo, estado de cada entregable y quién destraba cada bloqueo. |

## Cómo trabajamos

- Claude hace los cambios, los prueba y los sube a este repositorio.
- Las tareas para Codex están en **Issues**.
- **Publicar:** desde la carpeta del repositorio, `firebase deploy --only hosting --project taller-de-bolsillo-ar-26`.
- **Publicar solo:** el workflow `.github/workflows/deploy.yml` publica cada cambio en `dist/` cuando está cargado el secreto `FIREBASE_SERVICE_ACCOUNT` (Settings → Secrets and variables → Actions).
- **Regenerar:**
  - Agenda: `python3 -I herramientas/agenda-ferias/generar.py herramientas/agenda-ferias/ferias.json dist DD/MM/AAAA`
  - Caja: `python3 -I herramientas/caja-de-feria/generar_caja.py dist herramientas/caja-de-feria/kit`

## Reglas

- La agenda lleva solo datos que estén en la fuente original, con el enlace y la fecha de la nota.
- El botón de compra del kit en `dist/ferias.html` apunta a Wecito y no se cambia.
- Todo el texto va en español de Argentina, de vos y simple.
