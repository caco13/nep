#!/bin/bash

echo "Cleaning db..."
rm db.sqlite3

echo "Migrating db..."
python manage.py migrate

echo "Create test users..."
python manage.py shell < create_users.py

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

read -n1 -r -p "Press Enter to POST new studie..." key
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
    http -a lab1:nep-lab1 POST http://127.0.0.1:8000/api/studies/2/experiments/ title='First experiment' description='First experiment description' nes_id=1
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
