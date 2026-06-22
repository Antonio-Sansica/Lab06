# Importiamo direttamente le TUE funzioni dal TUO unico file DAO
from database.sales_dao import get_tutti_anni, get_tutti_brand, get_tutti_retailers, get_top_vendite, get_statistiche_vendite

class Model:
    def __init__(self):
        """
        Prepariamo la scatola della memoria (Cache / Identity Map)
        per salvarci i Retailer ed evitare di scaricarli due volte.
        """
        self.retailers_map = {}

    def get_years(self):
        """
        Chiama la tua funzione nel DAO e restituisce la lista degli anni.
        """
        return get_tutti_anni()

    def get_brands(self):
        """
        Chiama la tua funzione nel DAO e restituisce la lista dei brand.
        """
        return get_tutti_brand()

    def get_retailers(self):
        """
        Chiama il DAO, riempie la mappa di memoria e restituisce i dati.
        """
        # 1. Chiedo al TUO DAO la lista "grezza" dei retailer
        lista_retailers = get_tutti_retailers()

        # 2. LA MAGIA DELLA CACHE:
        # Visto che il tuo DAO estrae solo la lista, usiamo il Model per
        # riempire il dizionario (Identity Map).
        for r in lista_retailers:
            # Salvo l'oggetto Retailer nel dizionario usando il suo codice come "Chiave"
            self.retailers_map[r.retailer_code] = r

        # 3. Restituisco la lista al Controller per riempire la tendina
        return lista_retailers

    def get_top_vendite(self, anno, brand, retailer_code):
        """
        Passacarte: chiede al DAO le migliori 5 vendite filtrate.
        """
        return get_top_vendite(anno, brand, retailer_code)

    def get_statistiche_vendite(self, anno, brand, retailer_code):
        """
        Passacarte: chiede al DAO le statistiche calcolate su misura.
        """
        return get_statistiche_vendite(anno, brand, retailer_code)


