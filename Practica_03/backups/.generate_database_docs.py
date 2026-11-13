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
# Count inserted tuples by table. Walk each INSERT statement with quote and
# parenthesis awareness so commas/parentheses inside string values do not count.
def insert_tuple_count(statement):
    vm=re.search(r'\bVALUES\b',statement,re.I)
    if not vm: return 0
    count=0; depth=0; quote=None; esc=False; i=vm.end()
    while i<len(statement):
        c=statement[i]
        if quote:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c==quote:
                if i+1<len(statement) and statement[i+1]==quote: i+=1
                else: quote=None
        elif c in "'\"`": quote=c
        elif c=='(':
            if depth==0: count+=1
            depth+=1
        elif c==')': depth=max(0,depth-1)
        i+=1
    return count
row_counts=defaultdict(int)
for section in re.finditer(r'-- Dumping data for table `([^`]+)`',src,re.I):
    end=src.find('UNLOCK TABLES;',section.end())
    if end<0: end=len(src)
    data_block=src[section.end():end]
    for m in re.finditer(r'\bINSERT\s+INTO\s+`?([^`\s(]+)`?',data_block,re.I):
        j=m.end(); quote=None; esc=False
        while j<len(data_block):
            c=data_block[j]
            if quote:
                if esc: esc=False
                elif c=='\\': esc=True
                elif c==quote:
                    if j+1<len(data_block) and data_block[j+1]==quote: j+=1
                    else: quote=None
            elif c in "'\"`": quote=c
            elif c==';': break
            j+=1
        row_counts[m[1]]+=insert_tuple_count(data_block[m.start():j])
for t in tables: row_counts.setdefault(t,0)
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
 mer.append(f'        int registros "{row_counts[t]:,} reg."')
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
 db += ['',f'Table {t} {{',f"  Note: 'Registros: {row_counts[t]:,}'"]
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
 group_total=sum(row_counts[t] for t in ts)
 unit='tabla' if len(ts)==1 else 'tablas'
 db += ['',f'TableGroup "{module}" [color: {color}] {{',f"  Note: '{len(ts)} {unit}; registros: {group_total:,}'"]+[f'  {t}' for t in ts]+['}']
dbml='\n'.join(db)
# View base tables via FROM/JOIN table identifiers.
def view_tables(body): return list(dict.fromkeys(x for x in re.findall(r'\b(?:FROM|JOIN)\s+`([^`]+)`',body,re.I) if x in tables))
# Build report.
counts={'Tablas':len(tables),'Llaves foráneas':len(fks),'Vistas':len(views),'Triggers':len(trigs),'Funciones':sum(x[0].upper()=='FUNCTION' for x in routines),'Procedimientos':sum(x[0].upper()=='PROCEDURE' for x in routines),'Eventos':len(set(events))}
md=['# Diccionario de Datos — db_test_7b','','**Motor:** MySQL 8.0+ / InnoDB · **Juego de caracteres:** utf8mb4 · **Fuente:** `db_test_7b1211.sql`','', '## Índice general','','1. [Resumen ejecutivo e inventario](#resumen-ejecutivo-e-inventario)','2. [Clasificación por módulos](#clasificación-por-módulos-funcionales)','3. [Fichas de tablas](#fichas-técnicas-de-tablas)','4. [Vistas y automatización](#catálogo-de-automatización-y-vistas)','', '## Resumen ejecutivo e inventario','','El esquema modela comercio electrónico: identidad, catálogo, órdenes, pagos, logística y trazabilidad. El siguiente inventario se obtuvo del DDL; los textos funcionales no definidos mediante comentarios en el SQL se identifican como interpretación basada en nombres y restricciones.','', '| Objeto | Cantidad |','|---|---:|']
md += [f'| {k} | {v} |' for k,v in counts.items()]
total_rows=sum(row_counts[t] for t in tables)
md += ['',f'**Integridad de extracción:** {len(tables)} tablas físicas y {len(fks)} cláusulas `FOREIGN KEY` extraídas.','', '## Resumen Volumétrico y Estado de Población de Datos','',
       'Conteos calculados a partir de las tuplas de cada sentencia `INSERT INTO` del respaldo. Las tablas sin sentencias de inserción se reportan con cero filas.','',
       '| # | Nombre de la Tabla | Módulo | Registros Poblados | Porcentaje del Total | Observaciones / Regla de Negocio Aplicada |',
       '|---:|---|---|---:|---:|---|']
vol_notes={
 'tb_users':'Cuentas cargadas como entidades de identidad; el estado activo/inactivo se conserva por fila.',
 'tb_people':'Datos personales asociados a cuentas; la carga mantiene la relación definida por sus claves.',
 'tb_products':'Catálogo de productos poblado con sus atributos comerciales.',
 'tbc_categories':'Catálogo de 100 categorías, con jerarquía/autorreferencia definida por el DDL.',
 'tbd_products_categorias':'Relaciones producto-categoría cargadas para clasificar el catálogo.',
 'tbd_products_users_providers':'Ofertas producto-proveedor cargadas para asociar inventario y proveedor.',
 'tb_logs':f'Bitácora con {row_counts["tb_logs"]:,} eventos; conserva operaciones de auditoría registradas en el respaldo.'}
index=0
module_labels={'Usuarios y Seguridad':'1. Usuarios y Seguridad','Catálogo y Productos':'2. Catálogo y Productos','Órdenes y Pagos':'3. Órdenes y Pagos','Envíos, Devoluciones y Cancelaciones':'4. Envíos, Devoluciones y Cancelaciones','Auditoría y Bitácora':'5. Auditoría y Bitácora'}
for mod,ts in modules.items():
 for tn in ts:
  index+=1; n=row_counts[tn]; pct=(100*n/total_rows) if total_rows else 0
  note=vol_notes.get(tn,'Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla.' if n==0 else 'Registros cargados según las tuplas INSERT del respaldo.')
  md.append(f'| {index} | `{tn}` | {module_labels[mod]} | {n:,} | {pct:.2f}% | {note} |')
md += [f'|  | **Total General de Registros** | **25 tablas** | **{total_rows:,}** | **100.00%** | Conteo exacto de tuplas INSERT. |','', '## Clasificación por módulos funcionales','']
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
 md += [f'### `{tn}`', '',f'- **Nombre:** `{tn}`',f'- **Módulo:** {mod}', '- **Motor:** InnoDB', '- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).',f'- **Registros Actuales:** {row_counts[tn]:,} registros'+(' (Tabla estructural lista para operación)' if row_counts[tn]==0 else ''),f'- **Descripción funcional:** {table_desc.get(tn, tn.replace("_"," ").capitalize()+"; propósito inferido de sus columnas y relaciones.")}',f'- **Triggers asociados:** {", ".join(f"`{x}`" for x in tr) or "ninguno"}.',f'- **Vistas asociadas:** {", ".join(f"`{x}`" for x in vw) or "ninguna"}.','', '| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |','|---:|---|---|---|---|---|---|']
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
print('Conteo exacto de registros por tabla (db_test_7b1211.sql):')
print(json.dumps({t:row_counts[t] for t in tables},ensure_ascii=False,indent=2))
print('Total general:',f'{total_rows:,}')
P('DICCIONARIO_DATOS_db_test_7b.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
# Produce a self-contained, searchable HTML rendition of the full dictionary.
def inline_html(text):
    value=html.escape(text,quote=False)
    value=re.sub(r'`([^`]+)`',r'<code>\1</code>',value)
    value=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',value)
    value=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',value)
    return value
def render_dictionary(markdown):
    out=[]; lines=markdown.splitlines(); i=0; card=False
    while i<len(lines):
        line=lines[i]
        ficha=re.match(r'^### `([^`]+)`\s*$',line)
        if ficha:
            if card: out.append('</div></details>')
            name=ficha[1]; mod=''
            for nxt in lines[i+1:i+5]:
                mm=re.match(r'- \*\*Módulo:\*\* (.+)',nxt)
                if mm: mod=mm[1]; break
            out.append(f'<details class="table-card" data-table="{html.escape(name)}" data-module="{html.escape(mod)}" data-count="{row_counts[name]}"><summary><span class="table-name">{inline_html(name)}</span><span class="table-module">{html.escape(mod)}</span><span class="table-count">{row_counts[name]:,} registros</span><span class="chevron">▼</span></summary><div class="ficha-content">')
            card=True; i+=1; continue
        if line.startswith('## ') or (line.startswith('### ') and not ficha):
            if card: out.append('</div></details>'); card=False
            level=len(line)-len(line.lstrip('#')); title=line[level+1:].strip()
            out.append(f'<h{level}>{inline_html(title)}</h{level}>'); i+=1; continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[c.strip().replace('\\|','|') for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-{3,}:?',c.replace(' ','')) for c in cells): rows.append(cells)
                i+=1
            if rows:
                out.append('<div class="table-wrap"><table><thead><tr>'+''.join(f'<th>{inline_html(c)}</th>' for c in rows[0])+'</tr></thead><tbody>')
                out.extend('<tr>'+''.join(f'<td>{inline_html(c)}</td>' for c in row)+'</tr>' for row in rows[1:])
                out.append('</tbody></table></div>')
            continue
        if line.startswith('- '):
            out.append('<ul>')
            while i<len(lines) and lines[i].startswith('- '): out.append('<li>'+inline_html(lines[i][2:])+'</li>'); i+=1
            out.append('</ul>'); continue
        if line.startswith('---'):
            out.append('<hr>'); i+=1; continue
        if line.strip(): out.append('<p>'+inline_html(line)+'</p>')
        i+=1
    if card: out.append('</div></details>')
    return '\n'.join(out)
dict_html='''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Diccionario de datos · db_test_7b</title><style>
:root{color-scheme:dark;--red:#B91C1C;--blue:#1D4ED8;--night:#080C14;--panel:#0F172A;--line:#334155;--text:#F8FAFC;--muted:#CBD5E1}*{box-sizing:border-box}body{margin:0;background:var(--night);color:var(--text);font:15px/1.55 system-ui,Segoe UI,Arial,sans-serif}header{position:sticky;top:0;z-index:5;background:linear-gradient(110deg,#B91C1C,#1D4ED8);padding:18px clamp(16px,4vw,48px);box-shadow:0 5px 24px #0009}h1{margin:0 0 12px;font-size:clamp(22px,3vw,34px)}.controls{display:flex;flex-wrap:wrap;gap:10px}.controls input,.controls select,.controls button{border:1px solid #64748b;border-radius:8px;padding:10px 12px;background:#0B1120;color:#fff;font:inherit}.controls input{flex:1;min-width:250px}.controls button{background:#B91C1C;font-weight:750;cursor:pointer}.controls button:hover{background:#EF4444}.count{align-self:center;font-weight:800;background:#0B1120;border-radius:99px;padding:8px 13px}main{max-width:1600px;margin:auto;padding:24px clamp(12px,3vw,36px)}h2,h3{scroll-margin-top:140px}h2{margin:38px 0 14px;padding:10px 14px;border-left:6px solid #EF4444;background:linear-gradient(90deg,#B91C1C,#1D4ED833);font-size:24px}h3{margin:0 0 12px;color:#fff;background:#B91C1C;border:1px solid #EF4444;border-radius:8px;padding:11px 14px}.table-card{margin:18px 0 28px;padding:16px;background:#0B1120;border:1px solid #1D4ED8;border-radius:12px;box-shadow:0 8px 30px #0006}.table-card ul{padding-left:24px}.table-wrap{overflow:auto;margin:14px 0 22px;border:1px solid var(--line);border-radius:8px}table{width:100%;border-collapse:collapse;background:#0F172A;font-size:13px}th,td{padding:8px 10px;border:1px solid #334155;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{position:sticky;top:0;background:#172544;color:#fff;font-weight:800}tbody tr:nth-child(odd){background:#0F172A}tbody tr:nth-child(even){background:#162238}code{color:#FDE68A;background:#1e293b;padding:1px 4px;border-radius:4px}a{color:#93C5FD}p{margin:10px 0;color:#E2E8F0}hr{border:0;border-top:1px solid #334155;margin:28px 0}.empty{display:none;padding:24px;text-align:center;color:#CBD5E1}
@media print{ :root{color-scheme:light}body{background:white!important;color:#111!important;font-size:10pt}header{position:static;background:white!important;color:#111;box-shadow:none;padding:0 0 12px}.controls{display:none}main{max-width:none;padding:0}h1,h2,h3{color:#111!important;background:#eee!important;border-color:#555!important;break-after:avoid}.table-card{background:white!important;color:#111!important;box-shadow:none;border:1px solid #888;break-inside:avoid-page}p,td,th,li{color:#111!important}table{font-size:8pt;background:white!important}th{position:static;background:#ddd!important;color:#111!important}tbody tr,tbody tr:nth-child(odd),tbody tr:nth-child(even){background:white!important}td,th{border:1px solid #888!important}code{background:#eee;color:#111}a{color:#111;text-decoration:none}.table-wrap{overflow:visible;border:0}tr{break-inside:avoid}h2{break-before:page}}
</style></head><body><header><h1>Diccionario de Datos · db_test_7b</h1><div class="controls"><input id="search" type="search" placeholder="Buscar tabla, columna, tipo o restricción…" aria-label="Buscar en el diccionario"><select id="module"><option value="">Todos los módulos</option>__MODULES__</select><button onclick="window.print()">Imprimir / Guardar PDF</button><span class="count">25 tablas · __TOTAL__ registros</span></div></header><main id="content">__BODY__<div id="empty" class="empty">No hay resultados para esos filtros.</div></main><script>const q=document.querySelector('#search'),m=document.querySelector('#module');function filter(){const term=q.value.trim().toLowerCase(),mod=m.value;document.querySelectorAll('#content table').forEach(t=>{for(const r of t.querySelectorAll('tbody tr')){const match=!term||r.innerText.toLowerCase().includes(term);r.hidden=!match}});let shown=0;document.querySelectorAll('.table-card').forEach(card=>{const moduleOK=!mod||card.dataset.module===mod;const rows=[...card.querySelectorAll('tbody tr')],rowMatch=!term||card.querySelector('h3').innerText.toLowerCase().includes(term)||rows.some(r=>!r.hidden)||card.querySelector('ul')?.innerText.toLowerCase().includes(term);card.hidden=!(moduleOK&&rowMatch);if(!card.hidden)shown++});document.querySelectorAll('#content>h2,#content>p,#content>table,#content>.table-wrap,#content>ul').forEach(el=>{if(!term&&!mod){el.hidden=false;return}if(el.matches('h2')){el.hidden=false;return}if(el.matches('p,ul'))el.hidden=!!term&&!el.innerText.toLowerCase().includes(term);if(el.matches('table,.table-wrap'))el.hidden=!el.querySelector('tbody tr:not([hidden])')});document.querySelector('#empty').style.display=shown||(!term&&!mod)?'none':'block'}q.addEventListener('input',filter);m.addEventListener('change',filter);</script></body></html>'''
module_options=''.join(f'<option value="{html.escape(k)}">{html.escape(module_labels[k])}</option>' for k in modules)
dict_html=dict_html.replace('__MODULES__',module_options).replace('__TOTAL__',f'{total_rows:,}').replace('__BODY__',render_dictionary('\n'.join(md)))
dict_html=dict_html.replace('const match=!term||r.innerText.toLowerCase().includes(term);r.hidden=!match','const card=t.closest(".table-card"),moduleOK=!mod||(card?card.dataset.module===mod:r.innerText.includes(mod)),nameHit=!!(card&&term&&card.dataset.table.toLowerCase().includes(term));const match=moduleOK&&(!term||nameHit||r.innerText.toLowerCase().includes(term));r.hidden=!match')
dict_html=dict_html.replace('<button onclick="window.print()">','<button id="toggleAll" class="quiet" type="button">Expandir / Contraer todas</button><button onclick="window.print()">')
dict_html=dict_html.replace("card.querySelector('h3').innerText.toLowerCase().includes(term)","card.dataset.table.toLowerCase().includes(term)")
dict_html=dict_html.replace("card.hidden=!(moduleOK&&rowMatch);if(!card.hidden)shown++", "card.hidden=!(moduleOK&&rowMatch);if(term&&!card.hidden)card.open=true;if(!card.hidden)shown++")
dict_html=dict_html.replace('</style>', '''
:root{color-scheme:dark;--red:#CC0000;--red-edge:#FF0000;--black:#000000;--black-row:#121212;--bio:#79ADFF;--white:#FFFFFF}body{background:#000000;color:#FFFFFF}header{background:linear-gradient(105deg,#CC0000,#0D0D0D 72%);border-bottom:2px solid #FF0000}.controls input,.controls select,.controls button{background:#0D0D0D;color:#FFFFFF;border-color:#FF0000}.controls button{background:#CC0000}.controls button.quiet{background:#0D0D0D;color:#79ADFF;border-color:#79ADFF;font-size:13px}.controls button:hover{background:#FF0000}.count,.table-count{color:#79ADFF}.table-card{display:block;margin:12px 0;padding:0;background:#000000;border:1px solid #FF0000;border-radius:8px;box-shadow:none;overflow:hidden}.table-card>summary{display:flex;align-items:center;gap:14px;list-style:none;cursor:pointer;background:#CC0000;border:1px solid #FF0000;padding:12px 16px;color:#FFFFFF;font-weight:800}.table-card>summary::-webkit-details-marker{display:none}.table-name{color:#FFFFFF;min-width:220px}.table-module{font-weight:500;color:#FFFFFF;opacity:.92}.table-count{margin-left:auto;font-weight:900;white-space:nowrap}.chevron{color:#FFFFFF;transition:transform .15s}.table-card[open]>.table-card>summary .chevron,.table-card[open]>summary .chevron{transform:rotate(180deg)}.ficha-content{padding:14px;background:#000000}.ficha-content h3{background:#0D0D0D;border-color:#FF0000;color:#FFFFFF}.table-wrap{border-color:#FF0000}table{background:#000000;color:#FFFFFF}th{background:#CC0000;color:#FFFFFF;border-color:#FF0000}tbody tr:nth-child(odd){background:#000000;color:#FFFFFF}tbody tr:nth-child(even){background:#121212;color:#FFFFFF}td{color:#FFFFFF;border-color:#333}code{background:#0D0D0D;color:#79ADFF}a{color:#79ADFF}.table-card[hidden]{display:none!important}
@media print{body{background:#fff!important}.controls{display:none!important}.table-card{break-inside:auto;background:#fff!important;border:1px solid #555!important;overflow:visible}.table-card>summary{display:list-item!important;background:#eee!important;color:#111!important;border-color:#555!important;break-after:avoid}.table-name,.table-module,.chevron,.table-count{color:#111!important}.table-card>.ficha-content,.table-card:not([open])>.ficha-content{display:block!important;background:#fff!important}.table-card[hidden]{display:block!important}.ficha-content{padding:6px}.ficha-content h3{background:#eee!important;color:#111!important;border-color:#555!important}table,tbody tr,tbody tr:nth-child(odd),tbody tr:nth-child(even){background:#fff!important;color:#111!important}th{background:#ddd!important;color:#111!important}td,th{color:#111!important;border-color:#777!important}.table-wrap{overflow:visible}h2{break-before:page}}
</style>''')
dict_html=dict_html.replace("const q=document.querySelector('#search'),m=document.querySelector('#module');function filter()", "const q=document.querySelector('#search'),m=document.querySelector('#module'),details=[...document.querySelectorAll('.table-card')],toggle=document.querySelector('#toggleAll');toggle.addEventListener('click',()=>{const expand=details.some(d=>!d.open);details.forEach(d=>d.open=expand)});let beforePrint={open:[],term:'',module:''};window.addEventListener('beforeprint',()=>{beforePrint={open:details.map(d=>d.open),term:q.value,module:m.value};q.value='';m.value='';filter();details.forEach(d=>d.open=true)});window.addEventListener('afterprint',()=>{q.value=beforePrint.term;m.value=beforePrint.module;filter();details.forEach((d,i)=>d.open=beforePrint.open[i])});function filter()")
for old,new in {'#B91C1C':'#CC0000','#1D4ED8':'#79ADFF','#080C14':'#000000','#0F172A':'#000000','#162238':'#121212','#EF4444':'#FF0000','#F8FAFC':'#FFFFFF','#93C5FD':'#79ADFF','#FDE68A':'#79ADFF'}.items(): dict_html=dict_html.replace(old,new)
dict_html=dict_html.replace('<h1>Diccionario de Datos · db_test_7b</h1>','<h1>Miles Morales · Diccionario de Datos · db_test_7b</h1>')
P('diccionario_datos.html').write_text(dict_html,encoding='utf-8')
# ER markdown and html.
P('DIAGRAMA_ER_db_test_7b.md').write_text('# Diagrama Entidad–Relación — db_test_7b\n\nDER extraído del DDL `db_test_7b1211.sql`. Cardinalidad determinada por nulabilidad y unicidad de cada FK; cada línea corresponde a una constraint. Se verificaron '+str(len(fks))+' FKs. Aunque `tb_people.user_ID` es unique, admite NULL; por eso la relación con `tb_users` se representa opcional en ambos extremos, como permite el DDL.\n\n```mermaid\n'+mermaid+'\n```\n\n## Módulos\n\n'+ '\n'.join(f'- **{m}:** '+', '.join('`'+t+'`' for t in ts) for m,ts in modules.items())+'\n',encoding='utf-8')
P('schema.dbml').write_text(dbml+'\n',encoding='utf-8')
# HTML standalone document embeds Mermaid source; CDN supplies renderer. Pan/zoom and SVG/PNG export.
mer_js=json.dumps(mermaid,ensure_ascii=False).replace('</','<\\/')
page='''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DER · db_test_7b</title><script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script><style>*{box-sizing:border-box}body{margin:0;background:#101827;color:#eef4ff;font:15px system-ui}header{position:sticky;top:0;background:#17263d;padding:14px 22px;z-index:2;display:flex;align-items:center;gap:8px;flex-wrap:wrap}h1{font-size:19px;margin:0 auto 0 0}button{padding:8px 12px;border:1px solid #526987;border-radius:6px;background:#223754;color:white;cursor:pointer}#view{height:calc(100vh - 64px);overflow:hidden;cursor:grab;background:#f8fafc}#stage{transform-origin:0 0;width:max-content;min-width:100%;padding:25px}.mermaid{background:white;color:#111;padding:16px}.hint{color:#aebdd1;font-size:12px}@media print{header{position:static}#view{height:auto;overflow:visible}}</style></head><body><header><h1>Diagrama Entidad–Relación · db_test_7b · 25 tablas / 34 FK</h1><button onclick="zoom(1.2)">＋ Zoom</button><button onclick="zoom(.83)">− Zoom</button><button onclick="resetView()">Ajustar</button><button onclick="downloadSVG()">Descargar SVG</button><button onclick="downloadPNG()">Descargar PNG</button><span class="hint">Rueda: zoom · arrastrar: paneo</span></header><div id="view"><div id="stage"><pre class="mermaid"></pre></div></div><script>const source=__MERMAID__;document.querySelector('.mermaid').textContent=source;mermaid.initialize({startOnLoad:true,theme:'default',er:{diagramPadding:30},securityLevel:'strict'});let scale=1,x=0,y=0,stage=document.querySelector('#stage'),view=document.querySelector('#view');function paint(){stage.style.transform=`translate(${x}px,${y}px) scale(${scale})`}function zoom(f){scale=Math.max(.15,Math.min(4,scale*f));paint()}function resetView(){scale=Math.min((view.clientWidth-30)/stage.scrollWidth,(view.clientHeight-30)/stage.scrollHeight,1);x=10;y=10;paint()}view.addEventListener('wheel',e=>{e.preventDefault();zoom(e.deltaY<0?1.1:.9)},{passive:false});let drag=false,sx,sy;view.onpointerdown=e=>{drag=true;sx=e.clientX-x;sy=e.clientY-y;view.setPointerCapture(e.pointerId);view.style.cursor='grabbing'};view.onpointermove=e=>{if(drag){x=e.clientX-sx;y=e.clientY-sy;paint()}};view.onpointerup=()=>{drag=false;view.style.cursor='grab'};function downloadSVG(){let svg=document.querySelector('.mermaid svg');if(!svg)return alert('El diagrama aún se está renderizando');let c=svg.cloneNode(true);c.setAttribute('xmlns','http://www.w3.org/2000/svg');let blob=new Blob([new XMLSerializer().serializeToString(c)],{type:'image/svg+xml'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='diagrama_er_db_test_7b.svg';a.click();URL.revokeObjectURL(a.href)}function downloadPNG(){let svg=document.querySelector('.mermaid svg');if(!svg)return alert('El diagrama aún se está renderizando');let c=svg.cloneNode(true);c.setAttribute('xmlns','http://www.w3.org/2000/svg');let b=new Blob([new XMLSerializer().serializeToString(c)],{type:'image/svg+xml'}),u=URL.createObjectURL(b),im=new Image();im.onload=()=>{let vb=c.viewBox.baseVal,w=vb.width||im.width,h=vb.height||im.height,canvas=document.createElement('canvas');canvas.width=w*2;canvas.height=h*2;canvas.getContext('2d').scale(2,2);canvas.getContext('2d').drawImage(im,0,0,w,h);canvas.toBlob(blob=>{let a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='diagrama_er_db_test_7b.png';a.click();URL.revokeObjectURL(a.href);URL.revokeObjectURL(u)})};im.src=u}window.addEventListener('load',()=>setTimeout(resetView,1200));</script></body></html>'''.replace('__MERMAID__',mer_js)
page=page.replace("theme:'default',er:{diagramPadding:30}","theme:'base',themeVariables:{primaryColor:'#CC0000',primaryTextColor:'#FFFFFF',primaryBorderColor:'#FF0000',attributeBackgroundColorOdd:'#000000',attributeBackgroundColorEven:'#121212',textColor:'#FFFFFF',lineColor:'#79ADFF',edgeLabelBackground:'#000000',secondaryColor:'#000000',tertiaryColor:'#121212',mainBkg:'#000000',nodeBorder:'#FF0000',background:'#000000'},er:{diagramPadding:30}")
page=page.replace('</style>', '''
body{background:#080C14;color:#F8FAFC}header{background:linear-gradient(110deg,#B11313 0%,#E23636 48%,#0F2557 100%);box-shadow:0 4px 26px #e2363644}h1{display:flex;align-items:center;gap:10px}h1:before{content:"🕷";font-size:25px}button{border:1px solid #7fa8ff;background:#0F2557;color:#fff;border-radius:8px;font-weight:700;box-shadow:0 0 12px #1d4ed844}button:hover{background:#1D4ED8;border-color:#fff}#view{background-color:#080C14;background-image:radial-gradient(ellipse at 50% 50%,#1d4ed822,transparent 62%);cursor:grab}#stage{padding:25px}.mermaid{background:transparent;padding:0;filter:drop-shadow(0 0 12px #e2363622)}.record-badge{padding:6px 12px;border:1px solid #fff8;border-radius:99px;background:#080C14;color:white;font-weight:800;box-shadow:0 0 16px #1d4ed888}.hint{color:#fff}.er.entityBox{fill:#B11313!important;stroke:#E23636!important;stroke-width:2.5px!important;filter:drop-shadow(0 0 5px #e2363688)}.er.attributeBoxEven{fill:#0F172A!important;stroke:#1D4ED8!important}.er.attributeBoxOdd{fill:#162238!important;stroke:#1D4ED8!important}.er.relationshipLine,.er.relationshipLabelBox{stroke:#CBD5E1!important;stroke-width:1.6px!important}.er.relationshipLabel{fill:#fff!important;font-weight:700!important}.er text{fill:#F8FAFC!important;font-weight:600!important}.er.entityLabel{fill:#fff!important;font-weight:800!important}
@media print{header{position:static}#view{height:auto;overflow:visible}}
</style>''')
page=page.replace('<h1>Diagrama Entidad–Relación · db_test_7b · 25 tablas / 34 FK</h1>',f'<h1>Spider-Man · DER db_test_7b · 25 tablas / 34 FK</h1><span class="record-badge">{total_rows:,} registros</span>')
web_helper='''function addWebBackground(svg){if(svg.querySelector('#spiderWebPattern'))return;let ns='http://www.w3.org/2000/svg',defs=document.createElementNS(ns,'defs'),pat=document.createElementNS(ns,'pattern');pat.setAttribute('id','spiderWebPattern');pat.setAttribute('width','240');pat.setAttribute('height','240');pat.setAttribute('patternUnits','userSpaceOnUse');let path=document.createElementNS(ns,'path');path.setAttribute('d','M120 0V240M0 120H240M0 0L240 240M240 0L0 240M0 120Q120 92 240 120M120 0Q92 120 120 240');path.setAttribute('fill','none');path.setAttribute('stroke','#9fb4d0');path.setAttribute('stroke-opacity','.12');path.setAttribute('stroke-width','1');pat.appendChild(path);defs.appendChild(pat);svg.insertBefore(defs,svg.firstChild);let vb=svg.viewBox.baseVal,rect=document.createElementNS(ns,'rect');rect.setAttribute('id','spiderWebBackdrop');rect.setAttribute('x',vb.x);rect.setAttribute('y',vb.y);rect.setAttribute('width',vb.width);rect.setAttribute('height',vb.height);rect.setAttribute('fill','#080C14');rect.setAttribute('stroke','none');svg.insertBefore(rect,defs);let web=document.createElementNS(ns,'rect');web.setAttribute('x',vb.x);web.setAttribute('y',vb.y);web.setAttribute('width',vb.width);web.setAttribute('height',vb.height);web.setAttribute('fill','url(#spiderWebPattern)');web.setAttribute('stroke','none');svg.insertBefore(web,defs)}function withSpiderBackground(svg){let c=svg.cloneNode(true);c.setAttribute('xmlns','http://www.w3.org/2000/svg');let style=document.createElementNS('http://www.w3.org/2000/svg','style');style.textContent='.er.entityBox{fill:#B11313;stroke:#E23636;stroke-width:2.5px}.er.attributeBoxEven{fill:#0F172A;stroke:#1D4ED8}.er.attributeBoxOdd{fill:#162238;stroke:#1D4ED8}.er.relationshipLine{stroke:#CBD5E1;stroke-width:1.6px}.er.relationshipLabel{fill:#fff;font-weight:bold}.er text{fill:#F8FAFC;font-weight:600}';c.insertBefore(style,c.firstChild);addWebBackground(c);return c}new MutationObserver(()=>{let s=document.querySelector('.mermaid svg');if(s)addWebBackground(s)}).observe(document.querySelector('.mermaid'),{childList:true,subtree:true});'''
page=page.replace('function downloadSVG(){',web_helper+'function downloadSVG(){')
page=page.replace("let c=svg.cloneNode(true);c.setAttribute('xmlns','http://www.w3.org/2000/svg');",'let c=withSpiderBackground(svg);')
page=page.replace('function withSpiderBackground(svg){let c=withSpiderBackground(svg);','function withSpiderBackground(svg){let c=svg.cloneNode(true);c.setAttribute(\'xmlns\',\'http://www.w3.org/2000/svg\');')
page=page.replace('.er.entityBox{fill:#B11313!important;stroke:#E23636!important;stroke-width:2.5px!important;filter:drop-shadow(0 0 5px #e2363688)}.er.attributeBoxEven{fill:#0F172A!important;stroke:#1D4ED8!important}.er.attributeBoxOdd{fill:#162238!important;stroke:#1D4ED8!important}.er.relationshipLine,.er.relationshipLabelBox{stroke:#CBD5E1!important;stroke-width:1.6px!important}', '.er.entityBox{fill:#B91C1C!important;stroke:#EF4444!important;stroke-width:2.5px!important;filter:drop-shadow(0 0 5px #ef444488)}.er.attributeBoxOdd,.er.attributeBoxOdd rect{fill:#0F172A!important;stroke:#1D4ED8!important}.er.attributeBoxEven,.er.attributeBoxEven rect{fill:#172544!important;stroke:#1D4ED8!important}.er.relationshipLine{stroke:#94A3B8!important;stroke-width:1.6px!important}.er.relationshipLabelBox{fill:#0B1120!important;stroke:#94A3B8!important}')
readability_helper='''function styleReadability(svg){if(!svg.querySelector('#milesSvgStyles')){let s=document.createElementNS('http://www.w3.org/2000/svg','style');s.id='milesSvgStyles';s.textContent='.entityBox,.entityBox rect{fill:#CC0000!important;stroke:#FF0000!important}.entityBox text,.entityLabel{fill:#FFFFFF!important;font-weight:900!important}rect.attributeBoxOdd,.attributeBoxOdd rect{fill:#000000!important;stroke:#CC0000!important}rect.attributeBoxEven,.attributeBoxEven rect{fill:#121212!important;stroke:#CC0000!important}.attributeBoxOdd text,.attributeBoxEven text{fill:#FFFFFF!important}.recordRow text,.recordRow .label{fill:#79ADFF!important;font-weight:900!important}.recordRow rect{fill:#000000!important;stroke:#79ADFF!important}path.relationshipLine,.relationshipLine{stroke:#79ADFF!important;stroke-width:1.8px!important}.relationshipLabelBox,.relationshipLabelBox rect{fill:#000000!important;stroke:#79ADFF!important}.relationshipLabel,.relationshipLabel text{fill:#FFFFFF!important}';svg.insertBefore(s,svg.firstChild)}svg.querySelectorAll('g.er.attributeBoxOdd,g.er.attributeBoxEven').forEach(g=>{let r=g.querySelector('rect');if(!r)return;let label=(g.textContent||'').toLowerCase();if(label.includes('registros')){g.classList.add('recordRow');r.setAttribute('fill','#000000');r.setAttribute('stroke','#79ADFF');g.querySelectorAll('text').forEach(t=>{t.setAttribute('fill','#79ADFF');t.style.fontWeight='900'})}else{let odd=g.classList.contains('attributeBoxOdd');r.setAttribute('fill',odd?'#000000':'#121212');r.setAttribute('stroke','#CC0000');g.querySelectorAll('text').forEach(t=>t.setAttribute('fill','#FFFFFF'))}});svg.querySelectorAll('path.relationshipLine').forEach(p=>p.setAttribute('stroke','#79ADFF'));svg.querySelectorAll('.relationshipLabelBox rect').forEach(r=>{r.setAttribute('fill','#000000');r.setAttribute('stroke','#79ADFF')})}'''
page=page.replace('function withSpiderBackground(svg){',readability_helper+'function withSpiderBackground(svg){')
page=page.replace('addWebBackground(c);return c}', 'addWebBackground(c);styleReadability(c);return c}')
page=page.replace("if(s)addWebBackground(s)","if(s){addWebBackground(s);styleReadability(s)}")
page=page.replace(".er.entityBox{fill:#B11313;stroke:#E23636;stroke-width:2.5px}.er.attributeBoxEven{fill:#0F172A;stroke:#1D4ED8}.er.attributeBoxOdd{fill:#162238;stroke:#1D4ED8}.er.relationshipLine{stroke:#CBD5E1;stroke-width:1.6px}.er.relationshipLabel{fill:#fff;font-weight:bold}.er text{fill:#F8FAFC;font-weight:600}", ".er.entityBox{fill:#B91C1C;stroke:#EF4444;stroke-width:2.5px}.er.attributeBoxOdd,.er.attributeBoxOdd rect{fill:#0F172A;stroke:#1D4ED8}.er.attributeBoxEven,.er.attributeBoxEven rect{fill:#172544;stroke:#1D4ED8}.er.relationshipLine{stroke:#94A3B8;stroke-width:1.6px}.er.relationshipLabelBox{fill:#0B1120}.er.relationshipLabel{fill:#F8FAFC;font-weight:bold}.er text{fill:#F8FAFC;font-weight:600}.recordRow,.recordRow rect{fill:#FACC15;stroke:#FACC15}.recordRow text{fill:#0B1120;font-weight:900}")
for old,new in {'#B11313':'#CC0000','#B91C1C':'#CC0000','#E23636':'#FF0000','#EF4444':'#FF0000','#080C14':'#000000','#101827':'#000000','#17263d':'#0D0D0D','#0F2557':'#0D0D0D','#F8FAFC':'#FFFFFF','#eef4ff':'#FFFFFF','#CBD5E1':'#79ADFF','#94A3B8':'#79ADFF','#0F172A':'#000000','#172544':'#121212','#162238':'#121212','#0B1120':'#000000','#1D4ED8':'#79ADFF','#7fa8ff':'#79ADFF','#9fb4d0':'#FFFFFF','#FACC15':'#79ADFF','#e23636':'#FF0000','#1d4ed8':'#79ADFF'}.items(): page=page.replace(old,new)
page=page.replace('<button onclick="zoom(1.2)">＋ Zoom</button><button onclick="zoom(.83)">− Zoom</button><button onclick="resetView()">Ajustar</button>','')
page=page.replace('<span class="hint">Rueda: zoom · arrastrar: paneo</span>','')
page=page.replace('<h1>Spider-Man · DER db_test_7b · 25 tablas / 34 FK</h1>','<h1>Miles Morales · DER db_test_7b · 25 tablas / 34 FK</h1>')
page=page.replace('</style>', '''
body{background:#000000;color:#FFFFFF}header{background:linear-gradient(105deg,#CC0000,#0D0D0D 76%);border-bottom:2px solid #FF0000}button{background:#0D0D0D;border-color:#79ADFF;color:#FFFFFF}button:hover{background:#CC0000;border-color:#FF0000}.record-badge{background:#000000;color:#79ADFF!important;border-color:#79ADFF;box-shadow:0 0 18px #79ADFF55}#view{background-color:#000000;background-image:radial-gradient(ellipse at 50% 50%,#79ADFF18,transparent 65%)}.er.entityBox{fill:#CC0000!important;stroke:#FF0000!important}.er.attributeBoxOdd,.er.attributeBoxOdd rect{fill:#000000!important;stroke:#CC0000!important}.er.attributeBoxEven,.er.attributeBoxEven rect{fill:#121212!important;stroke:#CC0000!important}.er text{fill:#FFFFFF!important}.recordRow text{fill:#79ADFF!important;font-weight:900!important}.er.relationshipLine{stroke:#79ADFF!important}.er.relationshipLabelBox{fill:#000000!important;stroke:#79ADFF!important}
</style>''')
P('diagrama_er.html').write_text(page,encoding='utf-8')
print(json.dumps({'counts':counts,'rowCounts':dict(row_counts),'tableModules':{m:len(v) for m,v in modules.items()},'viewNames':list(views),'fkCount':len(fks),'triggerCount':len(trigs),'tableColumns':sum(len(t['cols']) for t in tables.values())},ensure_ascii=False,indent=2))


