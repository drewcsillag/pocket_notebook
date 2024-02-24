python3 notepaper.py
for i in monthly1 monthly2 weekp1 weekp2 weekp3 weekp4
do
    /Applications/Inkscape.app/Contents/MacOS/inkscape --export-filename=$i.pdf $i.svg
done
pdfunite weekp{1,2,3,4}.pdf monthly{1,2}.pdf orgpages.pdf
