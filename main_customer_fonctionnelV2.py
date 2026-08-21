from Classes.customer_fonctionnelV2 import *

if __name__ == "__main__":
    # Création des clients
    customers = [
        create_customer(
            customer_id=1,
            name="  Lionel  ",
            email="LIONEL@EXAMPLE.COM",
            phone="0123456789 "
        ),
        create_customer(
            customer_id=2,
            name="Nico",
            email="Nico@example.com"
        ),
    ]

    # Affichage des clients #renvoie Lionel et Nico
    print('Affichage clients:')
    for customer in customers:
        print(format_customer(customer))

    # Archivage Lionel
    print('\nArchivage de Lionel - nouvel objet sans modifier la liste ')
    customer_archived = archive_customer(customers[0])
    #Affichage des clients #renvoie Lionel et Nico : l'objet customer_archived n'a pas été sauvegardé
    print('Affichage clients:')
    for customer in customers:
        print(format_customer(customer))
    print('nouvel objet :')
    print(customer_archived)

    # Archivage Lionel
    print('\nArchivage de Lionel - modifie la liste')
    customers = archive_customer_by_id(customers, 1)

    #Affichage des clients #renvoie Nico
    print('\nAffichage clients:')
    for customer in customers:
        print(format_customer(customer))

    #Récup emails des clients actifs  # Renvoie nico
    print('\nMail des Clients actifs:')
    active_emails = get_active_customer_emails(customers)

    for email in active_emails:
        print(email)

    #Recup nb de clients actifs
    print('\nNombre de clients actifs:')
    print(calculate_active_customer_count(customers))