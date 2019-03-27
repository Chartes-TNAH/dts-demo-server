# nous importons le package csv
import csv

# on ouvre en mode écriture un nv fichier qui est un .tsv et on le stocke dans la variable 'tsv_file'
with open('Chansons.tsv', 'w') as tsv_file:
    # ds une varaible 'colnames' on créé les en-têtes de colonnes du fichier tsv
    colnames = ['ID', 'collection', 'collection_parent', 'Titre', 'Auteur', 'Interprete', 'Date', 'Content', 'Link']
    # utilisation de la méthode DictWriter pour dire que mon fichier tsv a comme nom de colonnes 'colnames'
    # et on définit la tabulation comme étant le délimiteur de notre fichier tsv
    writer = csv.DictWriter(tsv_file, fieldnames=colnames, delimiter='\t')
    # permet dans le fichier d'écrire les noms de colonnes dans le fichier
    writer.writeheader()

    # on ouvre un fichier txt en mode lectutre, on le stocke dans la variable 'txt_file'
    with open('../../Collection_initiale/Commune/LeTempsdesCerises.txt', 'a') as txt_file:
    # on écrit dans notre fichier les métadonnées et le chemin du fichier vers le .txt
        writer.writerow({'ID': '1',
                     'collection': '/Commune',
                     'collection_parent': '/Collection_initiale',
                     'Titre': 'Le Temps des Cerises',
                     'Auteur': 'Jean-Baptiste Clément',
                     'Interprete': 'Antoine  Renard et alii',
                     'Date': '1868',
                     'Content': '../../Collection_initiale/Commune/LeTempsdesCerises.txt',
                     'Link': 'https://fr.wikipedia.org/wiki/Le_Temps_des_cerises_(chanson)'})

    # create table -> insert avec les chemins de fichiers xml et txt (à récupérer avec un pgm) @route
    # faire d'abord le txt et le xml -> parser le txt en xml avec une fonction

    with open('../../Collection_initiale/1789_Révolution/Carmagnole.txt', 'r') as txt_file:
        writer.writerow({'ID': '2',
                     'collection': '/1789_Révolution',
                     'collection_parent': '/Collection_initiale',
                     'Titre': 'Carmagnole',
                     'Auteur': 'anonyme',
                     'Interprete': 'anonyme',
                     'Date': '1792',
                     'Content': '../../Collection_initiale/Révolution_1789/Carmagnole.txt',
                     'Link': 'https://fr.wikipedia.org/wiki/La_Carmagnole'})

    with open('../../Collection_initiale/1789_Révolution/Marseillaise.txt', 'a') as txt_file:
        writer.writerow({'ID': '3',
                     'collection': '/1789_Révolution',
                     'collection_parent': '/Collection_initiale',
                     'Titre': 'Marseillaise',
                     'Auteur': 'Rouget de l\'Isle',
                     'Interprete': 'Rouget de l\'Isle',
                     'Date': '1792',
                     'Content': '../../Collection_initiale/1789_Révolution/Marseillaise.txt',
                     'Link': 'https://fr.wikipedia.org/wiki/La_Marseillaise'})

    with open('../../Collection_initiale/Commune/Internationale.txt', 'a') as txt_file:
        writer.writerow({'ID': '4',
                     'collection': '/Commune',
                     'collection_parent': '/Collection_initiale',
                     'Titre': 'Internationale',
                     'Auteur': 'Eugnène Pottier',
                     'Interprete': 'Gustave Nadaud',
                     'Date': '1871',
                     'Content': '../../Collection_initiale/Commune/Internationale.txt',
                     'Link': 'https://fr.wikipedia.org/wiki/L%27Internationale'})

    with open('../../Collection_initiale/Chants_contre/Triomphe_Anarchie.txt', 'a') as txt_file:
        writer.writerow({'ID': '5',
                     'collection': '/Chants_contre',
                     'collection_parent': '/Collection_initiale',
                     'Titre': 'Le Triomphe de l\'Anarchie',
                     'Auteur': 'Charles d\'Avray',
                     'Interprete': 'Charles d\'Avray',
                     'Date': '1901',
                     'Content': '../../Collection_initiale/Chants_contre/Triomphe_Anarchie.txt',
                     'Link': 'https://fr.wikipedia.org/wiki/Le_Triomphe_de_l%27anarchie'})
