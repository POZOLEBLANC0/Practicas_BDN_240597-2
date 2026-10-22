import re,json,pathlib
p=pathlib.Path('db_test_7b_1510.sql')
s=p.read_text(encoding='utf-8',errors='replace')
# Find CREATE TABLE statements, then split their body on commas outside quotes/parentheses.
def split_top(body):
    out=[]; start=0; depth=0; quote=None; i=0
    while i<len(body):
        c=body[i]
        if quote:
            if c=='\\': i+=2; continue
            if c==quote:
                if i+1<len(body) and body[i+1]==quote: i+=2; continue
                quote=None
        elif c in "'\"`": quote=c
        elif c=='(': depth+=1
        elif c==')': depth-=1
        elif c==',' and depth==0: out.append(body[start:i].strip()); start=i+1
        i+=1
    out.append(body[start:].strip()); return out

def tuples_count(txt):
    # Count top-level VALUES tuples, respecting SQL quoted strings and escaped chars.
    m=re.search(r'\bVALUES\s*',txt,re.I)
    if not m:return 0
    i=m.end(); depth=0; quote=None; count=0; in_tuple=False
    while i<len(txt):
        c=txt[i]
        if quote:
            if c=='\\': i+=2; continue
            if c==quote:
                if i+1<len(txt) and txt[i+1]==quote: i+=2; continue
                quote=None
        else:
            if c in "'\"": quote=c
            elif c=='(':
                if depth==0: count+=1; in_tuple=True
                depth+=1
            elif c==')':
                depth-=1
                if depth==0: in_tuple=False
            elif c==';' and depth==0: break
        i+=1
    return count

# Get individual table definitions with balanced parentheses.
tables={}
for m in re.finditer(r'CREATE\s+TABLE\s+`([^`]+)`\s*\(',s,re.I):
    name=m.group(1); start=m.end(); depth=1; quote=None; i=start
    while i<len(s) and depth:
        c=s[i]
        if quote:
            if c=='\\': i+=2; continue
            if c==quote:
                if i+1<len(s) and s[i+1]==quote: i+=2; continue
                quote=None
        elif c in "'\"`": quote=c
        elif c=='(': depth+=1
        elif c==')': depth-=1
        i+=1
    body=s[start:i-1]
    lines=split_top(body); cols=[]; indexes=[]; fks=[]; pk=[]; unique=[]
    for line in lines:
        cm=re.match(r'`([^`]+)`\s+(.+)$',line,re.S)
        if cm:
            col,decl=cm.groups(); typ=re.match(r'(?is)^(.+?)(?=\s+(?:NOT\s+NULL|NULL\b|DEFAULT\b|AUTO_INCREMENT\b|ON\s+UPDATE\b|COMMENT\b|GENERATED\b)|$)',decl.strip())
            datatype=typ.group(1).strip() if typ else decl.strip()
            flags=[]
            if re.search(r'\bNOT\s+NULL\b',decl,re.I): flags.append('NOT NULL')
            elif re.search(r'\bNULL\b',decl,re.I): flags.append('NULL')
            if re.search(r'\bAUTO_INCREMENT\b',decl,re.I): flags.append('AUTO_INCREMENT')
            dm=re.search(r'\bDEFAULT\s+(.+?)(?=\s+ON\s+UPDATE\b|\s+COMMENT\b|$)',decl,re.I)
            if dm: flags.append('DEFAULT '+dm.group(1).strip())
            um=re.search(r'\bON\s+UPDATE\s+(.+?)(?=\s+COMMENT\b|$)',decl,re.I)
            if um: flags.append('ON UPDATE '+um.group(1).strip())
            cols.append({'name':col,'type':datatype,'decl':decl.strip(),'flags':flags,'key':[]})
            continue
        pm=re.match(r'PRIMARY KEY\s*\(([^)]+)\)',line,re.I)
        if pm: pk=[x.strip().strip('`') for x in pm.group(1).split(',')]; continue
        um=re.match(r'(?:UNIQUE\s+(?:KEY|INDEX))\s+`([^`]+)`\s*\(([^)]+)\)',line,re.I)
        if um:
            names=[x.strip().split('(')[0].strip('`') for x in um.group(2).split(',')]; unique.append({'name':um.group(1),'columns':names}); indexes.append({'name':um.group(1),'kind':'UNIQUE','columns':names}); continue
        km=re.match(r'(?:KEY|INDEX)\s+`([^`]+)`\s*\(([^)]+)\)',line,re.I)
        if km:
            names=[x.strip().split('(')[0].strip('`') for x in km.group(2).split(',')]; indexes.append({'name':km.group(1),'kind':'INDEX','columns':names}); continue
        fm=re.match(r'CONSTRAINT\s+`([^`]+)`\s+FOREIGN KEY\s*\(([^)]+)\)\s+REFERENCES\s+`([^`]+)`\s*\(([^)]+)\)(.*)',line,re.I|re.S)
        if fm:
            fn,fc,rt,rc,tail=fm.groups(); fk={'name':fn,'columns':[x.strip().strip('`') for x in fc.split(',')],'table':rt,'references':[x.strip().strip('`') for x in rc.split(',')],'on_delete':None,'on_update':None}
            for action in ('delete','update'):
                am=re.search(r'ON\s+'+action.upper()+r'\s+(RESTRICT|CASCADE|SET NULL|NO ACTION|SET DEFAULT)',tail,re.I)
                if am: fk['on_'+action]=am.group(1).upper()
            fks.append(fk)
    idx=[]
    for x in cols:
        if x['name'] in pk:x['key'].append('pk')
        if any(x['name'] in u['columns'] for u in unique):x['key'].append('uk')
        if any(x['name'] in fk['columns'] for fk in fks):x['key'].append('fk')
    tables[name]={'cols':cols,'pk':pk,'unique':unique,'indexes':indexes,'fks':fks}

# Associate tuple counts with each table across all INSERT statements.
counts={n:0 for n in tables}
for m in re.finditer(r'INSERT\s+INTO\s+`?([\w]+)`?',s,re.I):
    name=m.group(1)
    if name not in counts: continue
    end=s.find(';',m.end())
    # INSERT clauses in this dump have no semicolons in quoted payload values except SQL escapes.
    # Use quote-aware scan to locate statement end.
    i=m.end(); quote=None
    while i<len(s):
        c=s[i]
        if quote:
            if c=='\\': i+=2; continue
            if c==quote:
                if i+1<len(s) and s[i+1]==quote:i+=2;continue
                quote=None
        elif c in "'\"":quote=c
        elif c==';':break
        i+=1
    counts[name]+=tuples_count(s[m.start():i+1])

triggers={n:[] for n in tables}
for m in re.finditer(r'TRIGGER\s+`([^`]+)`\s+(BEFORE|AFTER)\s+(INSERT|UPDATE|DELETE)\s+ON\s+`([^`]+)`',s,re.I):
    t,timing,event,table=m.groups()
    if table in triggers: triggers[table].append(f'{t} · {timing} {event}')

# Functional domains use rectangular column bands.
domains={'tb_users':'Identidad','tb_carts':'Identidad','tb_products':'Catálogo','tbc_categories':'Catálogo','tb_logs':'Auditoría','tbd_products_categorias':'Relaciones','tbd_products_users_providers':'Relaciones','tbd_users_wishlist_products':'Relaciones'}
positions={'tb_users':(0,0),'tb_carts':(1,0),'tb_products':(0,1),'tbc_categories':(1,1),'tb_logs':(0,2),'tbd_products_categorias':(0,3),'tbd_products_users_providers':(1,3),'tbd_users_wishlist_products':(2,3)}
entities=[]; relationships=[]
for name,data in tables.items():
    row,col=positions[name]
    attrs=[]
    for a in data['cols']:
        typ=a['type']+(' · '+' · '.join(a['flags']) if a['flags'] else '')
        item={'name':a['name'],'type':typ}
        if a['key']: item['key']=a['key'] if len(a['key'])>1 else a['key'][0]
        fk=next((f for f in data['fks'] if a['name'] in f['columns']),None)
        if fk: item['references']=fk['table']+'.'+fk['references'][fk['columns'].index(a['name'])]
        attrs.append(item)
    entities.append({'id':name,'label':name,'sublabel':f"{counts[name]:,} registros · {len(attrs)} columnas",'tag':domains[name],'row':row,'col':col,'attributes':attrs})
    for fk in data['fks']:
        parent=fk['table']; child=name
        nullable=any('NOT NULL' not in next(a['decl'] for a in data['cols'] if a['name']==c).upper() for c in fk['columns'])
        action=f"DELETE {fk['on_delete'] or 'NO ESPECIFICADO'} · UPDATE {fk['on_update'] or 'NO ESPECIFICADO'}"
        relationships.append({'id':fk['name'],'from':child,'to':parent,'label':f"{fk['name']} · {action}",'fromCardinality':'many','toCardinality':'one','fromOptional':nullable,'toOptional':True,'identifying':all(c in data['pk'] for c in fk['columns'])})

cards=[]
for name,data in tables.items():
    items=[]
    items += [f"PK: {', '.join(data['pk'])}" ] if data['pk'] else []
    items += [f"{x['kind']} {x['name']}: {', '.join(x['columns'])}" for x in data['indexes']]
    items += ['Trigger: '+x for x in triggers[name]]
    if not items: items=['Sin índices secundarios ni triggers definidos en el dump.']
    cards.append({'dot':'cyan','title':f'{name} · índices y triggers','items':items})

candidate={'schema_version':1,'diagram_type':'erd','meta':{'title':'Modelo EER · db_test_7b','locale':'es','output':'.archify/erd-db-test-7b-1510-20261022-120000/db-test-7b-1510.html','quality_profile':'standard','subtitle':f"{len(tables)} tablas · {sum(counts.values()):,} filas declaradas en INSERT · MySQL 8.0.36",'legend':{'mode':'all','entries':{'pk':{'label':'Clave primaria'},'fk':{'label':'Clave foránea'},'uk':{'label':'Única'}}}},'layout':{'mode':'grid','gapX':60,'gapY':34},'entities':entities,'relationships':relationships,'cards':cards}
out=pathlib.Path('.archify/erd-db-test-7b-1510-20261022-120000/candidate.json'); out.write_text(json.dumps(candidate,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'tables':{n:counts[n] for n in tables},'total_rows':sum(counts.values()),'fk':len(relationships),'triggers':sum(map(len,triggers.values())),'candidate':str(out)},ensure_ascii=False))
