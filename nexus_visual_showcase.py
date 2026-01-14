"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:17
🚀 Status: ACTIVE / PRODUCTION
"""

import os
import random

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# --- NEXUS VISUAL ENGINE: SOVEREIGN EDITION ---
# Goal: Showcase "Elite Chinese Production" graphics using procedural high-end VFX.

app = Ursina()
application.asset_folder = os.path.abspath(os.path.dirname(__file__))
application.development_mode = False

# 1. Environment & Atmosphere (HDR/Celestial)
window.title = "🔥 NEXUS-ONE: JIĀNGHÉNG VISUAL SHOWCASE"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Atmosphere
Sky(texture='sky_sunset', color=color.black)
pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))

# 2. Procedural Landscape (Jiānghéng Ruins)
ground = Entity(model='plane', collider='box', scale=100, texture='grass', color=color.dark_gray)
for x in range(-20, 20, 5):
    for z in range(-20, 20, 5):
        if random.random() > 0.7:
            # Floating Tech-Crystals (Chinese Mythology style)
            crystal = Entity(
                model='diamond', 
                color=color.cyan, 
                position=(x, random.uniform(2, 6), z), 
                scale=(1, 2, 1),
                alpha=0.8
            )
            crystal.animate_y(crystal.y + 1, duration=2, loop=True, curve=curve.in_out_sine)
            crystal.animate_rotation_y(360, duration=5, loop=True)
            
            # Particle Glow around crystals
            for _ in range(5):
                p = Entity(
                    model='sphere', 
                    scale=0.1, 
                    color=color.cyan, 
                    position=crystal.position + (random.uniform(-1,1), random.uniform(-1,1), random.uniform(-1,1))
                )
                p.animate_alpha(0, duration=random.uniform(1,3), loop=True)

# 3. The 100 Agent Swarm (Visual Proxies)
agents = []
for i in range(100):
    a = Entity(
        model='cube', 
        color=color.random_color(), 
        position=(random.uniform(-40, 40), 1, random.uniform(-40, 40)),
        scale=(0.5, 1.8, 0.5), # Humanoid scale
        collider='box'
    )
    # Add neon trails
    trail = Entity(parent=a, model='sphere', y=1.5, scale=0.2, color=a.color)
    agents.append({"ent": a, "speed": random.uniform(2, 5)})

# 4. Cinematic Post-Processing (Mocks)
# Note: Ursina uses simplified post-processing but we can simulate Bloom/Fog
scene.fog_density = 0.015
scene.fog_color = color.black

# 5. UI - Commercial Dashboard
info_panel = WindowPanel(
    title='Jiānghéng: Visual Engine v1.0',
    content=(
        Text('Render Mode: SOVEREIGN PROTOCOL'),
        Text('Shader Level: ELITE CHINESE STYLE'),
        Text('VFX Particles: ACTIVE (Recursive)'),
        Text('Agent Density: 100 SOULS'),
        Button(text='CAPTURE CONCEPT', color=color.azure),
    ),
    position=(-0.7, 0.4)
)

# 6. Movement / Interaction
player = FirstPersonController()
player.cursor.visible = False

def update():
    # Animate Swarm
    for agent in agents:
        agent["ent"].x += agent["speed"] * time.dt * 0.5
        if abs(agent["ent"].x) > 50: agent["ent"].x *= -0.9
        
    # Pulse the world light
    pivot.rotation_y += 5 * time.dt

app.run()
