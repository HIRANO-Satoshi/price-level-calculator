echo installing pypyenv with pypy3

deactivate 2>/dev/null || true
if [ "`which pypy3`" == "" ]; then
    brew install pypy3
fi
if [ "`which virtualenv`" == "" ]; then
    pip install virtualenv
fi

if [ ! -e pypyenv ]; then
   virtualenv --python pypy3 pypyenv
fi

. pypyenv/bin/activate
pip install -r requirements-pypy.txt


echo installing pyenv with Python 3.9

deactivate 2>/dev/null || true
if [ "`which python3`" == "" ]; then
    brew install python3
fi
if [ ! -e pyenv ]; then
   virtualenv --python python3 pyenv
fi

. pyenv/bin/activate
pip install -r requirements.txt
