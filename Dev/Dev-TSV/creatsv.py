import csv

with open('hymnes2.tsv', 'w') as csv_file:
	colnames = ['ID','collection', 'collection_parent','Titre', 'Auteur','Interprete', 'Date', 'Content', 'Link']
	writer = csv.DictWriter(csv_file, fieldnames=colnames, delimiter='\t')

	with open('LeTempsdesCerises.txt','r') as txt_file:
		texte = txt_file.read()

	writer.writeheader()

	writer.writerow({ 'ID' : '1',
	 'collection': '/Commune',
	 'collection_parent' : '/collection_intiale',	
	 'Titre' : 'Le Temps des Cerises',
	 'Auteur' : 'Jean-Baptiste Clément',
	 'Interprete' :'Antoine  Renard et alii',
	 'Date' : '1868',
	 'Content' : texte,
	 'Link' : 'https://fr.wikipedia.org/wiki/Le_Temps_des_cerises_(chanson)'})

	with open('Carmagnole.txt','r') as txt_file:
		texte_C = txt_file.read()
	writer.writerow({'ID' : '2',
	 'collection' : '/revolution1789',
	 'collection_parent' : '/collection_intiale',
	 'Titre' : 'Carmagnole',
	 'Auteur' : 'anonyme',
	 'Interprete' : 'anonyme',
	 'Date' : '1792',
	 'Content' : texte_C,
	 'Link' : 'https://fr.wikipedia.org/wiki/La_Carmagnole'})

	with open('Marseillaise.txt','r') as txt_file:
		texte_M = txt_file.read()
	writer.writerow({ 'ID' : '3',
	 'collection' : '/revolution1789',
	 'collection_parent' : '/collection_intiale',
	 'Titre' : 'Marseillaise',
	 'Auteur' : 'Rouget de l\'Isle',
	 'Interprete' : 'Rouget de l\'Isle',
	 'Date' : '1792',
	 'Content' : texte_M,
	 'Link' : 'https://fr.wikipedia.org/wiki/La_Marseillaise'})
	
	with open('Internationale.txt','r') as txt_file:
		texte_I = txt_file.read()
	writer.writerow({ 'ID' : '4',
	 'collection' : '/Commune',
	 'collection_parent' : '/collection_intiale',
	 'Titre' : 'Internationale',
	 'Auteur' : 'Eugnène Pottier',
	 'Interprete' : 'Gustave Nadaud',
	 'Date' : '1871',
	 'Content' : texte_I,
	 'Link' : 'https://fr.wikipedia.org/wiki/L%27Internationale'})

	with open('Triomphe_Anarchie.txt','r') as txt_file:
		texte_TA = txt_file.read()
	writer.writerow({ 'ID' : '5',
	 'collection' : '/chant_contre',
	 'collection_parent' : '/collection_intiale',
	 'Titre' : 'Le Triomphe de l\'Anarchie',
	 'Auteur' : 'Charles d\'Avray',
	 'Interprete' : 'Charles d\'Avray',
	 'Date' : '1901',
	 'Content' : texte_TA,
	 'Link' : 'https://fr.wikipedia.org/wiki/Le_Triomphe_de_l%27anarchie'})
