from database.DB_connect import DBConnect
from model.retailer import Retailer

def get_tutti_anni():
    """Estrae tutti gli anni distinti in cui ci sono state vendite"""
    cnx = DBConnect.get_connection()
    result = []
    if cnx is None:
        return result
    try:
        cursor = cnx.cursor()
        # YEAR(Date) estrae solo l'anno dalla data. DISTINCT evita i doppioni.
        query = "SELECT DISTINCT YEAR(Date) as anno FROM go_daily_sales ORDER BY anno"
        cursor.execute(query)
        for row in cursor:
            result.append(row[0]) # Aggiungiamo l'anno alla lista
        return result
    except Exception as e:
        print(f"Errore DAO anni: {e}")
        return []
    finally:
        cursor.close()
        cnx.close()

def get_tutti_brand():
    """Estrae tutti i brand distinti dei prodotti"""
    cnx = DBConnect.get_connection()
    result = []
    if cnx is None:
        return result
    try:
        cursor = cnx.cursor()
        query = "SELECT DISTINCT Product_brand FROM go_products ORDER BY Product_brand"
        cursor.execute(query)
        for row in cursor:
            result.append(row[0])
        return result
    except Exception as e:
        print(f"Errore DAO brand: {e}")
        return []
    finally:
        cursor.close()
        cnx.close()

def get_tutti_retailers():
    """Estrae tutti i retailer e crea gli oggetti (Da mettere nella tendina come Mappa)"""
    cnx = DBConnect.get_connection()
    result = []
    if cnx is None:
        return result
    try:
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM go_retailers ORDER BY Retailer_name"
        cursor.execute(query)
        for row in cursor:
            r = Retailer(
                retailer_code=row["Retailer_code"],
                retailer_name=row["Retailer_name"],
                type=row["Type"],
                country=row["Country"]
            )
            result.append(r)
        return result
    except Exception as e:
        print(f"Errore DAO retailers: {e}")
        return []
    finally:
        cursor.close()
        cnx.close()


from model.sale import Sale


def get_top_vendite(anno, brand, retailer_code):
    """
    Trova le migliori 5 vendite filtrate per anno, brand e retailer.
    Ordina in senso decrescente in base al ricavo (Unit_sale_price * Quantity).
    """
    cnx = DBConnect.get_connection()
    result = []
    if cnx is None:
        return result
    try:
        cursor = cnx.cursor(dictionary=True)

        # LA SUPER QUERY CON COALESCE E LE JOIN
        # Dobbiamo unire le vendite con i prodotti per poter filtrare sul 'brand'
        query = """
            SELECT 
                s.Date, s.Quantity, s.Unit_price, s.Unit_sale_price, 
                s.Retailer_code, s.Product_number, s.Order_method_code
            FROM go_daily_sales s
            JOIN go_products p ON s.Product_number = p.Product_number
            WHERE 
                YEAR(s.Date) = COALESCE(%s, YEAR(s.Date))
                AND p.Product_brand = COALESCE(%s, p.Product_brand)
                AND s.Retailer_code = COALESCE(%s, s.Retailer_code)
            ORDER BY (s.Unit_sale_price * s.Quantity) DESC
            LIMIT 5
        """

        # Passiamo la tupla dei filtri (Se sono None, COALESCE li ignora!)
        cursor.execute(query, (anno, brand, retailer_code))

        for row in cursor:
            # Creiamo l'oggetto Sale
            vendita = Sale(
                date=row["Date"],
                quantity=row["Quantity"],
                unit_price=row["Unit_price"],
                unit_sale_price=row["Unit_sale_price"],
                retailer_code=row["Retailer_code"],
                product_number=row["Product_number"],
                order_method_code=row["Order_method_code"]
            )
            result.append(vendita)

        return result
    except Exception as e:
        print(f"Errore DAO Top Vendite: {e}")
        return []
    finally:
        cursor.close()
        cnx.close()


def get_statistiche_vendite(anno, brand, retailer_code):
    """
    Calcola le statistiche aggregate (somma ricavi, conteggi) filtrate dall'utente.
    """
    cnx = DBConnect.get_connection()
    if cnx is None:
        return None
    try:
        cursor = cnx.cursor(dictionary=True)

        # Facciamo fare la matematica a SQL!
        # SUM somma i ricavi. COUNT conta le righe. COUNT(DISTINCT) conta i valori univoci senza doppioni.
        query = """
            SELECT 
                SUM(s.Unit_sale_price * s.Quantity) AS giro_affari,
                COUNT(*) AS numero_vendite,
                COUNT(DISTINCT s.Retailer_code) AS retailers_coinvolti,
                COUNT(DISTINCT s.Product_number) AS prodotti_coinvolti
            FROM go_daily_sales s
            JOIN go_products p ON s.Product_number = p.Product_number
            WHERE 
                YEAR(s.Date) = COALESCE(%s, YEAR(s.Date))
                AND p.Product_brand = COALESCE(%s, p.Product_brand)
                AND s.Retailer_code = COALESCE(%s, s.Retailer_code)
        """

        cursor.execute(query, (anno, brand, retailer_code))

        # Usiamo fetchone() perché questa query restituirà SEMPRE E SOLO una riga coi totali!
        result = cursor.fetchone()
        return result

    except Exception as e:
        print(f"Errore DAO Statistiche: {e}")
        return None
    finally:
        cursor.close()
        cnx.close()