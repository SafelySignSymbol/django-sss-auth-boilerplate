if [ ! -e 'db.sqlite3' ]; then
    # 初回起動
    echo "### initialize start   ####"
    python manage.py makemigrations web3auth
    python manage.py migrate
    echo "### initialize end   ####"
else
    # 2回目以降
    echo "### Already setup ###"
fi
# Djangoの起動
python manage.py runserver 0.0.0.0:8000