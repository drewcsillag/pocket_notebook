bash clean.sh
source bin/activate
black notepaper*.py svg_gen.py constants.py utils.py
ruff check notepaper*.py svg_gen.py constants.py utils.py
python -m unittest notepaper_test
python notepaper.py 2025-01-01 8 todos.yaml holidays.yaml
for i in *.svg
do
  diff -u $i exemplar/$i

done
pylint *.py
bash clean.sh
