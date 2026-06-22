from dataclasses import dataclass

@dataclass
class Retailer:
    retailer_code: int
    retailer_name: str
    type: str
    country: str


    # Metodo per stamparlo bene a schermo
    def __str__(self):
        return f"Codice:{self.retailer_code}, Nome: {self.retailer_name}, Tipo: {self.type}, Nazione: {self.country}"

    # Metodi per permettere a Python di confrontare gli oggetti
    def __eq__(self, other):
        return self.retailer_code == other.retailer_code

    def __hash__(self):
        return hash(self.retailer_code)