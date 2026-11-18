# Load the GregoBase MySQL dump into SQLite (gb.sqlite).
import re, sqlite3, sys
src=open('/home/claude/dl/gregobase/gregobase_online.sql',encoding='utf8').read()
db=sqlite3.connect('gb.sqlite')
def rows(vals):
    i=0;n=len(vals);out=[]
    while i<n:
        if vals[i]!='(': i+=1; continue
        i+=1; row=[]
        while True:
            while vals[i] in ' \n': i+=1
            if vals[i]=="'":
                i+=1; buf=[]
                while True:
                    c=vals[i]
                    if c=='\\': buf.append({'n':'\n','r':'\r','t':'\t','0':'\0'}.get(vals[i+1],vals[i+1])); i+=2; continue
                    if c=="'":
                        if vals[i+1]=="'": buf.append("'"); i+=2; continue
                        i+=1; break
                    buf.append(c); i+=1
                row.append(''.join(buf))
            else:
                j=i
                while vals[j] not in ',)': j+=1
                t=vals[i:j].strip(); row.append(None if t=='NULL' else (float(t) if '.' in t else int(t))); i=j
            while vals[i] in ' \n': i+=1
            if vals[i]==',': i+=1; continue
            if vals[i]==')': i+=1; break
        out.append(row)
    return out
made=set()
for m in re.finditer(r"INSERT INTO `(\w+)` \(([^)]*)\) VALUES\n(.*?);\n(?=\n|INSERT|--|/\*|ALTER|$)", src, re.S):
    t,cols,vals=m.group(1),[c.strip('` ') for c in m.group(2).split(',')],m.group(3)
    if t not in made:
        db.execute(f'drop table if exists {t}'); db.execute(f'create table {t} ({",".join(chr(34)+c+chr(34) for c in cols)})'); made.add(t)
    R=rows(vals)
    db.executemany(f'insert into {t} values ({",".join("?"*len(cols))})', R)
db.commit()
for t in made: print(t, db.execute(f'select count(*) from {t}').fetchone())
