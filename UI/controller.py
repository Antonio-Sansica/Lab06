import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        # === VARIABILI DI MEMORIA DEL CONTROLLER ===
        # Prepariamo tre cassetti vuoti. Si riempiranno in automatico
        # appena l'utente tocca i menu a tendina.
        self._anno_selezionato = None
        self._brand_selezionato = None
        self._retailer_code_selezionato = None

    # ====================================================================
    # 1. TENDINA ANNI
    # ====================================================================
    def populate_dd_anno(self):
        """Chiede gli anni al Model e crea le opzioni grafiche per la tendina"""
        anni = self._model.get_years()

        # AGGIUNTA: L'opzione di default in cima alla lista
        self._view.dd_anno.options.append(ft.dropdown.Option(key="None", text="Nessun filtro"))

        # Scorro la lista pulita che arriva dal nostro DAO
        for anno in anni:
            # Creo un'opzione visiva. Essendo numeri, li trasformiamo in stringa per Flet (opzionale ma più sicuro)
            self._view.dd_anno.options.append(ft.dropdown.Option(str(anno)))

        self._view.update_page()

    def read_anno(self, e):
        """Si attiva in automatico appena l'utente clicca su un anno nella tendina"""
        # Se l'utente clicca su "Nessun filtro" (che Flet legge come stringa "None")
        if e.control.value == "None":
            self._anno_selezionato = None
        else:
            # Salvo l'anno scelto nel cassetto del Controller.
            # Lo trasformo in int perché Flet restituisce sempre stringhe!
            self._anno_selezionato = int(e.control.value)

    # ====================================================================
    # 2. TENDINA BRAND
    # ====================================================================
    def populate_dd_brand(self):
        """Chiede i brand al Model e popola la tendina"""
        brands = self._model.get_brands()

        # AGGIUNTA: L'opzione di default in cima alla lista
        self._view.dd_brand.options.append(ft.dropdown.Option(key="None", text="Nessun filtro"))


        for brand in brands:
            # Inserisco il nome del brand come opzione
            self._view.dd_brand.options.append(ft.dropdown.Option(brand))

        self._view.update_page()

    def read_brand(self, e):
        """Si attiva in automatico appena l'utente seleziona un brand"""
        if e.control.value == "None":
            self._brand_selezionato = None
        else:
            # Salvo il testo del brand esattamente come l'ha cliccato l'utente
            self._brand_selezionato = e.control.value

    # ====================================================================
    # 3. TENDINA RETAILER (Metodo Avanzato ad Oggetti)
    # ====================================================================
    def populate_dd_retailer(self):
        """Chiede i Retailer completi al Model e li nasconde dentro la tendina"""
        # Chiamando questa funzione, si attiva ANCHE la Cache nel Model!
        retailers = self._model.get_retailers()

        # AGGIUNTA: L'opzione di default per il Retailer
        opzione_vuota = ft.dropdown.Option(
            key="None",
            text="Nessun filtro",
            data=None,  # Non c'è nessun oggetto nascosto!
            on_click=self.read_retailer
        )
        self._view.dd_retailer.options.append(opzione_vuota)

        for r in retailers:
            # Creiamo l'opzione speciale:
            # text = Quello che legge l'utente (Nome del negozio)
            # data = Quello che Flet nasconde in memoria (Tutto l'oggetto Retailer)
            # on_click = La funzione da chiamare appena si clicca QUESTA singola opzione
            opzione_speciale = ft.dropdown.Option(
                text=r.retailer_name,
                data=r,
                on_click=self.read_retailer
            )
            self._view.dd_retailer.options.append(opzione_speciale)

        self._view.update_page()

    def read_retailer(self, e):
        """Si attiva quando l'utente clicca la singola opzione nel menu.
           Va a scavare nel parametro 'data' per recuperare l'oggetto nascosto."""

        # e.control in questo caso NON è la tendina intera, ma è la singola riga cliccata!
        if e.control.data is None:
            self._retailer_code_selezionato = None
        else:
            # Recupero l'oggetto Retailer nascosto in "data" e mi salvo solo il suo codice (int)
            # Ci servirà più avanti per fare le query SQL filtrate per codice!
            oggetto_retailer = e.control.data
            self._retailer_code_selezionato = oggetto_retailer.retailer_code

    # ====================================================================
    # 4. BOTTONI DI RICERCA (Segnaposto)
    # ====================================================================
    def top_vendite(self, e):
        """Funzione collegata al bottone Top Vendite"""

        # 1. RECUPERO I FILTRI (Già pronti e impacchettati dalle tendine in tempo reale!)
        anno = self._anno_selezionato
        brand = self._brand_selezionato
        retailer_code = self._retailer_code_selezionato

        # 2. CHIAMATA AL MODEL
        # Passo i tre filtri. Se l'utente non ha scelto nulla, passeremo dei 'None' e
        # il magico COALESCE di SQL li ignorerà!
        top_vendite = self._model.get_top_vendite(anno, brand, retailer_code)

        # 3. PULIZIA SCHERMO (Fondamentale per non accavallare vecchie ricerche)
        self._view.txt_result.controls.clear()

        # 4. GESTIONE E STAMPA DEI RISULTATI
        if len(top_vendite) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessuna vendita trovata con questi filtri."))
        else:
            # Scorro la lista delle vendite arrivate dal database
            for vendita in top_vendite:
                # Grazie al metodo magico __str__ che hai messo nel DTO (Sale),
                # basta passare direttamente l'oggetto 'vendita' e si formatterà da solo!
                self._view.txt_result.controls.append(ft.Text(str(vendita)))

        # 5. AGGIORNO LA GRAFICA
        self._view.update_page()

    def analizza_vendite(self, e):
        """Funzione collegata al bottone Analizza Vendite"""

        # 1. Recupero i filtri
        anno = self._anno_selezionato
        brand = self._brand_selezionato
        retailer_code = self._retailer_code_selezionato

        # 2. Chiamo il Model
        statistiche = self._model.get_statistiche_vendite(anno, brand, retailer_code)

        # 3. Pulisco lo schermo per fare spazio ai nuovi risultati
        self._view.txt_result.controls.clear()

        # 4. GESTIONE E STAMPA
        # Se c'è un errore o se il conteggio delle vendite è 0
        if statistiche is None or statistiche["numero_vendite"] == 0:
            self._view.txt_result.controls.append(ft.Text("Nessuna vendita trovata con questi filtri."))
        else:
            # Stampo riga per riga seguendo il layout richiesto dal prof
            self._view.txt_result.controls.append(ft.Text("Statistiche vendite:", weight="bold"))

            # Formatto il giro d'affari con due cifre decimali (.2f)
            self._view.txt_result.controls.append(
                ft.Text(f"Giro d'affari: {statistiche['giro_affari']:.2f}")
            )
            self._view.txt_result.controls.append(
                ft.Text(f"Numero vendite: {statistiche['numero_vendite']}")
            )
            self._view.txt_result.controls.append(
                ft.Text(f"Numero retailers coinvolti: {statistiche['retailers_coinvolti']}")
            )
            self._view.txt_result.controls.append(
                ft.Text(f"Numero prodotti coinvolti: {statistiche['prodotti_coinvolti']}")
            )

        # 5. Dico alla grafica di aggiornarsi
        self._view.update_page()