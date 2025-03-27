echo "Inicializando db"
flask db init

echo "Genero migración"
flask db migrate -m "Inicializacion db"

echo "Aplicando migraciones..."
flask db upgrade

echo "Arranco proyecto"
python run.py