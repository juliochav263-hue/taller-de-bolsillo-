# Genera dist/ferias-san-luis.html a partir de ferias.json. Uso: python3 -I generar.py ferias.json dist/
import json,sys,html,pathlib,datetime
datos=json.load(open(sys.argv[1],encoding="utf-8")); out=pathlib.Path(sys.argv[2])
revisado=sys.argv[3] if len(sys.argv)>3 else datetime.date.today().strftime("%d/%m/%Y")
src=(out/"muestras/precio-con-comision.html").read_text(encoding="utf-8")
style=src[src.index("<style>")+7:src.index("</style>")]
extra=""".agenda{width:min(920px,100% - 36px);margin:28px auto}.agenda h1{font:clamp(2.2rem,7vw,3.8rem)/1.02 Georgia,serif;margin:6px 0 12px}
.filtros{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}.filtros button{border:1px solid #91a08d;background:#fffefa;border-radius:20px;padding:7px 13px;font:inherit;cursor:pointer}.filtros button[aria-pressed=true]{background:#1b3428;color:#f6f7ed;border-color:#1b3428}
.feria{background:#fffefa;border:1px solid #d3d9cc;border-radius:16px;padding:18px;margin:12px 0}.feria h2{font:1.5rem/1.15 Georgia,serif;margin:4px 0 10px}
.pill{display:inline-block;font-size:.85rem;font-weight:750;border-radius:20px;padding:3px 10px}.abierta{background:#d9f39a;color:#1e382b}.repite{background:#e6ecf7;color:#23345c}.temporada{background:#f7ead0;color:#5c3e12}
.feria dl{display:grid;grid-template-columns:150px 1fr;gap:6px 14px;margin:0}.feria dt{font-weight:750;color:#455e50}.feria dd{margin:0}.fuente{font-size:.88rem;color:#455e50;margin-top:10px}
.calc{background:#1b3428;color:#f6f7ed;border-radius:22px;padding:22px;margin:30px 0}.calc h2{font:2rem Georgia,serif;margin:0 0 6px}.calc label{font-weight:700;display:block}.calc input{width:100%;padding:10px;border-radius:8px;border:0;margin-top:4px;font:inherit}
.calc .fields{display:grid;grid-template-columns:1fr 1fr;gap:12px}.calc .res{background:#eaf0c9;color:#182720;border-radius:12px;padding:14px;margin-top:14px}.calc .res strong{font-size:1.25rem}
.aviso{background:#fff7e0;border:1px solid #ecd9a4;border-radius:12px;padding:12px 14px}
.acciones{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 0}.accion{display:inline-block;background:#1b3428;color:#f6f7ed;border-radius:10px;padding:10px 14px;font-weight:750;text-decoration:none}
@media(max-width:560px){.feria dl{grid-template-columns:1fr}.feria dt{margin-top:6px}.calc .fields{grid-template-columns:1fr}}"""
etiqueta={"abierta":"Inscripción abierta","repite":"Se repite · llamá para la próxima fecha","temporada":"Temporada de verano · confirmá si abre"}
import urllib.parse,re as _re
SITIO="https://taller-de-bolsillo-ar-26.web.app/ferias-san-luis.html"
def slug(f): return _re.sub(r"[^a-z0-9]+","-",(f["localidad"]+" "+f["nombre"]).lower().translate(str.maketrans("áéíóúñü","aeiounu"))).strip("-")[:60]
def texto_wsp(f):
    return (f"📍 {f['nombre']} ({f['localidad']})\n🗓 {f['cuando']}\n📌 {f['donde']}\n✍️ Cómo anotarte: {f['anotarte']}\n\nTodas las ferias de San Luis: {SITIO}?utm_source=whatsapp&utm_medium=compartir")
def ics(f):
    from datetime import date,timedelta
    fin=(date.fromisoformat(f["hasta"])+timedelta(days=1)).strftime("%Y%m%d")
    esc=lambda s:s.replace("\\","\\\\").replace(",","\\,").replace(";","\\;").replace("\n","\\n")
    return "\r\n".join(["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Taller de Bolsillo//Ferias San Luis//ES","BEGIN:VEVENT",f"UID:{slug(f)}@tallerdebolsillo",
      f"DTSTAMP:{revisado[6:10]}{revisado[3:5]}{revisado[0:2]}T000000Z",f"DTSTART;VALUE=DATE:{f['desde'].replace('-','')}",f"DTEND;VALUE=DATE:{fin}",
      "SUMMARY:"+esc(f["nombre"]+" · "+f["localidad"]),"LOCATION:"+esc(f["donde"]+", "+f["localidad"]+", San Luis"),
      "DESCRIPTION:"+esc("Cómo anotarte: "+f["anotarte"]+"\nFuente: "+f["fuente"]),"END:VEVENT","END:VCALENDAR"])+"\r\n"
def acciones(f):
    a=f'<p class="acciones"><a class="accion" href="https://wa.me/?text={urllib.parse.quote(texto_wsp(f))}" target="_blank" rel="noopener">📲 Pasalo por WhatsApp</a>'
    if f.get("desde") and f.get("hasta"): a+=f'<a class="accion" href="ferias/{slug(f)}.ics" download>📅 Agendalo en el celu</a>'
    return a+'</p>'
def card(f):
    e=lambda k:html.escape(f[k])
    return (f'<article class="feria" data-loc="{e("localidad")}"><span class="pill {f["estado"]}">{etiqueta[f["estado"]]}</span>'
            f'<h2>{e("nombre")}</h2><dl><dt>Dónde queda</dt><dd>{e("localidad")} · {e("donde")}</dd><dt>Cuándo</dt><dd>{e("cuando")}</dd><dt>Horario</dt><dd>{e("horario")}</dd>'
            f'<dt>Cómo anotarte</dt><dd>{e("anotarte")}</dd><dt>Qué te piden</dt><dd>{e("piden")}</dd><dt>Cuánto sale el puesto</dt><dd>{e("costo")}</dd><dt>Qué llevar</dt><dd>{e("llevar")}</dd></dl>'+
            acciones(f)+f'<p class="fuente">Fuente: <a href="{e("fuente")}" rel="noopener" target="_blank">{e("medio")}</a> ({e("fecha_fuente")})</p></article>')
locs=sorted({f["localidad"] for f in datos})
orden={"abierta":0,"repite":1,"temporada":2}
cards="".join(card(f) for f in sorted(datos,key=lambda f:(orden[f["estado"]],f["localidad"])))
botones='<button type="button" data-loc="" aria-pressed="true">Todas</button>'+"".join(f'<button type="button" data-loc="{html.escape(l)}" aria-pressed="false">{html.escape(l)}</button>' for l in locs)
page=f"""<!doctype html><html lang="es-AR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ferias en San Luis: dónde, cuándo y cómo anotarte · Taller de Bolsillo</title><meta name="description" content="Las ferias de emprendedores y artesanos de San Luis, Juana Koslay, Villa Mercedes y Merlo: fechas, dónde anotarte, qué te piden y cuánto sale el puesto. Y una cuenta rápida para saber si te conviene ir."><style>{style}{extra}</style></head>
<body><nav><div class="wrap"><a class="brand" href="./"><i aria-hidden="true">TB</i>Taller de Bolsillo</a></div></nav><main class="agenda">
<p class="status">Para feriantes de San Luis · revisado el {revisado}</p><h1>Ferias en San Luis: dónde hay, cuándo y cómo anotarte</h1>
<p>Juntamos en un solo lugar las ferias de la provincia, con los teléfonos y lo que te piden para tener puesto. Revisamos las noticias y las convocatorias de los municipios todos los días.</p>
<p class="aviso">Las fechas cambian seguido y en muchas ferias hay que anotarse para cada fecha. <strong>Antes de ir, llamá o pasá a confirmar.</strong> Cada feria tiene el link a la nota de donde sacamos los datos.</p>
<div class="filtros" aria-label="Elegí tu localidad">{botones}</div>
<div id="lista">{cards}</div>
<section class="calc" aria-labelledby="calc-t"><h2 id="calc-t">¿Te conviene ir?</h2><p>Poné tus números y fijate cuánto te queda en limpio al final del día.</p>
<form id="cuenta"><div class="fields">
<label>Lo que pagás por el puesto (si es gratis, 0)<input type="number" min="0" step="any" required value="0"></label>
<label>Nafta, remis o colectivo, ida y vuelta<input type="number" min="0" step="any" required value="6000"></label>
<label>Otros gastos del día (comida, bolsas, cambio)<input type="number" min="0" step="any" required value="4000"></label>
<label>A cuánto vendés cada cosa<input type="number" min="0" step="any" required value="7000"></label>
<label>Cuánto te sale hacer cada cosa<input type="number" min="0" step="any" required value="2800"></label>
<label>Cuántas pensás vender<input type="number" min="0" step="1" required value="12"></label>
</div><div class="res" role="status"><strong id="r1"></strong><p id="r2" style="margin:6px 0 0"></p></div></form>
<p style="margin:12px 0 0">¿Querés tener estas cuentas en el celu sin internet? <a href="ferias.html" style="color:#e7efa9">Mirá el Kit para ferias</a>. Y el día de la feria, anotá cada venta con la <a href="muestras/caja-de-feria.html" style="color:#e7efa9">Caja de feria</a>.</p></section>
<p>¿Falta tu feria o cambió algún dato? Mandanos un mensaje por Instagram a <strong>@tallerdebolsillo.ar</strong> y la sumamos.</p>
<p><a href="./">Ver todas las herramientas</a></p></main>
<script>
const botones=[...document.querySelectorAll('.filtros button')];const tarjetas=[...document.querySelectorAll('.feria')];
function filtrar(loc){{for(const b of botones)b.setAttribute('aria-pressed',String(b.dataset.loc===loc));for(const t of tarjetas)t.hidden=!!loc&&t.dataset.loc!==loc;}}
for(const b of botones)b.addEventListener('click',()=>filtrar(b.dataset.loc));
const q=new URLSearchParams(location.search).get('localidad');if(q){{const b=botones.find(b=>b.dataset.loc.toLowerCase()===q.toLowerCase());if(b)filtrar(b.dataset.loc);}}
const form=document.querySelector('#cuenta');const r1=document.querySelector('#r1');const r2=document.querySelector('#r2');
const plata=v=>new Intl.NumberFormat('es-AR',{{style:'currency',currency:'ARS',maximumFractionDigits:0}}).format(v);
function cuenta(){{
 if(!form.checkValidity()){{r1.textContent='Completá todos los números.';r2.textContent='';return;}}
 const [puesto,viaje,otros,precio,costo,cant]=[...form.querySelectorAll('input')].map(i=>i.valueAsNumber);
 const gastos=puesto+viaje+otros;const queda=precio-costo;
 if(queda<=0){{r1.textContent='Así perdés plata en cada venta.';r2.textContent='Lo que cobrás no cubre lo que te sale hacerlo. Revisá el precio antes de ir.';return;}}
 const minimo=Math.ceil(gastos/queda);const neto=queda*cant-gastos;
 r1.textContent=neto>=0?'Te quedan '+plata(neto)+' limpios':'Perdés '+plata(-neto)+' en el día';
 r2.textContent=gastos===0?'No tenés gastos fijos ese día: cada venta te deja '+plata(queda)+'.':'Con '+minimo+(minimo===1?' venta':' ventas')+' cubrís el puesto, el viaje y los otros gastos ('+plata(gastos)+'). Cada venta te deja '+plata(queda)+'.';
}}
form.addEventListener('input',cuenta);form.addEventListener('submit',e=>e.preventDefault());cuenta();
</script></body></html>"""
(out/"ferias-san-luis.html").write_text(page,encoding="utf-8");print("ok",len(datos),"ferias")
(out/"ferias").mkdir(exist_ok=True)
for f in datos:
    if f.get("desde") and f.get("hasta"): (out/"ferias"/f"{slug(f)}.ics").write_text(ics(f),encoding="utf-8",newline="")
idx=out/"index.html"
if idx.exists():
    h=idx.read_text(encoding="utf-8")
    prox=sorted(datos,key=lambda f:(orden[f["estado"]],f["localidad"]))[:3]
    filas="".join(f'<li style="padding:10px 0;border-top:1px solid #d3d9cc"><span class="pill {f["estado"]}" style="font-size:.8rem;font-weight:750;border-radius:20px;padding:2px 9px;background:{ {"abierta":"#d9f39a","repite":"#e6ecf7","temporada":"#f7ead0"}[f["estado"]] }">{etiqueta[f["estado"]]}</span><br><strong>{html.escape(f["nombre"])}</strong> · {html.escape(f["localidad"])}<br><span style="color:#455e50">{html.escape(f["cuando"])}</span></li>' for f in prox)
    bloque=(f'<!--ferias-inicio--><section aria-labelledby="prox-t" style="background:#fffefa;border:1px solid #d3d9cc;border-radius:16px;padding:20px;margin:18px 0">'
            f'<h2 id="prox-t" style="font:1.9rem Georgia,serif;margin:0">Próximas ferias en San Luis</h2><p style="margin:4px 0 0;color:#455e50">Revisado el {revisado}</p>'
            f'<ul style="list-style:none;padding:0;margin:8px 0">{filas}</ul><a href="ferias-san-luis.html"><strong>Ver todas, con teléfonos y cómo anotarte</strong></a></section><!--ferias-fin-->')
    if "<!--ferias-inicio-->" in h: h=_re.sub(r"<!--ferias-inicio-->.*?<!--ferias-fin-->",lambda m:bloque,h,flags=_re.S)
    else:
        i=h.index("</section>",h.index('<section class="hero">'))+len("</section>"); h=h[:i]+"\n"+bloque+h[i:]
    idx.write_text(h,encoding="utf-8")
