black notepaper*.py
ruff check notepaper*.py
python -m unittest notepaper_test
python notepaper.py 2025-01-01 8
for i in *.svg
do
  diff -u $i exemplar/$i

done
