#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Diva mod_pv_db.txt Generator GUI
Generates mod_pv_db.txt files for Project Diva song packs with GUI interface
"""

import os
import time
import glob
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class SongVariantDialog:
    def __init__(self, parent, variant_data=None):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configure Audio Variant")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Variables
        self.name_var = tk.StringVar(value=variant_data.get('name', '') if variant_data else '')
        self.name_en_var = tk.StringVar(value=variant_data.get('name_en', '') if variant_data else '')
        self.name_en2_var = tk.StringVar(value=variant_data.get('name_en2', '') if variant_data else '')
        self.name_ro_var = tk.StringVar(value=variant_data.get('name_ro', '') if variant_data else '')
        self.vocal_disp_var = tk.StringVar(value=variant_data.get('vocal_disp', '') if variant_data else '')
        self.vocal_disp_en_var = tk.StringVar(value=variant_data.get('vocal_disp_en', '') if variant_data else '')
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        ttk.Label(main_frame, text="Configure Audio Variant", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Fields
        fields = [
            ("Variant name:", self.name_var),
            ("English name:", self.name_en_var),
            ("Alternative English name:", self.name_en2_var),
            ("Romanized name:", self.name_ro_var),
            ("Variant artist:", self.vocal_disp_var),
            ("Artist in English:", self.vocal_disp_en_var)
        ]
        
        for i, (label, var) in enumerate(fields, 1):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            ttk.Entry(main_frame, textvariable=var, width=40).grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Accept", command=self.accept).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
        
        # Configure grid
        main_frame.columnconfigure(1, weight=1)
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        
    def accept(self):
        self.result = {
            'name': self.name_var.get().strip(),
            'name_en': self.name_en_var.get().strip(),
            'name_en2': self.name_en2_var.get().strip(),
            'name_ro': self.name_ro_var.get().strip(),
            'vocal_disp': self.vocal_disp_var.get().strip(),
            'vocal_disp_en': self.vocal_disp_en_var.get().strip()
        }
        self.dialog.destroy()
        
    def cancel(self):
        self.result = None
        self.dialog.destroy()

class SongConfigDialog:
    def __init__(self, parent, song_data=None):
        self.result = None
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configure Song")
        self.dialog.geometry("800x900")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Basic variables
        self.pv_id_var = tk.StringVar(value=song_data.get('pv_id', '') if song_data else '')
        self.song_name_var = tk.StringVar(value=song_data.get('song_name', '') if song_data else '')
        self.song_name_en_var = tk.StringVar(value=song_data.get('song_name_en', '') if song_data else '')
        self.song_name_en2_var = tk.StringVar(value=song_data.get('song_name_en2', '') if song_data else '')
        self.song_name_reading_var = tk.StringVar(value=song_data.get('song_name_reading', '') if song_data else '')
        self.song_name_ro_var = tk.StringVar(value=song_data.get('song_name_ro', '') if song_data else '')
        self.bpm_var = tk.StringVar(value=song_data.get('bpm', '') if song_data else '')
        self.date_var = tk.StringVar(value=song_data.get('date', '') if song_data else '')
        self.sabi_start_var = tk.StringVar(value=song_data.get('sabi_start', '') if song_data else '')
        self.sabi_play_var = tk.StringVar(value=song_data.get('sabi_play', '') if song_data else '')
        
        # Difficulty variables
        self.difficulties = {}
        if song_data and 'difficulties' in song_data:
            self.difficulties = song_data['difficulties'].copy()
        
        # Performer variables
        self.performers = song_data.get('performers', ['MIK']) if song_data else ['MIK']
        
        # Songinfo variables
        self.songinfo = song_data.get('songinfo', {}) if song_data else {}
        
        # Audio variant variables
        self.audio_variants = song_data.get('audio_variants', []) if song_data else []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.dialog)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Basic information tab
        self.create_basic_tab()
        
        # Difficulties tab
        self.create_difficulty_tab()
        
        # Performers tab
        self.create_performers_tab()
        
        # Songinfo tab
        self.create_songinfo_tab()
        
        # Audio variants tab
        self.create_variants_tab()
        
        # Main buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="Accept", command=self.accept).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)
        
    def create_basic_tab(self):
        basic_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(basic_frame, text="Basic Information")
        
        # Basic song information
        fields = [
            ("PV ID:", self.pv_id_var),
            ("Original name:", self.song_name_var),
            ("English name:", self.song_name_en_var),
            ("Alternative English name:", self.song_name_en2_var),
            ("Hiragana name:", self.song_name_reading_var),
            ("Romanized name:", self.song_name_ro_var),
            ("BPM:", self.bpm_var),
            ("Date (YYYYMMDD):", self.date_var),
            ("Sabi start time:", self.sabi_start_var),
            ("Sabi duration:", self.sabi_play_var)
        ]
        
        for i, (label, var) in enumerate(fields):
            ttk.Label(basic_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            ttk.Entry(basic_frame, textvariable=var, width=40).grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        basic_frame.columnconfigure(1, weight=1)
        
    def create_difficulty_tab(self):
        diff_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(diff_frame, text="Difficulties")
        
        # Difficulty checkbox variables
        self.easy_var = tk.BooleanVar(value='easy' in self.difficulties)
        self.normal_var = tk.BooleanVar(value='normal' in self.difficulties)
        self.hard_var = tk.BooleanVar(value='hard' in self.difficulties)
        self.extreme_var = tk.BooleanVar(value='extreme' in self.difficulties)
        self.extreme_extra_var = tk.BooleanVar(value='extreme_extra' in self.difficulties)
        
        # Level variables
        self.easy_level_var = tk.StringVar(value=self.difficulties.get('easy', {}).get('level', 'PV_LV_03_0'))
        self.normal_level_var = tk.StringVar(value=self.difficulties.get('normal', {}).get('level', 'PV_LV_05_5'))
        self.hard_level_var = tk.StringVar(value=self.difficulties.get('hard', {}).get('level', 'PV_LV_08_0'))
        self.extreme_level_var = tk.StringVar(value=self.difficulties.get('extreme', {}).get('level', 'PV_LV_08_5'))
        self.extreme_extra_level_var = tk.StringVar(value=self.difficulties.get('extreme_extra', {}).get('level', 'PV_LV_09_5'))
        
        difficulties = [
            ("Easy", self.easy_var, self.easy_level_var),
            ("Normal", self.normal_var, self.normal_level_var),
            ("Hard", self.hard_var, self.hard_level_var),
            ("Extreme", self.extreme_var, self.extreme_level_var),
            ("Extra Extreme", self.extreme_extra_var, self.extreme_extra_level_var)
        ]
        
        for i, (name, var, level_var) in enumerate(difficulties):
            ttk.Checkbutton(diff_frame, text=name, variable=var).grid(row=i, column=0, sticky=tk.W, pady=2)
            ttk.Label(diff_frame, text="Level:").grid(row=i, column=1, sticky=tk.W, padx=(20, 5))
            ttk.Entry(diff_frame, textvariable=level_var, width=15).grid(row=i, column=2, sticky=tk.W)
        
    def create_performers_tab(self):
        perf_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(perf_frame, text="Performers")
        
        # Performer list
        ttk.Label(perf_frame, text="Selected performers:").pack(anchor=tk.W)
        
        self.performers_listbox = tk.Listbox(perf_frame, height=6)
        self.performers_listbox.pack(fill='x', pady=(5, 10))
        
        # Performer management buttons
        perf_buttons = ttk.Frame(perf_frame)
        perf_buttons.pack(fill='x')
        
        ttk.Button(perf_buttons, text="Add", command=self.add_performer).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(perf_buttons, text="Remove", command=self.remove_performer).pack(side=tk.LEFT)
        
        # Character selection dropdown
        ttk.Label(perf_frame, text="Select character:").pack(anchor=tk.W, pady=(20, 5))
        
        self.characters = {
            'MIK': 'Hatsune Miku',
            'RIN': 'Kagamine Rin',
            'LEN': 'Kagamine Len',
            'LUK': 'Megurine Luka',
            'KAI': 'KAITO',
            'MEI': 'MEIKO',
            'HAK': 'Yowane Haku',
            'NER': 'Akita Neru',
            'SAK': 'Sakine Meiko',
            'TET': 'Kasane Teto'
        }
        
        self.character_var = tk.StringVar(value='MIK')
        char_combo = ttk.Combobox(perf_frame, textvariable=self.character_var, width=30)
        char_combo['values'] = [f"{code} - {name}" for code, name in self.characters.items()]
        char_combo.pack(fill='x')
        
        self.update_performers_display()
        
    def create_songinfo_tab(self):
        info_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(info_frame, text="Song Information")

        # Songinfo variables (Spanish and English)
        self.songinfo_vars = {}
        fields = ['arranger', 'guitar_player', 'lyrics', 'manipulator', 'music', 'pv_editor']

        # Create variables for Spanish version
        for field in fields:
            self.songinfo_vars[field] = tk.StringVar(value=self.songinfo.get(field, ''))

        # Create variables for English version
        for field in fields:
            field_en = field + '_en'
            self.songinfo_vars[field_en] = tk.StringVar(value=self.songinfo.get(field_en, ''))

        labels = {
            'arranger': 'Arranger:',
            'guitar_player': 'Guitar Player:',
            'lyrics': 'Lyricist:',
            'manipulator': 'Manipulator:',
            'music': 'Composer/Artist:',
            'pv_editor': 'PV Editor:'
        }

        labels_en = {
            'arranger_en': 'Arranger (EN):',
            'guitar_player_en': 'Guitar Player (EN):',
            'lyrics_en': 'Lyricist (EN):',
            'manipulator_en': 'Manipulator (EN):',
            'music_en': 'Composer/Artist (EN):',
            'pv_editor_en': 'PV Editor (EN):'
        }

        row = 0

        # Create fields for original version
        ttk.Label(info_frame, text="Original", font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        row += 1

        for field in fields:
            ttk.Label(info_frame, text=labels[field]).grid(row=row, column=0, sticky=tk.W, pady=2)
            ttk.Entry(info_frame, textvariable=self.songinfo_vars[field], width=40).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
            row += 1

        # Separator
        ttk.Separator(info_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1

        # Create fields for English version
        ttk.Label(info_frame, text="English", font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        row += 1

        for field in fields:
            field_en = field + '_en'
            ttk.Label(info_frame, text=labels_en[field_en]).grid(row=row, column=0, sticky=tk.W, pady=2)
            ttk.Entry(info_frame, textvariable=self.songinfo_vars[field_en], width=40).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
            row += 1

        info_frame.columnconfigure(1, weight=1)
        
    def create_variants_tab(self):
        variants_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(variants_frame, text="Audio Variants")
        
        ttk.Label(variants_frame, text="Configured audio variants:").pack(anchor=tk.W)
        
        # Variants list
        self.variants_tree = ttk.Treeview(variants_frame, columns=('name', 'name_en', 'artist'), show='headings', height=8)
        self.variants_tree.heading('name', text='Original Name')
        self.variants_tree.heading('name_en', text='English Name')
        self.variants_tree.heading('artist', text='Artist')
        self.variants_tree.pack(fill='both', expand=True, pady=(5, 10))
        
        # Variant buttons
        variants_buttons = ttk.Frame(variants_frame)
        variants_buttons.pack(fill='x')
        
        ttk.Button(variants_buttons, text="Add Variant", command=self.add_variant).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(variants_buttons, text="Edit Variant", command=self.edit_variant).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(variants_buttons, text="Remove Variant", command=self.remove_variant).pack(side=tk.LEFT)
        
        self.update_variants_display()
        
    def update_performers_display(self):
        self.performers_listbox.delete(0, tk.END)
        for performer in self.performers:
            char_name = self.characters.get(performer, performer)
            self.performers_listbox.insert(tk.END, f"{performer} - {char_name}")
    
    def add_performer(self):
        selected = self.character_var.get().split(' - ')[0]
        if selected not in self.performers:
            self.performers.append(selected)
            self.update_performers_display()
    
    def remove_performer(self):
        selection = self.performers_listbox.curselection()
        if selection:
            index = selection[0]
            del self.performers[index]
            self.update_performers_display()
    
    def update_variants_display(self):
        for item in self.variants_tree.get_children():
            self.variants_tree.delete(item)
        
        for i, variant in enumerate(self.audio_variants):
            self.variants_tree.insert('', 'end', values=(
                variant.get('name', ''),
                variant.get('name_en', ''),
                variant.get('vocal_disp', '')
            ))
    
    def add_variant(self):
        dialog = SongVariantDialog(self.dialog)
        self.dialog.wait_window(dialog.dialog)
        
        if dialog.result:
            self.audio_variants.append(dialog.result)
            self.update_variants_display()
    
    def edit_variant(self):
        selection = self.variants_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a variant to edit")
            return
        
        item = selection[0]
        index = self.variants_tree.index(item)
        
        dialog = SongVariantDialog(self.dialog, self.audio_variants[index])
        self.dialog.wait_window(dialog.dialog)
        
        if dialog.result:
            self.audio_variants[index] = dialog.result
            self.update_variants_display()
    
    def remove_variant(self):
        selection = self.variants_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a variant to remove")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this variant?"):
            item = selection[0]
            index = self.variants_tree.index(item)
            del self.audio_variants[index]
            self.update_variants_display()
    
    def accept(self):
        # Validate required fields
        if not self.pv_id_var.get().strip():
            messagebox.showerror("Error", "PV ID is required")
            return
        
        # Collect difficulties
        difficulties = {}
        if self.easy_var.get():
            difficulties['easy'] = {'level': self.easy_level_var.get(), 'level_sort_index': '50'}
        if self.normal_var.get():
            difficulties['normal'] = {'level': self.normal_level_var.get(), 'level_sort_index': '50'}
        if self.hard_var.get():
            difficulties['hard'] = {'level': self.hard_level_var.get(), 'level_sort_index': '80'}
        if self.extreme_var.get():
            difficulties['extreme'] = {'level': self.extreme_level_var.get(), 'level_sort_index': '20'}
        if self.extreme_extra_var.get():
            difficulties['extreme_extra'] = {'level': self.extreme_extra_level_var.get(), 'level_sort_index': '50'}
        
        # Collect songinfo
        songinfo = {}
        for field, var in self.songinfo_vars.items():
            value = var.get().strip()
            if value:
                songinfo[field] = value
        
        self.result = {
            'pv_id': self.pv_id_var.get().strip(),
            'song_name': self.song_name_var.get().strip(),
            'song_name_en': self.song_name_en_var.get().strip(),
            'song_name_en2': self.song_name_en2_var.get().strip(),
            'song_name_reading': self.song_name_reading_var.get().strip(),
            'song_name_ro': self.song_name_ro_var.get().strip(),
            'bpm': self.bpm_var.get().strip(),
            'date': self.date_var.get().strip(),
            'sabi_start': self.sabi_start_var.get().strip(),
            'sabi_play': self.sabi_play_var.get().strip(),
            'difficulties': difficulties,
            'performers': self.performers,
            'songinfo': songinfo,
            'audio_variants': self.audio_variants
        }
        
        self.dialog.destroy()
    
    def cancel(self):
        self.result = None
        self.dialog.destroy()

class ProjectDivaModEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MikuMikuDB Editor")
        self.root.geometry("900x700")
        self.set_icon()
        
        # Data
        self.pack_name = ""
        self.pack_name_jp = ""
        self.songs = []

        # Configurar autoguardado
        self.setup_autosave()

        self.create_widgets()

    def setup_autosave(self):
        """Set up the autosave system"""
        self.autosave_folder = "Autosaves"
        self.autosave_interval = 5 * 60 * 1000  # 5 minutos en milisegundos
        self.max_autosave_files = 60

        # Crear carpeta de autoguardado si no existe
        if not os.path.exists(self.autosave_folder):
            os.makedirs(self.autosave_folder)

        # Iniciar el timer de autoguardado
        self.schedule_autosave()

    def schedule_autosave(self):
        """Schedule the next autosave"""
        self.root.after(self.autosave_interval, self.autosave)

    def autosave(self):
        """Perform automatic autosave"""
        try:
            # Solo autoguardar si hay datos para guardar
            if self.songs or self.pack_name_var.get().strip():
                # Generar nombre de archivo con timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H_%M_%S")
                filename = os.path.join(self.autosave_folder, f"autosave_{timestamp}.pdpack")

                # Preparar configuración
                config = {
                    'pack_name': self.pack_name_var.get(),
                    'pack_name_jp': self.pack_name_jp_var.get(),
                    'songs': self.songs
                }

                # Guardar archivo
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)

                # Limpiar archivos viejos si es necesario
                self.cleanup_old_autosaves()

                print(f"Autosave done: {filename}")

        except Exception as e:
            print(f"Autosave error: {str(e)}")

        finally:
            # Programar el siguiente autoguardado
            self.schedule_autosave()

    def cleanup_old_autosaves(self):
        """Delete old autosave files if the limit is exceeded"""
        try:
            # Obtener todos los archivos de autoguardado
            pattern = os.path.join(self.autosave_folder, "autosave_*.pdpack")
            autosave_files = glob.glob(pattern)

            # Si hay más archivos que el límite permitido
            if len(autosave_files) > self.max_autosave_files:
                # Ordenar por fecha de modificación (más viejo primero)
                autosave_files.sort(key=os.path.getmtime)

                # Calcular cuántos archivos eliminar
                files_to_remove = len(autosave_files) - self.max_autosave_files

                # Eliminar los archivos más viejos
                for i in range(files_to_remove):
                    os.remove(autosave_files[i])
                    print(f"Autosave file removed: {autosave_files[i]}")

        except Exception as e:
            print(f"Error clearing autosaves: {str(e)}")

    def set_icon(self):
        try:
            self.root.iconbitmap("icon.ico")
        except Exception as e:
            print("Error setting iconbitmap:", e)
        
    def create_widgets(self):
        # Main title
        title_label = ttk.Label(self.root, text="MikuMikuDB Editor", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Pack information frame
        pack_frame = ttk.LabelFrame(self.root, text="Song Pack Information", padding="10")
        pack_frame.pack(fill='x', padx=10, pady=5)
        
        # Pack name
        ttk.Label(pack_frame, text="Song Pack Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.pack_name_var = tk.StringVar()
        ttk.Entry(pack_frame, textvariable=self.pack_name_var, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        ttk.Label(pack_frame, text="Japanese name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.pack_name_jp_var = tk.StringVar()
        ttk.Entry(pack_frame, textvariable=self.pack_name_jp_var, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        pack_frame.columnconfigure(1, weight=1)
        
        # Songs frame
        songs_frame = ttk.LabelFrame(self.root, text="Songs", padding="10")
        songs_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Song list
        self.songs_tree = ttk.Treeview(songs_frame, columns=('id', 'name', 'name_en'), show='headings', height=15)
        self.songs_tree.heading('id', text='PV ID')
        self.songs_tree.heading('name', text='Original Name')
        self.songs_tree.heading('name_en', text='English Name')
        
        self.songs_tree.column('id', width=80)
        self.songs_tree.column('name', width=300)
        self.songs_tree.column('name_en', width=300)
        
        scrollbar = ttk.Scrollbar(songs_frame, orient='vertical', command=self.songs_tree.yview)
        self.songs_tree.configure(yscrollcommand=scrollbar.set)
        
        self.songs_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Song buttons
        songs_buttons = ttk.Frame(self.root)
        songs_buttons.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(songs_buttons, text="Add Song", command=self.add_song).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(songs_buttons, text="Edit Song", command=self.edit_song).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(songs_buttons, text="Delete Song", command=self.delete_song).pack(side=tk.LEFT, padx=(0, 5))
        
        # Main buttons
        main_buttons = ttk.Frame(self.root)
        main_buttons.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(main_buttons, text="Generate File", command=self.generate_file).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(main_buttons, text="Load Configuration", command=self.load_config).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(main_buttons, text="Load Autosave", command=self.load_autosave).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(main_buttons, text="Save Configuration", command=self.save_config).pack(side=tk.RIGHT, padx=(10, 0))
        
    def update_songs_display(self):
        for item in self.songs_tree.get_children():
            self.songs_tree.delete(item)
        
        for song in self.songs:
            self.songs_tree.insert('', 'end', values=(
                song.get('pv_id', ''),
                song.get('song_name', ''),
                song.get('song_name_en', '')
            ))
    
    def add_song(self):
        dialog = SongConfigDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.songs.append(dialog.result)
            self.update_songs_display()
    
    def edit_song(self):
        selection = self.songs_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a song to edit")
            return
        
        item = selection[0]
        index = self.songs_tree.index(item)
        
        dialog = SongConfigDialog(self.root, self.songs[index])
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.songs[index] = dialog.result
            self.update_songs_display()
    
    def delete_song(self):
        selection = self.songs_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a song to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this song?"):
            item = selection[0]
            index = self.songs_tree.index(item)
            del self.songs[index]
            self.update_songs_display()
    
    def generate_file(self):
        if not self.pack_name_var.get().strip():
            messagebox.showerror("Error", "Enter the Song Pack name")
            return

        if not self.songs:
            messagebox.showerror("Error", "Add at least one song")
            return

        # Generate file content
        content = self.generate_file_content()

        # Save file
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="mod_pv_db.txt"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"File generated successfully: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {str(e)}")
    
    def generate_file_content(self):
        content = []
        
        # Header
        content.append("# Generated by MikuMikuDB Editor")
        content.append("# Created by NyxC")
        content.append("")

        content.append(f"#" + "-" * 30)
        pack_name_jp = self.pack_name_jp_var.get().strip() or self.pack_name_var.get().strip()
        content.append(f"# {self.pack_name_var.get()} Additional Charts")
        content.append("#")
        
        # Song list
        for song in self.songs:
            song_line = f"# pv_{song['pv_id']}\t{song['song_name']}"
            if song['song_name_en']:
                song_line += f" | {song['song_name_en']}"
            content.append(song_line)
        
        content.append("#" + "-" * 30)
        content.append("")
        
        # Generate each song
        for i, song in enumerate(self.songs):
            if i > 0:
                content.append("")  # Empty line between songs
            
            pv_id = song['pv_id']
            
            # Audio variants (if any)
            if song.get('audio_variants'):
                # Original song variant (index 0)
                content.extend([
                    f"pv_{pv_id}.another_song.0.name={song['song_name']}",
                    f"pv_{pv_id}.another_song.0.name_en={song['song_name_en']}",
                ])
                if song['song_name_en2']:
                    content.append(f"pv_{pv_id}.another_song.0.name_en2={song['song_name_en2']}")
                content.append(f"pv_{pv_id}.another_song.0.name_ro={song['song_name_ro']}")
                content.append(f"pv_{pv_id}.another_song.0.vocal_chara_num={song['performers'][0] if song['performers'] else 'MIK'}")
                
                # Additional variants
                for j, variant in enumerate(song['audio_variants'], 1):
                    content.extend([
                        f"pv_{pv_id}.another_song.{j}.name={variant['name']}",
                        f"pv_{pv_id}.another_song.{j}.name_en={variant['name_en']}"
                    ])
                    if variant['name_en2']:
                        content.append(f"pv_{pv_id}.another_song.{j}.name_en2={variant['name_en2']}")
                    content.extend([
                        f"pv_{pv_id}.another_song.{j}.name_ro={variant['name_ro']}",
                        f"pv_{pv_id}.another_song.{j}.song_file_name=rom/sound/song/pv_{pv_id}_{j}.ogg"
                    ])
                    if variant['vocal_disp']:
                        content.append(f"pv_{pv_id}.another_song.{j}.vocal_disp_name={variant['vocal_disp']}")
                    if variant['vocal_disp_en']:
                        content.append(f"pv_{pv_id}.another_song.{j}.vocal_disp_name_en={variant['vocal_disp_en']}")
                
                content.append(f"pv_{pv_id}.another_song.length={len(song['audio_variants']) + 1}")
            
            # Basic song info
            content.extend([
                f"pv_{pv_id}.bpm={song['bpm']}",
                f"pv_{pv_id}.chainslide_failure_name=slideng03",
                f"pv_{pv_id}.chainslide_first_name=slidelong02a",
                f"pv_{pv_id}.chainslide_sub_name=slidebutton08",
                f"pv_{pv_id}.chainslide_success_name=slideok03",
                f"pv_{pv_id}.date={song['date']}"
            ])
            
            # Difficulties
            difficulties = song.get('difficulties', {})
            
            # Easy
            if 'easy' in difficulties:
                content.extend([
                    f"pv_{pv_id}.difficulty.easy.0.edition=0",
                    f"pv_{pv_id}.difficulty.easy.0.level={difficulties['easy']['level']}",
                    f"pv_{pv_id}.difficulty.easy.0.level_sortindex={difficulties['easy']['level_sort_index']}",
                    f"pv_{pv_id}.difficulty.easy.0.script_filename=rom/script/pv_{pv_id}_easy.dsc",
                    f"pv_{pv_id}.difficulty.easy.0.scriptformat=0x15122517",
                    f"pv_{pv_id}.difficulty.easy.0.version=1",
                    f"pv_{pv_id}.difficulty.easy.length=1"
                ])
            else:
                content.append(f"pv_{pv_id}.difficulty.easy.length=0")
            
            # Extreme
            extreme_count = 0
            if 'extreme' in difficulties:
                content.extend([
                    f"pv_{pv_id}.difficulty.extreme.0.edition=0",
                    f"pv_{pv_id}.difficulty.extreme.0.level={difficulties['extreme']['level']}",
                    f"pv_{pv_id}.difficulty.extreme.0.level_sortindex={difficulties['extreme']['level_sort_index']}",
                    f"pv_{pv_id}.difficulty.extreme.0.script_filename=rom/script/pv_{pv_id}_extreme.dsc",
                    f"pv_{pv_id}.difficulty.extreme.0.scriptformat=0x15122517",
                    f"pv_{pv_id}.difficulty.extreme.0.version=1"
                ])
                extreme_count += 1
            
            if 'extreme_extra' in difficulties:
                content.extend([
                    f"pv_{pv_id}.difficulty.extreme.{extreme_count}.attribute.extra=1",
                    f"pv_{pv_id}.difficulty.extreme.{extreme_count}.attribute.original=0",
                    f"pv_{pv_id}.difficulty.extreme.{extreme_count}.edition=1",
                    f"pv_{pv_id}.difficulty.extreme.{extreme_count}.level={difficulties['extreme_extra']['level']}",
                    f"pv_{pv_id}.difficulty.extreme.{extreme_count}.level_sortindex={difficulties['extreme_extra']['level_sort_index']}",
                    f"pv_{pv_id}.difficulty.extreme.{extreme_count}.script_filename=rom/script/pv_{pv_id}_extreme{extreme_count}.dsc",
                    f"pv_{pv_id}.difficulty.extreme.{extreme_count}.scriptformat=0x15122517",
                    f"pv_{pv_id}.difficulty.extreme.{extreme_count}.version=1"
                ])
                extreme_count += 1
            
            content.append(f"pv_{pv_id}.difficulty.extreme.length={extreme_count}")
            
            # Hard
            if 'hard' in difficulties:
                content.extend([
                    f"pv_{pv_id}.difficulty.hard.0.edition=0",
                    f"pv_{pv_id}.difficulty.hard.0.level={difficulties['hard']['level']}",
                    f"pv_{pv_id}.difficulty.hard.0.level_sortindex={difficulties['hard']['level_sort_index']}",
                    f"pv_{pv_id}.difficulty.hard.0.script_filename=rom/script/pv_{pv_id}_hard.dsc",
                    f"pv_{pv_id}.difficulty.hard.0.scriptformat=0x15122517",
                    f"pv_{pv_id}.difficulty.hard.0.version=1",
                    f"pv_{pv_id}.difficulty.hard.length=1"
                ])
            else:
                content.append(f"pv_{pv_id}.difficulty.hard.length=0")
            
            # Normal
            if 'normal' in difficulties:
                content.extend([
                    f"pv_{pv_id}.difficulty.normal.0.edition=0",
                    f"pv_{pv_id}.difficulty.normal.0.level={difficulties['normal']['level']}",
                    f"pv_{pv_id}.difficulty.normal.0.level_sortindex={difficulties['normal']['level_sort_index']}",
                    f"pv_{pv_id}.difficulty.normal.0.script_filename=rom/script/pv_{pv_id}_normal.dsc",
                    f"pv_{pv_id}.difficulty.normal.0.scriptformat=0x15122517",
                    f"pv_{pv_id}.difficulty.normal.0.version=1",
                    f"pv_{pv_id}.difficulty.normal.length=1"
                ])
            else:
                content.append(f"pv_{pv_id}.difficulty.normal.length=0")
            
            # Standard settings
            content.extend([
                f"pv_{pv_id}.hiddentiming=0.3",
                f"pv_{pv_id}.high_speedrate=4",
                f"pv_{pv_id}.mdata.flag=1",
                f"pv_{pv_id}.motion.00=CMN_POSE_DEFAULT",
                f"pv_{pv_id}.movie_filename=rom/movie/pv_{pv_id}.mp4",
                f"pv_{pv_id}.movie_pvtype=ONLY",
                f"pv_{pv_id}.moviesurface=FRONT",
                f"pv_{pv_id}.pack=2"
            ])
            
            # Performers
            performers = song.get('performers', ['MIK'])
            for j, performer in enumerate(performers):
                content.extend([
                    f"pv_{pv_id}.performer.{j}.chara={performer}",
                    f"pv_{pv_id}.performer.{j}.pv_costume=1",
                    f"pv_{pv_id}.performer.{j}.type=VOCAL"
                ])
            content.append(f"pv_{pv_id}.performer.num={len(performers)}")
            
            # Sabi settings
            content.extend([
                f"pv_{pv_id}.sabi.playtime={song['sabi_play']}",
                f"pv_{pv_id}.sabi.start_time={song['sabi_start']}"
            ])
            
            # Standard sound settings
            content.extend([
                f"pv_{pv_id}.se_name=01button1",
                f"pv_{pv_id}.slide_name=slidese13",
                f"pv_{pv_id}.slidertouch_name=slidewindchime",
                f"pv_{pv_id}.song_filename=rom/sound/song/pv_{pv_id}.ogg"
            ])
            
            # Song names
            content.extend([
                f"pv_{pv_id}.song_name={song['song_name']}",
                f"pv_{pv_id}.song_name_en={song['song_name_en']}"
            ])
            if song['song_name_en2']:
                content.append(f"pv_{pv_id}.song_name_en2={song['song_name_en2']}")
            content.extend([
                f"pv_{pv_id}.song_name_reading={song['song_name_reading']}",
                f"pv_{pv_id}.song_name_ro={song['song_name_ro']}"
            ])
            
            # Songinfo
            songinfo = song.get('songinfo', {})
            for field in ['arranger', 'guitar_player', 'lyrics', 'manipulator', 'music', 'pv_editor']:
                if field in songinfo and songinfo[field]:
                    content.append(f"pv_{pv_id}.songinfo.{field}={songinfo[field]}")
                    # Add English version if it exists
                    en_field = f"{field}_en"
                    if en_field in songinfo and songinfo[en_field]:
                        content.append(f"pv_{pv_id}.songinfo_en.{field}={songinfo[en_field]}")
            
            content.append(f"pv_{pv_id}.sudden_timing=0.6")
        
        return '\n'.join(content)
    
    def save_config(self):
        if not self.songs:
            messagebox.showwarning("Warning", "No songs to save")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".pdpack",
            filetypes=[
                ("Project Diva Pack files", "*.pdpack")
            ],
            initialfile="config.pdpack"
        )

        if filename:
            try:
                config = {
                    'pack_name': self.pack_name_var.get(),
                    'pack_name_jp': self.pack_name_jp_var.get(),
                    'songs': self.songs
                }

                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)

                messagebox.showinfo("Success", f"Configuration saved: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving configuration: {str(e)}")

    def load_config(self):
        filename = filedialog.askopenfilename(
            filetypes=[
                ("Project Diva Pack files", "*.pdpack")
            ]
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                self.pack_name_var.set(config.get('pack_name', ''))
                self.pack_name_jp_var.set(config.get('pack_name_jp', ''))
                self.songs = config.get('songs', [])

                self.update_songs_display()
                messagebox.showinfo("Success", f"Configuration loaded: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading configuration: {str(e)}")

    def load_autosave(self):
        """Load an autosave file"""
        if not os.path.exists(self.autosave_folder):
            messagebox.showinfo("Information", "No autosave files available")
            return
        
        # Buscar archivos de autoguardado
        pattern = os.path.join(self.autosave_folder, "autosave_*.pdpack")
        autosave_files = glob.glob(pattern)
        
        if not autosave_files:
            messagebox.showinfo("Information", "No autosave files available")
            return
        
        # Mostrar diálogo de selección
        autosave_files.sort(key=os.path.getmtime, reverse=True)  # Más reciente primero
        
        # Crear ventana de selección
        dialog = tk.Toplevel(self.root)
        dialog.title("Load Autosave")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select autosave file:", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Lista de archivos
        listbox = tk.Listbox(dialog, height=15)
        listbox.pack(fill='both', expand=True, padx=10, pady=5)
        
        for file in autosave_files:
            filename = os.path.basename(file)
            # Extraer timestamp del nombre del archivo
            try:
                timestamp_part = filename.replace('autosave_', '').replace('.pdpack', '')
                year = timestamp_part[:4]
                month = timestamp_part[4:6]
                day = timestamp_part[6:8]
                hour = timestamp_part[9:11]
                minute = timestamp_part[12:14]
                second = timestamp_part[15:17]
                
                display_name = f"{day}/{month}/{year} {hour}:{minute}:{second} - {filename}"
            except:
                display_name = filename
            
            listbox.insert(tk.END, display_name)
        
        def load_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Select an autosave file")
                return
            
            selected_file = autosave_files[selection[0]]
            dialog.destroy()
            
            # Cargar el archivo seleccionado
            try:
                with open(selected_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.pack_name_var.set(config.get('pack_name', ''))
                self.pack_name_jp_var.set(config.get('pack_name_jp', ''))
                self.songs = config.get('songs', [])
                
                self.update_songs_display()
                messagebox.showinfo("Success", f"Autosave loaded: {os.path.basename(selected_file)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading autosave: {str(e)}")
        
        # Botones
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Load", command=load_selected).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ProjectDivaModEditor()
    app.run()