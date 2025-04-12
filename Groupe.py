import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import os
import webbrowser
from PIL import Image, ImageTk  # Pour afficher le logo
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from fpdf import FPDF  # Pour l'export PDF

# Define the base directory (current directory of the script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Liste des groupes électrogènes disponibles (en kVA)
GROUPES_DISPONIBLES = [8, 10, 12, 20, 25, 30, 37.5, 50, 62.5, 100, 125,150, 160,187.5,200, 250, 625]
FACTEUR_PUISSANCE = 0.8  # Facteur de puissance

# Relative paths for technical sheet directory and image
FICHE_TECHNIQUE_DIR = os.path.join(BASE_DIR," ")
IMAGE_PATH = os.path.join(BASE_DIR, "solar.jpg")

class ThinkerApp :
    def __init__(self, root):
        self.root = root
        self.root.title("Lano Power Design ")
        
        # ----- En-tête avec logo et titre -----
        header_frame = tk.Frame(root)
        header_frame.pack(pady=10)

        # Charger et afficher l'image du logo
        image_pil = Image.open(IMAGE_PATH)
        image_pil = image_pil.resize((100, 100))  # Redimensionner l'image
        self.logo_image = ImageTk.PhotoImage(image_pil)

        logo_label = tk.Label(header_frame, image=self.logo_image)
        logo_label.pack(side="left", padx=10)

        # Ajouter le titre principal
        title_label = tk.Label(header_frame, text="Lano Power", font=("Arial", 24, "bold"), fg="blue")
        title_label.pack(side="left", padx=20)

        self.data = []
        
        # ----- Champs pour client -----
        self.client_frame = tk.Frame(root)
        self.client_frame.pack(pady=10)

        # Nom du Client
        tk.Label(self.client_frame, text="Nom du Client", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        self.client_name = tk.Entry(self.client_frame, font=("Arial", 10))
        self.client_name.grid(row=0, column=1, padx=5)

        # Numéro de Téléphone
        tk.Label(self.client_frame, text="Numéro de Téléphone", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5)
        self.client_phone = tk.Entry(self.client_frame, font=("Arial", 10))
        self.client_phone.grid(row=1, column=1, padx=5)

        # Nom du Commercial
        tk.Label(self.client_frame, text="Nom du Commercial", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5)
        self.salesperson_name = tk.Entry(self.client_frame, font=("Arial", 10))
        self.salesperson_name.grid(row=2, column=1, padx=5)

        # Date du Devis
        tk.Label(self.client_frame, text="Date du Devis", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=5)
        self.estimate_date = tk.Entry(self.client_frame, font=("Arial", 10))
        self.estimate_date.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Default date as today
        self.estimate_date.grid(row=3, column=1, padx=5)

        # ----- Tableau d'entrée des matériels -----
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)
        
        self.headers = ["Matériel", "Puissance (W)", "Nombre", "Coefficient de Correction"]
        
        for i, header in enumerate(self.headers):
            tk.Label(self.frame, text=header, font=("Arial", 10, "bold")).grid(row=0, column=i)
        
        self.entries = []
        self.add_row()
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        
        self.add_button = tk.Button(button_frame, text="Ajouter une ligne", command=self.add_row)
        self.add_button.grid(row=0, column=0, padx=5)
        
        self.remove_button = tk.Button(button_frame, text="Supprimer la dernière ligne", command=self.remove_row)
        self.remove_button.grid(row=0, column=1, padx=5)
        
        self.calculate_button = tk.Button(button_frame, text="Calculer Puissance Totale", command=self.calculate_total_power)
        self.calculate_button.grid(row=0, column=2, padx=5)
        
        self.total_power_label = tk.Label(root, text="Puissance Totale: 0 W", font=("Arial", 12, "bold"))
        self.total_power_label.pack(pady=5)
        
        self.generator_recommendation_label = tk.Label(root, text="Groupe électrogène recommandé: N/A", font=("Arial", 12, "bold"))
        self.generator_recommendation_label.pack(pady=5)
        
        self.suggestion_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.suggestion_label.pack(pady=5)
        
        self.tech_sheet_frame = tk.Frame(root)
        self.tech_sheet_frame.pack(pady=5)
        
        self.tech_sheet_buttons = []
        for i, power in enumerate(GROUPES_DISPONIBLES):
            btn = tk.Button(self.tech_sheet_frame, text=f"{power} kVA", command=lambda p=power: self.view_tech_sheet(p))
            btn.grid(row=i//6, column=i%6, padx=5, pady=5)
            self.tech_sheet_buttons.append(btn)
        
        self.export_button = tk.Button(root, text="Exporter en Excel", command=self.export_excel)
        self.export_button.pack(pady=5)

        # ----- Bouton pour générer PDF -----
        self.generate_pdf_button = tk.Button(root, text="Générer PDF", command=self.generate_pdf)
        self.generate_pdf_button.pack(pady=10)

        # ----- Espace pour afficher les graphiques Plotly -----
        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack(pady=10)
    
    def view_tech_sheet(self, power):
    #Ouvre la fiche technique PDF correspondant au groupe électrogène sélectionné.

        pdf_filename = f"{power}kVA.pdf"  # Nom du fichier PDF attendu
        pdf_path = os.path.abspath(pdf_filename)  # Chemin absolu du fichier

        if os.path.exists(pdf_path):
            webbrowser.open(pdf_path)  # Ouvre le fichier avec le programme par défaut
        else:
            messagebox.showerror("Erreur", f"Fiche technique introuvable pour {power} kVA.")    

    def add_row(self):
        row_entries = []
        row_index = len(self.entries) + 1
        
        for col in range(len(self.headers)):
            entry = tk.Entry(self.frame)
            entry.grid(row=row_index, column=col, padx=5, pady=2)
            row_entries.append(entry)
        
        self.entries.append(row_entries)
    
    def remove_row(self):
        if self.entries:
            last_row = self.entries.pop()
            for entry in last_row:
                entry.destroy()
    
    def calculate_total_power(self):
        total_power_w = 0
        material_names = []
        power_values = []
        
        for row in self.entries:
            try:
                material = row[0].get()
                power = float(row[1].get()) if row[1].get() else 0
                quantity = int(row[2].get()) if row[2].get() else 0
                correction = float(row[3].get()) if row[3].get() else 1
                
                total_power_w += power * quantity * correction
                
                if power * quantity * correction > 0:
                    material_names.append(material)
                    power_values.append(power * quantity * correction)
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")
                return
        
        total_power_kva = total_power_w / (1000 * FACTEUR_PUISSANCE)
        
        # Trouver le groupe électrogène disponible le plus proche
        recommended_generator = next((g for g in GROUPES_DISPONIBLES if g >= total_power_kva), "Aucun disponible")
        
        # Stocker les valeurs dans l'objet
        self.total_power_w = total_power_w
        self.total_power_kva = total_power_kva
        self.recommended_generator = recommended_generator      

        self.total_power_label.config(text=f"Puissance Totale: {total_power_w:.2f} W ({total_power_kva:.2f} kVA)")
        self.generator_recommendation_label.config(text=f"Groupe électrogène recommandé: {recommended_generator} kVA")
        #self.suggestion_label.config(text=f"Madagascar Lano  vous suggère un groupe électrogène de {recommended_generator} kVA pour votre utilisation.")

        # Afficher les graphiques Plotly
        self.display_plotly_graphs(material_names, power_values)

    def get_power_values(self):
        return {
        "recommended_generator": self.recommended_generator,
        "total_power_w": self.total_power_w,
        "total_power_kva": self.total_power_kva
}

    def display_plotly_graphs(self, materials, power_values):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Créer un graphique à barres avec Plotly
        bar_fig = go.Figure([go.Bar(x=materials, y=power_values, marker_color='blue')])
        bar_fig.update_layout(title="Puissance des matériels", xaxis_title="Matériels", yaxis_title="Puissance (W)")

        # Créer un graphique circulaire
        pie_fig = go.Figure(go.Pie(labels=materials, values=power_values))

        # Convertir les figures Plotly en HTML
        bar_html = bar_fig.to_html(full_html=False)
        pie_html = pie_fig.to_html(full_html=False)

        # Afficher les graphiques dans Tkinter
        bar_widget = tk.Label(self.graph_frame, text="Bar Chart")
        bar_widget.grid(row=0, column=0, padx=5)
        pie_widget = tk.Label(self.graph_frame, text="Pie Chart")
        pie_widget.grid(row=0, column=1, padx=5)

        webbrowser.open_new(bar_html)
        webbrowser.open_new(pie_html)

    def export_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if not file_path:
            return
        
        try:
            data = []
            for row in self.entries:
                row_data = [entry.get() for entry in row]
                data.append(row_data)
            
            df = pd.DataFrame(data, columns=self.headers)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Succès", f"Le fichier a été exporté avec succès sous {file_path}.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'exportation: {str(e)}")

    def generate_pdf(self):
        # Création du PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Devis pour Groupe Électrogène - Lano Power", ln=True, align='C')

        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(100, 10, txt=f"Client: {self.client_name.get()}", ln=True)
        pdf.cell(100, 10, txt=f"Téléphone: {self.client_phone.get()}", ln=True)
        pdf.cell(100, 10, txt=f"Commercial: {self.salesperson_name.get()}", ln=True)
        pdf.cell(100, 10, txt=f"Date du Devis: {self.estimate_date.get()}", ln=True)

        # Ajout du tableau
        pdf.ln(10)
        pdf.set_font("Arial", size=10)
        pdf.cell(50, 10, "Matériel", border=1, align='C')
        pdf.cell(40, 10, "Puissance (W)", border=1, align='C')
        pdf.cell(30, 10, "Quantité", border=1, align='C')
        pdf.cell(50, 10, "Coefficient de Correction", border=1, align='C')
        pdf.ln()

#pdf.cell(200, 10, txt="Devis - Lano Power", ln=True, align='C')

        for row in self.entries:
            for entry in row:
                pdf.cell(50, 10, entry.get(), border=1, align='C')
            pdf.ln()

        pdf.cell(200, 10, txt=f"Puissance active des equipements :{self.total_power_w:.2f} W", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Puissance active des equipements :{self.total_power_kva:.2f} KVA", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Groupe electrogene correspondant:{self.recommended_generator:.2f} KVA ",ln=True, align='L')
        pdf.ln()
        
        # Enregistrer le fichier PDF
        pdf_output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if pdf_output_path:
            pdf.output(pdf_output_path)
            messagebox.showinfo("Succès", f"Le devis a été exporté avec succès sous {pdf_output_path}.")
        else:
            messagebox.showerror("Erreur", "Erreur lors de l'exportation du PDF.")

        #Ajoute une texte
        pdf.cell(200, 10, txt="Puissance des equipements : ", ln=True, align='L')
        pdf.cell(200, 10, txt=" Groupe electrogene correspondant : ", ln=True, align='L')
        pdf.ln()


# Création de la fenêtre principale Tkinter
root = tk.Tk()
app = ThinkerApp(root)
root.mainloop()
