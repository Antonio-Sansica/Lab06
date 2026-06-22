import datetime
from dataclasses import dataclass

@dataclass
class Sale:
    date: datetime.date
    quantity: int
    unit_price: float
    unit_sale_price: float

    # relazioni
    retailer_code: int
    product_number: int
    order_method_code: int

    # Calcolo automatico del ricavo richiesto dalla traccia
    @property
    def ricavo(self):
        return self.unit_sale_price * self.quantity

    # Metodo per stamparlo bene a schermo
    def __str__(self):
        return f"Data: {self.date}; Ricavo: {self.ricavo:.2f}; Retailer: {self.retailer_code}; Product: {self.product_number}"

    # Metodi per permettere a Python di confrontare gli oggetti
    def __eq__(self, other):
        return (self.retailer_code == other.retailer_code and
                self.product_number == other.product_number and
                self.order_method_code == other.order_method_code)

    def __hash__(self):
        # NOTA LE DOPPIE PARENTESI: stiamo passando una tupla!
        return hash((self.retailer_code, self.product_number, self.order_method_code))