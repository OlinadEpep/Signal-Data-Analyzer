import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import os
import platform
import subprocess
import pandas as pd
import sqlite3
import getpass  
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
from ttkthemes import ThemedTk
from zoneinfo import ZoneInfo
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import pysqlcipher3
import sys
import shutil 
import subprocess

import os
import subprocess
import shutil
import tkinter.messagebox as messagebox


import os
import subprocess
import shutil
import tkinter.messagebox as messagebox
import pathlib

def run_ex_sh(self=None):
    """
    Esegue uno script Bash su Windows utilizzando WSL, con percorsi specificati direttamente nel codice.
    """
    try:
        # Percorsi specificati direttamente
        percorso_script = r"C:\ex\ex.sh"
        percorso_esecuzione = r"C:\ex"

        # Converti i percorsi Windows in percorsi WSL
        percorso_script_wsl = percorso_script.replace("\\", "/").replace("C:", "/mnt/c")
        percorso_esecuzione_wsl = percorso_esecuzione.replace("\\", "/").replace("C:", "/mnt/c")

        # Costruisce il comando per WSL
        comando = ['wsl', 'bash', '-c', f"cd {percorso_esecuzione_wsl} && bash {percorso_script_wsl}"]

        # Esegue il comando
        risultato = subprocess.run(comando, capture_output=True, text=True, check=True)

        # Output
        print("Output:", risultato.stdout)
        print("Error:", risultato.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Errore nell'esecuzione dello script: {e}")
        print("Stdout:", e.stdout)
        print("Stderr:", e.stderr)
    except Exception as e:
        print(f"Errore generico: {e}")

class SignalDataAnalyzer:
    def __init__(self, master):
        self.master = master
        master.title("Signal Data Analyzer")
        
        # Imposta il tema e lo stile
        style = ttk.Style()
        style.configure("Main.TFrame", padding=20)
        style.configure("Header.TLabel", font=('Helvetica', 16, 'bold'))
        style.configure("SubHeader.TLabel", font=('Helvetica', 12))
        style.configure("Action.TButton", padding=10)
        
        # Container principale
        self.main_frame = ttk.Frame(master, style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.header = ttk.Label(header_frame, 
                              text="Signal Data Analyzer",
                              style="Header.TLabel")
        self.header.pack(side=tk.LEFT)
        
        # Frame per i pulsanti principali
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Stile personalizzato per i pulsanti
        style.configure("Action.TButton",
                       font=('Helvetica', 10),
                       padding=10)
        
        self.load_button = ttk.Button(button_frame,
                                    text="📂 Carica Dati",
                                    style="Action.TButton",
                                    command=self.load_data)
        self.load_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Notebook per le diverse visualizzazioni
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab per il conteggio messaggi
        self.messages_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.messages_frame, text="📊 Conteggio di messaggi per conversazione")
        
        # Tab per la timeline
        self.timeline_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.timeline_frame, text="📅 Timeline")
        
        # Tab per la word cloud
        self.wordcloud_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.wordcloud_frame, text="☁️ Word Cloud")
        
        # Tab per i messaggi
        self.all_messages_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.all_messages_frame, text="💬 Mostra tutti i messaggi")
        
        # Inizializza le visualizzazioni
        self.init_messages_view()
        self.init_timeline_view()
        self.init_wordcloud_view()
        self.init_all_messages_view()
        
        self.data = None
        self.conversation_dict = {}
        
        # Stato iniziale dei tab (disabilitati fino al caricamento dei dati)
        self.update_tab_states(False)

        # Aggiungi un pulsante per l'estrazione del database
        self.extract_button = ttk.Button(button_frame,
                                         text="📦 Estrai Database Signal",
                                         style="Action.TButton",
                                         command=self.run_ex_sh_script)
        self.extract_button.pack(side=tk.LEFT, padx=(10, 0))
    
    def run_ex_sh_script(self):
        """Wrapper for executing the ex.sh script"""
        try:
            run_ex_sh(self)  # Pass self as an argument
            messagebox.showinfo("Info", "Estrazione database eseguita. Controllare Downloads.")
        except Exception as e:
            messagebox.showerror("Error", f"Errore durante l'estrazione del database {e}")

    def update_tab_states(self, enabled=True):
        """Abilita/disabilita i tab basandosi sulla presenza dei dati"""
        state = "normal" if enabled else "disabled"
        for i in range(self.notebook.index("end")):
            self.notebook.tab(i, state=state)
    
    def init_messages_view(self):
        """Inizializza la vista delle statistiche dei messaggi"""
        frame = ttk.Frame(self.messages_frame, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.message_canvas = tk.Canvas(frame)
        self.message_canvas.pack(fill=tk.BOTH, expand=True)
    
    def init_timeline_view(self):
        """Inizializza la vista della timeline"""
        frame = ttk.Frame(self.timeline_frame, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.timeline_canvas = tk.Canvas(frame)
        self.timeline_canvas.pack(fill=tk.BOTH, expand=True)
    
    def init_wordcloud_view(self):
        """Inizializza la vista della word cloud"""
        frame = ttk.Frame(self.wordcloud_frame, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.wordcloud_canvas = tk.Canvas(frame)
        self.wordcloud_canvas.pack(fill=tk.BOTH, expand=True)
    
    def init_all_messages_view(self):
        """Inizializza la vista di tutti i messaggi"""
        # Frame per i controlli di ricerca
        search_frame = ttk.Frame(self.all_messages_frame, padding=10)
        search_frame.pack(fill=tk.X)
        
        # Stile per i controlli di ricerca
        controls_style = {'padx': 5, 'pady': 5}
        
        # Ricerca per testo
        search_box_frame = ttk.LabelFrame(search_frame, text="Filtri di Ricerca", padding=10)
        search_box_frame.pack(fill=tk.X, **controls_style)
        
        # Griglia per i controlli
        ttk.Label(search_box_frame, text="Testo:").grid(row=0, column=0, **controls_style)
        self.message_entry = ttk.Entry(search_box_frame)
        self.message_entry.grid(row=0, column=1, **controls_style)
        
        ttk.Label(search_box_frame, text="Conversazione:").grid(row=0, column=2, **controls_style)
        self.sender_combobox = ttk.Combobox(search_box_frame, width=20)
        self.sender_combobox.grid(row=0, column=3, **controls_style)
        
        ttk.Label(search_box_frame, text="Data:").grid(row=1, column=0, **controls_style)
        self.date_entry = ttk.Entry(search_box_frame)
        self.date_entry.insert(0, "YYYY-MM-DD")  # Aggiunge il placeholder
        self.date_entry.configure(foreground='gray')  # Colore grigio per il placeholder
        self.date_entry.grid(row=1, column=1, **controls_style)
        
        # Aggiungi gli eventi per gestire il placeholder
        self.date_entry.bind('<FocusIn>', self.on_date_entry_focus_in)
        self.date_entry.bind('<FocusOut>', self.on_date_entry_focus_out)
        
        ttk.Label(search_box_frame, text="Tipo:").grid(row=1, column=2, **controls_style)
        self.type_combobox = ttk.Combobox(search_box_frame, 
                                         values=["Tutti", "Inviati", "Ricevuti"],
                                         width=20)
        self.type_combobox.set("Tutti")
        self.type_combobox.grid(row=1, column=3, **controls_style)
        
        # Pulsanti di ricerca
        button_frame = ttk.Frame(search_box_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, 
                  text="🔍 Cerca",
                  command=lambda: self.filter_messages()).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame,
                  text="↺ Reset",
                  command=self.reset_search).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, 
                  text="📤 Esporta PDF",
                  command=self.export_to_pdf).pack(side=tk.LEFT, padx=5)

        self.sort_column = None
        self.sort_reverse = False
        
        self.tree = ttk.Treeview(self.all_messages_frame, 
                                columns=("conversazione", "messaggio", "data", "ora", "direzione"),
                                show='headings')
        
        # Modifica gli heading per aggiungere il comando di ordinamento
        self.tree.heading("conversazione", text="Conversazione", 
                        command=lambda: self.treeview_sort_column("conversazione"))
        self.tree.heading("messaggio", text="Messaggio", 
                        command=lambda: self.treeview_sort_column("messaggio"))
        self.tree.heading("data", text="Data", 
                        command=lambda: self.treeview_sort_column("data"))
        self.tree.heading("ora", text="Ora", 
                        command=lambda: self.treeview_sort_column("ora"))
        self.tree.heading("direzione", text="Tipo", 
                        command=lambda: self.treeview_sort_column("direzione"))
        
        # Tabella dei messaggi
        self.tree = ttk.Treeview(self.all_messages_frame, 
                                columns=("conversazione", "messaggio", "data", "ora", "direzione"),
                                show='headings')
        
        self.tree.heading("conversazione", text="Conversazione")
        self.tree.heading("messaggio", text="Messaggio")
        self.tree.heading("data", text="Data")
        self.tree.heading("ora", text="Ora")
        self.tree.heading("direzione", text="Tipo")
        
        # Configurazione colonne
        self.tree.column("conversazione", width=150)
        self.tree.column("messaggio", width=400)
        self.tree.column("data", width=100)
        self.tree.column("ora", width=100)
        self.tree.column("direzione", width=80, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.all_messages_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Pack
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

    def export_to_pdf(self):
            """Esporta i messaggi filtrati in un file PDF"""
            if not self.tree.get_children():
                messagebox.showwarning("Attenzione", "Nessun messaggio da esportare.")
                return
            
            file_path = filedialog.asksaveasfilename(
                title="Salva come PDF",
                defaultextension=".pdf",
                filetypes=[("File PDF", "*.pdf")]
            )

            if not file_path:
                return  # L'utente ha annullato il salvataggio
            
            try:
                # Creazione del documento PDF
                pdf = SimpleDocTemplate(file_path)
                elements = []

                # Creazione dei dati della tabella
                data = [["Conversazione", "Messaggio", "Data", "Ora", "Tipo"]]
                for item in self.tree.get_children():
                    values = self.tree.item(item, "values")
                    data.append(values)
                
                # Stile della tabella
                table = Table(data)
                style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ])
                table.setStyle(style)

                elements.append(table)

                # Genera il file PDF
                pdf.build(elements)

                messagebox.showinfo("Successo", "Conversazioni esportate con successo!")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'esportazione: {e}")

    def treeview_sort_column(self, col):
        """Ordina il treeview quando si clicca su una colonna"""
        if self.sort_column == col:
            # Se si clicca sulla stessa colonna, inverte l'ordine
            self.sort_reverse = not self.sort_reverse
        else:
            # Se si clicca su una nuova colonna, ordina in modo ascendente
            self.sort_reverse = False
        self.sort_column = col
        
        # Prende tutti gli item correnti
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        
        # Funzione per convertire le date nel formato corretto per l'ordinamento
        def convert_date(date_str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')
            except:
                return datetime.min
        
        # Ordina gli elementi in base al tipo di colonna
        if col == "data":
            l.sort(key=lambda x: convert_date(x[0]), reverse=self.sort_reverse)
        elif col == "ora":
            l.sort(key=lambda x: datetime.strptime(x[0], '%H:%M:%S'), reverse=self.sort_reverse)
        elif col == "fuso_orario":
            # Ordina i fusi orari mantenendo N/A in fondo
            l.sort(key=lambda x: (x[0] == 'N/A', x[0]), reverse=self.sort_reverse)
        else:
            l.sort(reverse=self.sort_reverse)
        
        # Riorganizza gli item nel treeview
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        
        # Aggiunge un indicatore visivo della direzione dell'ordinamento
        for col_name in self.tree["columns"]:
            if col_name == col:
                self.tree.heading(col_name, text=f"{self.tree.heading(col_name)['text']} {'↑' if not self.sort_reverse else '↓'}")
            else:
                # Rimuove l'indicatore dalle altre colonne
                self.tree.heading(col_name, text=self.tree.heading(col_name)['text'].replace(' ↑', '').replace(' ↓', ''))

    def on_date_entry_focus_in(self, event):
        """Gestisce l'evento di focus sull'input della data"""
        if self.date_entry.get() == "YYYY-MM-DD":
            self.date_entry.delete(0, tk.END)
            self.date_entry.configure(foreground='black')
    
    def on_date_entry_focus_out(self, event):
        """Gestisce l'evento di perdita del focus dall'input della data"""
        if not self.date_entry.get():
            self.date_entry.insert(0, "YYYY-MM-DD")
            self.date_entry.configure(foreground='gray')
    
    def load_data(self):
        file_path = filedialog.askopenfilename(
            title="Seleziona il file di dati Signal",
            filetypes=[("File CSV", "*.csv"), ("File di testo", "*.txt"), ("Tutti i file", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    lines = file.readlines()
                    messages_data = []
                    conversations_data = {}
                    
                    for line in lines:
                        if line.strip() == "ok":
                            continue
                            
                        if "|" in line:
                            try:
                                parts = line.split("|")
                                conv_id = parts[0]
                                conv_json = json.loads(parts[1])
                                
                                conv_info = {
                                    'id': conv_id,
                                    'profileName': conv_json.get('profileName', ''),
                                    'name': conv_json.get('name', ''),
                                    'systemGivenName': conv_json.get('systemGivenName', '')
                                }
                                conversations_data[conv_id] = conv_info
                            except:
                                continue
                        else:
                            try:
                                msg_data = json.loads(line)
                                messages_data.append(msg_data)
                            except:
                                continue
                    
                    self.data = pd.DataFrame(messages_data)
                    
                    self.conversation_dict = {}
                    for conv_id, conv_info in conversations_data.items():
                        name = conv_info['profileName'] or conv_info['name'] or conv_info['systemGivenName'] or "Sconosciuto"
                        self.conversation_dict[conv_id] = name
                    
                    if not self.data.empty:
                        self.update_tab_states(True)
                        self.update_all_views()
                        messagebox.showinfo("Successo", "Dati caricati con successo!")
                    else:
                        messagebox.showwarning("Attenzione", "Nessun dato valido trovato nel file.")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante il caricamento dei dati: {e}")
    
    def update_all_views(self):
        """Aggiorna tutte le visualizzazioni dopo il caricamento dei dati"""
        self.update_message_counts()
        self.update_time_distribution()
        self.update_wordcloud()
        self.update_message_list()
        
        # Aggiorna la lista delle conversazioni nel combobox
        senders = sorted(set(self.conversation_dict.values()))
        self.sender_combobox['values'] = senders
    
    def update_message_counts(self):
        """Aggiorna il grafico dei conteggi dei messaggi"""
        if self.data is not None:
            counts = self.data['conversationId'].value_counts()
            named_counts = {self.conversation_dict.get(conv_id, "Sconosciuto"): count 
                          for conv_id, count in counts.items()}
            
            fig = Figure(figsize=(8, 6))
            ax = fig.add_subplot(111)
            
            bars = ax.barh(list(named_counts.keys()), list(named_counts.values()))
            ax.set_title('Messaggi per Conversazione')
            ax.set_xlabel('Numero di Messaggi')
            
            # Aggiungi i valori sulle barre
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2,
                       f'{int(width)}',
                       ha='left', va='center', fontweight='bold')
            
            fig.tight_layout()
            
            # Aggiorna il canvas
            if hasattr(self, 'message_counts_canvas'):
                self.message_counts_canvas.get_tk_widget().destroy()
            
            self.message_counts_canvas = FigureCanvasTkAgg(fig, self.message_canvas)
            self.message_counts_canvas.draw()
            self.message_counts_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_time_distribution(self):
        """Aggiorna il grafico della distribuzione temporale"""
        if self.data is not None:
            data_copy = self.data.copy()
            data_copy['timestamp'] = pd.to_datetime(data_copy['timestamp'], unit='ms')
            daily_counts = data_copy.groupby(data_copy['timestamp'].dt.date).size()
            
            fig = Figure(figsize=(8, 6))
            ax = fig.add_subplot(111)
            
            ax.plot(daily_counts.index, daily_counts.values, 'b-', linewidth=2)
            ax.fill_between(daily_counts.index, daily_counts.values, alpha=0.3)
            
            ax.set_title('Distribuzione Temporale dei Messaggi')
            ax.set_xlabel('Data')
            ax.set_ylabel('Numero di Messaggi')
            
            # Rotazione delle date sull'asse x
            fig.autofmt_xdate()
            
            fig.tight_layout()
            
            # Aggiorna il canvas
            if hasattr(self, 'timeline_plot_canvas'):
                self.timeline_plot_canvas.get_tk_widget().destroy()
            
            self.timeline_plot_canvas = FigureCanvasTkAgg(fig, self.timeline_canvas)
            self.timeline_plot_canvas.draw()
            self.timeline_plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    

    def update_wordcloud(self):
        """Aggiorna la word cloud"""
        if self.data is not None:
            text = ' '.join(self.data['body'].dropna())
            wordcloud = WordCloud(width=800, 
                                height=400, 
                                background_color='white',
                                min_font_size=10,
                                max_font_size=50).generate(text)
            
            fig = Figure(figsize=(8, 6))
            ax = fig.add_subplot(111)
            
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            
            # Aggiorna il canvas
            if hasattr(self, 'wordcloud_plot_canvas'):
                self.wordcloud_plot_canvas.get_tk_widget().destroy()
            
            self.wordcloud_plot_canvas = FigureCanvasTkAgg(fig, self.wordcloud_canvas)
            self.wordcloud_plot_canvas.draw()
            self.wordcloud_plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_message_list(self):
        """Aggiorna la lista dei messaggi"""
        if self.data is not None:
            self.populate_treeview(self.data)

    def populate_treeview(self, data):
        """Popola la treeview con i dati filtrati"""
        # Pulisci la treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Modifica la definizione delle colonne per aggiungere il fuso orario
        self.tree["columns"] = ("conversazione", "messaggio", "data", "ora", "fuso_orario", "direzione")
        
        # Modifica gli heading
        self.tree.heading("conversazione", text="Conversazione")
        self.tree.heading("messaggio", text="Messaggio")
        self.tree.heading("data", text="Data")
        self.tree.heading("ora", text="Ora")
        self.tree.heading("fuso_orario", text="Fuso Orario")
        self.tree.heading("direzione", text="Tipo")
        
        # Configurazione colonne
        self.tree.column("conversazione", width=150)
        self.tree.column("messaggio", width=350)
        self.tree.column("data", width=100)
        self.tree.column("ora", width=80)
        self.tree.column("fuso_orario", width=80)
        self.tree.column("direzione", width=80, anchor="center")
        
        # Aggiungi le nuove righe
        for index, row in data.iterrows():
            timestamp = pd.to_datetime(row['timestamp'], unit='ms')
            
            # Imposta il fuso orario di Roma come predefinito se non riconosciuto
            if timestamp.tzinfo is None:
                from zoneinfo import ZoneInfo
                timestamp = timestamp.replace(tzinfo=ZoneInfo("Europe/Rome"))
            
            date = timestamp.strftime('%Y-%m-%d')  # Modifica il formato della data per l'ordinamento
            time = timestamp.strftime('%H:%M:%S')
            
            # Ottieni il fuso orario formattato
            timezone = timestamp.strftime('%z')
            if timezone:
                timezone = f"{timezone[:3]}:{timezone[3:]}"  # Aggiungi : tra ore e minuti
            else:
                timezone = "+02:00"  # Default per Roma se non riconosciuto
            
            profile_name = self.conversation_dict.get(row['conversationId'], "Sconosciuto")
            direction = "↑ Inviato" if row['type'] == 'outgoing' else "↓ Ricevuto"
            
            item = self.tree.insert("", "end", values=(profile_name, 
                                                    row['body'], 
                                                    date, 
                                                    time,
                                                    timezone,
                                                    direction))
            
            if row['type'] == 'outgoing':
                self.tree.tag_configure('outgoing', background='#e8f4f9')
                self.tree.item(item, tags=('outgoing',))
        
        # Se c'era un ordinamento attivo, riapplicalo
        if self.sort_column:
            self.treeview_sort_column(self.sort_column)
    
    def filter_messages(self):
        """Filtra i messaggi in base ai criteri di ricerca"""
        if self.data is not None:
            filtered_data = self.data.copy()
            
            # Filtra per testo del messaggio
            message_text = self.message_entry.get()
            if message_text:
                filtered_data = filtered_data[filtered_data['body'].str.contains(
                    message_text, case=False, na=False)]
            
            # Filtra per mittente
            sender = self.sender_combobox.get()
            if sender:
                sender_mask = filtered_data['conversationId'].map(
                    lambda x: self.conversation_dict.get(x, "Sconosciuto") == sender)
                filtered_data = filtered_data[sender_mask]
            
            # Filtra per data
            date = self.date_entry.get()
            if date:
                try:
                    search_date = datetime.strptime(date, '%Y-%m-%d').date()
                    date_mask = pd.to_datetime(filtered_data['timestamp'], 
                                             unit='ms').dt.date == search_date
                    filtered_data = filtered_data[date_mask]
                except ValueError:
                    messagebox.showwarning("Attenzione", 
                                         "Formato data non valido. Usa YYYY-MM-DD")
            
            # Filtra per tipo di messaggio
            message_type = self.type_combobox.get()
            if message_type == "Inviati":
                filtered_data = filtered_data[filtered_data['type'] == 'outgoing']
            elif message_type == "Ricevuti":
                filtered_data = filtered_data[filtered_data['type'] == 'incoming']
            
            # Aggiorna la visualizzazione
            self.populate_treeview(filtered_data)
    
    def reset_search(self):
        """Resetta tutti i filtri di ricerca"""
        self.message_entry.delete(0, tk.END)
        self.sender_combobox.set('')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, "YYYY-MM-DD")  # Ripristina il placeholder
        self.date_entry.configure(foreground='gray')  # Ripristina il colore grigio
        self.type_combobox.set("Tutti")
        
        # Ripopola la tabella con tutti i dati
        if self.data is not None:
            self.populate_treeview(self.data)

def main():
    # Imposta il tema
    root = ThemedTk(theme="arc")
    root.title("Signal Data Analyzer")
    
    # Imposta l'icona della finestra
    try:
        icon_path = r"C:\Users\peppe\OneDrive - Università degli Studi di Bari\da ordinare\Desktop\for\tentativo con nuovo .txt\icona.ico"
        # Verifica se il file è un'immagine ICO
        if icon_path.lower().endswith('.ico'):
            root.iconbitmap(icon_path)
        else:
            # Se non è un file ICO, converte l'immagine in un formato compatibile
            from PIL import Image, ImageTk
            icon = Image.open(icon_path)
            # Converti l'immagine in formato ICO in memoria
            icon_photo = ImageTk.PhotoImage(icon)
            root.iconphoto(True, icon_photo)
    except Exception as e:
        print(f"Errore nel caricamento dell'icona: {e}")
        # Continua l'esecuzione anche se c'è un errore con l'icona
    
    # Imposta la dimensione minima della finestra
    root.minsize(800, 600)
    
    # Centra la finestra sullo schermo
    window_width = 1024
    window_height = 768
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Crea l'applicazione
    app = SignalDataAnalyzer(root)
    
    # Avvia il loop principale
    root.mainloop()

if __name__ == "__main__":
    main()
