import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None

        self.dd_anno = None
        self.dd_brand = None
        self.dd_retailer = None

        self.btn_topVendite = None
        self.btn_analizzaVendite = None

        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Analizza Vendite", color="blue", size=24)
        self._page.controls.append(self._title)

        # TEMPLATE DROPDOWN (Menu a tendina event-driven)
        self.dd_anno = ft.Dropdown(
            label="anno",
            width=100,
            hint_text="Scegli l'anno",
            options=[],
            autofocus=True,  # Utile per far partire il cursore da qui
            on_change=self._controller.read_anno  # Avvisa il controller ad ogni cambio!
        )

        self.dd_brand = ft.Dropdown(
            label="brand",
            width=100,
            hint_text="Scegli il brand",
            options=[],
            on_change=self._controller.read_brand  # Avvisa il controller ad ogni cambio!
        )

        self.dd_retailer = ft.Dropdown(
            label="retailer",
            width=250,
            hint_text="Scegli il retailer",
            options=[],
        )

        self.btn_topVendite = ft.ElevatedButton(text="Top Vendite", on_click=self._controller.top_vendite)
        self.btn_analizzaVendite = ft.ElevatedButton(text="Analizza Vendite", on_click=self._controller.analizza_vendite)


        #Riga1
        row1 = ft.Row([self.dd_anno, self.dd_brand, self.dd_retailer], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        #Riga2
        row2 = ft.Row(controls=[self.btn_topVendite, self.btn_analizzaVendite], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)

        # === CHIAVE DI ACCENSIONE TENDINE ===
        # Dico al controller di andare al DB e riempire i menu appena l'app si apre!
        self._controller.populate_dd_anno()
        self._controller.populate_dd_brand()
        self._controller.populate_dd_retailer()



        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
