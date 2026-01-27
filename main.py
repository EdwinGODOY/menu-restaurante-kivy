import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


# ---------- Pantalla Inicio ----------
class InicioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)

        titulo = Label(
            text="Restaurante El Patio",
            font_size=32,
            size_hint=(1, 0.7)
        )

        boton = Button(
            text="Ver menú",
            size_hint=(1, 0.3)
        )
        boton.bind(on_press=self.ir_menu)

        layout.add_widget(titulo)
        layout.add_widget(boton)
        self.add_widget(layout)

    def ir_menu(self, instance):
        self.manager.current = "categorias"


# ---------- Pantalla Categorías ----------
class CategoriasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        titulo = Label(text="Categorías", font_size=28, size_hint=(1, 0.2))
        layout.add_widget(titulo)

        self.contenedor = BoxLayout(orientation='vertical', spacing=10)
        layout.add_widget(self.contenedor)

        self.add_widget(layout)

    def on_enter(self):
        self.contenedor.clear_widgets()
        categorias = set(p["categoria"] for p in App.get_running_app().productos)

        for categoria in categorias:
            btn = Button(text=categoria, size_hint_y=None, height=50)
            btn.bind(on_press=self.ver_productos)
            self.contenedor.add_widget(btn)

    def ver_productos(self, instance):
        app = App.get_running_app()
        app.categoria_actual = instance.text
        self.manager.current = "productos"


# ---------- Pantalla Productos ----------
class ProductosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.titulo = Label(font_size=26, size_hint=(1, 0.15))
        layout.add_widget(self.titulo)

        scroll = ScrollView()
        self.lista = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.lista.bind(minimum_height=self.lista.setter('height'))

        scroll.add_widget(self.lista)
        layout.add_widget(scroll)

        btn_volver = Button(text="Volver", size_hint=(1, 0.15))
        btn_volver.bind(on_press=self.volver)
        layout.add_widget(btn_volver)

        self.add_widget(layout)

    def on_enter(self):
        app = App.get_running_app()
        categoria = app.categoria_actual
        self.titulo.text = f"Productos - {categoria}"
        self.lista.clear_widgets()

        for p in app.productos:
            if p["categoria"] == categoria:
                texto = f"{p['nombre']} - $ {p['precio']:.2f}"
                lbl = Label(text=texto, size_hint_y=None, height=40)
                self.lista.add_widget(lbl)

    def volver(self, instance):
        self.manager.current = "categorias"


# ---------- Aplicación ----------
class MenuApp(App):
    def build(self):
        self.cargar_datos()
        self.categoria_actual = ""

        sm = ScreenManager()
        sm.add_widget(InicioScreen(name="inicio"))
        sm.add_widget(CategoriasScreen(name="categorias"))
        sm.add_widget(ProductosScreen(name="productos"))

        return sm

    def cargar_datos(self):
        with open("menu.json", "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
            self.productos = data["productos"]


if __name__ == "__main__":
    MenuApp().run()
