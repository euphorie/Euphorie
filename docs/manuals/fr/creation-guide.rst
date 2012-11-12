=====================================================
Guide de création d'un outil d'évaluation des risques  
=====================================================


1. Introduction
===============

Votre but est de créer le contenu de l'outil OiRA pour des entreprises de votre  secteur  et de leur offrir cet outil qui est spécifique à leur métier.

L'outil OiRA  propose une approche  de l'évaluation des risques en 5 étapes:

  * **Préparation** > introduction de la problématique de l'évaluation des risques dans le secteur

  * **Identification** > l'utilisateur passe en revue les situations de travail à risque par une série de questions auxquelles il doit répondre par  OUI ou NON 

  * **Évaluation** > les utilisateurs évaluent (cotent) les risques pour chacune des situations problématiques identifiées à l'étape précédente

  * **Plan d’action** > l'utilisateur  remplit un plan d'action avec des mesures pour maîtriser chaque risque cité	

  * **Rapport** > le contenu devient un rapport qui peut être téléchargé et imprimé 

1.1 Pensez à l'utilisateur final
--------------------------------------

Il est important de **considérer votre utilisateur final: les très petites et petites entreprises (employeur et salarié(s))**, la structure de l'outil d'évaluation de risques doit être aussi adaptée que possible aux activités quotidiennes des entreprises.

La manière de penser de l'expert est souvent différente de la pratique de l'utilisateur final. Ce dernier pense selon des processus propres à son métier, et le langage qu'il utilise lui est propre. Voici quelques exemples:

  * l’expert pense à la charge de travail physique, *tandis que l’utilisateur final pense au travail physique ou manuel*

  * l’expert pense à l’environnement thermique, tandis que *l’utilisateur final pense au travail sous la chaleur/dans le froid*

  * l’expert pense à la sécurité et crée un module contenant tout ce qui concerne ce domaine; *l’utilisateur final peut envisager, par exemple, d’ouvrir ou de fermer un magasin, et de réfléchir à ce que cela implique. Il peut également réfléchir à la façon de prendre en charge un client agressif.*


1.2 Utilisez un langage facile à comprendre par tous
----------------------------------------------------

**Structurer le contenu de l'outil d'évaluation des risques en tenant compte de la manière de penser et d'agir de l'utilisateur final**, permet un contenu compréhensible, qui facilite l’élaboration d’un plan d'action pour maîtriser les risques avec des mesures  réalistes et opérationnelles.

Un autre aspect décisif est le langage utilisé. Le **langage** doit être facile à comprendre sans nécessiter d’interprétation, et il doit utiliser des mots qui sont familiers et communs aux entreprises du secteur.

Des phrases courtes (pas plus de dix mots) et un langage de tous les jours pouvant être facilement lu par des non-initiés, éviteront de développer une certaine aversion de la part de l’utilisateur final. Ils lui permettront de dresser un inventaire et d’utiliser correctement l’outil d’évaluation des risques. 

Au début de l’outil vous avez l’occasion d’écrire un bref texte introductif, envoyant un **message positif** et encourageant portant sur: 

  * **l’importance** de l’évaluation des risques

  * le fait que l’évaluation des risques **n'est pas forcément compliquée** (pour contribuer à la démystification de l’évaluation des risques)

  * le fait que l’outil a été conçu spécifiquement pour **répondre aux besoins des petites entreprises** dans ce domaine 

Il est important que le texte ne soit pas trop long, pour ne pas décourager l'utilisateur final.


2. Équipe
=========

Bien qu’il soit important de maintenir l’équipe projet maîtrisable en terme de taille, il doit se composer idéalement de:

  * représentant(s) des organisations professionnelles du secteur

  * représentant(s) des syndicats de salariés du secteur

  * le développeur de l’outil OiRA

  * un expert en matière de santé et sécurité au travail (connaissant le secteur)

  * des utilisateurs finaux (employeurs, salariés, chargés de sécurité d'entreprises du secteur, représentants des salariés délégués du personnel etc.)


3. Structure 
============

3.1 Structurez le contenu hiérarchiquement
------------------------------------------

Avant de commencer de créer un outil OiRA nous recommandons de considérer le nombre de situations de travail que vous voulez aborder. Une structure bien pensée s’avère avantageusement par la suite. Veillez donc à classifier les rubriques dans un ordre correspondant aux besoins des utilisateurs finaux. 

Le système offre la possibilité de réunir des rubriques, des sous-rubriques et des types de risque en un groupe. L’objectif principal de ce groupement est de rendre l'outil plus simple et plus logique pour l'utilisateur final. Votre outil d’évaluation des risques se composera donc de:
 
.. image:: ../images/creation/module.png 
  :align: left
  :height: 32 px
  
**MODULES** = rubriques (lieux, activités, ...)
  
  *Exemple*: 
    Module 1: *Shampouiner des cheveux*  (domaine coiffeur)
  
  .. image:: ../images/creation/submodule.png 
    :align: left
    :height: 32 px
    
  **SOUS-MODULES** (facultatif) = sous-rubriques
  
    *Exemple*: 
      Sous-module 1: *Tenue de travail*
  
      Sous-module 2: *Contact avec de l’eau et des produits cosmétiques*
    
    .. image:: ../images/creation/risk.png 
      :align: left
      :height: 32 px
      
    **RISQUES** = déclarations concernant une situation qui est régulière
    
      *Exemple*: 
        *1.1 La station de shampooing est ajustable*
  
        *2.1 Les équipements de protection adéquats, comme p. ex. des gants de protection jetables, ont été acquis*
      
      .. image:: ../images/creation/solution.png 
        :align: left
        :height: 32 px
        
      **SOLUTIONS** = mesures préventives recommandées par l’expert pour résoudre le problème 
      
        *Exemple*: 
          *1.1 Equiper le salon de sièges ajustables*
  
          *2.1 Utiliser des produits sans poussière*

Le système offre aussi la possibilité de:

  * passer un ou plusieurs module(s) si le contenu ne s’applique pas à l’activité de l’entreprise

  * répéter certains modules, au cas où des entreprises ont plusieurs implantations

3.2 Définissez les risques par des déclarations positives (affirmation)
-----------------------------------------------------------------------

Dès que vous avez défini la trame principale de l'outil d'évaluation des risques vous pouvez commencer à identifier et à expliquer différents les risques. 

Le système fonctionne avec des **déclarations positives ou des affirmations** et non pas avec des questions sur les risques. C’est-à-dire le système indique si une **situation « est conforme ou maitrisée » (l’objectif à atteindre) ou « n'est pas conforme ou maitrisée ».**  

.. note::

  Exemple: Un bon éclairage est disponible.

La réponse de l’utilisateur final sera soit un « oui » explicite soit « non ». Si l’utilisateur final répond par « non » (= la situation n’est pas conforme), le problème sera alors automatiquement inclut dans l'étape suivante « plan d'action » et l'utilisateur final devra y proposer une mesure pour maîtriser ce risque.

3.3 Considérez les types de risques différents
----------------------------------------------

Vous avez le choix entre 3 types de risques (déclarations positives) :

  * **risques prioritaires**: se réfèrent à des risques considérés comme majeurs dans le secteur. 
  
    .. note::
  
      Exemple: Travailler en hauteur dans le domaine de construction. L’échafaudage est installé sur un sous-sol solide.

  * **risque**: se réfère à des déclarations à propos des risques existants sur le lieu de travail ou associés au travail effectué. 

    .. note:: 
    
      Exemple: Toutes les chaises de bureau sont ajustables.

Pour identifier et évaluer  de tels risques il est souvent nécessaire de faire une analyse spécifique à l'entreprise (parcourir le lieu de travail et regarder  ce qui pourrait causer des dommages, consulter les salariés, …).

  * **management**: se réfère à des modes d'action et des décisions de management en lien avec la sécurité et la santé au travail. Il est possible de répondre à ce type de questions depuis un bureau (il n'y a pas besoin d'analyser le lieu de travail). 

    .. note:: 
  
      Exemple: On demande régulièrement aux fournisseurs des produits alternatifs et sûrs. 
      
Il est possible de répondre à ce type de questions depuis un bureau (il n’y a pas besoin d’analyser le lieu de travail).

3.4 Paramétrez  l'évaluation des risques 
----------------------------------------------

Pour chaque type de « risque » vous avez le choix entre 2 méthodes d’évaluation:

  * **Estimative** : l'utilisateur définit un niveau priorité haute, moyenne ou basse. 

  * **Calculée** : l'utilisateur estime la probabilité, la fréquence et la sévérité séparément. L'outil OiRA calculera automatiquement la priorité.

Les items suivants seront classés automatiquement, les utilisateurs finaux n'auront pas besoin de les évaluer dans l'étape « Évaluation » :

  * risques prioritaires (considéré automatiquement comme « priorité haute » et indiqué comme tels dans le plan d’action)

  * management (il ne s’agit pas d’un risque)


3.5 Proposez des solutions
--------------------------

Les acteurs du secteur sont généralement bien renseignés sur les risques  d‘accidents et de maladies au travail les plus présents dans leur activité. Pour aider l'utilisateur final vous pouvez inclure des solutions recommandées par les experts. Lors de l'étape « plan d'action », l'utilisateur final aura la possibilité de choisir les solutions et de les modifier selon la situation dans son entreprise.

.. note::

  Tous les documents requis sont disponibles sur le site Web de la communauté OiRA http://www.oiraproject.eu/documentation


