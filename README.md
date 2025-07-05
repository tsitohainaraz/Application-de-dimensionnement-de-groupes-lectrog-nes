
# 💡 Lano Power Design

**Application de dimensionnement de groupes électrogènes**, développée avec `Tkinter`, `Plotly`, `Pandas` et `FPDF`. Cette interface permet d'estimer la puissance totale d'une installation, de recommander un groupe électrogène adapté, et de générer des rapports en Excel et PDF.

---

## 📦 Fonctionnalités

- Interface utilisateur graphique (GUI) intuitive avec `Tkinter`
- Calcul automatique de la puissance totale corrigée
- Recommandation du groupe électrogène adéquat
- Visualisation graphique des consommations avec `Plotly`
- Ouverture des fiches techniques PDF
- Export des données en **Excel** et **PDF**

---

## 🧰 Technologies utilisées

- Python 3
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/python/)
- [Pillow (PIL)](https://python-pillow.org/)
- [FPDF](https://py-pdf.github.io/fpdf2/)
- [Webbrowser](https://docs.python.org/3/library/webbrowser.html)
- Standard libraries (`os`, `datetime`)

---

## 📁 Arborescence du projet

```
.
├── main.py                  # Code principal
├── README.md                # Ce fichier
├── requirements.txt         # Dépendances Python
├── solar.jpg                # Logo affiché dans l'interface
├── 8kVA.pdf                 # Exemple de fiche technique
├── 10kVA.pdf
├── ...
└── (autres fichiers PDF de fiches techniques)
```

---

## ⚙️ Installation

1. **Cloner le dépôt ou copier les fichiers** :

```bash
git clone <URL_DU_DEPOT>
cd lano-power-design
```

2. **Créer un environnement virtuel (optionnel mais recommandé)** :

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. **Installer les dépendances** :

```bash
pip install -r requirements.txt
```

> Si tu n’as pas de `requirements.txt`, tu peux le créer avec ce contenu :

```txt
tk
pandas
plotly
fpdf
Pillow
```

---

## 🚀 Utilisation

Lance simplement le script principal :

```bash
python main.py
```

Ensuite, une fenêtre graphique s’ouvrira. Tu pourras :

- Entrer les informations client
- Ajouter les matériels avec leur puissance, nombre et coefficient
- Calculer la puissance totale
- Visualiser les résultats
- Télécharger les fiches techniques
- Exporter les résultats en PDF ou Excel

## 📌 Remarques importantes

- Les fichiers PDF des fiches techniques doivent être nommés exactement comme ceci : `8kVA.pdf`, `10kVA.pdf`, etc., et placés dans le **même dossier que le script**.
- L’image `solar.jpg` est utilisée comme logo en haut de l’application. Tu peux la remplacer par ton propre logo.

## 📧 Contact

Développé par **Razafindrajoa Tsitohaina **  
📫 rztsitohaina@gmail.com

![Aperçu de l’application](APK.jpg)
+2610388103083
