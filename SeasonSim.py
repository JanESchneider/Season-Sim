# -*- coding: utf-8 -*-
import os
os.environ['AUTOBAHN_USE_NVX'] = '0'

from vpython import *
import math

# 1. Setup Scene
scene = canvas(title="<b>SeasonSim v0.9</b>", 
               width=1000, height=700, background=color.black)
scene.lights = []
scene.ambient = color.gray(0.1)
sun_light = local_light(pos=vector(0,0,0), color=color.white)

# 2. Global State
state = {
    'running': True,
    'orbit_speed': 0.005,
    'show_lines': False,
    'focus_north': True,
    'theta': 0
}
ORBIT_RADIUS = 50
DAYS_PER_YEAR = 40 

# 3. UI Functions
def toggle_run(b):
    state['running'] = not state['running']
    b.text = "PAUSE" if state['running'] else "START"
    b.background = color.red if state['running'] else color.green

def set_speed(s):
    state['orbit_speed'] = s.value

def toggle_lines(b):
    state['show_lines'] = not state['show_lines']
    for line in earth_lines: line.visible = state['show_lines']
    b.text = "Linien: AN" if state['show_lines'] else "Linien: AUS"

def toggle_hem(b):
    state['focus_north'] = not state['focus_north']
    b.text = "Fokus: NORD" if state['focus_north'] else "Fokus: SÜD"

def reset_sim():
    state['theta'] = 0
    scene.camera.follow(None)
    scene.center = vector(0,0,0)

# 4. DASHBOARD LAYOUT
scene.append_to_caption("<br><b>STEUERUNG</b><br>")
button(text="PAUSE", bind=toggle_run, background=color.red, color=color.white)
scene.append_to_caption(" ")
button(text="Reset", bind=reset_sim)

scene.append_to_caption("<br><br><b>ANSICHT</b><br>")

# --- HOVER FLAG FOR HEMISPHERE ---
scene.append_to_caption("<span title='Erklärungen der Jahreszeiten relativ für Nord-/Südhalbkugel.'>")
button(text="Fokus: NORD", bind=toggle_hem)
scene.append_to_caption("</span> ")

# --- HOVER FLAG FOR LINES ---
scene.append_to_caption("<span title='Ein- und Ausblenden von Äquator (weiß), Wendekreisen (gelb) und Polarkreisen (cyan).'>")
button(text="Linien: AUS", bind=toggle_lines)
scene.append_to_caption("</span>")

scene.append_to_caption("<br><br><b>GESCHWINDIGKEIT</b><br>")
slider(min=0, max=0.02, value=0.005, bind=set_speed)

scene.append_to_caption("<br><br><hr><b>DETAILS</b><br>")
info_box = wtext(text="<div style='background-color: #1a1a1a; color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #444;'>Bereit...</div>") 
scene.append_to_caption("<br><hr>")

# 5. Objects
sun = sphere(pos=vector(0,0,0), radius=10, color=color.yellow, emissive=True)
orbit_path = ring(pos=vector(0,0,0), axis=vector(0,1,0), radius=ORBIT_RADIUS, thickness=0.1, color=color.gray(0.4))

tilt_angle = radians(23.4)
tilt_axis = rotate(vector(0,1,0), angle=tilt_angle, axis=vector(1,0,0))

earth = sphere(pos=vector(ORBIT_RADIUS, 0, 0), radius=2, texture=textures.earth, shininess=0)
earth_axis = cylinder(axis=tilt_axis * 6, radius=0.05, color=color.white)

earth_lines = []
lats = [0, 23.4, -23.4, 66.6, -66.6]
cols = [color.white, color.yellow, color.yellow, color.cyan, color.cyan]
for i in range(5):
    lat_rad = radians(lats[i])
    L = ring(axis=tilt_axis, radius=(2 * cos(lat_rad)) * 1.01, thickness=0.03, color=cols[i], visible=False)
    earth_lines.append(L)

def handle_click():
    picked = scene.mouse.pick
    if picked == earth: scene.camera.follow(earth)
    elif picked == sun: scene.camera.follow(None); scene.center = vector(0,0,0)
scene.bind('mousedown', handle_click)

# Station Markers
sphere(pos=vector(50, 0, 0), radius=0.8, color=color.orange) 
sphere(pos=vector(0, 0, 50), radius=0.8, color=color.cyan)   
sphere(pos=vector(-50, 0, 0), radius=0.8, color=color.green) 
sphere(pos=vector(0, 0, -50), radius=0.8, color=color.red)   

# 6. Animation Loop
while True:
    rate(100)
    if state['running']:
        state['theta'] += state['orbit_speed']
        if state['theta'] > 2 * pi: state['theta'] -= 2 * pi 
        
        t = state['theta']
        earth.pos = vector(ORBIT_RADIUS * cos(t), 0, ORBIT_RADIUS * sin(t))
        earth_axis.pos = earth.pos - (tilt_axis * 3)
        
        for i, line in enumerate(earth_lines):
            line.pos = earth.pos + tilt_axis * (2 * sin(radians(lats[i])))
            line.axis = tilt_axis
            
        earth.rotate(angle=state['orbit_speed'] * DAYS_PER_YEAR, axis=tilt_axis, origin=earth.pos)
        
        # Info Logic
        msg = ""
        if 0 <= t < 0.2 or t > 6.1:
            msg = "<b>Tagundnachtgleiche (September):</b> " + ("Sonne im Zenit über dem Äquator - Herbstanfang. Weltweit gleiche Tageslänge." if state['focus_north'] else "Sonne im Zenit über dem Äquator - Frühlingsanfang. Weltweit gleiche Tageslänge.")
        elif 1.3 < t < 1.8:
            msg = "<b>Sonnenwende (Dezember):</b> " + ("Sonne im Zenit über dem südlichen Wendekreis - Kürzester Tag, längste Nacht. </br> Die Sonne geht nördlich des nördlichen Polarkreises nicht mehr auf - Polarnacht." if state['focus_north'] else "Sonne im Zenit über dem südlichen Wendekreis - Kürzeste Nacht, längster Tag. </br> Die Sonne geht südlich des südlichen Polarkreises nicht mehr unter - Polartag.")
        elif 2.9 < t < 3.3:
            msg = "<b>Tagundnachtgleiche (März):</b> " + ("Sonne im Zenit über dem Äquator - Frühlingsanfang. Weltweit gleiche Tageslänge." if state['focus_north'] else "Sonne im Zenit über dem Äquator - Herbstanfang. Weltweit gleiche Tageslänge.")
        elif 4.5 < t < 4.9:
            msg = "<b>Sonnenwende (Juni):</b> " + ("Sonne im Zenit über dem nördlichen Wendekreis - Kürzeste Nacht, längster Tag. </br> Die Sonne geht nördlich des nördlichen Polarkreises nicht mehr unter - Polartag." if state['focus_north'] else "Sonne im Zenit über dem nördlichen Wendekreis - Kürzester Tag, längste Nacht. </br> Die Sonne geht südlich des südlichen Polarkreises nicht mehr auf - Polarnacht.")
        else:
            msg = "Die Erde bewegt sich weiter..."
        
        info_box.text = f"<div style='background-color: #1a1a1a; color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #444; font-family: sans-serif;'>{msg}</div>"