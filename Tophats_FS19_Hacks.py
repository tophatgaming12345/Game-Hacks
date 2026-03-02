import os
import shutil
import tkinter as tk
import xml.etree.ElementTree as ET
from pathlib import Path
from tkinter import messagebox, ttk

def find_fs19_folder():
    home = Path.home()

    possible_paths = [
        home / "Documents" / "My Games" / "FarmingSimulator2019",
        home / "OneDrive" / "Documents" / "My Games" / "FarmingSimulator2019",
        Path(os.path.expandvars("%USERPROFILE%")) / "Documents" / "My Games" / "FarmingSimulator2019",
    ]

    for path in possible_paths:
        if path.exists() and any(path.glob("savegame*")):
            return path

    return None

def run_editor():
    try:
        status_label.config(text="Locating save folder...", fg="yellow")
        root.update()

        fs_path = find_fs19_folder()
        if not fs_path:
            messagebox.showerror("Error", "Could not find FarmingSimulator2019 save folder.")
            status_label.config(text="Save folder not found.", fg="red")
            return

        slot = slot_var.get()
        amount = int(money_entry.get())
        save_dir = fs_path / f'savegame{slot}'

        if not save_dir.exists():
            messagebox.showerror("Error", f"Savegame {slot} not found.")
            return

        # Backup + edit careerSavegame.xml
        cs_path = save_dir / 'careerSavegame.xml'
        if cs_path.exists():
            shutil.copy(cs_path, str(cs_path) + ".bak")
            tree = ET.parse(cs_path)
            money_node = tree.getroot().find('.//statistics/money')
            if money_node is not None:
                money_node.text = str(amount)
            tree.write(cs_path, encoding='utf-8', xml_declaration=True)

        # Backup + edit farms.xml
        f_path = save_dir / 'farms.xml'
        if f_path.exists():
            shutil.copy(f_path, str(f_path) + ".bak")
            tree = ET.parse(f_path)
            farm = tree.getroot().find('.//farm[@farmId="1"]')
            if farm is not None:
                farm.set('money', str(float(amount)))
                farm.set('loan', "0.000000")
            tree.write(f_path, encoding='utf-8', xml_declaration=True)

        # Backup + edit farmland.xml
        l_path = save_dir / 'farmland.xml'
        if l_path.exists():
            shutil.copy(l_path, str(l_path) + ".bak")
            tree = ET.parse(l_path)
            for land in tree.getroot().findall('farmland'):
                land.set('farmId', '1')
            tree.write(l_path, encoding='utf-8', xml_declaration=True)

        status_label.config(text="Hack Complete!", fg="green")
        messagebox.showinfo("Success", f"Tophat's FS19 Hacks applied to save slot {slot}.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# UI Setup
root = tk.Tk()
root.title("Tophat's FS19 Hacks")
root.geometry("400x300")

tk.Label(root, text="Tophat's FS19 Hacks", font=("Arial", 14, "bold")).pack(pady=5)

tk.Label(root, text="Select Save Slot:").pack(pady=5)
slot_var = tk.IntVar(value=1)
slot_menu = ttk.Combobox(root, textvariable=slot_var, values=list(range(1, 21)), state="readonly")
slot_menu.pack()

tk.Label(root, text="Money Amount:").pack(pady=5)
money_entry = tk.Entry(root, justify='center')
money_entry.insert(0, "10000000")
money_entry.pack()

status_label = tk.Label(root, text="Ready.", fg="gray")
status_label.pack(pady=10)

tk.Button(root, text="Apply Hacks", command=run_editor, width=20, height=2).pack(pady=20)

root.mainloop()
