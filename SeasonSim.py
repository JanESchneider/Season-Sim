# ******************************************************************
#   SeasonSim v0.9 - 01.06.2026 (Latest Build 0.9a; 02.06.2026)
#   Jan-Erik Schneider
# 
#   Simple season-simulation tool
#
# ******************************************************************

# -*- coding: utf-8 -*-
import os
os.environ['AUTOBAHN_USE_NVX'] = '0'

from vpython import *
import math

# ******************************************************************
#  Scene Setup and Explanations
# ******************************************************************
title_html = """
<div style='width: 100%; max-width: 900px; background-color: #1a1a1a; color: white; padding: 15px; 
            border-radius: 8px; border: 1px solid #444; font-family: sans-serif; 
            box-sizing: border-box; margin-bottom: 10px; overflow-x: hidden;'>
    
    <h1 style='margin: 0 0 10px 0; color: #ffcc00; font-size: 22px;'>SeasonSim v0.9a</h1>

    <details open style='width: 100%; background-color: #1a1a1a; color: #e0e0e0; padding: 10px; 
                         border-radius: 8px; border: 1px solid #444; cursor: pointer; 
                         box-sizing: border-box; margin-bottom: 10px;'>
        <summary style='color: #ffcc00; font-weight: bold;'>Allgemeine Erklärungen</summary>
        <div style='width: 100%; white-space: normal; overflow-wrap: break-word; 
                    word-wrap: break-word; word-break: break-word; line-height: 1.4; 
                    margin-top: 10px; display: block;'>
            Dieser Simulator stellt vereinfacht den Umlauf der Erde um die Sonne im Jahresverlauf dar. 
            Durch die Neigung der Erdachse (um 23,4°) relativ zur sogenannten <b>Ekliptik</b> 
            (der Ebene in welcher die Planeten die Sonne umkreisen) ist die Sonneneinstrahlung 
            über das Jahr auf den Halbkugeln unterschiedlich. Durch diesen von uns als "Sonnenstand" 
            wahrgenommenen Effekt entstehen die Jahreszeiten.
            <br><br>
            Der Bereich zwischen dem nördlichen und südlichen <b>Wendekreis</b> (gelbe Linien) 
            wird <b>Tropen</b> genannt. Zur Juni-Sonnenwende steht die Sonne über dem nördlichen 
            Wendekreis im Zenit - auf der Nordhalbkugel beginnt der Sommer. Zur Dezember-Sonnenwende 
            über dem südlichen Wendekreis.
            <br><br>
            An den <b>Polarkreisen</b> (hellblaue Linien) geht die Sonne zu den Sonnenwenden 
            gerade nicht mehr auf bzw. unter (Polarnacht/Polartag).
        </div>
    </details>

    <details style='width: 100%; background-color: #1a1a1a; color: #e0e0e0; padding: 10px; 
                    border-radius: 8px; border: 1px solid #444; cursor: pointer; 
                    box-sizing: border-box;'>
        <summary style='color: #ffcc00; font-weight: bold;'>Hilfe & Steuerung</summary>
        
        <div style='display: flex; flex-wrap: wrap; width: 100%; margin-top: 10px; 
                    border-top: 1px solid #333; padding-top: 10px; gap: 10px;'>
            
            <div style='flex: 1; min-width: 200px; max-width: 100%; white-space: normal;'>
                <b style="color: #ffcc00;">Navigation:</b><br>
                • <b>Ansicht drehen</b>: Rechtsklick + Ziehen<br>
                • <b>Ansicht bewegen</b>: Shift + Linksklick<br>
                • <b>Zoom</b>: Mausrad
            </div>
            
            <div style='flex: 1; min-width: 200px; max-width: 100%; white-space: normal;'>
                <b style="color: #ffcc00;">Interaktion:</b><br>
                • <b>Klick auf Erde/Sonne</b>: Fokus setzen<br>
                • <b>Linien</b>: Einblenden von Äquator/Wendekreisen<br>
                • <b>Springe zu</b>: Vordefinierte Daten wählen
            </div>

        </div>
        <div style="width: 100%; margin-top: 10px; font-size: 0.85em; color: #bbb; border-top: 1px solid #333; padding-top: 5px;">
            Zur besseren Übersicht: Simulation pausieren, dann die Ansicht auf die Erde zentrieren. 
            Nun kann man mit "Springe zu" die Positionen wechseln.
        </div>
    </details>
</div>
"""
scene.append_to_title(title_html)

scene = canvas(title=title_html, 
               width=1000, height=700, background=color.black)
scene.lights = []
scene.ambient = color.gray(0.1)
sun_light = local_light(pos=vector(0,0,0), color=color.white)

# ******************************************************************
#  Global state variables
# ******************************************************************
state = {
    'running': True,
    'orbit_speed': 0.001,
    'show_lines': True,
    'focus_north': True,
    'theta': pi
}
ORBIT_RADIUS = 50
DAYS_PER_YEAR = 40 

# ******************************************************************
#  Functions setup
# ******************************************************************
def toggle_run(b):
    state['running'] = not state['running']
    b.text = "PAUSE" if state['running'] else "START"
    b.background = color.red if state['running'] else color.green

def set_speed(s):
    state['orbit_speed'] = s.value

def toggle_lines(b):
    state['show_lines'] = not state['show_lines']
    for line in earth_lines: 
        line.visible = state['show_lines']
        if not state['show_lines']:
            line.my_label.visible = False
            
    b.text = "Linien: AN" if state['show_lines'] else "Linien: AUS"

def toggle_hem(b):
    state['focus_north'] = not state['focus_north']
    b.text = "Fokus: NORD" if state['focus_north'] else "Fokus: SÜD"

def reset_sim():
    state['theta'] = pi
    scene.camera.follow(None)
    scene.center = vector(0,0,0)
    speed_slider.value = 0.001
    state['orbit_speed'] = 0.001

# ******************************************************************
#  Dashboard Layout
# ******************************************************************

scene.append_to_caption("<br><b>Steuerung</b><br>")
button(text="Pause", bind=toggle_run, background=color.red, color=color.white)
scene.append_to_caption(" ")
button(text="Simulation Zurücksetzen", bind=reset_sim)

scene.append_to_caption("<br><br><b>Ansicht</b><br>")

# ******* Watch out, these don't show up! Maybe kick them out later... *********

scene.append_to_caption("<span title='Erklärungen der Jahreszeiten relativ für Nord-/Südhalbkugel.'>")
button(text="Fokus: NORD", bind=toggle_hem)
scene.append_to_caption("</span> ")

scene.append_to_caption("<span title='Ein- und Ausblenden von Äquator (weiß), Wendekreisen (gelb) und Polarkreisen (cyan).'>")
button(text="Linien: EIN", bind=toggle_lines)
scene.append_to_caption("</span>")

scene.append_to_caption("<br><br><b>Umlauf/Rotationsgeschwindigkeit</b><br>")
speed_slider = slider(min=0, max=0.02, value=0.001, bind=set_speed)

def jump_to(angle):
    state['theta'] = angle

scene.append_to_caption("<br><br><b>Springe zu</b><br>")
button(text="Sep (Äquin.)", bind=lambda: jump_to(0))
scene.append_to_caption(" ")
button(text="Dez (Wende)", bind=lambda: jump_to(pi/2))
scene.append_to_caption(" ")
button(text="Mär (Äquin.)", bind=lambda: jump_to(pi))
scene.append_to_caption(" ")
button(text="Jun (Wende)", bind=lambda: jump_to(1.5*pi))

scene.append_to_caption("<br><br><hr><b>Erklärungen</b><br>")
info_box = wtext(text="<div style='background-color: #1a1a1a; color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #444;'>Bereit...</div>") 
scene.append_to_caption("<br><hr>")

# ******************************************************************
#  Render Objects (Sun, Earth, ...)
# ******************************************************************
sun = sphere(pos=vector(0,0,0), radius=10, color=color.yellow, emissive=True)
orbit_path = ring(pos=vector(0,0,0), axis=vector(0,1,0), radius=ORBIT_RADIUS, thickness=0.1, color=color.gray(0.4))

tilt_angle = radians(23.4)
tilt_axis = rotate(vector(0,1,0), angle=tilt_angle, axis=vector(1,0,0))

earth = sphere(pos=vector(ORBIT_RADIUS, 0, 0), radius=2, texture=textures.earth, shininess=0, up=tilt_axis)
earth_axis = cylinder(axis=tilt_axis * 6, radius=0.05, color=color.white)

earth_lines = []
lats = [0, 23.4, -23.4, 66.6, -66.6]
line_names = ["Äquator", "Nördl. Wendekreis", "Südl. Wendekreis", "Nördl. Polarkreis", "Südl. Polarkreis"]
cols = [color.white, color.yellow, color.yellow, color.cyan, color.cyan]

for i in range(5):
    lat_rad = radians(lats[i])
    L = ring(axis=tilt_axis, radius=(2 * cos(lat_rad)) * 1.01, thickness=0.03, color=cols[i], visible=True)
    L.my_lat = lats[i] 
    
    L.my_label = label(text=line_names[i], height=10, border=2, 
                       box=False, line=False, opacity=0,
                       visible=False, color=cols[i],
                       xoffset=10, align='left')
    
    earth_lines.append(L)
    
    earth_lines.append(L)

def handle_click():
    picked = scene.mouse.pick
    if picked == earth: scene.camera.follow(earth)
    elif picked == sun: scene.camera.follow(None); scene.center = vector(0,0,0)
    
    elif hasattr(picked, 'my_label'):
        picked.my_label.visible = not picked.my_label.visible
        
scene.bind('mousedown', handle_click)

# ******************************************************************
#  Station Markers (Solstices, Equinoxes)
# ******************************************************************
stations = [
    {'pos': vector(50, 0, 0), 'color': color.orange, 'name': 'Tagundnachtgleiche\n(September)'},
    {'pos': vector(0, 0, 50), 'color': color.cyan,   'name': 'Sonnenwende\n(Dezember)'},
    {'pos': vector(-50, 0, 0), 'color': color.green,  'name': 'Tagundnachtgleiche\n(März)'},
    {'pos': vector(0, 0, -50), 'color': color.red,    'name': 'Sonnenwende\n(Juni)'}
]

station_objects = []

for s in stations:
    m = sphere(pos=s['pos'], radius=0.8, color=s['color'])
    
    m.my_label = label(pos=s['pos'], text=s['name'], 
                       xoffset=20, yoffset=20, space=30, 
                       height=12, border=4, font='sans',
                       visible=True, opacity=0.3)
    
    station_objects.append(m)

# ******************************************************************
#  Animation
# ******************************************************************
while True:
    rate(100)
    
    if state['running']:
        state['theta'] += state['orbit_speed']
        if state['theta'] > 2 * pi: state['theta'] -= 2 * pi 
    
    t = state['theta']
    earth.pos = vector(ORBIT_RADIUS * cos(t), 0, ORBIT_RADIUS * sin(t))
    earth_axis.pos = earth.pos - (tilt_axis * 3)
    
    t = state['theta']
    earth.pos = vector(ORBIT_RADIUS * cos(t), 0, ORBIT_RADIUS * sin(t))
    earth_axis.pos = earth.pos - (tilt_axis * 3)
    
    label_offset_dir = vector(0, 0, 1) 

    surface_direction = vector(1, 0, 0)

    for line in earth_lines:
        line.pos = earth.pos + tilt_axis * (2 * sin(radians(line.my_lat)))
        line.axis = tilt_axis
        
        if hasattr(line, 'my_label'):
            line.my_label.pos = line.pos + surface_direction * line.radius
            
    if state['running']:
        earth.rotate(angle=state['orbit_speed'] * DAYS_PER_YEAR, axis=tilt_axis, origin=earth.pos)
        
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

# ******************************************************************