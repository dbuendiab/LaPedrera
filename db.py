import sys
import pymongo

cli = pymongo.MongoClient()
db = cli.pedrera
c_es = db.espais_simples
c_ec = db.espais_complexos

def get_es(filtro={}):
    es = []
    for e in c_es.find(filtro):
        es.append(e)
    return es
    
def get_ec(filtro={}):
    ec = []
    for e in c_ec.find():
        espais = e['espais']
        filtro2 = {'id': {'$in': espais}}
        espais_ext = []
        for ex in c_es.find(filtro2):
            espai_ext_dict = {'_id': ex['_id'], 'id': ex['id'], 'nom': ex['nom']}
            espais_ext.append(espai_ext_dict)
        e['espais'] = espais_ext
        ec.append(e)
    return ec
    