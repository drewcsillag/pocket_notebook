python notepaper.py 2025-01-01 8
for i in *.svg
do
  diff -u $i exemplar/$i 

done
