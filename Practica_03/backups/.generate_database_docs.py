import re, json, pathlib, html
from collections import defaultdict
P=pathlib.Path
src=P('db_test_7b1211.sql').read_text(encoding='utf-8',errors='replace')
def split_defs(s):
 out=[]; cur=''; depth=0; q=None; esc=False
 for c in s:
  cur+=c
  if q:
   if esc: esc=False
   elif c=='\\': esc=True
   elif c==q: q=None
  elif c in "'\"`": q=c
  elif c=='(': depth+=1
  elif c==')': depth-=1
  elif c==',' and depth==0: out.append(cur[:-1].strip()); cur=''
 if cur.strip(): out.append(cur.strip())
 return out
def block_after(pos):
 a=src.find('(',pos); dep=0; q=None; esc=False
 for i in range(a,len(src)):
  c=src[i]
  if q:
   if esc: esc=False
   elif c=='\\': esc=True
   elif c==q:q=None
  elif c in "'\"`":q=c
  elif c=='(':dep+=1
  elif c==')':
   dep-=1
   if dep==0:return src[a+1:i],src[i+1:i+350]
 raise ValueError('Unbalanced DDL at '+str(pos))
# Module taxonomy explicitly assigns every physical table.
modules={
'Usuarios y Seguridad':['tb_users','tb_people','tb_user_addresses','tbd_address_components','tbd_user_payment_methods','tbd_users_wishlist_products'],
'Catálogo y Productos':['tb_products','tbc_categories','tbd_products_categorias','tbd_products_users_providers','tbc_payment_methods_types'],
'Órdenes y Pagos':['tb_buyer_orders','tb_carts','tb_payment_methods','tb_payment_transaction','tb_payments','tbd_carts_items','tbd_order_items'],
'Envíos, Devoluciones y Cancelaciones':['tb_shipments','tb_returns','tb_refunds','tb_order_cancellations','tbd_return_items','tbd_cancellation_items'],
'Auditoría y Bitácora':['tb_logs']}
# Extract table definitions only, never data INSERTs.
tables={}; fks=[]
for m in re.finditer(r'CREATE TABLE `([^`]+)`\s*\(',src,re.I):
 name=m.group(1); inside,tail=block_after(m.start()); defs=split_defs(inside); cols=[]; keys=[]
 for d in defs:
  cm=re.match(r'`([^`]+)`\s+(.+)',d,re.S)
  if cm:
   cn,rest=cm.group(1),cm.group(2).strip().rstrip(','); typ=re.match(r'([a-zA-Z]+(?:\s*\([^)]*\))?(?:\s+unsigned)?(?:\s+zerofill)?)',rest,re.I).group(1)
   cols.append({'name':cn,'type':typ,'raw':rest,'notnull':bool(re.search(r'\bNOT NULL\b',rest,re.I)),'ai':bool(re.search(r'\bAUTO_INCREMENT\b',rest,re.I)),'default':(re.search(r'\bDEFAULT\s+((?:\'[^\']*\')|(?:"[^"]*")|(?:b\'[^\']*\')|(?:NULL)|(?:CURRENT_TIMESTAMP(?:\(\))?)|(?:[\w.]+))',rest,re.I) or [None,None])[1]})
  else: keys.append(d)
 tables[name]={'cols':cols,'keys':keys,'tail':tail}
for tn,t in tables.items():
 for d in t['keys']:
  m=re.search(r'CONSTRAINT `([^`]+)`\s+FOREIGN KEY\s*\(([^)]+)\)\s+REFERENCES `([^`]+)`\s*\(([^)]+)\)(.*)',d,re.I|re.S)
  if m:
   fk={'name':m[1],'table':tn,'columns':[x.strip().strip('`') for x in m[2].split(',')],'ref_table':m[3],'ref_columns':[x.strip().strip('`') for x in m[4].split(',')],'rules':m[5].strip()}; fks.append(fk)
# views: the active final CREATE VIEW definitions (exclude DROP/CREATE placeholders).
views={}
for m in re.finditer(r'/\*!50001 VIEW `([^`]+)` AS\s*(.*?)(?:\*/;)',src,re.S|re.I):
 name=m[1]; body=m[2].strip(); views[name]=body
# fallback / top-level simplified CREATE VIEW if wrappers differ
if not views:
 for m in re.finditer(r'CREATE VIEW `([^`]+)` AS\s*(.*?);',src,re.S|re.I):views[m[1]]=m[2]
trigs=[]
for m in re.finditer(r'TRIGGER \x60([^\x60]+)\x60 (.*?)\s*END \*/;;',src,re.S|re.I):trigs.append((m[1],m[2]))
# Object counts also cross-checked by direct identifier scans.
routines=re.findall(r'CREATE DEFINER=`[^`]+`@`[^`]+`\s+(FUNCTION|PROCEDURE) `([^`]+)`',src,re.I)
events=re.findall(r'/\*!50106 EVENT `([^`]+)`',src,re.I)
# Documentation helpers.
def escmd(x): return str(x).replace('|','\\|').replace('\n',' ')
def business(table,col):
 names={'ID':'Identificador primario de la fila.','status':'Indicador de estado/activo según la lógica de la entidad.','creation_date':'Fecha y hora de creación del registro.','last_update':'Fecha y hora de la última modificación.','user_ID':'Identificador de usuario asociado.','product_ID':'Identificador de producto asociado.','category_ID':'Identificador de categoría asociada.','seller_ID':'Identificador del vendedor.','buyer_ID':'Identificador del comprador.','name':'Nombre visible de la entidad.','description':'Descripción textual de la entidad.','email':'Correo de acceso/contacto.','nick':'Nombre de usuario público o de acceso.','password':'Credencial almacenada.','current_price':'Precio vigente.','current_stock':'Existencia disponible.','operation_date':'Fecha y hora de la operación auditada.','table_name':'Nombre de la tabla afectada.','table_operation':'Tipo de operación auditada.','db_user':'Usuario de base de datos que ejecutó la operación.'}
 return names.get(col, f'Campo {col}; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación.')
def rules_for(t,c):
 res=[]
 if c['name'] in pk_cols[t]:res.append('PK')
 if c['name'] in fk_cols[t]:res.append('FK')
 if c['name'] in uq_member_cols[t] and c['name'] not in pk_cols[t]:res.append('UQ')
 if c['notnull']:res.append('NN')
 if re.search(r'\bUNSIGNED\b',c['raw'],re.I):res.append('UN')
 if c['ai']:res.append('AI')
 return ', '.join(res) or '—'
pk_cols=defaultdict(set); pk_defs=defaultdict(list); fk_cols=defaultdict(set); unique_cols=defaultdict(set); uq_member_cols=defaultdict(set)
for t,meta in tables.items():
 for d in meta['keys']:
  m=re.match(r'PRIMARY KEY\s*\(([^)]+)',d,re.I)
  if m:
   pcols=[x.strip().strip('`') for x in m[1].split(',')]; pk_cols[t].update(pcols); pk_defs[t].append(pcols)
  m=re.match(r'(?:UNIQUE KEY|UNIQUE INDEX)\s+`?[^ `(]+`?\s*\(([^)]+)',d,re.I)
  if m:
   uc=re.findall(r'`([^`]+)`',m[1]); uq_member_cols[t].update(uc)
   # A composite UNIQUE index does not make each member column unique.
   if len(uc)==1: unique_cols[t].add(uc[0])
for f in fks:fk_cols[f['table']].update(f['columns'])
for t,meta in tables.items():
 for c in meta['cols']:
  if re.search(r'\bUNIQUE\b',c['raw'],re.I):unique_cols[t].add(c['name']); uq_member_cols[t].add(c['name'])
# Include derived table membership in both requested model syntaxes.
# Mermaid relation optionality and 1:1 detect unique child FK.
mer=['erDiagram']
for t,m in tables.items():
 mer.append('    '+t+' {')
 for c in m['cols']:
  typ=re.sub(r'_+','_',re.sub(r'[^A-Za-z0-9_]','_',c['type'])).strip('_')
  mark=' '+', '.join(x for x,yes in [('PK',c['name'] in pk_cols[t]),('FK',c['name'] in fk_cols[t]),('UK',c['name'] in uq_member_cols[t])] if yes) if any(c['name'] in z[t] for z in (pk_cols,fk_cols,uq_member_cols)) else ''
  mer.append(f'        {typ} {c["name"]}{mark}')
 mer.append('    }')
for f in fks:
 child=f['table']; parent=f['ref_table']; childcol=f['columns'][0]; unique=childcol in unique_cols[child] or [childcol] in pk_defs[child]; optional=not next(c for c in tables[child]['cols'] if c['name']==childcol)['notnull']
 # parent has many child rows unless child FK is unique, then one-to-one/zero-or-one.
 # A child row references exactly one parent (or zero/one when nullable); a parent can have zero children.
 left='o|' if optional else '||'; right='o|' if unique else 'o{'
 label=f['name']
 mer.append(f'    {parent} {left}--{right} {child} : "{label}"')
mermaid='\n'.join(mer)
# DBML with table groups and complete column/type/constraint data.
db=['Project db_test_7b {','  database_type: "MySQL"','  Note: "Extraído de db_test_7b1211.sql; 25 tablas y 34 FK"','}']
for t,meta in tables.items():
 db += ['',f'Table {t} {{']
 for c in meta['cols']:
  opts=[]
  if c['name'] in pk_cols[t] and len(pk_defs[t])==1 and len(pk_defs[t][0])==1:opts.append('pk')
  if c['name'] in unique_cols[t] and c['name'] not in pk_cols[t]:opts.append('unique')
  if c['notnull']:opts.append('not null')
  if c['ai']:opts.append('increment')
  if c['default'] is not None:
   dv=c['default']
   if dv.upper().startswith('CURRENT_TIMESTAMP') or re.match(r"b'[^']*'",dv,re.I): dv='`'+dv+'`'
   elif dv.upper()=='NULL': dv='null'
   opts.append('default: '+dv)
  db.append('  '+c['name']+' '+c['type']+(' ['+', '.join(opts)+']' if opts else ''))
 unique_indexes=[]
 for pcols in pk_defs[t]:
  if len(pcols)>1: unique_indexes.append(('PRIMARY',pcols,'pk'))
 for keydef in meta['keys']:
  um=re.match(r'UNIQUE KEY `([^`]+)`\s*\(([^)]+)\)',keydef,re.I)
  if um:
   ucols=re.findall(r'`([^`]+)`',um[2])
   if len(ucols)>1: unique_indexes.append((um[1],ucols,'unique'))
 if unique_indexes:
  db.append('  indexes {')
  for iname,ucols,itype in unique_indexes: db.append('    ('+', '.join(ucols)+") ["+itype+(", name: '"+iname+"'" if iname!='PRIMARY' else '')+"]")
  db.append('  }')
 db.append('}')
for f in fks:
 ondel=re.search(r'ON DELETE (CASCADE|SET NULL|RESTRICT|NO ACTION|SET DEFAULT)',f['rules'],re.I); onupd=re.search(r'ON UPDATE (CASCADE|SET NULL|RESTRICT|NO ACTION|SET DEFAULT)',f['rules'],re.I)
 opts=[]
 if ondel:opts.append('delete: '+ondel[1].lower())
 if onupd:opts.append('update: '+onupd[1].lower())
 lhs=f['table']+'.'+f['columns'][0] if len(f['columns'])==1 else f['table']+'.('+', '.join(f['columns'])+')'
 rhs=f['ref_table']+'.'+f['ref_columns'][0] if len(f['ref_columns'])==1 else f['ref_table']+'.('+', '.join(f['ref_columns'])+')'
 source_col=next(c for c in tables[f['table']]['cols'] if c['name']==f['columns'][0])
 unique_ref=len(f['columns'])==1 and (f['columns'][0] in unique_cols[f['table']] or [f['columns'][0]] in pk_defs[f['table']])
 operator=('-' if unique_ref else '>')+('?' if not source_col['notnull'] else '')
 db.append(f"Ref {f['name']}: {lhs} {operator} {rhs}"+(' ['+', '.join(opts)+']' if opts else ''))
# correct DBML column tuple syntax refs for single-column FKs.
for module,ts in modules.items():
 color={'Usuarios y Seguridad':'#DDEBFF','Catálogo y Productos':'#E3F5E8','Órdenes y Pagos':'#FFF0D6','Envíos, Devoluciones y Cancelaciones':'#F6E1ED','Auditoría y Bitácora':'#E9E1FF'}[module]
 db += ['',f'TableGroup "{module}" [color: {color}] {{']+[f'  {t}' for t in ts]+['}']
dbml='\n'.join(db)
# View base tables via FROM/JOIN table identifiers.
def view_tables(body): return list(dict.fromkeys(x for x in re.findall(r'\b(?:FROM|JOIN)\s+`([^`]+)`',body,re.I) if x in tables))
# Build report.
counts={'Tablas':len(tables),'Llaves foráneas':len(fks),'Vistas':len(views),'Triggers':len(trigs),'Funciones':sum(x[0].upper()=='FUNCTION' for x in routines),'Procedimientos':sum(x[0].upper()=='PROCEDURE' for x in routines),'Eventos':len(set(events))}
md=['# Diccionario de Datos — db_test_7b','','**Motor:** MySQL 8.0+ / InnoDB · **Juego de caracteres:** utf8mb4 · **Fuente:** `db_test_7b1211.sql`','', '## Índice general','','1. [Resumen ejecutivo e inventario](#resumen-ejecutivo-e-inventario)','2. [Clasificación por módulos](#clasificación-por-módulos-funcionales)','3. [Fichas de tablas](#fichas-técnicas-de-tablas)','4. [Vistas y automatización](#catálogo-de-automatización-y-vistas)','', '## Resumen ejecutivo e inventario','','El esquema modela comercio electrónico: identidad, catálogo, órdenes, pagos, logística y trazabilidad. El siguiente inventario se obtuvo del DDL; los textos funcionales no definidos mediante comentarios en el SQL se identifican como interpretación basada en nombres y restricciones.','', '| Objeto | Cantidad |','|---|---:|']
md += [f'| {k} | {v} |' for k,v in counts.items()]
md += ['',f'**Integridad de extracción:** {len(tables)} tablas físicas y {len(fks)} cláusulas `FOREIGN KEY` extraídas.','', '## Clasificación por módulos funcionales','']
for mod,ts in modules.items():md += [f'### {mod}', '', ', '.join(f'`{t}`' for t in ts), '']
md += ['## Fichas técnicas de tablas','']
# trigger/view association lookups
table_desc={
'tb_users':'Cuentas, credenciales y estado de usuario.', 'tb_people':'Datos personales asociados a una cuenta.', 'tb_user_addresses':'Direcciones de entrega vinculadas a usuarios.', 'tbd_address_components':'Componentes jerárquicos de direcciones y relación padre-hijo.', 'tbd_user_payment_methods':'Métodos de pago asociados a usuarios.', 'tbd_users_wishlist_products':'Productos guardados por usuarios en listas de deseos.',
'tb_products':'Catálogo de productos, precios, existencias y estado.', 'tbc_categories':'Catálogo jerárquico de categorías con autorreferencia.', 'tbd_products_categorias':'Asociación de productos con categorías.', 'tbd_products_users_providers':'Ofertas de productos por proveedores/vendedores.', 'tbc_payment_methods_types':'Catálogo de tipos de método de pago.',
'tb_buyer_orders':'Órdenes de compra, importes y estado de cumplimiento.', 'tb_carts':'Carritos de compra asociados a usuarios.', 'tb_payment_methods':'Métodos de pago registrados por usuarios.', 'tb_payment_transaction':'Transacciones enviadas al procesador de pagos.', 'tb_payments':'Pagos aplicados a órdenes con un método asociado.', 'tbd_carts_items':'Renglones de producto/proveedor dentro de carritos.', 'tbd_order_items':'Renglones de producto/proveedor dentro de órdenes.',
'tb_shipments':'Envíos de órdenes y dirección de entrega.', 'tb_returns':'Solicitudes de devolución asociadas a órdenes.', 'tb_refunds':'Reembolsos vinculados con órdenes.', 'tb_order_cancellations':'Cancelaciones solicitadas para órdenes.', 'tbd_return_items':'Productos incluidos en solicitudes de devolución.', 'tbd_cancellation_items':'Productos incluidos en cancelaciones.', 'tb_logs':'Bitácora de operaciones, usuario, fecha y descripción para auditoría.'}
for tn,meta in tables.items():
 mod=next(k for k,v in modules.items() if tn in v); tr=[n for n,b in trigs if re.search(r'\bON\s+`'+re.escape(tn)+r'`',b,re.I)]; vw=[n for n,b in views.items() if tn in view_tables(b)]
 md += [f'### `{tn}`', '',f'- **Módulo:** {mod}', '- **Motor/cotejamiento:** InnoDB / utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).',f'- **Descripción funcional:** {table_desc.get(tn, tn.replace("_"," ").capitalize()+"; propósito inferido de sus columnas y relaciones.")}',f'- **Triggers asociados:** {", ".join(f"`{x}`" for x in tr) or "ninguno"}.',f'- **Vistas asociadas:** {", ".join(f"`{x}`" for x in vw) or "ninguna"}.','', '| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional y Reglas de Negocio |','|---:|---|---|---|---|---|---|']
 for i,c in enumerate(meta['cols'],1):
  refs=[]
  for f in fks:
   if f['table']==tn:
    for j,col in enumerate(f['columns']):
     if col==c['name']:
      rules='; '.join(re.findall(r'ON (?:DELETE|UPDATE) (?:CASCADE|SET NULL|RESTRICT|NO ACTION|SET DEFAULT)',f['rules'],re.I)) or 'regla no declarada (MySQL: RESTRICT/NO ACTION)'
      refs.append(f'{f["name"]}: {f["ref_table"]}.{f["ref_columns"][j]} ({rules})')
  md.append(f'| {i} | `{c["name"]}` | `{escmd(c["type"])}` | {rules_for(tn,c)} | {escmd(c["default"] if c["default"] is not None else "—")} | {escmd("; ".join(refs) or "—")} | {business(tn,c["name"])} |')
 md += ['', '**Índices y restricciones declaradas:**']
 for k in meta['keys']:md.append('- `'+escmd(k)+'`')
 md += ['']
md += ['## Catálogo de automatización y vistas','','### Vistas','', '| Vista | Tablas base detectadas | Propósito (según SQL) |','|---|---|---|']
for n,b in sorted(views.items()):
 ts=view_tables(b); purpose=('Árbol recursivo y agregados de productos por categoría.' if n=='vw_total_products_by_category' else ('Consulta de trazabilidad de operaciones desde `tb_logs`.' if n.startswith('vw_trazabilidad_') else 'Vista de consulta derivada del DDL.'))
 md.append(f'| `{n}` | {", ".join(f"`{x}`" for x in ts) or "No resueltas"} | {purpose} |')
md += ['', '### Procedimientos almacenados','', '| Procedimiento | Propósito / tablas según código |','|---|---|']
for typ,n in routines:
 if typ.upper()=='PROCEDURE':
  m=re.search(r'PROCEDURE `'+re.escape(n)+r'`.*?\nBEGIN(.*?)END ;;',src,re.S); body=m[1] if m else ''; md.append(f'| `{n}` | {", ".join(f"`{x}`" for x in list(dict.fromkeys(t for t in re.findall(r"\\b(?:FROM|INTO|UPDATE)\\s+`?(\\w+)`?",body,re.I) if t in tables))) or "Ver cuerpo"} |')
md += ['', '### Funciones','', '| Función | Características declaradas |','|---|---|']
for typ,n in routines:
 if typ.upper()=='FUNCTION':
  mm=re.search(r'CREATE DEFINER=`[^`]+`@`[^`]+` FUNCTION `'+re.escape(n)+r'`.*?\n(.*?)\nBEGIN',src,re.S); md.append(f'| `{n}` | {escmd(mm[1].strip()) if mm else "Ver definición"} |')
md += ['', '### Eventos programados','', '| Evento | Agenda y operación |','|---|---|']
for n in sorted(set(events)):
 mm=re.search(r'EVENT `'+re.escape(n)+r'` ([^\n]+)',src); md.append(f'| `{n}` | {escmd(mm[1] if mm else "Ver definición en DDL")} |')
md += ['', '### Triggers de auditoría','',f'El esquema contiene **{len(trigs)} triggers**. Son AFTER INSERT, AFTER UPDATE o AFTER DELETE y escriben eventos en `tb_logs` con tabla, operación, usuario y fecha. Se distribuyen en las tablas operativas que tienen las tres operaciones; el inventario completo:']
md += ['', '| Trigger | Evento/tabla | Destino |','|---|---|---|']
for n,b in trigs:
 mm=re.search(r'(AFTER\s+(?:INSERT|UPDATE|DELETE)\s+ON\s+`([^`]+)`)',b,re.I); md.append(f'| `{n}` | {mm[1] if mm else "evento extraído"} | `tb_logs` |')
md += ['', '---','', '## Notas de interpretación','', '- Los tipos, nullabilidad, claves, valores predeterminados, motor y cotejamiento provienen del DDL. La descripción funcional por columna es interpretativa cuando el respaldo no contiene comentarios `COMMENT`.', '- Las reglas FK `ON DELETE` y `ON UPDATE` solo se consignan si aparecen explícitamente; en ausencia de cláusula se indica la regla predeterminada de restricción de MySQL.', '- El archivo SQL registra definiciones y también datos. El diccionario se construye desde `CREATE TABLE`, `CREATE VIEW` y bloques de rutinas, sin tratar filas de datos como DDL.']
P('DICCIONARIO_DATOS_db_test_7b.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
# ER markdown and html.
P('DIAGRAMA_ER_db_test_7b.md').write_text('# Diagrama Entidad–Relación — db_test_7b\n\nDER extraído del DDL `db_test_7b1211.sql`. Cardinalidad determinada por nulabilidad y unicidad de cada FK; cada línea corresponde a una constraint. Se verificaron '+str(len(fks))+' FKs. Aunque `tb_people.user_ID` es unique, admite NULL; por eso la relación con `tb_users` se representa opcional en ambos extremos, como permite el DDL.\n\n```mermaid\n'+mermaid+'\n```\n\n## Módulos\n\n'+ '\n'.join(f'- **{m}:** '+', '.join('`'+t+'`' for t in ts) for m,ts in modules.items())+'\n',encoding='utf-8')
P('schema.dbml').write_text(dbml+'\n',encoding='utf-8')
# HTML standalone document embeds Mermaid source; CDN supplies renderer. Pan/zoom and SVG/PNG export.
mer_js=json.dumps(mermaid,ensure_ascii=False).replace('</','<\\/')
page='''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DER · db_test_7b</title><script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script><style>*{box-sizing:border-box}body{margin:0;background:#101827;color:#eef4ff;font:15px system-ui}header{position:sticky;top:0;background:#17263d;padding:14px 22px;z-index:2;display:flex;align-items:center;gap:8px;flex-wrap:wrap}h1{font-size:19px;margin:0 auto 0 0}button{padding:8px 12px;border:1px solid #526987;border-radius:6px;background:#223754;color:white;cursor:pointer}#view{height:calc(100vh - 64px);overflow:hidden;cursor:grab;background:#f8fafc}#stage{transform-origin:0 0;width:max-content;min-width:100%;padding:25px}.mermaid{background:white;color:#111;padding:16px}.hint{color:#aebdd1;font-size:12px}@media print{header{position:static}#view{height:auto;overflow:visible}}</style></head><body><header><h1>Diagrama Entidad–Relación · db_test_7b · 25 tablas / 34 FK</h1><button onclick="zoom(1.2)">＋ Zoom</button><button onclick="zoom(.83)">− Zoom</button><button onclick="resetView()">Ajustar</button><button onclick="downloadSVG()">Descargar SVG</button><button onclick="downloadPNG()">Descargar PNG</button><span class="hint">Rueda: zoom · arrastrar: paneo</span></header><div id="view"><div id="stage"><pre class="mermaid"></pre></div></div><script>const source=__MERMAID__;document.querySelector('.mermaid').textContent=source;mermaid.initialize({startOnLoad:true,theme:'default',er:{diagramPadding:30},securityLevel:'strict'});let scale=1,x=0,y=0,stage=document.querySelector('#stage'),view=document.querySelector('#view');function paint(){stage.style.transform=`translate(${x}px,${y}px) scale(${scale})`}function zoom(f){scale=Math.max(.15,Math.min(4,scale*f));paint()}function resetView(){scale=Math.min((view.clientWidth-30)/stage.scrollWidth,(view.clientHeight-30)/stage.scrollHeight,1);x=10;y=10;paint()}view.addEventListener('wheel',e=>{e.preventDefault();zoom(e.deltaY<0?1.1:.9)},{passive:false});let drag=false,sx,sy;view.onpointerdown=e=>{drag=true;sx=e.clientX-x;sy=e.clientY-y;view.setPointerCapture(e.pointerId);view.style.cursor='grabbing'};view.onpointermove=e=>{if(drag){x=e.clientX-sx;y=e.clientY-sy;paint()}};view.onpointerup=()=>{drag=false;view.style.cursor='grab'};function downloadSVG(){let svg=document.querySelector('.mermaid svg');if(!svg)return alert('El diagrama aún se está renderizando');let c=svg.cloneNode(true);c.setAttribute('xmlns','http://www.w3.org/2000/svg');let blob=new Blob([new XMLSerializer().serializeToString(c)],{type:'image/svg+xml'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='diagrama_er_db_test_7b.svg';a.click();URL.revokeObjectURL(a.href)}function downloadPNG(){let svg=document.querySelector('.mermaid svg');if(!svg)return alert('El diagrama aún se está renderizando');let c=svg.cloneNode(true);c.setAttribute('xmlns','http://www.w3.org/2000/svg');let b=new Blob([new XMLSerializer().serializeToString(c)],{type:'image/svg+xml'}),u=URL.createObjectURL(b),im=new Image();im.onload=()=>{let vb=c.viewBox.baseVal,w=vb.width||im.width,h=vb.height||im.height,canvas=document.createElement('canvas');canvas.width=w*2;canvas.height=h*2;canvas.getContext('2d').scale(2,2);canvas.getContext('2d').drawImage(im,0,0,w,h);canvas.toBlob(blob=>{let a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='diagrama_er_db_test_7b.png';a.click();URL.revokeObjectURL(a.href);URL.revokeObjectURL(u)})};im.src=u}window.addEventListener('load',()=>setTimeout(resetView,1200));</script></body></html>'''.replace('__MERMAID__',mer_js)
P('diagrama_er.html').write_text(page,encoding='utf-8')
print(json.dumps({'counts':counts,'tableModules':{m:len(v) for m,v in modules.items()},'viewNames':list(views),'fkCount':len(fks),'triggerCount':len(trigs),'tableColumns':sum(len(t['cols']) for t in tables.values())},ensure_ascii=False,indent=2))


