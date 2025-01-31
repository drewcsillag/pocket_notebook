set -e
python notepaper.py $1 $2
for i in *.svg
do
    rootname=$(echo $i | sed 's/\.svg//')
    /Applications/Inkscape.app/Contents/MacOS/inkscape --export-filename=${rootname}.pdf ${rootname}.svg
done
pdfunite daily*.pdf monthly{1,2}.pdf monthly_dated{1,2,3,4}.pdf blank{1,2}.pdf header_*pdf orgpages.pdf
