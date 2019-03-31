#!/usr/bin/env python3

import sys,re,os

def help():
    print("Use it like this :")
    print("\t"+sys.argv[0]+" [directory] \"Something to find\"")
    print()
    print("findall version 1.0")
    print("By Kezzoul Massili -> mailto:massy.kezzoul@gmail.com")
    print("Github -> https://github.com/massykezzoul")
    print("Mar. 2019")
    exit()

## retourne l'extension du fichier (sans le '.')
def extension(name):
    ext = re.search(".+\.([^.]+)$",name) 
    if ext :
        return ext.group(1)
    else :
        return ""

# appliquer une Expression Régulière sur une liste d'elements
def listRe(rep,l,reg):
    listResultat = []
    for e in l:
        res = re.search(reg,e.lower())
        if res:
            listResultat.append(os.path.join(rep,e))
    return listResultat

# Fonction de parcour de repertoire avec recherche de mot cle
def parcours(rep,find) :
    print("\rEn Cours ...",end="")
    liste = os.listdir(rep)
    files = listRe(rep,liste,"^.*"+find+".*$") # recherche sur les nom de fichiers
    for file in liste:
        if os.path.isdir(os.path.join(rep,file)):
            files = files + parcours(os.path.join(rep,file),find)
        else:
            ## liste des extensions ouvrables
            extOuvrable = ["pdf","txt","cpp","h","hpp","c","cc","py","java","js","json","xml","html","css","php","tex","sh"]
            ext = extension(os.path.join(rep,file))
            if (ext in extOuvrable):
                if (ext == "pdf"):
                    ## fichier pdf doit etre convertit en text avec la commande "pdftotext [file] - 2> /dev/null"  en ignorant la sortie d'erreur 
                    pdf = os.popen("pdftotext \""+os.path.join(rep,file)+"\" - 2> /dev/null")
                else:
                    ## fichier hors pdf, ouverture standard
                    pdf = open(os.path.join(rep,file),"r")
                if pdf :
                    try: 
                        for line in pdf:
                            if (re.search("^.*"+find+".*$",line.lower())):
                                files.append("inside : "+os.path.join(rep,file))
                                break
                    except UnicodeDecodeError as err:
                        ## Erreur d'encodage du fichier (fichier n'est pas en UTF-8)
                        ## Réesseyer avec l'encodage ISO-8859-1
                        pdf.close()
                        pdf = open(os.path.join(rep,file),"r",encoding = "ISO-8859-1")
                        try:
                            for line in pdf:
                                if (re.search("^.*"+find+".*$",line.lower())):
                                    files.append("inside : "+os.path.join(rep,file))
                                    break
                        except UnicodeDecodeError as err:
                            ## Erreur d'encodage du fichier (fichier n'est pas en ISO-8859-1)
                            ## abondon du fichier
                            print("\r",err,"on file :",os.path.join(rep,file),file=sys.stderr)
                    finally:
                        pdf.close()
                else : 
                    print("Erreur dans la lecture du fichier :",os.path.join(rep,file))
    return files

# trier les resultats d'abord les noms de fichier ensuite le contenu
def trie(files):
    res = []
    for file in files:
        if not re.search("^inside :.*",file):
            res.append(file)
    for file in files:
        if re.search("^inside :.*",file):
            res.append(file)
    return res


## main
directory = ""
find = ""

# si Aucun argument donnée
if (len(sys.argv) < 2):
    help()
# Si un seul argument donnée (rechercher sur le dosser courent)
elif (len(sys.argv) < 3):
    directory = "." # Use current directory
    find = sys.argv[1]
# sinon 1ER argument est le dossier où chercher et le 2EME est la chaine à rechercher
else:
    directory = sys.argv[1]
    find = sys.argv[2]

res = trie(parcours(directory,find.lower()))
print("\r",end="")

if (len(res) == 0):
    print("Aucun resultat trouver!")
else :    
    tropR = (len(res) > 100) ## si il y'a plus de 100 resultat demander si l'utilisateur veut tous les afficher
    if (tropR):
        print("Voulez-vous afficher les",len(res),"resultats ? (O/N)",end=" ")
        rep = input()
        if (rep.lower()[0] != 'o'):
            exit()
    print(len(res),"Resultats trouvé : ")
    for r in res :
        print(r)
