"""
=============================================================================
🎮 PIXEL REALMS: GUI EDITION (TKINTER CANVAS) 🎮
=============================================================================
A windowed pixel art companion game powered by the exact same OOP classes
from main.py! Demonstrates how OOP decouples game logic from the presentation
layer (CLI vs GUI).
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

# Import shared OOP classes directly from main.py
from main import (
    Character, Assassin, Tank, Mage, Fighter,
    Goblin, SkeletonKnight, ShadowDragon,
    Inventory, SoundManager, SPRITES, strip_ansi
)

# Retro Palette
BG_COLOR       = "#11111b"  # Deep dark arcade background
PANEL_BG       = "#1e1e2e"  # Dark panel background
BORDER_COLOR   = "#45475a"  # Crisp pixel border
TEXT_COLOR     = "#cdd6f4"  # Off-white retro text
ACCENT_YELLOW  = "#f9e2af"  # Retro gold
HP_GREEN       = "#a6e3a1"  # Retro green health
HP_YELLOW      = "#f9e2af"  # Mid health
HP_RED         = "#f38ba8"  # Low health
MP_CYAN        = "#89dceb"  # Mana blue
EMPTY_BAR      = "#313244"  # Bar background


class PixelCanvas(tk.Canvas):
    """Custom canvas that renders retro chunky pixel blocks and battle animations."""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=BG_COLOR, highlightthickness=2,
                         highlightbackground=BORDER_COLOR, **kwargs)

    def draw_pixel_sprite(self, x_offset: int, y_offset: int, sprite_lines: list[str],
                          pixel_size: int = 7, default_color: str = "#cdd6f4"):
        """Renders ASCII/Unicode block sprites as chunky pixel tiles on the canvas."""
        color_map = {
            '31': '#f38ba8',  # Red
            '91': '#f38ba8',
            '32': '#a6e3a1',  # Green
            '92': '#a6e3a1',
            '33': '#f9e2af',  # Yellow
            '93': '#f9e2af',
            '34': '#89b4fa',  # Blue
            '94': '#89b4fa',
            '35': '#cba6f7',  # Purple
            '95': '#cba6f7',
            '36': '#89dceb',  # Cyan
            '96': '#89dceb',
            '37': '#cdd6f4',  # White
            '97': '#cdd6f4',
            '90': '#6c7086',  # Gray
        }

        import re
        ansi_regex = re.compile(r'\033\[([0-9;]+)m')

        for row_idx, line in enumerate(sprite_lines):
            col_idx = 0
            current_color = default_color
            pos = 0

            while pos < len(line):
                match = ansi_regex.match(line, pos)
                if match:
                    code = match.group(1).split(';')[-1]
                    if code == '0':
                        current_color = default_color
                    else:
                        current_color = color_map.get(code, default_color)
                    pos = match.end()
                    continue

                ch = line[pos]
                px = x_offset + col_idx * pixel_size
                py = y_offset + row_idx * pixel_size

                if ch in ('█', '●', '☼', '▐', '▌', '▄', '▀'):
                    self.create_rectangle(
                        px, py, px + pixel_size, py + pixel_size,
                        fill=current_color, outline=""
                    )
                col_idx += 1
                pos += 1

    def draw_bar(self, x: int, y: int, width: int, height: int,
                 current: int, maximum: int, bar_type: str = "hp"):
        """Draws a bordered retro health or mana bar."""
        ratio = max(0.0, min(1.0, current / maximum)) if maximum > 0 else 0.0
        fill_width = int(width * ratio)

        if bar_type == "hp":
            color = HP_GREEN if ratio > 0.50 else (HP_YELLOW if ratio > 0.20 else HP_RED)
        else:
            color = MP_CYAN

        # Background track
        self.create_rectangle(x, y, x + width, y + height, fill=EMPTY_BAR, outline=BORDER_COLOR, width=2)
        # Filled section
        if fill_width > 0:
            self.create_rectangle(x, y, x + fill_width, y + height, fill=color, outline="")


class PixelGameGUI:
    """Tkinter-based Graphic User Interface for Pixel Realms."""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("⚔️ Pixel Realms: Turn-Based RPG (OOP GUI)")
        self.root.geometry("980x750")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.player = None
        self.enemy = None
        self.floor = 1
        self.inventory = Inventory(hp_potions=3, mp_potions=2)
        self.stages = [
            ("Floor 1: Whispering Woods", Goblin),
            ("Floor 2: Cursed Crypt", SkeletonKnight),
            ("Floor 3: Dragon's Spire (BOSS)", ShadowDragon)
        ]

        self.setup_char_select_screen()

    # -------------------------------------------------------------------------
    # CHARACTER SELECTION VIEW
    # -------------------------------------------------------------------------
    def setup_char_select_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        header = tk.Label(
            self.root,
            text="⚔️ PIXEL REALMS: SELECT HERO ⚔️",
            font=("Courier", 24, "bold"),
            bg=BG_COLOR,
            fg=ACCENT_YELLOW
        )
        header.pack(pady=(25, 10))

        subtitle = tk.Label(
            self.root,
            text="Choose your class role to enter the dungeon",
            font=("Courier", 12),
            bg=BG_COLOR,
            fg="#a6adc8"
        )
        subtitle.pack(pady=(0, 15))

        # Name Entry Frame
        name_frame = tk.Frame(self.root, bg=BG_COLOR)
        name_frame.pack(pady=10)

        tk.Label(
            name_frame, text="Hero Name:", font=("Courier", 14, "bold"),
            bg=BG_COLOR, fg=TEXT_COLOR
        ).pack(side=tk.LEFT, padx=8)

        self.name_entry = tk.Entry(
            name_frame, font=("Courier", 14, "bold"), width=20,
            bg=PANEL_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
            highlightthickness=2, highlightbackground=BORDER_COLOR
        )
        self.name_entry.insert(0, "ShadowKnight")
        self.name_entry.pack(side=tk.LEFT, padx=8)

        # Roles Grid Frame
        roles_frame = tk.Frame(self.root, bg=BG_COLOR)
        roles_frame.pack(pady=20)

        roles_data = [
            ("Assassin", "#cba6f7", "High Crit & High Speed\nHP: 95  | ATK: 26\nDEF: 6   | SPD: 18 | CRIT: 35%", Assassin),
            ("Tank", "#89dceb", "High Defense & Sturdy HP\nHP: 170 | ATK: 15\nDEF: 20  | SPD: 7  | CRIT: 5%", Tank),
            ("Mage", "#89b4fa", "High Magic Damage & Deep Mana\nHP: 85  | ATK: 11 (230% Spell)\nDEF: 5   | SPD: 12 | MP: 100", Mage),
            ("Fighter", "#f38ba8", "Balanced Warrior & Tenacity\nHP: 130 | ATK: 21\nDEF: 12  | SPD: 13 | CRIT: 18%", Fighter),
        ]

        for idx, (r_name, r_color, r_stats, r_cls) in enumerate(roles_data):
            col = idx % 2
            row = idx // 2
            card = tk.Frame(
                roles_frame, bg=PANEL_BG, highlightthickness=2,
                highlightbackground=BORDER_COLOR, padx=20, pady=16, width=420, height=190
            )
            card.grid(row=row, column=col, padx=20, pady=14)
            card.pack_propagate(False)

            lbl_title = tk.Label(
                card, text=f"⚔ {r_name.upper()}", font=("Courier", 16, "bold"),
                bg=PANEL_BG, fg=r_color
            )
            lbl_title.pack(anchor="w", pady=(0, 6))

            lbl_stats = tk.Label(
                card, text=r_stats, font=("Courier", 11),
                bg=PANEL_BG, fg=TEXT_COLOR, justify="left"
            )
            lbl_stats.pack(anchor="w", pady=(0, 10))

            btn = tk.Button(
                card, text=f"Choose {r_name} ▶", font=("Courier", 11, "bold"),
                bg="#313244", fg=TEXT_COLOR, activebackground=r_color,
                activeforeground="#11111b", relief="flat", cursor="hand2",
                pady=6, command=lambda cls=r_cls: self.start_game_with_role(cls)
            )
            btn.pack(side=tk.BOTTOM, fill=tk.X)

    def start_game_with_role(self, role_cls):
        name = self.name_entry.get().strip() or "Hero"
        self.player = role_cls(name)
        self.floor = 1
        self.inventory = Inventory(hp_potions=3, mp_potions=2)
        SoundManager.play("victory")
        self.load_floor()

    # -------------------------------------------------------------------------
    # BATTLE ARENA VIEW
    # -------------------------------------------------------------------------
    def load_floor(self):
        if self.floor > len(self.stages):
            self.show_victory_screen()
            return

        stage_name, enemy_cls = self.stages[self.floor - 1]
        self.enemy = enemy_cls()
        self.setup_battle_screen(stage_name)
        self.log(f"⚔️ Floor {self.floor}: {stage_name} — A wild {self.enemy.name} appeared!")

    def setup_battle_screen(self, stage_name: str):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Header
        top_frame = tk.Frame(self.root, bg=BG_COLOR)
        top_frame.pack(fill=tk.X, padx=15, pady=6)

        self.lbl_title = tk.Label(
            top_frame, text=f"⚔️ {stage_name.upper()} ⚔️",
            font=("Courier", 14, "bold"), bg=BG_COLOR, fg=ACCENT_YELLOW
        )
        self.lbl_title.pack(side=tk.LEFT)

        self.lbl_inv = tk.Label(
            top_frame, text=f"🧪 Potions: {self.inventory.hp_potions} | 🔷 Ethers: {self.inventory.mp_potions}",
            font=("Courier", 11, "bold"), bg=BG_COLOR, fg=TEXT_COLOR
        )
        self.lbl_inv.pack(side=tk.RIGHT)

        # Pixel Canvas Arena (Spacious 940x330 frame)
        self.canvas = PixelCanvas(self.root, width=940, height=330)
        self.canvas.pack(padx=20, pady=8)

        # Bottom Frame: Left (Log), Right (Action Buttons)
        bottom_frame = tk.Frame(self.root, bg=BG_COLOR)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        # Battle Log Text Box
        log_frame = tk.Frame(bottom_frame, bg=PANEL_BG, highlightthickness=2, highlightbackground=BORDER_COLOR)
        log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        self.log_text = tk.Text(
            log_frame, font=("Courier", 11), bg=PANEL_BG, fg=TEXT_COLOR,
            wrap=tk.WORD, state=tk.DISABLED, relief="flat", padx=12, pady=10
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Action Buttons Panel
        btn_frame = tk.Frame(bottom_frame, bg=PANEL_BG, highlightthickness=2, highlightbackground=BORDER_COLOR, width=250)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y)
        btn_frame.pack_propagate(False)

        tk.Label(
            btn_frame, text="ACTIONS", font=("Courier", 13, "bold"),
            bg=PANEL_BG, fg=ACCENT_YELLOW
        ).pack(pady=(10, 8))

        self.btn_attack = tk.Button(
            btn_frame, text="⚔️ Attack", font=("Courier", 11, "bold"),
            bg="#313244", fg=TEXT_COLOR, activebackground="#45475a",
            relief="flat", cursor="hand2", pady=4, command=self.action_attack
        )
        self.btn_attack.pack(fill=tk.X, padx=12, pady=4)

        self.btn_skills = tk.Button(
            btn_frame, text="✨ Skills", font=("Courier", 11, "bold"),
            bg="#313244", fg=TEXT_COLOR, activebackground="#45475a",
            relief="flat", cursor="hand2", pady=4, command=self.open_skills_menu
        )
        self.btn_skills.pack(fill=tk.X, padx=12, pady=4)

        self.btn_defend = tk.Button(
            btn_frame, text="🛡️ Guard", font=("Courier", 11, "bold"),
            bg="#313244", fg=TEXT_COLOR, activebackground="#45475a",
            relief="flat", cursor="hand2", pady=4, command=self.action_defend
        )
        self.btn_defend.pack(fill=tk.X, padx=12, pady=4)

        self.btn_potion = tk.Button(
            btn_frame, text="🧪 Heal Potion", font=("Courier", 11, "bold"),
            bg="#313244", fg=TEXT_COLOR, activebackground="#45475a",
            relief="flat", cursor="hand2", pady=4, command=self.action_potion
        )
        self.btn_potion.pack(fill=tk.X, padx=12, pady=4)

        self.btn_ether = tk.Button(
            btn_frame, text="🔷 Mana Ether", font=("Courier", 11, "bold"),
            bg="#313244", fg=TEXT_COLOR, activebackground="#45475a",
            relief="flat", cursor="hand2", pady=4, command=self.action_ether
        )
        self.btn_ether.pack(fill=tk.X, padx=12, pady=4)

        self.update_arena_display()

    def log(self, message: str):
        """Appends formatted message to scrolling battle log."""
        clean_msg = strip_ansi(message)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"> {clean_msg}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_arena_display(self):
        """Redraws the pixel canvas with current HP/MP and retro sprites."""
        self.canvas.delete("all")

        # Inventory counter update
        self.lbl_inv.config(
            text=f"🧪 Potions: {self.inventory.hp_potions} | 🔷 Ethers: {self.inventory.mp_potions}"
        )

        # 1. Left (Player) Info & Bars
        p_name = f"{self.player.name} ({self.player.role} Lv.{self.player.level})"
        self.canvas.create_text(30, 24, text=p_name, anchor="w", fill=ACCENT_YELLOW, font=("Courier", 13, "bold"))
        self.canvas.create_text(30, 54, text=f"HP {self.player.hp}/{self.player.max_hp}", anchor="w", fill=TEXT_COLOR, font=("Courier", 10, "bold"))
        self.canvas.draw_bar(155, 46, 240, 16, self.player.hp, self.player.max_hp, "hp")

        self.canvas.create_text(30, 82, text=f"MP {self.player.mp}/{self.player.max_mp}", anchor="w", fill=TEXT_COLOR, font=("Courier", 10, "bold"))
        self.canvas.draw_bar(155, 74, 240, 16, self.player.mp, self.player.max_mp, "mp")

        # 2. Right (Enemy) Info & Bars
        e_name = f"{self.enemy.name} (Lv.{self.enemy.level})"
        self.canvas.create_text(910, 24, text=e_name, anchor="e", fill="#f38ba8", font=("Courier", 13, "bold"))
        self.canvas.create_text(525, 54, text=f"HP {self.enemy.hp}/{self.enemy.max_hp}", anchor="w", fill=TEXT_COLOR, font=("Courier", 10, "bold"))
        self.canvas.draw_bar(670, 46, 240, 16, self.enemy.hp, self.enemy.max_hp, "hp")

        e_stats = f"ATK: {self.enemy.attack}  DEF: {self.enemy.defense}  SPD: {self.enemy.speed}"
        self.canvas.create_text(910, 82, text=e_stats, anchor="e", fill="#a6adc8", font=("Courier", 10, "bold"))

        # 3. Chunky Pixel Sprites (Enlarged with pixel_size=13)
        # Player Sprite on Left
        self.canvas.draw_pixel_sprite(140, 125, self.player.sprite, pixel_size=13)
        # Enemy Sprite on Right
        self.canvas.draw_pixel_sprite(590, 125, self.enemy.sprite, pixel_size=13)

    # -------------------------------------------------------------------------
    # TURN MANAGEMENT
    # -------------------------------------------------------------------------
    def action_attack(self):
        dmg, is_crit, did_hit = self.player.serang(self.enemy)
        if not did_hit:
            self.log(f"{self.player.name} attacked, but {self.enemy.name} dodged!")
        else:
            SoundManager.play("crit" if is_crit else "hit")
            crit_txt = " CRITICAL HIT!" if is_crit else ""
            self.log(f"{self.player.name} strikes for {dmg} damage!{crit_txt}")

        self.update_arena_display()
        self.check_turn_resolution()

    def action_defend(self):
        self.player.defend()
        SoundManager.play("defend")
        self.log(f"{self.player.name} assumes Guard Stance! Defense boosted & +10 MP restored.")
        self.update_arena_display()
        self.check_turn_resolution()

    def action_potion(self):
        success, msg = self.inventory.use_hp_potion(self.player)
        if not success:
            messagebox.showinfo("Potion", msg)
            return
        self.log(msg)
        self.update_arena_display()
        self.check_turn_resolution()

    def action_ether(self):
        success, msg = self.inventory.use_mp_potion(self.player)
        if not success:
            messagebox.showinfo("Ether", msg)
            return
        self.log(msg)
        self.update_arena_display()
        self.check_turn_resolution()

    def open_skills_menu(self):
        skills = self.player.get_skills()
        win = tk.Toplevel(self.root)
        win.title(f"✨ {self.player.role} Skills")
        win.geometry("450x260")
        win.configure(bg=PANEL_BG)
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        tk.Label(
            win, text=f"SELECT SKILL (Current MP: {self.player.mp}/{self.player.max_mp})",
            font=("Courier", 11, "bold"), bg=PANEL_BG, fg=ACCENT_YELLOW
        ).pack(pady=8)

        for idx, sk in enumerate(skills):
            s_frame = tk.Frame(win, bg="#313244", highlightthickness=1, highlightbackground=BORDER_COLOR)
            s_frame.pack(fill=tk.X, padx=12, pady=4)

            t_text = f"{sk['name']} ({sk['cost']} MP)"
            lbl = tk.Label(s_frame, text=t_text, font=("Courier", 10, "bold"), bg="#313244", fg="#89dceb")
            lbl.pack(anchor="w", padx=6, pady=2)

            d_lbl = tk.Label(s_frame, text=sk['desc'], font=("Courier", 8), bg="#313244", fg=TEXT_COLOR)
            d_lbl.pack(anchor="w", padx=6)

            btn = tk.Button(
                s_frame, text="Cast", font=("Courier", 9, "bold"),
                bg=BORDER_COLOR, fg=TEXT_COLOR, activebackground=ACCENT_YELLOW,
                command=lambda i=idx, w=win: self.cast_skill(i, w)
            )
            btn.pack(side=tk.RIGHT, padx=6, pady=4)

    def cast_skill(self, skill_idx: int, window: tk.Toplevel):
        success, msg = self.player.use_skill(skill_idx, self.enemy)
        if not success:
            messagebox.showwarning("Skills", msg, parent=window)
            return

        window.destroy()
        self.log(msg)
        self.update_arena_display()
        self.check_turn_resolution()

    def check_turn_resolution(self):
        """Checks if enemy died, else executes enemy turn and end-of-round ticks."""
        if not self.enemy.is_alive():
            SoundManager.play("victory")
            self.log(f"💥 {self.enemy.name} was defeated!")
            self.root.after(1000, self.handle_stage_clear)
            return

        # Enemy turn after short delay
        self.set_buttons_state(False)
        self.root.after(800, self.execute_enemy_turn)

    def execute_enemy_turn(self):
        if not self.enemy.is_alive():
            return

        msg = self.enemy.take_turn(self.player)
        self.log(msg)

        # End of turn ticks (poison, buff decays)
        p_logs = self.player.start_turn()
        e_logs = self.enemy.start_turn()
        for l in p_logs + e_logs:
            self.log(l)

        self.update_arena_display()

        if not self.player.is_alive():
            SoundManager.play("game_over")
            self.log(f"☠️ {self.player.name} fell in combat...")
            self.root.after(1000, self.show_game_over_screen)
        else:
            self.set_buttons_state(True)

    def set_buttons_state(self, enabled: bool):
        st = tk.NORMAL if enabled else tk.DISABLED
        self.btn_attack.config(state=st)
        self.btn_skills.config(state=st)
        self.btn_defend.config(state=st)
        self.btn_potion.config(state=st)
        self.btn_ether.config(state=st)

    def handle_stage_clear(self):
        self.player.level_up()
        self.inventory.hp_potions += 1
        self.inventory.mp_potions += 1
        messagebox.showinfo(
            "Stage Clear!",
            f"✨ FLOOR {self.floor} CLEARED! ✨\n\n"
            f"{self.player.name} reached Level {self.player.level}!\n"
            f"+25 Max HP | +15 Max MP | +4 ATK | +3 DEF | +2 SPD\n"
            f"Loot: +1 Health Potion, +1 Mana Ether\nHP & MP fully restored!"
        )
        self.floor += 1
        self.load_floor()

    def show_victory_screen(self):
        messagebox.showinfo(
            "🏆 GRAND VICTORY!",
            f"🎉 CONGRATULATIONS, {self.player.name.upper()}! 🎉\n\n"
            f"You conquered the Pixel Dungeon and vanquished the Shadow Dragon Lord!\n"
            f"Final Level: {self.player.level} {self.player.role}\n"
            f"HP: {self.player.hp}/{self.player.max_hp} | MP: {self.player.mp}/{self.player.max_mp}\n\n"
            f"Thank you for playing Pixel Realms OOP Edition!"
        )
        self.setup_char_select_screen()

    def show_game_over_screen(self):
        retry = messagebox.askyesno(
            "Game Over",
            f"☠️ {self.player.name} was defeated on Floor {self.floor}.\n\nWould you like to try again?"
        )
        if retry:
            self.setup_char_select_screen()
        else:
            self.root.destroy()


def run_gui():
    root = tk.Tk()
    app = PixelGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
