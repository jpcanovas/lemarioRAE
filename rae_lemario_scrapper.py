import requests
from lxml import html
import json
import time

url = 'https://dle.rae.es/data/search'
reqData={'w' : '', 'm' : '31', 'f' : '1', 't':'200'}
user=''    # Consultar hilo de Jaime Gomez-Obregón en https://twitter.com/JaimeObregon/status/1329780273064669186?s=20
passwd=''  # Consultar hilo de Jaime Gomez-Obregón en https://twitter.com/JaimeObregon/status/1329780273064669186?s=20

abecedario=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z','ü',
            'A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z',' ',
            '-']

def valida_prefix(prefix):
    # No poner más de un espacio seguido
    if (prefix.endswith('  ')):
        return False  
    if (prefix.endswith('--')):
        return False
    if (prefix[0]=='ü' or prefix[0]==' '):
        return False
    # la 'ü' solo detrás de la g
    if (prefix[-1] == 'ü' and prefix[-2] != 'g'):
        return False       
    # detrás de 'q' va una 'u'
    if (prefix[-2] == 'q' and prefix[-1] != 'u'):
        return False
    #en cualquier otro caso, valida el prefijo
    return True
        

def get_lemas(empieza_por,indexabc):
    lemas = set(()) # set
    reqData["w"] = empieza_por
    try:
        r = requests.get(url, auth=(user,passwd), params=reqData)
    except:
        print(f'Exception with {empieza_por}')
        return lemas
    if (r.status_code == 200):
        jList = json.loads(r.text)
        nLemas = len(jList["res"])
        #print (f'Empieza_por: {empieza_por} returned {nLemas} lemas ')
        if (nLemas == 200):
            for i in range(indexabc, len(abecedario), 1):
                if (valida_prefix(empieza_por+abecedario[indexabc])):
                    lemas.update(get_lemas(empieza_por+abecedario[indexabc],0))
                indexabc += 1
        else:
            for lema in jList["res"]:
                #print(lema["header"][:-1], lema["id"])
                lemas.add(lema["header"]);
    if (nLemas > 0 and nLemas < 200):
        print (f'{empieza_por}: {len(jList["res"])}')
    return lemas

start = time.time()
for p in abecedario:
    prefix=p
    lemasSet = get_lemas(prefix,0)        
    print (f'{prefix}: Extraídos {len(lemasSet)} lemas')
    #print (lemasSet)
    f = open("lemas_raw.txt", "a")
    for l in sorted(lemasSet):
        f.write(f'{l}\n')
    f.close()
end = time.time()
print(f'Elapsed time: {end - start}')
