Explication et Ajout pour les fichiers lié à la demande de Eric, concernant le paradigme fonctionnel.  

Ajout des classes : customer_fonctionnelV1.py et customer_fonctionnelV2.py dans Classes  
Ajout des main : main_fonctionnel.py et main_fonctionnelV2.py à la racine  

customer_fonctionnelV1 : Je suis reparti de ma classe Customer, mais en recodant de zero une solution avec ce que je pense avoir compris du paradigme fonctionnel.  
customer_fonctionnelV2 : J'ai appliqué ce que j'ai pu faire dans Customer_fonctionnelV1, et l'ai réappliqué a ma classe Customer, afin de la garder et ne pas partir sur des dictionnaires  

Modifications :  

1) Immuabilité du customer  :
Dans Customer.py, un client était un objet avec un état (1, Lionel, Lionel@example.com, actif), et dont l'état pouvait changer (archive, unarchive).

- Dans Customer_fonctionnelV1.py, le client n'est plus une classe, mais une représentation de données, dont le comportement est déplacé dans les fonctions. Quand on archive avec "customers = archive_customer(customer)", on ne modifie pas l'objet, on crée une nouvelle valeur.
- Dans Customer_fonctionnelV2.py, j'ai gardé ma classe que j'ai passé en frozen=True pour la rendre immuable.

2) Archivage Customer  :
 - Dans Customer_fonctionnelV1.py  :
Dans la fonction
def archive_customer(customer):
    return {
        **customer,
        "active": False,
    }
Utilisation de ** pour l'immutabilité des valeurs, sauf celle que l'on souhaite modifier, ici le statut active du client.
 - Dans Customer_fonctionnelV2.py  : on retourne un nouvel objet avec la valeur active remplacée.  
-->  Donc, a présent, on a ceci : Customer actif  --> fonction --> Customer archivé  sans modifier l'entrée.  
     On a donc un passage de l'ancien état au nouvel état sans modifier l'objet en interne.  
     Archive_customer renvoie un nouveau client avec la modification de l'etat. mais le client original n'a pas été modifié.  
   Tout comme Archive_customer_by_id crée une nouvelle liste, au lieu de modifier la valeur.  

3) Suppression des Setter, remplacer par des fonctions appelées a la creation de l'objet (validate_XXXX) pour validation, normalisation et renvoi de la valeur. AU lieu d'avoir des fonctions rattachées à l'objet, elles deviennent des fonctions indépendantes.  
--> De ce que j'ai pu lire et comprendre du paradigme fonctionnel dont Eric me parlait, ceci est une caractéristique importante: composer des fonctions simples pour construire un traitement plus complexe.  
Cela permettrais également de tester avec des assert les différentes fonctions au niveau des tests.  

4) Remplacement de Customer.isactive par fonction def is_active(customer):  
Toute la logique permettant de déterminer si un client est actif reste alors centralisée dans une fonction métier.  
Cela permet de centraliser la règle métier et de la rendre testable à son niveau.  

5) Utilisation de filter et map, pour filtrer les utilisateur actifs, ou les mails de ces derniers.
   (Les fonctions peuvent donc être manipulées comme des valeurs. ce qui fait partie du paradigme fonctionnel)  

6) Suppression de print et repr. remplacement par def format_customer(customer)  
Vu qu'il n'y a plus de classe Customer, on utilise la novuelle fonction pour de l'affichage pur.  

Conclusion :
Avant, j'avais le stockage de l'état, la validation, la normalisation, l'archivage et le désarchivage, et l'affichage dans ma classe Customer.  
Mon ancienne classe contient beaucoup de mutations d'état via les setters et archive() / unarchive().  
Cette nouvelle version fonctionnelle sépare bien plus les responsabilités. 
Enfin, la logique métier de ma classe Customer est préservée (validation, normalisation du telephone, creation des clients, (dés)archivage d'un client.

