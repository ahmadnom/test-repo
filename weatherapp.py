import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import ttkbootstrap as tb


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x400")

        # API Key (keep here for now)
        self.API_key = "92ae024b53637ac1bc545f09aa077742"

        # --- Widgets ---
        self.city_entry = tb.Entry(self.root, font=("Helvetica", 18))
        self.city_entry.pack(pady=10)

        self.search_button = tb.Button(
            self.root, text="Search", command=self.search, bootstyle="warning"
        )
        self.search_button.pack(pady=10)

        self.location_label = tk.Label(self.root, font=("Helvetica", 25))
        self.location_label.pack(pady=20)

        self.icon_label = tk.Label(self.root)
        self.icon_label.pack()

        self.temperature_label = tk.Label(self.root, font=("Helvetica", 20))
        self.temperature_label.pack()

        self.description_label = tk.Label(self.root, font=("Helvetica", 20))
        self.description_label.pack()

    # --- Function: Fetch weather from API ---
    def get_weather(self, city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_key}"
        res = requests.get(url)

        if res.status_code == 404:
            messagebox.showerror("Error", "City Not Found")
            return None

        weather = res.json()
        icon_id = weather["weather"][0]["icon"]
        temperature = weather["main"]["temp"] - 273.15
        description = weather["weather"][0]["description"]
        city = weather["name"]
        country = weather["sys"]["country"]

        icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
        return icon_url, temperature, description, city, country

    # --- Function: Search button handler ---
    def search(self):
        city = self.city_entry.get()
        result = self.get_weather(city)
        if result is None:
            return

        icon_url, temperature, description, city, country = result
        self.location_label.configure(text=f"{city}, {country}")

        # Weather icon
        image = Image.open(requests.get(icon_url, stream=True).raw)
        icon = ImageTk.PhotoImage(image)
        self.icon_label.configure(image=icon)
        self.icon_label.image = icon

        # Update labels
        self.temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
        self.description_label.configure(text=f"Description: {description}")


if __name__ == "__main__":
    root = tb.Window(themename="morph")
    app = WeatherApp(root)
    root.mainloop()
