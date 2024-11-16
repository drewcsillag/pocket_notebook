set -e
python notepaper.py $1 $2
for i in *.svg
do
    rootname=$(echo $i | sed 's/\.svg//')
    /Applications/Inkscape.app/Contents/MacOS/inkscape --export-filename=${rootname}.pdf ${rootname}.svg
done
# pdfunite weekp{1,2,3,4,5,6,7,8}.pdf monthly{1,2}.pdf blank{1,2}.pdf orgpages.pdf
pdfunite daily*.pdf monthly{1,2}.pdf blank{1,2}.pdf orgpages.pdf
