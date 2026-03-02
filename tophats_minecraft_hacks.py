import tkinter as tk
import pyautogui
import keyboard
import time

HOTKEY = '\\'  # Press this in Minecraft

class MinecraftTrainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tophat's Minecraft Trainer")
        self.geometry("400x350")

        tk.Label(self, text="Block/Item Command:").pack(pady=5)
        self.block_entry = tk.Entry(self, justify='center')
        self.block_entry.insert(0, "block_diamond_64")
        self.block_entry.pack()

        tk.Label(self, text="XP Amount:").pack(pady=5)
        self.xp_entry = tk.Entry(self, justify='center')
        self.xp_entry.insert(0, "500")
        self.xp_entry.pack()

        self.heal_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Heal", variable=self.heal_var).pack()

        self.feed_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Feed", variable=self.feed_var).pack()

        self.creative_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Creative", variable=self.creative_var).pack()

        self.status_label = tk.Label(self, text="Press \\ in Minecraft to apply!", fg="gray")
        self.status_label.pack(pady=15)

        keyboard.add_hotkey(HOTKEY, self.apply)  # Listen for hotkey

    def parse_block_command(self, cmd):
        if cmd.startswith("block_"):
            parts = cmd.split('_')
            if len(parts) >= 3:
                return f"/give @p minecraft:{parts[1]} {parts[2]}"
        return cmd

    def apply(self):
        block_cmd = self.block_entry.get().strip()
        xp_amount = self.xp_entry.get().strip()
        status_text = "Applied: "

        # Tiny delay to make sure Minecraft is ready
        time.sleep(0.1)

        if block_cmd:
            mc_cmd = self.parse_block_command(block_cmd)
            pyautogui.typewrite(mc_cmd)
            pyautogui.press('enter')
            status_text += f"{mc_cmd} "

        if xp_amount:
            try:
                xp = int(xp_amount)
                pyautogui.typewrite(f"/xp add @p {xp}")
                pyautogui.press('enter')
                status_text += f"{xp} XP "
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid XP input.")
                return

        if self.heal_var.get():
            pyautogui.typewrite("/effect give @p minecraft:instant_health 1 255")
            pyautogui.press('enter')
            status_text += "Heal | "
        if self.feed_var.get():
            pyautogui.typewrite("/effect give @p minecraft:saturation 1 255")
            pyautogui.press('enter')
            status_text += "Feed | "
        if self.creative_var.get():
            pyautogui.typewrite("/gamemode creative @p")
            pyautogui.press('enter')
            status_text += "Creative | "

        self.status_label.config(text=status_text)

if __name__ == "__main__":
    app = MinecraftTrainer()
    app.mainloop()