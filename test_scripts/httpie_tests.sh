 #!/bin/bash

echo "Cleaning db..."
rm db.sqlite3

echo "Migrating..."
python manage.py migrate

echo "Creating test users..."
python manage.py shell < ./test_scripts/create_users.py

echo "Creating experiment status..."
python manage.py shell < ./test_scripts/create_status.py

read -n1 -r -p "Press Enter to GET researchers..." key
if [ "$key" = '' ]; then
    echo "GETing researchers..."
    http http://127.0.0.1:8000/api/researchers/
    # echo [$key] is empty when SPACE is pressed # uncomment to trace
fi

read -n1 -r -p "Press Enter to POST new researchers..." key
if [ "$key" = '' ]; then
    echo 'POSTing new researcher...'
    http -a lab1:nep-lab1 POST http://127.0.0.1:8000/api/researchers/ first_name='John' surname='Evans' nes_id=1
fi

read -n1 -r -p "Press Enter to GET studies..." key
if [ "$key" = '' ]; then
    echo "GETing studies..."
    http http://127.0.0.1:8000/api/studies/
fi

read -n1 -r -p "Press Enter to POST new study..." key
if [ "$key" = '' ]; then
    echo "POSTing new study..."
    http -a lab1:nep-lab1 POST http://127.0.0.1:8000/api/researchers/1/studies/ title='First study' description='First study description' start_date='2017-02-02' nes_id=2
fi

read -n1 -r -p "Press Enter to GET experiments..." key
if [ "$key" = '' ]; then
    echo "GETing experiments..."
    http http://127.0.0.1:8000/api/experiments/
fi

read -n1 -r -p "Press Enter to POST new experiment..." key
if [ "$key" = '' ]; then
    echo "POSTing new experiment..."
    http -a lab1:nep-lab1 -f POST http://127.0.0.1:8000/api/studies/2/experiments/ title='First experiment' description='First experiment description' data_acquisition_done='True' nes_id=1 ethics_committee_project_file@~/Downloads/autores.png
fi

read -n1 -r -p "Press Enter to GET protocol_components..." key
if [ "$key" = '' ]; then
    echo "GETing protocol components..."
    http http://127.0.0.1:8000/api/protocol_components/
fi

read -n1 -r -p "Press Enter to POST protocol_components..." key
if [ "$key" = '' ]; then
    echo "POSTing new protocol component..."
    http -a lab1:nep-lab1 POST http://127.0.0.1:8000/api/experiments/1/protocol_components/ identification='First identification' description='First prococol component description' component_type='First component type' duration_unit='hora' duration_value=2 nes_id=1
fi

read -n1 -r -p "Press Enter to GET groups..." key
if [ "$key" = '' ]; then
    echo "GETing groups..."
    http http://127.0.0.1:8000/api/groups/
fi

read -n1 -r -p "Press Enter to POST groups..." key
if [ "$key" = '' ]; then
    echo "POSTing new group..."
    http -a lab1:nep-lab1 POST http://127.0.0.1:8000/api/experiments/1/protocol_components/1/groups/ title='First group' description='First group description' nes_id=1
fi

read -n1 -r -p "Press Enter to GET participants..." key
if [ "$key" = '' ]; then
    echo "GETing participants..."
    http http://127.0.0.1:8000/api/participants/
fi

read -n1 -r -p "Press Enter to POST participants..." key
if [ "$key" = '' ]; then
    echo "POSTing new participant..."
    http -a lab1:nep-lab1 POST http://127.0.0.1:8000/api/groups/1/participants/ date_birth='2000-01-01' district='Rio Pequeno' city='São Paulo' state='SP' country='Brasil' gender='M' marital_status='Solteiro' nes_id=1
fi
