#echo " BUILD START"
#python3.9 -m pip install -r requirements.txt
#python3.9 manage.py collectstatic --noinput --clear
#echo " BUILD END"

# build_files.sh
pip install -r requirements.txt
python3.9 manage.py collectstatic

echo "Make Migrations"
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "Collect Static"
python3.9 manage.py collectstatic --noinput --clear

