RUN AS:
python3 carga.py YYYY-MM-DD-HH-MM-SS YYYY-MM-DD-HH-MM-SS outfile.csv

donde la primera fecha es la fecha de inicio y la segunda de termino para los registros.

Necesita un config.ini así:

[database]
host = mongo ip
port = mongo puerto
user = admin
password = password
database = client db
