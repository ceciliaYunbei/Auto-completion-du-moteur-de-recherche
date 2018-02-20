#!/usr/bin/python3
# -*- coding: utf-8 -*

'''
ce script consiste à nettoyer le corpus initiale et préparer les pairs de mots 
ainsi que leurs fréquences. Dans ce script, on a utilisé les modules re, collection, pickle et nltk.
et pour les sorties: deux dictionnaires pairDictionary.txt wordFrequenceDictionary.txt sauvegardés sous format binaire de pickle.
'''
import re,pickle
import nltk,collections

#Nettoyer le texte: enlever des chiffres et des ponctuations
def clear(texte):
    texte = re.sub(u"[*&%!?\|\"{\(\[|_\)\]},\.;/:§»«”“‘…–—−]", "", texte)
    texte=texte.replace("-","")
    chiffre = re.compile(r'[0123456789]', re.I)
    texte = chiffre.sub("", texte)
    texte = texte.replace(u"’", u"'")
    texte = texte.replace(u"'", u"\' ")
    return texte

#Pour chaque mot dans une phrase, tirer ce mot et le mot suivant comme une paire
def makePairs(texte):
    pairs=[]
    texte=clear(texte)#nettoyer la phrase
    listWords=nltk.word_tokenize(texte,"french")
    for i in range(len(listWords)):
        if i<len(listWords)-1:
            temp=(listWords[i],listWords[i+1])#faire la paire
            pairs.append(temp)#combiner toutes les paires dans une liste
    return (pairs,listWords)


with open("corpus_fr.txt","r",encoding="utf-8") as file:
    texte=file.read()
    allWordsAndFrq = []
    allWordAndNextWord = {}
    for line in texte.split("\n"):#traiter ce corpus ligne par ligne
        pairs,wordlist=makePairs(line)#pour chaque ligne,collecter les mots et les paires de chaque mot
        allWordsAndFrq.extend(wordlist)#ajouter la liste de mots de cette phrase à la liste commune
        for word in wordlist:#chercher les paires de chaque mot dans la liste de mots
            for pair in pairs:
                if pair[0]==word:
                    allWordAndNextWord.setdefault(pair[0],[]).append(pair[1])#dans ce dictionaire, le cle est mot,la valeur est une liste contenant tous les mots suivant ce mot




allWordsAndFrq=dict(collections.Counter(allWordsAndFrq))#utiliser le counter pour calculer les frequences des mots
for key in allWordAndNextWord.keys():
    allWordAndNextWord[key]=dict(collections.Counter(allWordAndNextWord[key]))#counter calcule les frequences des mots suivant un mot

#stocker les dictionaires
f1=open("pairDictionary.txt","wb")
pickle.dump(allWordAndNextWord,f1)
f1.close()
f2=open("wordFrequenceDictionary.txt","wb")
pickle.dump(allWordsAndFrq,f2)
f2.close()





