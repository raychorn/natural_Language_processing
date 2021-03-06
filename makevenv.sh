#!/bin/bash

VENV=.venv
REQS=./requirements.txt

ARRAY=()

# \/usr\/bin\/python(?P<version>[0-9]\.[0-9])$

PYTHONS=$(whereis python)
for val in $PYTHONS; do
    if [[ $val == *"/usr/bin/"* ]]; then
        if [[ $val != *"-config"* ]]; then
            ARRAY+=($val)
        fi
    fi
done

PS3="Choose: "

select option in "${ARRAY[@]}";
do
    echo "Selected number: $REPLY"
    choice=${ARRAY[$REPLY-1]}
    break
done

version=$($choice --version)
echo "Use this -> $choice --> $version"

v=$($choice -c 'import sys; i=sys.version_info; print("{}{}{}".format(i.major,i.minor,i.micro))')
echo "Use this -> $choice --> $v"

VENV=$VENV$v
echo "VENV -> $VENV"

if [[ -d $VENV ]]
then
    rm -R -f $VENV
fi

if [[ ! -d $VENV ]]
then
    virtualenv --python $choice -v $VENV
fi

if [[ -d $VENV ]]
then
    . ./$VENV/bin/activate
    pip install --upgrade pip

    if [[ -f $REQS ]]
    then
        pip install -r $REQS
    fi

fi