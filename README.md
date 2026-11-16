# ⚔️ Pixel Realms: Turn-Based RPG (OOP Edition)

A retro 8-bit turn-based pixel RPG built in Python to showcase **Object-Oriented Programming (OOP)** principles.

---

## 🕹️ How to Play

You can play in either **Terminal Mode** or **Windowed GUI Mode**:

### Option 1: Terminal Mode (Retro ANSI Pixel Graphics)
Run the game directly in your terminal:
```bash
python main.py
```
*Features retro ANSI pixel art sprites, real-time health/mana bars, combat dialogue boxes, and 8-bit chiptune sound effects.*

### Option 2: Windowed GUI Mode (Tkinter Canvas)
Run the graphic arcade window:
```bash
python gui_game.py
```
*(Or launch it from the `[2]` menu option inside `main.py`!)*

---

## 🎭 Roles & Specific Stats

| Role | HP | MP | ATK | DEF | SPD | CRIT | Playstyle & Signature Skills |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Assassin** | `95` | `50` | `26` | `6` | `18` | `35%` | **High Crit & Agility:** Attacks first and dodges attacks. Skills: *Shadow Strike*, *Poison Blade*, *Smoke Bomb*. |
| **Tank** | `170` | `35` | `15` | `20` | `7` | `5%` | **High Armor & Vitality:** Absorbs heavy blows with high damage reduction. Skills: *Shield Slam*, *Iron Fortress*, *Earthquake*. |
| **Mage** | `85` | `100` | `11` | `5` | `12` | `12%` | **Arcane Glass Cannon:** Deep mana reserves and piercing magical bursts. Skills: *Fireball*, *Arcane Heal*, *Blizzard Surge*. |
| **Fighter** | `130` | `45` | `21` | `12` | `13` | `18%` | **Balanced Frontliner:** High physical damage with self-sustain. Skills: *Heavy Cleave*, *Battle Roar*, *Berserk Strike*. |

---

## 🏰 Dungeon Progression & Enemies

1. **Floor 1: Whispering Woods** — Face the treacherous `Goblin Sneak` *(uses poisonous darts and sneaky bites)*.
2. **Floor 2: Cursed Crypt** — Battle the sturdy `Skeleton Knight` *(raises bone shield walls and pierces armor)*.
3. **Floor 3: Dragon's Spire (BOSS)** — Slay the mighty `Shadow Dragon Lord` *(unleashes hellfire infernos and dark roars)*!

### 🌟 Level Up System
Defeating each monster grants a **Level Up**, fully restoring your HP and MP, increasing your maximum stats, and awarding bonus potions!

---

## 🧠 OOP Architecture

- **Inheritance:** `Character` is the base class containing all combat logic. Subclasses (`Assassin`, `Tank`, `Mage`, `Fighter`, and `Enemy`) inherit from it.
- **Polymorphism:** Each role overrides `get_skills()` and `use_skill()` to implement unique mechanics, while enemies implement `take_turn()` with distinct AI strategies.
- **Encapsulation:** Stat changes (HP, MP, damage calculations, and buff durations) are safely managed through methods like `take_damage()`, `heal()`, and `use_mp()`.
- **Code Reusability:** Both the Terminal version (`main.py`) and the Graphical GUI version (`gui_game.py`) share the exact same OOP classes without duplicating game logic.
