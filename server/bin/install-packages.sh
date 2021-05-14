deactivate || true
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
pwd
ls -l
