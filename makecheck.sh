python notepaper.py 2025-01-01 8
for i in *.svg
do
  diff $i exemplar/$i
done
