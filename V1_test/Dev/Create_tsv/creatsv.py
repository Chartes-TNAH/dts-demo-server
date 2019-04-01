# nous importons le package csv
import csv

# on ouvre en mode écriture un nv fichier qui est un .tsv et on le stocke dans la variable 'tsv_file'
with open('Chansons.tsv', 'w') as tsv_file:
	# ds une varaible 'colnames' on créé les en-têtes de colonnes du fichier tsv
	colnames = ['ID','collection', 'collection_parent','Titre', 'Auteur','Interprete', 'Date', 'Content', 'Link']
	# utilisation de la méthode DictWriter pour dire que mon fichier tsv a comme nom de colonnes 'colnames'
	# et on définit la tabulation comme étant le délimiteur de notre fichier tsv
	writer = csv.DictWriter(tsv_file, fieldnames=colnames, delimiter='\t')
	# permet dans le fichier d'écrire les noms de colonnes dans le fichier
	writer.writeheader()

# on ouvre un fichier txt en mode lectutre, on le stocke dans la variable 'txt_file'
	with open('..//Collection_initiale/Commune/LeTempsdesCerises.txt','r') as txt_file:
		# dans la variable texte on stocke le résultat du parsage de la méthode .read()
		texte = txt_file.read()
	# on écrit dans notre fichier les métadonnées et le contenu en texte brut
	writer.writerow({ 'ID' : '1',
	 'collection': '/Commune',
	 'collection_parent' : '/Collection_intiale',
	 'Titre' : 'Le Temps des Cerises',
	 'Auteur' : 'Jean-Baptiste Clément',
	 'Interprete' :'Antoine  Renard et alii',
	 'Date' : '1868',
	 'Content' : texte,
	 'Link' : 'https://fr.wikipedia.org/wiki/Le_Temps_des_cerises_(chanson)'})

	with open('..//Collection_initiale/Révolution_1789/Carmagnole.txt','r') as txt_file:
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

	with open('..//Collection_initiale/Révolution_1789/Marseillaise.txt','r') as txt_file:
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
	
	with open('..//Collection_initiale/Commune/Internationale.txt','r') as txt_file:
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

	with open('..//Collection_initiale/Chants_"contre"/Triomphe_Anarchie.txt','r') as txt_file:
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
