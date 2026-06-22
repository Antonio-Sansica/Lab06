from dataclasses import dataclass

@dataclass
class Product:
    product_number: int
    product_line: str
    product_type: str
    product: str
    product_brand: str
    product_color: str
    unit_cost: float
    unit_price: float

    # Metodo per stamparlo bene a schermo
    def __str__(self):
        return f"Numero: {self.product_number}, Prodotto: {self.product}"

    # Metodi per permettere a Python di confrontare gli oggetti
    def __eq__(self, other):
        return self.product_number== other.product_number

    def __hash__(self):
        return hash(self.product_number)