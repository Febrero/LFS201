# -*- coding: utf-8 -*-

import os.path
import glob
import re
import bs4

tag_compat=['p','li', 'legend', 'td', 'th']

tt=re.compile(".*?LFS201_\d+.\d+_([^/]+?)(_popup \(\d+\))?.md$")
cp=re.compile(".*?LFS201_(\d+)\..*$")
pr=re.compile("(.*)¿(.*?)-(.*)")
bk=re.compile("<(fieldset|head|body|meta|link|script|p|ul|ol|li|div)>")
ck=re.compile("(Haga|Haz) click (en|sobre) (el|los|en)", re.UNICODE|re.MULTILINE|re.DOTALL)
fg=re.compile(".*?(Figura|Figure)\s+\d+\.\d+(:|.)", re.UNICODE|re.MULTILINE|re.DOTALL)
lab=re.compile(".*\s+para\s+descargar\s+el\s+Laboratorio\s+(\d+\.\d+).*", re.UNICODE|re.MULTILINE|re.DOTALL)
sp=re.compile("\s+", re.UNICODE)

hts=sorted(glob.glob('html/clean/*.html'))

caB=0
n=0
f=0

tpt="out/_LFS201.html"
oht="out/LFS201.html"
html4="out/LFS201_4.html"

def get_soup(html):
	html = open(html,"r+")
	soup = bs4.BeautifulSoup(html,'html.parser')#"lxml")
	html.close()
	return soup

def find_text(soup,r):
	rt=[]
	ps=soup.findAll('p')
	for p in ps:
		if r.match(p.get_text()):
			rt.append(p)
	return rt

def set_anchor(i,ca,f=None):
	a=soup.new_tag("a", **{"href": "#"+i.attrs['id'], "title":u"Cápitulo "+str(ca)})
	if f:
		a.attrs['title']=a.attrs['title']+", ficha "+str(f)
	if i.name=="fieldset":
		i=i.legend
	a.string=i.string
	i.string=""
	i.append(a)

soup = get_soup(tpt)
soup.body.clear()
div=soup.new_tag("div", **{"class":"content"})
soup.body.append(div)

fldB=None
divCp=None

for ht in hts:
	soup2 = get_soup(ht)
	t=soup2.title
	b=soup2.body

	if "_popup" in ht:
		n=3
	else:
		ca=int(cp.sub("\\1",ht))
		if ca>caB:
			n=1
			f=1
			caB=ca
		else:
			n=2
			f=f+1

	if n==1:
		h=b.p.extract()#.strong
		h.name="h1"
		h.string=sp.sub(" ",h.get_text()).strip('.')[9:].strip()
		h.attrs['id']="c"+str(ca)
		set_anchor(h,ca)
		divCp=soup.new_tag("div", **{"id":"cp"+str(ca)})
		soup.body.div.append(divCp)
		#soup.body.div
		divCp.append(h)
		n=2

	fld = soup.new_tag("fieldset")
	fld.attrs['class']="n"+str(n)
	t.name="legend"
	fld.append(t)
	b.name="div"
	fld.attrs['id']="c"+str(ca)+"f"+str(f)
	fld.append(b)

	ps=fld.div.select(" > *")
	if len(ps)>0 and ps[0].name=="p" and ps[0].get_text().lower() == fld.legend.get_text().lower():
		ps[0].extract()

	if n==3:
		cs=[]
		if fg.match(fld.legend.string):
			cs=find_text(fldB,fg)
		else:
			cs=find_text(fldB,ck)
		if len(cs)>0:
			c=cs[0]
			c.replace_with(fld)
		else:
			fldB.append(fld)
	else:
		set_anchor(fld,ca,f)
		#soup.body.div
		divCp.append(fld)
		fldB=fld

flds=soup.findAll("fieldset", attrs={'class': re.compile(r".*\bn3\b.*")})
for fld in flds:
	if len(fld.parent.select(" > *"))==1:
		fld.parent.replace_with(fld.div)

labs=find_text(soup,lab)
for f in labs:
	l=lab.sub("\\1",f.get_text())
	n=f.select(" > *")[0]
	a=soup.new_tag("a", href="https://lms.360training.com/custom/12396/808239/LAB_"+l+".pdf")
	a.append(n)
	f.append(a)

for d in soup.body.div.select(" > div"):
	a=d.h1.a
	a.attrs['title']=a.attrs['title']+" de "+str(ca)
	mrks=d.select(" > fieldset > legend > a")
	z=str(len(mrks))
	for m in mrks:
		m.attrs['title']=m.attrs['title']+" de "+z

h=unicode(soup)#HTMLBeautifier.beautify(unicode(soup), 4) soup.prettify()
h=bk.sub("\\n<\\1>",h)
# Erratas
h=h.replace("Objectivos de aprendizaje","Objetivos de aprendizaje") #7 11
h=h.replace(">31.</a></h1>",">31. zypper</a></h1>") #31
with open(oht, "wb") as file:
	file.write(h.encode('utf8'))

