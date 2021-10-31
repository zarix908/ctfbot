mkdir locales 2>/dev/null

# extract translatable strings from sources
pybabel extract --mapping babel.cfg -o locales/base.pot .

# create translations for every language
# Russian Federation
pybabel init -l ru_RU -i locales/base.pot -d locales
