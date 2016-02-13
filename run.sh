#!/bin/bash
mv ~/Descargas/LFS201*.html html/ori 2> /dev/null
rm html/clean/* 2> /dev/null
rm md/* 2> /dev/null
cp html/ori/* html/clean/
python clean.py
for f in html/clean/*.html; do
	#cat "$f" | tr -dc '[[:print:]]áéíóúñäëïöüÁÉÍÓÚÑÄËÏÖÜ\n' > aux
	#mv aux "$f"
	MD=`basename "$f" | sed 's/html$/md/'`
	echo "Generando $MD"
	MD="md/$MD"
	pandoc --ascii -o "$MD" "$f"
	if [[ "$f" != *_popup*.html ]]; then
		tail -n +382 "$MD" | head -n -3 > aux
		mv aux "$MD"
	fi
	cat "$MD"| tr -dc '[[:print:]]áéíóúñäëïöüÁÉÍÓÚÑÄËÏÖÜ\n' | awk -f clean.awk > aux
	mv aux "$MD"
	sed '/\!\[\].images\/defaultProgBarH.gif/d' -i "$MD"
done
