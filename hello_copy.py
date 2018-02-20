#!/usr/bin/python3
# -*- coding: utf-8 -*
'''
ce script sert à réaliser des fonctionnalités conçus à partir de notre dictionnaire et à l'aide 
du module flask.
'''
from flask import Flask, jsonify, request
import pickle
app = Flask(__name__)

#prendre les dictionaires crées à partir du corpus
f3=open("pairDictionary.txt","rb")
f4=open("wordFrequenceDictionary.txt","rb")
dependance_dic=pickle.load(f3)
wordFrq_dic=pickle.load(f4)
f3.close()
f4.close()

#---------------Fonction_1--------------------#
'''
cette fonction prend le resultat de dictionaire ordonné selon la valeur---[(key,value),(key2,value2)...]
comme entrée, et sort une liste des valeurs
'''
def toList(dicionary):
    reponse=[]
    for item in dicionary:
        reponse.append(item[0])
    return reponse

#---------------Fonction_2--------------------#
'''
cette fonction sert à prendre la liste des mots proposés selon le dernier mot de l'entrée; combiner la chaine
entrée et chaque mot dans la liste pour composer un nouvelle liste contenant des proposition,
comme si l'entrée est "il est " et on a besoin d'obtenir les reponses comme "il est pas", "il est un", tous les
propositions sont combiner 'il est' et les mots proposés: 'un' 'pas'...
'''
def dependanceAnswer(chaine,list):
    result=[]
    for item in list:
        result.append(chaine+item)
    return result

#---------------Fonction_3--------------------#
'''
c'est la fonction principale qui prend une chaine de caractère comme entrée et proposer une liste de autocomplete
selon différentes situations. 
'''
def autocomplete(input):
    anwser={}

    #première sitaution est que l'entrée est un seul mot et le résultat dont on a besoin est aussi un seul mot

    if input.split(" ")[-1]!="" and len(input.split(" "))<2:
        theWord=input.split(" ")[-1]
        for word in wordFrq_dic.keys():
            if word.startswith(theWord):
                anwser[word] = wordFrq_dic[word]
        anwser = sorted(anwser.items(), key=lambda d: d[1], reverse=True)[:5]
        reponse_word = toList(anwser)


        # si les propositions ne sont pas suffisants, on vérifie si le dernier mot est un mot assez complet et on
        # peut trouver ses mots dépendants, si oui on retourne une liste de proposition compris le mot proposés et
        # les dépendants, par exemple si on entre 'conventionnel', il retourne 'conventionnelles', 'conventionnelle'
        # et 'conventionnel de'...

        if len(reponse_word)<5:
            if theWord in dependance_dic.keys():
                reponseDic = sorted(dependance_dic[theWord].items(), key=lambda d: d[1], reverse=True)[:5]
                reponse_dependance = toList(reponseDic)
                reponse_dependance_final=[]
                for mot in reponse_dependance:
                     reponse_dependance_final.append(" "+mot)
                reponse_dependance_final=dependanceAnswer(input,reponse_dependance_final)
                reponse_word.extend(reponse_dependance_final)
                return reponse_word
            else:
                return reponse_word
        else:
            return reponse_word

    #deuxième situation est que l'éntrée combinée par plusieurs mots et l'usage ne type pas espace après dernier mot
    #dans ce cas, la sortie doit être inclue les chaine de caractères entrés et le mot proposé, ou des mots dépendnats proposés
    #par exemple si l'entrée est "il est", il retourne des propositions comme 'il estime'...
    elif input.split(" ")[-1]!="" and len(input.split(" "))>=2:
        theWord = input.split(" ")[-1]
        for word in wordFrq_dic.keys():
            if word.startswith(theWord):
                anwser[word] = wordFrq_dic[word]
        anwser = sorted(anwser.items(), key=lambda d: d[1], reverse=True)[:5]
        reponse_word_first = toList(anwser)
        reponse_word=[]
        for item in reponse_word_first:
            tempo=input.split(" ")[:-1]
            tempo.append(item)
            tempo=" ".join(tempo)
            reponse_word.append(tempo)
        #meme logique que la première situation
        if len(reponse_word) < 5:
            if theWord in dependance_dic.keys():
                reponseDic = sorted(dependance_dic[theWord].items(), key=lambda d: d[1], reverse=True)[:5]
                reponse_dependance = toList(reponseDic)
                reponse_dependance_final = []
                for mot in reponse_dependance:
                    reponse_dependance_final.append(" " + mot)
                reponse_dependance_final = dependanceAnswer(input, reponse_dependance_final)
                reponse_word.extend(reponse_dependance_final)
                return reponse_word
            else:
                return reponse_word
        else:
            return reponse_word
    #dernière situation est que l'utilisateur entre un espace après une chaine de caractère dons il attend la proposition de mots dépendants
    #cette situation est simple, il retourne une liste des mots dépendant selon le dernier mot entré
    #par exemple, si entree est "il est ", il retourne la liste de résultat comme 'il est pas', 'il est un'...
    elif input.split(" ")[-1]=="":
        wordIn=input.split(" ")[-2]
        if wordIn in dependance_dic.keys():
            reponseDic=sorted(dependance_dic[wordIn].items(), key=lambda d:d[1],reverse=True)[:5]
            reponse_dependance=toList(reponseDic)
            reponse_dependance=dependanceAnswer(input,reponse_dependance)
            return(reponse_dependance)

#appliquer sur le site
@app.route('/', methods=['GET'])
def hello_world():
    response = ""
    term = request.args['term']
    if term:
        items=autocomplete(term)
        response = jsonify(items)
        response.headers.add('Access-Control-Allow-Origin', '*') #Pour éviter les erreurs de type CORS en dév local
    return response

