if [ -e pypyenv ]; then
   virtualenv --python pypy3 pypyenv
fi

. pypyenv/bin/activate
pip install -r requirements-pypy.txt
pwd
ls -l
