"""
=============================================================================
⚔️  PIXEL REALMS: TURN-BASED RPG (OOP EDITION) ⚔️
=============================================================================
A retro 8-bit turn-based pixel RPG built with clean Object-Oriented Programming (OOP)
in Python. Demonstrates:
  - Inheritance: Character -> Assassin, Tank, Mage, Fighter, Enemy
  - Polymorphism: Custom role stats, unique skills, and AI behaviors
  - Encapsulation: HP/MP boundaries, defense mitigations, status effects
  - Retro Aesthetics: ANSI pixel art sprites, HP/MP bars, 8-bit chiptune sound
=============================================================================
"""

import os
import sys
import time
import random
import re

# Enable ANSI escape sequences on Windows console
if os.name == 'nt':
    os.system('')

# =============================================================================
# ANSI COLORS & STYLES
# =============================================================================
C_RESET  = '\033[0m'
C_BOLD   = '\033[1m'
C_DIM    = '\033[2m'
C_RED    = '\033[91m'
C_GREEN  = '\033[92m'
C_YELLOW = '\033[93m'
C_BLUE   = '\033[94m'
C_PURPLE = '\033[95m'
C_CYAN   = '\033[96m'
C_WHITE  = '\033[97m'
C_GRAY   = '\033[90m'

# Background colors
BG_RED   = '\033[41m'
BG_BLUE  = '\033[44m'
BG_DARK  = '\033[40m'


def strip_ansi(text: str) -> str:
    """Removes ANSI escape codes to accurately measure visible string width."""
    return re.sub(r'\033\[[0-9;]*m', '', text)


# =============================================================================
# 8-BIT RETRO SOUND EFFECTS (WINDOWS COMPATIBLE WITH SILENT FALLBACK)
# =============================================================================
class SoundManager:
    """Manages retro 8-bit chiptune beeps for battle sound effects."""
    enabled = True

    @classmethod
    def play(cls, sfx_type: str):
        if not cls.enabled:
            return
        try:
            import winsound
            if sfx_type == "hit":
                winsound.Beep(380, 50)
                winsound.Beep(260, 60)
            elif sfx_type == "crit":
                winsound.Beep(620, 70)
                winsound.Beep(920, 120)
            elif sfx_type == "heal":
                winsound.Beep(523, 60)
                winsound.Beep(659, 60)
                winsound.Beep(784, 90)
            elif sfx_type == "magic":
                winsound.Beep(450, 50)
                winsound.Beep(700, 70)
                winsound.Beep(900, 90)
            elif sfx_type == "defend":
                winsound.Beep(220, 100)
            elif sfx_type == "victory":
                for note in [523, 659, 784, 1046]:
                    winsound.Beep(note, 110)
            elif sfx_type == "game_over":
                for note in [440, 370, 311, 261]:
                    winsound.Beep(note, 160)
            elif sfx_type == "select":
                winsound.Beep(850, 40)
        except Exception:
            pass  # Fail gracefully if audio device is unavailable


# =============================================================================
# PIXEL ART SPRITES (STANDARDIZED 16x8 CHARACTERS)
# =============================================================================
SPRITES = {
    'Assassin': [
        f'     {C_PURPLE}▄████▄{C_RESET}     ',
        f'    {C_PURPLE}██{C_CYAN}●{C_PURPLE}██{C_CYAN}●{C_PURPLE}██{C_RESET}    ',
        f'    {C_PURPLE}▀██████▀{C_RESET}    ',
        f' {C_YELLOW}▄{C_RESET}   {C_PURPLE}██████{C_RESET}   {C_YELLOW}▄{C_RESET} ',
        f'{C_YELLOW}▐█▌{C_RESET} {C_PURPLE}████████{C_RESET} {C_YELLOW}▐█▌{C_RESET}',
        f' {C_YELLOW}▀{C_RESET}  {C_PURPLE}████████{C_RESET}  {C_YELLOW}▀{C_RESET} ',
        f'    {C_PURPLE}███  ███{C_RESET}    ',
        f'    {C_PURPLE}█▀    ▀█{C_RESET}    ',
    ],
    'Tank': [
        f'    {C_GRAY}▄██████▄{C_RESET}    ',
        f'   {C_GRAY}███{C_CYAN}▀▀▀▀{C_GRAY}███{C_RESET}   ',
        f'   {C_GRAY}▀████████▀{C_RESET}   ',
        f' {C_CYAN}▄▄{C_RESET}  {C_WHITE}██████{C_RESET}  {C_WHITE}▄▄{C_RESET} ',
        f'{C_CYAN}███{C_RESET} {C_WHITE}█▀████▀█{C_RESET} {C_WHITE}██{C_RESET} ',
        f'{C_CYAN}███{C_RESET} {C_WHITE}████████{C_RESET} {C_WHITE}██{C_RESET} ',
        f' {C_CYAN}▀█{C_RESET}  {C_WHITE}██  ██{C_RESET}  {C_WHITE}▀▀{C_RESET} ',
        f'     {C_WHITE}█▀  ▀█{C_RESET}     ',
    ],
    'Mage': [
        f'      {C_BLUE}▄██▄{C_RESET}      ',
        f'     {C_BLUE}▄████▄{C_RESET}     ',
        f'   {C_BLUE}▄████████▄{C_RESET}   ',
        f'   {C_BLUE}▀▀{C_YELLOW}██████{C_BLUE}▀▀{C_RESET}   ',
        f' {C_YELLOW}☼{C_RESET}   {C_PURPLE}██{C_WHITE}●  ●{C_PURPLE}██{C_RESET}   ',
        f' {C_YELLOW}█{C_RESET}   {C_PURPLE}████████{C_RESET}   ',
        f' {C_YELLOW}█{C_RESET}   {C_BLUE}████████{C_RESET}   ',
        f' {C_YELLOW}█{C_RESET}    {C_BLUE}█▀  ▀█{C_RESET}    ',
    ],
    'Fighter': [
        f'    {C_RED}▄██████▄{C_RESET}    ',
        f'   {C_RED}██████████{C_RESET}   ',
        f'   {C_YELLOW}▀█{C_WHITE}●{C_YELLOW}████{C_WHITE}●{C_YELLOW}█▀{C_RESET}   ',
        f' {C_WHITE}▄{C_RESET}   {C_RED}██████{C_RESET}     ',
        f'{C_WHITE}▐█▌{C_RESET} {C_YELLOW}████████{C_RESET}    ',
        f' {C_WHITE}█{C_RESET}  {C_YELLOW}████████{C_RESET}    ',
        f' {C_WHITE}█{C_RESET}   {C_RED}███  ███{C_RESET}   ',
        f' {C_WHITE}▀{C_RESET}   {C_RED}█▀    ▀█{C_RESET}   ',
    ],
    'Goblin': [
        f'    {C_GREEN}▄█▀▀▀▀█▄{C_RESET}    ',
        f'   {C_GREEN}██▀{C_RED}●{C_GREEN}██{C_RED}●{C_GREEN}▀██{C_RESET}   ',
        f'   {C_GREEN}▀████████▀{C_RESET}   ',
        f'     {C_GREEN}██████{C_RESET}  {C_YELLOW}▄{C_RESET}  ',
        f'    {C_GREEN}████████{C_RESET} {C_YELLOW}█▌{C_RESET} ',
        f'     {C_GREEN}██████{C_RESET}  {C_YELLOW}▀{C_RESET}  ',
        f'     {C_GREEN}██  ██{C_RESET}     ',
        f'     {C_GREEN}█▀  ▀█{C_RESET}     ',
    ],
    'Skeleton': [
        f'     {C_WHITE}▄████▄{C_RESET}     ',
        f'   {C_WHITE}██ {C_RED}█  █{C_WHITE} ██{C_RESET}   ',
        f'     {C_WHITE}▀████▀{C_RESET}     ',
        f'  {C_GRAY}▄{C_RESET}   {C_WHITE}▄████▄{C_RESET}    ',
        f' {C_GRAY}▐█▌{C_RESET} {C_WHITE}████████{C_RESET}   ',
        f'  {C_GRAY}█{C_RESET}  {C_WHITE}█ █  █ █{C_RESET}   ',
        f'  {C_GRAY}█{C_RESET}   {C_WHITE}██  ██{C_RESET}    ',
        f'  {C_GRAY}▀{C_RESET}   {C_WHITE}█▀  ▀█{C_RESET}    ',
    ],
    'Dragon': [
        f' {C_RED}▄█▄        ▄█▄{C_RESET} ',
        f'{C_RED}▀████▄    ▄████▀{C_RESET}',
        f'  {C_RED}▀██████████▀{C_RESET}  ',
        f'   {C_RED}██{C_YELLOW}●{C_RED}████{C_YELLOW}●{C_RED}██{C_RESET}   ',
        f'  {C_RED}▄██████████▄{C_RESET}  ',
        f' {C_RED}█████{C_YELLOW}▀▀▀▀{C_RED}█████{C_RESET} ',
        f' {C_RED}▀████    ████▀{C_RESET} ',
        f'   {C_RED}▀▀      ▀▀{C_RESET}   ',
    ]
}


# =============================================================================
# OOP BASE CHARACTER CLASS (ENCAPSULATION & CORE LOGIC)
# =============================================================================
class Character:
    """
    Base class representing any combatant in the game.
    Demonstrates encapsulation of character stats and state transitions.
    """
    def __init__(self, name: str, role: str, max_hp: int, max_mp: int,
                 attack: int, defense: int, speed: int, crit_rate: float,
                 sprite_key: str, color: str = C_WHITE, level: int = 1):
        self.name = name
        self.role = role
        self.level = level
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.crit_rate = crit_rate
        self.sprite_key = sprite_key
        self.color = color

        # Combat States & Buffs
        self.is_defending = False
        self.buffs = {}  # e.g. {"atk_buff": {"turns": 2, "val": 6}, "poison": {"turns": 3, "val": 10}}

    @property
    def sprite(self):
        return SPRITES.get(self.sprite_key, SPRITES['Fighter'])

    def is_alive(self) -> bool:
        return self.hp > 0

    def effective_attack(self) -> int:
        buff_val = self.buffs.get("atk_buff", {}).get("val", 0)
        return max(1, self.attack + buff_val)

    def effective_defense(self) -> int:
        buff_val = self.buffs.get("def_buff", {}).get("val", 0)
        base_def = self.defense + buff_val
        if self.is_defending:
            return int(base_def * 2.0) + 5
        return base_def

    def take_damage(self, raw_damage: int, is_crit: bool = False, ignore_def_pct: float = 0.0) -> int:
        """Applies incoming damage reduced by effective defense and flags."""
        effective_def = self.effective_defense() * (1.0 - ignore_def_pct)
        # Defense softens damage: Damage = Raw * (100 / (100 + EffectiveDef * 2.5))
        mitigation = max(0.2, 100 / (100 + max(0, effective_def) * 2.5))
        actual_dmg = int(raw_damage * mitigation)
        actual_dmg = max(1, actual_dmg + random.randint(-2, 2))

        self.hp = max(0, self.hp - actual_dmg)
        return actual_dmg

    def heal(self, amount: int) -> int:
        """Heals HP without exceeding max_hp."""
        if not self.is_alive():
            return 0
        healed = min(amount, self.max_hp - self.hp)
        self.hp += healed
        return healed

    def restore_mp(self, amount: int) -> int:
        """Restores MP without exceeding max_mp."""
        restored = min(amount, self.max_mp - self.mp)
        self.mp += restored
        return restored

    def use_mp(self, amount: int) -> bool:
        """Checks and consumes MP."""
        if self.mp >= amount:
            self.mp -= amount
            return True
        return False

    def defend(self):
        """Puts character in defensive stance (doubles defense, recovers 10 MP)."""
        self.is_defending = True
        self.restore_mp(10)

    def reset_defend(self):
        self.is_defending = False

    def apply_buff(self, name: str, turns: int, val: int):
        self.buffs[name] = {"turns": turns, "val": val}

    def start_turn(self) -> list[str]:
        """Processes buff timers and damage-over-time effects at round start."""
        self.reset_defend()
        logs = []

        # Poison effect
        if "poison" in self.buffs:
            p_dmg = self.buffs["poison"]["val"]
            self.hp = max(0, self.hp - p_dmg)
            logs.append(f"{self.color}{self.name}{C_RESET} takes {C_GREEN}{p_dmg} poison damage{C_RESET}! ☠️")
            SoundManager.play("hit")
            self.buffs["poison"]["turns"] -= 1
            if self.buffs["poison"]["turns"] <= 0:
                del self.buffs["poison"]
                logs.append(f"The poison on {self.color}{self.name}{C_RESET} has worn off.")

        # ATK Buff countdown
        if "atk_buff" in self.buffs:
            self.buffs["atk_buff"]["turns"] -= 1
            if self.buffs["atk_buff"]["turns"] <= 0:
                del self.buffs["atk_buff"]
                logs.append(f"{self.color}{self.name}'s{C_RESET} attack boost has expired.")

        # DEF Buff countdown
        if "def_buff" in self.buffs:
            self.buffs["def_buff"]["turns"] -= 1
            if self.buffs["def_buff"]["turns"] <= 0:
                del self.buffs["def_buff"]
                logs.append(f"{self.color}{self.name}'s{C_RESET} defense fortification expired.")

        return logs

    def serang(self, target: 'Character') -> tuple[int, bool, bool]:
        """
        Standard attack action. Compatible with original user method name!
        Returns (damage, is_crit, did_hit).
        """
        # Speed-based dodge chance
        dodge_chance = max(0.05, min(0.40, (target.speed - self.speed) * 0.02))
        if random.random() < dodge_chance:
            return 0, False, False

        # Crit roll
        is_crit = random.random() < self.crit_rate
        mult = 1.8 if is_crit else 1.0
        raw = int(self.effective_attack() * mult)

        dmg = target.take_damage(raw, is_crit=is_crit)
        return dmg, is_crit, True

    def level_up(self):
        """Grows character attributes upon winning a stage."""
        self.level += 1
        self.max_hp += 25
        self.hp = self.max_hp
        self.max_mp += 15
        self.mp = self.max_mp
        self.attack += 4
        self.defense += 3
        self.speed += 2

    def tampilkan_info(self):
        """Displays character status card in console."""
        print(f"\n{self.color}=== {self.name} ({self.role} Lv.{self.level}) ==={C_RESET}")
        print(f"HP: {self.hp}/{self.max_hp} | MP: {self.mp}/{self.max_mp}")
        print(f"ATK: {self.attack} | DEF: {self.defense} | SPD: {self.speed} | CRIT: {int(self.crit_rate*100)}%")

    # Polymorphic methods to be overridden by subclasses
    def get_skills(self) -> list[dict]:
        return []

    def use_skill(self, skill_index: int, target: 'Character') -> tuple[bool, str]:
        return False, "No skills available."


# =============================================================================
# SUBCLASSES: PLAYER ROLES (INHERITANCE & POLYMORPHISM)
# =============================================================================
class Assassin(Character):
    """
    Assassin Role:
    High speed and critical strike probability. Lethal burst damage but fragile.
    """
    def __init__(self, name: str):
        super().__init__(
            name=name,
            role="Assassin",
            max_hp=95,
            max_mp=50,
            attack=26,
            defense=6,
            speed=18,
            crit_rate=0.35,
            sprite_key="Assassin",
            color=C_PURPLE
        )

    def get_skills(self) -> list[dict]:
        return [
            {
                "name": "Shadow Strike",
                "cost": 15,
                "desc": "High-velocity sneak attack (185% ATK, +25% bonus crit)."
            },
            {
                "name": "Poison Blade",
                "cost": 12,
                "desc": "Slashes target and inflicts Poison (12 dmg/turn for 3 turns)."
            },
            {
                "name": "Smoke Bomb",
                "cost": 18,
                "desc": "Drops smoke, recovers 25 HP and boosts SPD & DEF for 2 turns."
            }
        ]

    def use_skill(self, skill_index: int, target: Character) -> tuple[bool, str]:
        skills = self.get_skills()
        if skill_index < 0 or skill_index >= len(skills):
            return False, "Invalid skill selection."

        skill = skills[skill_index]
        if not self.use_mp(skill["cost"]):
            return False, f"Not enough MP! ({self.mp}/{skill['cost']} MP)"

        if skill_index == 0:  # Shadow Strike
            is_crit = random.random() < (self.crit_rate + 0.25)
            mult = 2.2 if is_crit else 1.85
            raw = int(self.effective_attack() * mult)
            dmg = target.take_damage(raw, is_crit=is_crit)
            SoundManager.play("crit" if is_crit else "hit")
            crit_str = f" {C_YELLOW}CRITICAL HIT!{C_RESET}" if is_crit else ""
            return True, f"{C_PURPLE}{self.name}{C_RESET} bursts from the shadows with {C_YELLOW}Shadow Strike{C_RESET}!{crit_str} Dealing {C_RED}{dmg} damage{C_RESET}!"

        elif skill_index == 1:  # Poison Blade
            raw = int(self.effective_attack() * 1.2)
            dmg = target.take_damage(raw)
            target.apply_buff("poison", turns=3, val=12)
            SoundManager.play("hit")
            return True, f"{C_PURPLE}{self.name}{C_RESET} cuts with {C_GREEN}Poison Blade{C_RESET} for {C_RED}{dmg} damage{C_RESET} and {C_GREEN}poisons{C_RESET} {target.name}!"

        elif skill_index == 2:  # Smoke Bomb
            healed = self.heal(25)
            self.apply_buff("def_buff", turns=2, val=10)
            SoundManager.play("magic")
            return True, f"{C_PURPLE}{self.name}{C_RESET} throws a {C_GRAY}Smoke Bomb{C_RESET}, vanishing into mist! Restores {C_GREEN}+{healed} HP{C_RESET} and gains defense!"

        return False, "Error executing skill."


class Tank(Character):
    """
    Tank Role:
    Massive health pool and impenetrable armor. Protects and controls the battle.
    """
    def __init__(self, name: str):
        super().__init__(
            name=name,
            role="Tank",
            max_hp=170,
            max_mp=35,
            attack=15,
            defense=20,
            speed=7,
            crit_rate=0.05,
            sprite_key="Tank",
            color=C_CYAN
        )

    def get_skills(self) -> list[dict]:
        return [
            {
                "name": "Shield Slam",
                "cost": 10,
                "desc": "Heavy shield bash (140% ATK) that reduces enemy ATK by -6."
            },
            {
                "name": "Iron Fortress",
                "cost": 14,
                "desc": "Hardens armor (+12 DEF for 3 turns) and restores 30 HP."
            },
            {
                "name": "Earthquake",
                "cost": 18,
                "desc": "Seismic ground slam dealing heavy damage ignoring 60% armor."
            }
        ]

    def use_skill(self, skill_index: int, target: Character) -> tuple[bool, str]:
        skills = self.get_skills()
        if skill_index < 0 or skill_index >= len(skills):
            return False, "Invalid skill selection."

        skill = skills[skill_index]
        if not self.use_mp(skill["cost"]):
            return False, f"Not enough MP! ({self.mp}/{skill['cost']} MP)"

        if skill_index == 0:  # Shield Slam
            raw = int(self.effective_attack() * 1.4)
            dmg = target.take_damage(raw)
            target.apply_buff("atk_buff", turns=2, val=-6)
            SoundManager.play("hit")
            return True, f"{C_CYAN}{self.name}{C_RESET} bashes with {C_WHITE}Shield Slam{C_RESET} for {C_RED}{dmg} damage{C_RESET}! {target.name}'s attack was weakened!"

        elif skill_index == 1:  # Iron Fortress
            healed = self.heal(30)
            self.apply_buff("def_buff", turns=3, val=14)
            SoundManager.play("heal")
            return True, f"{C_CYAN}{self.name}{C_RESET} activates {C_CYAN}Iron Fortress{C_RESET}! Armor hardened (+14 DEF) and restored {C_GREEN}+{healed} HP{C_RESET}!"

        elif skill_index == 2:  # Earthquake
            raw = int(self.effective_attack() * 1.7)
            dmg = target.take_damage(raw, ignore_def_pct=0.60)
            SoundManager.play("crit")
            return True, f"{C_CYAN}{self.name}{C_RESET} triggers a mighty {C_YELLOW}Earthquake{C_RESET}! Cracking the earth for {C_RED}{dmg} armor-piercing damage{C_RESET}!"

        return False, "Error executing skill."


class Mage(Character):
    """
    Mage Role:
    High magical damage with elemental spells and deep mana reserves.
    """
    def __init__(self, name: str):
        super().__init__(
            name=name,
            role="Mage",
            max_hp=85,
            max_mp=100,
            attack=11,
            defense=5,
            speed=12,
            crit_rate=0.12,
            sprite_key="Mage",
            color=C_BLUE
        )

    def get_skills(self) -> list[dict]:
        return [
            {
                "name": "Fireball",
                "cost": 20,
                "desc": "Blazing inferno blast (230% ATK, pierces 40% enemy DEF)."
            },
            {
                "name": "Arcane Heal",
                "cost": 22,
                "desc": "Restores 50 HP through sacred restorative magic."
            },
            {
                "name": "Blizzard Surge",
                "cost": 25,
                "desc": "Freezing gale (160% ATK) with a chance to freeze the enemy."
            }
        ]

    def use_skill(self, skill_index: int, target: Character) -> tuple[bool, str]:
        skills = self.get_skills()
        if skill_index < 0 or skill_index >= len(skills):
            return False, "Invalid skill selection."

        skill = skills[skill_index]
        if not self.use_mp(skill["cost"]):
            return False, f"Not enough MP! ({self.mp}/{skill['cost']} MP)"

        if skill_index == 0:  # Fireball
            raw = int(self.effective_attack() * 2.3)
            dmg = target.take_damage(raw, ignore_def_pct=0.40)
            SoundManager.play("magic")
            return True, f"{C_BLUE}{self.name}{C_RESET} launches a roaring {C_RED}Fireball{C_RESET}! 🔥 Scorch dealt {C_RED}{dmg} magic damage{C_RESET}!"

        elif skill_index == 1:  # Arcane Heal
            healed = self.heal(50)
            SoundManager.play("heal")
            return True, f"{C_BLUE}{self.name}{C_RESET} chants {C_CYAN}Arcane Heal{C_RESET}! Radiant light restores {C_GREEN}+{healed} HP{C_RESET}!"

        elif skill_index == 2:  # Blizzard Surge
            raw = int(self.effective_attack() * 1.6)
            dmg = target.take_damage(raw)
            SoundManager.play("magic")
            freeze_str = ""
            if random.random() < 0.40:
                target.is_defending = True  # Stuns / forces defense
                freeze_str = f" {C_CYAN}{target.name} is FROZEN solid!{C_RESET}"
            return True, f"{C_BLUE}{self.name}{C_RESET} casts {C_CYAN}Blizzard Surge{C_RESET}! ❄️ Dealt {C_RED}{dmg} frost damage{C_RESET}!{freeze_str}"

        return False, "Error executing skill."


class Fighter(Character):
    """
    Fighter Role:
    Well-rounded frontline combatant with powerful physical strikes and durability.
    """
    def __init__(self, name: str):
        super().__init__(
            name=name,
            role="Fighter",
            max_hp=130,
            max_mp=45,
            attack=21,
            defense=12,
            speed=13,
            crit_rate=0.18,
            sprite_key="Fighter",
            color=C_RED
        )

    def get_skills(self) -> list[dict]:
        return [
            {
                "name": "Heavy Cleave",
                "cost": 12,
                "desc": "Brutal broadsword swing dealing 165% ATK damage."
            },
            {
                "name": "Battle Roar",
                "cost": 14,
                "desc": "Rallies strength, boosting ATK (+8 for 3 turns) & heals 20 HP."
            },
            {
                "name": "Berserk Strike",
                "cost": 20,
                "desc": "Devastating smash (240% ATK), but incurs 10 HP self-recoil."
            }
        ]

    def use_skill(self, skill_index: int, target: Character) -> tuple[bool, str]:
        skills = self.get_skills()
        if skill_index < 0 or skill_index >= len(skills):
            return False, "Invalid skill selection."

        skill = skills[skill_index]
        if not self.use_mp(skill["cost"]):
            return False, f"Not enough MP! ({self.mp}/{skill['cost']} MP)"

        if skill_index == 0:  # Heavy Cleave
            raw = int(self.effective_attack() * 1.65)
            dmg = target.take_damage(raw)
            SoundManager.play("hit")
            return True, f"{C_RED}{self.name}{C_RESET} swings with {C_WHITE}Heavy Cleave{C_RESET}! Dealt {C_RED}{dmg} damage{C_RESET}!"

        elif skill_index == 1:  # Battle Roar
            healed = self.heal(20)
            self.apply_buff("atk_buff", turns=3, val=8)
            SoundManager.play("heal")
            return True, f"{C_RED}{self.name}{C_RESET} unleashes a ferocious {C_YELLOW}Battle Roar{C_RESET}! Restored {C_GREEN}+{healed} HP{C_RESET} & ATK increased (+8)!"

        elif skill_index == 2:  # Berserk Strike
            raw = int(self.effective_attack() * 2.4)
            dmg = target.take_damage(raw)
            self.hp = max(1, self.hp - 10)  # Recoil
            SoundManager.play("crit")
            return True, f"{C_RED}{self.name}{C_RESET} delivers an all-out {C_RED}Berserk Strike{C_RESET}! Dealt massive {C_RED}{dmg} damage{C_RESET}! (Took 10 recoil damage)"

        return False, "Error executing skill."


# =============================================================================
# ENEMY CLASSES & AI LOGIC (POLYMORPHIC MONSTERS)
# =============================================================================
class Enemy(Character):
    """Base class for computer-controlled monsters with AI behaviors."""
    def take_turn(self, player: Character) -> str:
        """Determines the enemy's action based on AI heuristics."""
        raise NotImplementedError


class Goblin(Enemy):
    """Stage 1 Encounter: Quick and treacherous scout."""
    def __init__(self):
        super().__init__(
            name="Goblin Sneak",
            role="Monster",
            max_hp=75,
            max_mp=30,
            attack=15,
            defense=5,
            speed=10,
            crit_rate=0.15,
            sprite_key="Goblin",
            color=C_GREEN,
            level=1
        )

    def take_turn(self, player: Character) -> str:
        # If low HP and has mana, attempt a greedy heal
        if self.hp < 25 and self.use_mp(10):
            healed = self.heal(18)
            SoundManager.play("heal")
            return f"{C_GREEN}{self.name}{C_RESET} cackles and gulps stolen brew, restoring {C_GREEN}+{healed} HP{C_RESET}!"

        # Poison player if not already poisoned
        if "poison" not in player.buffs and self.use_mp(12):
            raw = int(self.effective_attack() * 1.1)
            dmg = player.take_damage(raw)
            player.apply_buff("poison", turns=3, val=9)
            SoundManager.play("hit")
            return f"{C_GREEN}{self.name}{C_RESET} spits a {C_GREEN}Poison Dart{C_RESET}! Deals {C_RED}{dmg} damage{C_RESET} and poisons {player.name}!"

        # Default normal attack
        dmg, is_crit, did_hit = self.serang(player)
        if not did_hit:
            return f"{C_GREEN}{self.name}{C_RESET} lunged with a shank, but {C_CYAN}{player.name} dodged{C_RESET}!"
        SoundManager.play("crit" if is_crit else "hit")
        crit_str = f" {C_YELLOW}CRITICAL HIT!{C_RESET}" if is_crit else ""
        return f"{C_GREEN}{self.name}{C_RESET} stabs with a rusty dagger!{crit_str} Dealing {C_RED}{dmg} damage{C_RESET}!"


class SkeletonKnight(Enemy):
    """Stage 2 Encounter: Sturdy undead warrior with defensive buffs."""
    def __init__(self):
        super().__init__(
            name="Skeleton Knight",
            role="Undead",
            max_hp=130,
            max_mp=40,
            attack=22,
            defense=14,
            speed=9,
            crit_rate=0.12,
            sprite_key="Skeleton",
            color=C_WHITE,
            level=2
        )

    def take_turn(self, player: Character) -> str:
        # Buff defense if not already buffed
        if "def_buff" not in self.buffs and self.use_mp(14):
            self.apply_buff("def_buff", turns=3, val=10)
            SoundManager.play("defend")
            return f"{C_WHITE}{self.name}{C_RESET} raises a {C_GRAY}Bone Shield Wall{C_RESET}! (+10 DEF for 3 turns)!"

        # Cursed piercing thrust
        if self.use_mp(16) and random.random() < 0.5:
            raw = int(self.effective_attack() * 1.6)
            dmg = player.take_damage(raw, ignore_def_pct=0.40)
            SoundManager.play("hit")
            return f"{C_WHITE}{self.name}{C_RESET} thrusts with {C_PURPLE}Cursed Blade{C_RESET}! Piercing armor for {C_RED}{dmg} damage{C_RESET}!"

        # Standard bone cleave
        dmg, is_crit, did_hit = self.serang(player)
        if not did_hit:
            return f"{C_WHITE}{self.name}{C_RESET} swings wide! {C_CYAN}{player.name} evaded cleanly{C_RESET}!"
        SoundManager.play("crit" if is_crit else "hit")
        crit_str = f" {C_YELLOW}CRITICAL HIT!{C_RESET}" if is_crit else ""
        return f"{C_WHITE}{self.name}{C_RESET} slashes with an ancient broadsword!{crit_str} Dealing {C_RED}{dmg} damage{C_RESET}!"


class ShadowDragon(Enemy):
    """Stage 3 Final Boss: Calamitous dragon lord of shadow and flame."""
    def __init__(self):
        super().__init__(
            name="Shadow Dragon Lord",
            role="Dragon Boss",
            max_hp=230,
            max_mp=70,
            attack=29,
            defense=18,
            speed=14,
            crit_rate=0.20,
            sprite_key="Dragon",
            color=C_RED,
            level=3
        )

    def take_turn(self, player: Character) -> str:
        # Boss Ultimate: Inferno Breath
        if self.use_mp(24) and random.random() < 0.45:
            raw = int(self.effective_attack() * 1.85)
            dmg = player.take_damage(raw, ignore_def_pct=0.35)
            SoundManager.play("magic")
            return f"{C_RED}{self.name}{C_RESET} breathes {C_YELLOW}HELLFIRE INFERNO{C_RESET}! 🔥 Dealing devastating {C_RED}{dmg} damage{C_RESET}!"

        # Terrifying Dark Roar: weakens player defense
        if self.use_mp(16) and random.random() < 0.35:
            player.apply_buff("def_buff", turns=2, val=-6)
            SoundManager.play("hit")
            return f"{C_RED}{self.name}{C_RESET} emits an ear-shattering {C_PURPLE}Dark Roar{C_RESET}! {player.name}'s defense weakened!"

        # Claw swipe
        dmg, is_crit, did_hit = self.serang(player)
        if not did_hit:
            return f"{C_RED}{self.name}{C_RESET} sweeps with colossal claws, but {C_CYAN}{player.name} dodged{C_RESET}!"
        SoundManager.play("crit" if is_crit else "hit")
        crit_str = f" {C_YELLOW}CRITICAL HIT!{C_RESET}" if is_crit else ""
        return f"{C_RED}{self.name}{C_RESET} rends with razor claws!{crit_str} Dealing {C_RED}{dmg} damage{C_RESET}!"


# =============================================================================
# INVENTORY SYSTEM
# =============================================================================
class Inventory:
    """Manages player supplies and consumable items."""
    def __init__(self, hp_potions: int = 3, mp_potions: int = 2):
        self.hp_potions = hp_potions
        self.mp_potions = mp_potions

    def use_hp_potion(self, character: Character) -> tuple[bool, str]:
        if self.hp_potions <= 0:
            return False, "You have no Health Potions left!"
        if character.hp >= character.max_hp:
            return False, "Your HP is already full!"
        self.hp_potions -= 1
        healed = character.heal(55)
        SoundManager.play("heal")
        return True, f"Drank Health Potion! Restored {C_GREEN}+{healed} HP{C_RESET}. ({self.hp_potions} remaining)"

    def use_mp_potion(self, character: Character) -> tuple[bool, str]:
        if self.mp_potions <= 0:
            return False, "You have no Mana Ethers left!"
        if character.mp >= character.max_mp:
            return False, "Your MP is already full!"
        self.mp_potions -= 1
        restored = character.restore_mp(40)
        SoundManager.play("magic")
        return True, f"Drank Mana Ether! Restored {C_CYAN}+{restored} MP{C_RESET}. ({self.mp_potions} remaining)"


# =============================================================================
# RETRO PIXEL UI RENDERER
# =============================================================================
class PixelRenderer:
    """Renders retro 8-bit frames, pixel art sprites, and health bars."""
    FRAME_WIDTH = 80

    @classmethod
    def clear(cls):
        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def make_bar(cls, current: int, maximum: int, length: int = 18,
                 bar_type: str = "hp") -> str:
        ratio = max(0.0, min(1.0, current / maximum)) if maximum > 0 else 0.0
        filled = int(round(ratio * length))
        empty = length - filled

        if bar_type == "hp":
            if ratio > 0.50:
                color = C_GREEN
            elif ratio > 0.20:
                color = C_YELLOW
            else:
                color = C_RED
        else:
            color = C_CYAN

        bar = f"{color}{'█' * filled}{C_GRAY}{'░' * empty}{C_RESET}"
        return f"{bar} {current:>3}/{maximum:<3}"

    @classmethod
    def center_text(cls, text: str, width: int = 80) -> str:
        clean_len = len(strip_ansi(text))
        pad_left = max(0, (width - clean_len) // 2)
        pad_right = max(0, width - clean_len - pad_left)
        return ' ' * pad_left + text + ' ' * pad_right

    @classmethod
    def format_row(cls, left: str, right: str, width: int = 78) -> str:
        l_len = len(strip_ansi(left))
        r_len = len(strip_ansi(right))
        gap = max(1, width - l_len - r_len)
        return left + (' ' * gap) + right

    @classmethod
    def render_battle_screen(cls, player: Character, enemy: Character,
                             floor: int, logs: list[str]):
        cls.clear()
        W = cls.FRAME_WIDTH

        print(f"{C_BLUE}╔" + "═" * W + f"╗{C_RESET}")

        # Title Header
        title = f"{C_BOLD}{C_YELLOW}⚔️  PIXEL DUNGEON BATTLE — FLOOR {floor}  ⚔️{C_RESET}"
        print(f"{C_BLUE}║{C_RESET}" + cls.center_text(title, W) + f"{C_BLUE}║{C_RESET}")
        print(f"{C_BLUE}╠" + "═" * W + f"╣{C_RESET}")

        # Name and Roles
        p_tag = f"{player.color}[PLAYER]{C_RESET} {C_BOLD}{player.name}{C_RESET} ({player.role} Lv.{player.level})"
        e_tag = f"{enemy.color}[ENEMY]{C_RESET} {C_BOLD}{enemy.name}{C_RESET} (Lv.{enemy.level})"
        print(f"{C_BLUE}║{C_RESET} " + cls.format_row(p_tag, e_tag, W - 2) + f" {C_BLUE}║{C_RESET}")

        # HP Bars
        p_hp = f"HP: {cls.make_bar(player.hp, player.max_hp, 18, 'hp')}"
        e_hp = f"HP: {cls.make_bar(enemy.hp, enemy.max_hp, 18, 'hp')}"
        print(f"{C_BLUE}║{C_RESET} " + cls.format_row(p_hp, e_hp, W - 2) + f" {C_BLUE}║{C_RESET}")

        # MP Bars / Stats
        p_mp = f"MP: {cls.make_bar(player.mp, player.max_mp, 18, 'mp')}"
        e_mp = f"ATK:{enemy.attack:<2} DEF:{enemy.effective_defense():<2} SPD:{enemy.speed:<2}"
        print(f"{C_BLUE}║{C_RESET} " + cls.format_row(p_mp, e_mp, W - 2) + f" {C_BLUE}║{C_RESET}")

        # Buff Status
        p_buffs = []
        if player.is_defending: p_buffs.append(f"{C_CYAN}[🛡️GUARD]{C_RESET}")
        for b_name, b_info in player.buffs.items():
            if b_name == "poison": p_buffs.append(f"{C_GREEN}[☠POISON {b_info['turns']}t]{C_RESET}")
            elif b_name == "atk_buff": p_buffs.append(f"{C_RED}[⚔ATK+{b_info['val']} {b_info['turns']}t]{C_RESET}")
            elif b_name == "def_buff": p_buffs.append(f"{C_CYAN}[🛡DEF+{b_info['val']} {b_info['turns']}t]{C_RESET}")
        p_buff_str = " ".join(p_buffs) if p_buffs else f"{C_GRAY}(No Status){C_RESET}"

        e_buffs = []
        if enemy.is_defending: e_buffs.append(f"{C_CYAN}[🛡️GUARD]{C_RESET}")
        for b_name, b_info in enemy.buffs.items():
            if b_name == "poison": e_buffs.append(f"{C_GREEN}[☠POISON {b_info['turns']}t]{C_RESET}")
            elif b_name == "atk_buff": e_buffs.append(f"{C_RED}[⚔ATK+{b_info['val']} {b_info['turns']}t]{C_RESET}")
            elif b_name == "def_buff": e_buffs.append(f"{C_CYAN}[🛡DEF+{b_info['val']} {b_info['turns']}t]{C_RESET}")
        e_buff_str = " ".join(e_buffs) if e_buffs else f"{C_GRAY}(Normal){C_RESET}"

        print(f"{C_BLUE}║{C_RESET} " + cls.format_row(p_buff_str, e_buff_str, W - 2) + f" {C_BLUE}║{C_RESET}")
        print(f"{C_BLUE}║{C_RESET}" + " " * W + f"{C_BLUE}║{C_RESET}")

        # Pixel Art Arena (Side-by-side sprites dynamically aligned)
        p_sprite = player.sprite
        e_sprite = enemy.sprite
        side_pad = 8
        mid_pad = max(2, W - 32 - side_pad * 2)
        for pl, el in zip(p_sprite, e_sprite):
            line_content = " " * side_pad + pl + " " * mid_pad + el + " " * side_pad
            print(f"{C_BLUE}║{C_RESET}" + line_content + f"{C_BLUE}║{C_RESET}")

        print(f"{C_BLUE}║{C_RESET}" + " " * W + f"{C_BLUE}║{C_RESET}")
        print(f"{C_BLUE}╠" + "═" * W + f"╣{C_RESET}")

        # Battle Event Log (Displays last 3 messages)
        recent_logs = logs[-3:] if logs else [" Battle begins! Prepare your moves."]
        while len(recent_logs) < 3:
            recent_logs.insert(0, "")

        for log in recent_logs:
            if log:
                line_str = f" > {log}"
            else:
                line_str = ""
            c_len = len(strip_ansi(line_str))
            pad = max(0, W - 2 - c_len)
            print(f"{C_BLUE}║{C_RESET} " + line_str + " " * pad + f" {C_BLUE}║{C_RESET}")

        print(f"{C_BLUE}╠" + "═" * W + f"╣{C_RESET}")


# =============================================================================
# BATTLE ENGINE (TURN-BASED COMBAT LOOP)
# =============================================================================
class BattleEngine:
    """
    Manages the turn-based duel between the player and an enemy.
    Determines turn initiative based on Speed.
    """
    def __init__(self, player: Character, enemy: Enemy, floor: int, inventory: Inventory):
        self.player = player
        self.enemy = enemy
        self.floor = floor
        self.inventory = inventory
        self.logs: list[str] = [f"A wild {enemy.color}{enemy.name}{C_RESET} blocks your path!"]

    def run(self) -> bool:
        """Executes the combat loop until victory or defeat. Returns True if player won."""
        round_count = 1

        while self.player.is_alive() and self.enemy.is_alive():
            PixelRenderer.render_battle_screen(self.player, self.enemy, self.floor, self.logs)

            # Prompt player action
            action_result = self.handle_player_turn()
            if action_result == "quit":
                return False

            # Check if enemy was defeated by player action
            if not self.enemy.is_alive():
                break

            # Enemy counter-turn
            PixelRenderer.render_battle_screen(self.player, self.enemy, self.floor, self.logs)
            time.sleep(0.7)
            self.handle_enemy_turn()

            # End of round processing (buff countdowns, poison ticks)
            p_logs = self.player.start_turn()
            e_logs = self.enemy.start_turn()
            self.logs.extend(p_logs)
            self.logs.extend(e_logs)

            round_count += 1
            time.sleep(0.5)

        # Final battle state rendering
        PixelRenderer.render_battle_screen(self.player, self.enemy, self.floor, self.logs)

        if self.player.is_alive():
            SoundManager.play("victory")
            time.sleep(0.8)
            return True
        else:
            SoundManager.play("game_over")
            time.sleep(0.8)
            return False

    def handle_player_turn(self) -> str:
        """Processes user input for the current round."""
        while True:
            W = PixelRenderer.FRAME_WIDTH
            menu_str = f" {C_BOLD}[1]{C_RESET} ⚔️ Attack   {C_BOLD}[2]{C_RESET} ✨ Skill   {C_BOLD}[3]{C_RESET} 🛡️ Guard   {C_BOLD}[4]{C_RESET} 🧪 Items   {C_BOLD}[5]{C_RESET} 📊 Stats"
            pad = max(0, W - len(strip_ansi(menu_str)))
            print(f"{C_BLUE}║{C_RESET}" + menu_str + " " * pad + f"{C_BLUE}║{C_RESET}")
            print(f"{C_BLUE}╚" + "═" * W + f"╝{C_RESET}")

            choice = input(f"{C_YELLOW}Choose action (1-5): {C_RESET}").strip()
            SoundManager.play("select")

            if choice == "1":
                # Standard Attack
                dmg, is_crit, did_hit = self.player.serang(self.enemy)
                if not did_hit:
                    self.logs.append(f"{self.player.color}{self.player.name}{C_RESET} attacked, but {self.enemy.name} swiftly dodged!")
                else:
                    SoundManager.play("crit" if is_crit else "hit")
                    crit_tag = f" {C_YELLOW}CRITICAL HIT!{C_RESET}" if is_crit else ""
                    self.logs.append(f"{self.player.color}{self.player.name}{C_RESET} strikes with {C_WHITE}Basic Attack{C_RESET}!{crit_tag} Deals {C_RED}{dmg} damage{C_RESET}!")
                return "acted"

            elif choice == "2":
                # Skills Menu
                skills = self.player.get_skills()
                print(f"\n{C_CYAN}--- {self.player.role.upper()} SKILLS (MP: {self.player.mp}/{self.player.max_mp}) ---{C_RESET}")
                for idx, sk in enumerate(skills, start=1):
                    print(f" [{idx}] {C_YELLOW}{sk['name']}{C_RESET} ({C_CYAN}{sk['cost']} MP{C_RESET}) - {sk['desc']}")
                print(" [0] Cancel / Back")

                s_choice = input(f"{C_YELLOW}Select skill (0-{len(skills)}): {C_RESET}").strip()
                SoundManager.play("select")
                if s_choice == "0" or not s_choice.isdigit():
                    PixelRenderer.render_battle_screen(self.player, self.enemy, self.floor, self.logs)
                    continue

                s_idx = int(s_choice) - 1
                success, msg = self.player.use_skill(s_idx, self.enemy)
                if not success:
                    print(f"{C_RED}{msg}{C_RESET}")
                    time.sleep(1.0)
                    PixelRenderer.render_battle_screen(self.player, self.enemy, self.floor, self.logs)
                    continue

                self.logs.append(msg)
                return "acted"

            elif choice == "3":
                # Defend Stance
                self.player.defend()
                SoundManager.play("defend")
                self.logs.append(f"{self.player.color}{self.player.name}{C_RESET} takes a {C_CYAN}Defensive Stance{C_RESET}! Defense doubled & +10 MP restored!")
                return "acted"

            elif choice == "4":
                # Items Menu
                print(f"\n{C_GREEN}--- INVENTORY ---{C_RESET}")
                print(f" [1] Health Potion ({self.inventory.hp_potions} remaining) - Heals 55 HP")
                print(f" [2] Mana Ether    ({self.inventory.mp_potions} remaining) - Restores 40 MP")
                print(" [0] Cancel / Back")

                i_choice = input(f"{C_YELLOW}Use item (0-2): {C_RESET}").strip()
                SoundManager.play("select")
                if i_choice == "1":
                    success, msg = self.inventory.use_hp_potion(self.player)
                    if not success:
                        print(f"{C_RED}{msg}{C_RESET}")
                        time.sleep(1.0)
                        PixelRenderer.render_battle_screen(self.player, self.enemy, self.floor, self.logs)
                        continue
                    self.logs.append(f"{self.player.color}{self.player.name}{C_RESET} {msg}")
                    return "acted"
                elif i_choice == "2":
                    success, msg = self.inventory.use_mp_potion(self.player)
                    if not success:
                        print(f"{C_RED}{msg}{C_RESET}")
                        time.sleep(1.0)
                        PixelRenderer.render_battle_screen(self.player, self.enemy, self.floor, self.logs)
                        continue
                    self.logs.append(f"{self.player.color}{self.player.name}{C_RESET} {msg}")
                    return "acted"
                else:
                    PixelRenderer.render_battle_screen(self.player, self.enemy, self.floor, self.logs)
                    continue

            elif choice == "5":
                # Show full statistics
                self.player.tampilkan_info()
                self.enemy.tampilkan_info()
                input(f"\n{C_GRAY}Press Enter to return to battle...{C_RESET}")
                PixelRenderer.render_battle_screen(self.player, self.enemy, self.floor, self.logs)

            else:
                print(f"{C_RED}Invalid option! Enter 1, 2, 3, 4, or 5.{C_RESET}")
                time.sleep(0.6)
                PixelRenderer.render_battle_screen(self.player, self.enemy, self.floor, self.logs)

    def handle_enemy_turn(self):
        """Executes the monster's turn action."""
        if not self.enemy.is_alive():
            return
        msg = self.enemy.take_turn(self.player)
        self.logs.append(msg)


# =============================================================================
# GAME CONTROLLER & CAMPAIGN
# =============================================================================
class Game:
    """Coordinates character creation, dungeon progression, and victory screens."""

    @staticmethod
    def print_title():
        PixelRenderer.clear()
        title_art = f"""{C_RED}
  ██████╗ ██╗██╗  ██╗███████╗██╗         ██████╗ ██████╗  ██████╗ 
  ██╔══██╗██║██║ ██╔╝██╔════╝██║         ██╔══██╗██╔══██╗██╔════╝ 
  ██████╔╝██║█████╔╝ █████╗  ██║         ██████╔╝██████╔╝██║  ███╗
  ██╔═══╝ ██║██╔═██╗ ██╔══╝  ██║         ██╔══██╗██╔═══╝ ██║   ██║
  ██║     ██║██║  ██╗███████╗███████╗    ██║  ██║██║     ╚██████╔╝
  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝      ╚═════╝ {C_RESET}
      {C_YELLOW}⚔️   AN 8-BIT RETRO TURN-BASED OOP ADVENTURE   ⚔️{C_RESET}
        """
        print(title_art)

    @classmethod
    def create_character(cls) -> Character:
        cls.print_title()
        print(f"{C_BOLD}{C_WHITE}Create Your Hero:{C_RESET}")
        name = input(f"{C_CYAN}Enter hero name: {C_RESET}").strip()
        if not name:
            name = "Hero"

        print(f"\n{C_YELLOW}SELECT YOUR CLASS ROLE:{C_RESET}")
        print(f" {C_BOLD}[1] Assassin{C_RESET}  - {C_PURPLE}High Crit & Agility (HP:95, ATK:26, DEF:6, SPD:18, CRIT:35%){C_RESET}")
        print(f" {C_BOLD}[2] Tank{C_RESET}      - {C_CYAN}High Defense & Vitality (HP:170, ATK:15, DEF:20, SPD:7, CRIT:5%){C_RESET}")
        print(f" {C_BOLD}[3] Mage{C_RESET}      - {C_BLUE}High Magic Burst & Mana (HP:85, MP:100, ATK:11, DEF:5, SPD:12){C_RESET}")
        print(f" {C_BOLD}[4] Fighter{C_RESET}   - {C_RED}Balanced Power & Tenacity (HP:130, ATK:21, DEF:12, SPD:13, CRIT:18%){C_RESET}")

        while True:
            choice = input(f"\n{C_YELLOW}Choose role (1-4): {C_RESET}").strip()
            SoundManager.play("select")
            if choice == "1":
                return Assassin(name)
            elif choice == "2":
                return Tank(name)
            elif choice == "3":
                return Mage(name)
            elif choice == "4":
                return Fighter(name)
            else:
                print(f"{C_RED}Please choose 1, 2, 3, or 4!{C_RESET}")

    @classmethod
    def start(cls):
        while True:
            cls.print_title()
            print(" [1] ⚔️ Start Dungeon Run (Terminal Retro Pixel)")
            print(" [2] 🖥️ Launch Windowed GUI Mode (Tkinter Canvas)")
            print(" [3] 🔊 Toggle 8-Bit Sound (Currently: " + (f"{C_GREEN}ON{C_RESET}" if SoundManager.enabled else f"{C_RED}OFF{C_RESET}") + ")")
            print(" [4] 🚪 Exit")

            menu_choice = input(f"\n{C_YELLOW}Select option: {C_RESET}").strip()
            if menu_choice == "2":
                try:
                    import gui_game
                    print(f"\n{C_CYAN}Launching Windowed GUI Pixel Game...{C_RESET}")
                    gui_game.run_gui()
                except Exception as e:
                    print(f"{C_RED}Could not open GUI: {e}{C_RESET}")
                    time.sleep(1.5)
                continue
            elif menu_choice == "3":
                SoundManager.enabled = not SoundManager.enabled
                continue
            elif menu_choice == "4":
                print("\nFarewell, traveler!")
                sys.exit(0)
            elif menu_choice == "1":
                break

        player = cls.create_character()
        inventory = Inventory(hp_potions=3, mp_potions=2)

        # Dungeon stages
        stages = [
            ("Floor 1: Whispering Woods", Goblin()),
            ("Floor 2: Cursed Crypt", SkeletonKnight()),
            ("Floor 3: Dragon's Spire (BOSS)", ShadowDragon())
        ]

        for floor_num, (stage_name, enemy) in enumerate(stages, start=1):
            PixelRenderer.clear()
            W = PixelRenderer.FRAME_WIDTH
            print(f"\n{C_YELLOW}╔" + "═" * W + f"╗{C_RESET}")
            print(f"{C_YELLOW}║{C_RESET}" + PixelRenderer.center_text(f"ENTERING {stage_name.upper()}", W) + f"{C_YELLOW}║{C_RESET}")
            print(f"{C_YELLOW}╚" + "═" * W + f"╝{C_RESET}")
            time.sleep(1.2)

            battle = BattleEngine(player, enemy, floor_num, inventory)
            won = battle.run()

            if not won:
                cls.show_game_over(player, stage_name)
                return

            # Victorious!
            if floor_num < len(stages):
                cls.show_stage_clear(player, floor_num, inventory)

        cls.show_grand_victory(player)

    @classmethod
    def show_stage_clear(cls, player: Character, floor_num: int, inventory: Inventory):
        PixelRenderer.clear()
        W = PixelRenderer.FRAME_WIDTH
        print(f"\n{C_GREEN}╔" + "═" * W + f"╗{C_RESET}")
        print(f"{C_GREEN}║{C_RESET}" + PixelRenderer.center_text("✨ FLOOR CLEARED! LEVEL UP! ✨", W) + f"{C_GREEN}║{C_RESET}")
        print(f"{C_GREEN}╚" + "═" * W + f"╝{C_RESET}")

        player.level_up()
        inventory.hp_potions += 1
        inventory.mp_potions += 1

        print(f"\n  {player.color}{player.name}{C_RESET} has reached {C_YELLOW}Level {player.level}{C_RESET}!")
        print(f"  {C_GREEN}+25 Max HP{C_RESET} | {C_CYAN}+15 Max MP{C_RESET} | {C_RED}+4 ATK{C_RESET} | {C_CYAN}+3 DEF{C_RESET} | {C_YELLOW}+2 SPD{C_RESET}")
        print(f"  {C_YELLOW}HP and MP fully restored!{C_RESET}")
        print(f"  Looted: {C_GREEN}+1 Health Potion{C_RESET}, {C_CYAN}+1 Mana Ether{C_RESET}!")

        input(f"\n{C_GRAY}Press Enter to advance to the next floor...{C_RESET}")

    @classmethod
    def show_grand_victory(cls, player: Character):
        PixelRenderer.clear()
        trophy = f"""{C_YELLOW}
             ___________
            '._==_==_=_.'
            .-\\:      /-.
           | (|:.     |) |
            '-|:.     |-'
              \\::.    /
               '::. .'
                 ) (
               _.' '._
              `\"\"\"\"\"\"\"`
        {C_RESET}"""
        print(trophy)
        print(f"{C_BOLD}{C_GREEN}CONGRATULATIONS, {player.name.upper()}!{C_RESET}")
        print(f"{C_WHITE}You defeated the Shadow Dragon Lord and conquered the Pixel Dungeon!{C_RESET}")
        print(f"Final Stats: Level {player.level} {player.role} | HP: {player.hp}/{player.max_hp} | MP: {player.mp}/{player.max_mp}")
        print(f"\n{C_CYAN}Thank you for playing Pixel Realms OOP Edition!{C_RESET}")
        input(f"\n{C_GRAY}Press Enter to return to main menu...{C_RESET}")
        cls.start()

    @classmethod
    def show_game_over(cls, player: Character, stage_name: str):
        PixelRenderer.clear()
        skull = f"""{C_RED}
             ▄████████▄
            ███  ██  ███
            ████████████
             ▀██ ▀▀ ██▀
              ████████
               █ █ █ █
        {C_RESET}"""
        print(skull)
        print(f"{C_BOLD}{C_RED}GAME OVER...{C_RESET}")
        print(f"{player.name} fell in battle at {stage_name}.")
        retry = input(f"\n{C_YELLOW}Would you like to try again? (y/n): {C_RESET}").strip().lower()
        if retry == 'y':
            cls.start()
        else:
            print("\nThanks for playing! See you next time.")
            sys.exit(0)


# =============================================================================
# BACKWARDS COMPATIBILITY WITH USER STARTER CODE
# =============================================================================
karakter = Character

def make_char():
    """Preserves user's original starter function signature."""
    return Game.create_character()


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    try:
        Game.start()
    except KeyboardInterrupt:
        print("\n\nGame closed. Goodbye!")
        sys.exit(0)
