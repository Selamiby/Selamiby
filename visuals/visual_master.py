import os
import random
import sys

# Production katmanlarını eklemek için yolu ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from production.nexus_layer_combat import Character, CombatMode, Enemy
from production.nexus_layer_economy import NexusOneEconomy
from production.nexus_layer_unique import Inventory, loot_master

# --- NEXUS VISUAL MASTER: JIANGHENG EDITION ---
app = Ursina()
application.asset_folder = os.path.abspath(os.path.dirname(__file__)) 
application.development_mode = False

# --- LOGIC INITIALIZATION ---
# Load config for economy
config_path = os.path.join(os.path.dirname(__file__), '..', 'nexus_one_config.json')
with open(config_path, 'r') as f:
    config_data = json.load(f)

player_logic = Character("Sovereign", 99, 0, 25430, 500, 200)
player_inventory = Inventory()
economy_logic = NexusOneEconomy(config_data)
current_enemy = Enemy("Chaos Wraith", 50, 5000, 100, 50)

# Window Setup
window.title = "NEXUS-ONE: JIANGHENG (The Great Dissonance)"
window.borderless = False
window.fullscreen = False
window.color = color.black
window.fps_counter.enabled = True

# Atmosphere
Sky(color=color.black)
Entity(model='sphere', scale=500, double_sided=True, color=color.dark_gray, alpha=0.1) # Nebula effect

# Lighting
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, 1))

# --- WORLD GEOMETRY ---
# Using primitives to avoid file system globbing issues
ground = Entity(model='cube', scale=(200, 1, 200), y=-1, texture='white_cube', color=color.hex('#1a1a1a'))

# Floating Structures (Elite Chinese Cyber-Fantasy)
for i in range(50):
    pillar = Entity(
        model='cube',
        position=(random.uniform(-40, 40), random.uniform(0, 20), random.uniform(-40, 40)),
        scale=(random.uniform(0.5, 2), random.uniform(5, 15), random.uniform(0.5, 2)),
        color=color.cyan if random.random() > 0.5 else color.magenta,
        alpha=0.7
    )
    pillar.animate_y(pillar.y + 2, duration=3, loop=True, curve=curve.in_out_sine)

# The "Nexus Core"
core = Entity(model='sphere', scale=5, color=color.gold, alpha=0.9, position=(0, 10, 0))
core_light = PointLight(parent=core, color=color.gold, range=30)

# The Enemy Visual
enemy_visual = Entity(
    model='sphere', 
    scale=3, 
    color=color.red, 
    position=(10, 5, 10), 
    double_sided=True,
    collider='sphere'
)
enemy_hp_bar = HealthBar(parent=enemy_visual, y=1.5, scale=(1.5, .1))

# Particles
for _ in range(100):
    Entity(
        model='cube',
        scale=0.1,
        position=(random.uniform(-50, 50), random.uniform(0, 30), random.uniform(-50, 50)),
        color=color.white,
        alpha=0.5
    ).animate_y(50, duration=random.uniform(5, 10), loop=True)

# --- SOVEREIGN UI ---
Text(text='[ NEXUS-ONE: JIANGHENG ]', position=(-0.85, 0.45), scale=2, color=color.gold)
wealth_text = Text(text='Wealth: $1,800 / 7 Days (Target)', position=(-0.85, 0.4), color=color.green)
status_text = Text(text='Status: Sovereign Evolution Active', position=(-0.85, 0.35), color=color.cyan)

# --- RPG HUD ELEMENTS (Mobile/Professional Look) ---
# HP Bar (Top Left)
hp_bg = Entity(parent=camera.ui, model='quad', scale=(0.4, 0.03), position=(-0.65, 0.3), color=color.black66)
hp_bar = Entity(parent=hp_bg, model='quad', scale=(0.98, 0.8), position=(0, 0), color=color.red, origin=(-0.5, 0))
hp_text = Text(parent=hp_bg, text='HP: 25,430 / 25,430', scale=0.7, position=(-0.05, 0.03))

# MP Bar (Below HP)
mp_bg = Entity(parent=camera.ui, model='quad', scale=(0.35, 0.02), position=(-0.675, 0.26), color=color.black66)
mp_bar = Entity(parent=mp_bg, model='quad', scale=(0.98, 0.8), position=(0, 0), color=color.azure, origin=(-0.5, 0))

# Level Indicator
level_circle = Entity(parent=camera.ui, model='circle', scale=0.08, position=(-0.85, 0.28), color=color.gold)
level_text = Text(parent=level_circle, text='99', scale=5, position=(-0.1, 0.1), color=color.black)

# --- INVENTORY SYSTEM ---
inv_panel = WindowPanel(
    title='Inventory',
    content=(
        Text('Items will appear here...'),
    ),
    enabled=False,
    position=(-0.25, 0.25),
    scale=(0.4, 0.5)
)

def toggle_inventory():
    inv_panel.enabled = not inv_panel.enabled
    if inv_panel.enabled:
        # Refresh Content
        for child in inv_panel.content:
            if isinstance(child, Text):
                items_str = "\n".join([str(i) for i in player_inventory.items]) or "Empty"
                child.text = f"Backpack:\n{items_str}"

inv_btn = Button(
    text='BAG',
    parent=camera.ui,
    scale=(0.1, 0.05),
    position=(0.75, -0.45),
    color=color.black66,
    on_click=toggle_inventory
)

# Skill Buttons (Bottom Right - Circular Layout)
skills = ['Fire', 'Ice', 'Void', 'Ultimate']
skill_btns = []

def cast_skill(skill_name):
    if not current_enemy or current_enemy.hp <= 0:
        return

    print(f"Casting {skill_name}!")
    damage = player_logic.attack * (3 if skill_name == 'Ultimate' else 1.5)
    
    # Logic Update
    is_alive = current_enemy.update_hp(-damage)
    
    # Visual Effects
    core.shake(duration=0.3, magnitude=1)
    enemy_visual.blink(color.white, duration=0.2)
    
    # Create an effect entity
    effect = Entity(model='sphere', color=color.cyan, scale=0.1, position=player.position)
    effect.animate_position(enemy_visual.position, duration=0.2, curve=curve.linear)
    destroy(effect, delay=0.3)

    if not is_alive:
        print("Enemy defeated!")
        status_text.text = f"Status: Defeated {current_enemy.name}"
        enemy_visual.animate_scale(0, duration=0.5)
        # Give rewards
        wealth_text.text = f'Wealth: ${int(wealth_text.text.split("$")[1].split(" ")[0].replace(",", "")) + 500:,} / 7 Days (Target)'

for i, name in enumerate(skills):
    btn = Button(
        text='', 
        parent=camera.ui, 
        scale=0.1, 
        position=(0.7 - (i*0.12), -0.35 + (i*0.05) if i < 3 else -0.2),
        color=color.orange if name == 'Ultimate' else color.gray,
        highlight_color=color.lime,
        radius=0.5
    )
    btn.on_click = lambda n=name: cast_skill(n)
    Text(parent=btn, text=name[0], scale=4, position=(-0.1, 0.1))
    skill_btns.append(btn)

# Mini-map Placeholder (Top Right)
minimap = Entity(parent=camera.ui, model='quad', scale=0.2, position=(0.75, 0.35), color=color.black66, texture='white_cube')
minimap_border = Entity(parent=minimap, model='quad', scale=1.05, z=0.1, color=color.gold)

# Player
player = FirstPersonController()
player.cursor.visible = True

def update():
    core.rotation_y += 50 * time.dt
    core.rotation_x += 20 * time.dt
    
    if current_enemy and current_enemy.hp > 0:
        enemy_visual.look_at(player)
        enemy_hp_bar.value = (current_enemy.hp / 5000) * 100
    
    # Update Player UI from Logic
    hp_bar.scale_x = (player_logic.hp / 25430) * 0.98
    hp_text.text = f'HP: {int(player_logic.hp)} / 25,430'
    level_text.text = str(player_logic.level)

    # Simple combat loop simulation
    if current_enemy and current_enemy.hp > 0:
        # Enemy attacks back occasionally
        if random.random() > 0.99:
            player_logic.update_hp(-20)
            camera.shake(duration=0.1, magnitude=0.1)
    
app.run()
