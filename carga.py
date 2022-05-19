from configparser import RawConfigParser
from datetime import datetime
from pymongo import MongoClient
import sys

config = RawConfigParser()
config.read('config.ini')

db_config = config['database']
host = db_config.get('host')
port = db_config.getint('port')
user = db_config.get('user')
password = db_config.get('password')
database = db_config.get('database')

def mdb_client(database=database, user=user, password=password, host=host, port=port):
    # Genera la ruta de conexión
    uri = 'mongodb://'+user+':'+password+'@'+host+':'+str(port)+'/'+database+'?authSource=admin'
    print('Request:', uri)
    # Genera la conexión
    try:
        client = MongoClient(uri)
        # Especifica la database
        database = client[database]
        return database
    except:
        print('No se pudo conectar a la base de datos')

def get_convos(datestart,dateend,db):
    conversaciones = db["conversaciones_log"]
    registros = conversaciones.find({"datatime":{"$gte":datestart,"$lte":dateend}},{"datos_contacto":1,"_id":1})
    registros = [r for r in registros]

    return registros

def get_intencion(registro_id,db):
    interacciones = db["interacciones_log"]

    intenciones = interacciones.find({"id_conversacion":str(registro_id)},{"intencion":1})
    intenciones = [i['intencion'] for i in intenciones]

    return intenciones

def writefile(contacts,fileout):
    #print(contacts)
    with open(fileout,'w') as f:
        f.write("Nombre;Telefono;Mail;Cargo;Jornada;Turno;Renta;Fecha_Entrevista;Horario_Entrevista;Link_Zoom\n")
        for c in contacts:
            f.write(f"{c.get('Nombre','')};{c.get('Telefono','')};{c.get('Mail','')};{c.get('Cargo')};{c.get('Jornada')};{c.get('Turno')};{c.get('Renta')};{c.get('Fecha_Entrevista')};{c.get('Horario_Entrevista')};{c.get('Link_Zoom')}\n")

if __name__ == "__main__":
    datestart = sys.argv[1]
    dateend = sys.argv[2]
    fout = sys.argv[3]

    datestart = datetime.strptime(datestart,"%Y-%d-%m-%H-%M-%S")
    dateend = datetime.strptime(dateend,"%Y-%d-%m-%H-%M-%S")

    db = mdb_client()

    registros = get_convos(datestart,dateend,db)

    yes_contacts = []

    for registro in registros:
        regid = registro["_id"]
        intenciones = get_intencion(regid,db)

        if "INTERESA" in intenciones:
            datos_contacto = registro['datos_contacto']
            yes_contacts.append(datos_contacto)
    writefile(yes_contacts,fout)