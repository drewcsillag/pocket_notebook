python3 notepaper.py
for i in monthly1 monthly2 weekp{1,2,3,4,5,6,7,8} blank1 blank2
do
    /Applications/Inkscape.app/Contents/MacOS/inkscape --export-filename=$i.pdf $i.svg
done
pdfunite weekp{1,2,3,4,5,6,7,8}.pdf monthly{1,2}.pdf blank{1,2}.pdf orgpages.pdf
