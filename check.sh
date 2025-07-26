bash clean.sh
#source bin/activate
uv run black notepaper*.py svg_gen.py constants.py utils.py
uv run ruff check notepaper*.py svg_gen.py constants.py utils.py
uv run python -m unittest notepaper_test
uv run python -m unittest yaml_load_test
uv run notepaper.py 2025-01-01 8 todos.yaml holidays.yaml
for i in *.svg
do
  diff -u $i exemplar/$i

done
uv run pylint *.py
bash clean.sh
