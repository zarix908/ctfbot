pybabel extract --mapping babel.cfg -o locales/base.pot .
pybabel update -i locales/base.pot -d locales
