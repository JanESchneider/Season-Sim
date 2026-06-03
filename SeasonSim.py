# ******************************************************************
#   SeasonSim v0.9 - 01.06.2026 (Latest Build 0.9b; 03.06.2026)
#   Jan-Erik Schneider
# 
#   Simple season-simulation tool
#
# ******************************************************************

# -*- coding: utf-8 -*-
import os
import datetime
os.environ['AUTOBAHN_USE_NVX'] = '0'

from vpython import *
import math

# ******************************************************************

LANG_DATA = {
    'de': {
        'title': "Jahreszeiten-Simulator",
        'header_html': """
        <div style='width: 100%; max-width: 900px; background-color: #1a1a1a; color: white; padding: 15px; 
            border-radius: 8px; border: 1px solid #444; font-family: sans-serif; 
            box-sizing: border-box; margin-bottom: 10px; overflow-x: hidden;'>
    
            <h1 style='margin: 0 0 10px 0; color: #ffcc00; font-size: 22px;'>Jahreszeiten-Simulator v0.9b</h1>

            <details open style='width: 100%; background-color: #1a1a1a; color: #e0e0e0; padding: 10px; 
                         border-radius: 8px; border: 1px solid #444; cursor: pointer; 
                         box-sizing: border-box; margin-bottom: 10px;'>
                <summary style='color: #ffcc00; font-weight: bold;'>Allgemeine Erklärungen</summary>
                <div style='width: 100%; white-space: normal; overflow-wrap: break-word; 
                    word-wrap: break-word; word-break: break-word; line-height: 1.4; 
                    margin-top: 10px; display: block;'>
                    <p style='margin-bottom: 12px;'>
                    Dieser Simulator stellt vereinfacht den Umlauf der Erde um die Sonne im Jahresverlauf dar. 
                    Durch die Neigung der Erdachse (um 23,4°) relativ zur sogenannten <b>Ekliptik</b> 
                    (der Ebene in welcher die Planeten die Sonne umkreisen) ist die Sonneneinstrahlung 
                    über das Jahr auf den Halbkugeln unterschiedlich. Durch diesen von uns als "Sonnenstand" 
                    wahrgenommenen Effekt entstehen die Jahreszeiten.
                    </p>
                    <p style='margin-bottom: 12px;'>
                    Der Bereich zwischen dem nördlichen und südlichen <b>Wendekreis</b> (gelbe Breitenkreise bei ca. 23° Nord/Süd) 
                    wird <b>Tropen</b> genannt. Zur Juni-Sonnenwende steht die Sonne über dem nördlichen 
                    Wendekreis im Zenit (das heißt senkrecht über dem Beobachter) - auf der Nordhalbkugel beginnt der Sommer. Zur Dezember-Sonnenwende 
                    steht die Sonne dann über dem südlichen Wendekreis im Zenit - auf der Nordhalbkugel ist Winterbeginn. In den Tropen ist die Tageslänge
                    das ganze Jahr über relativ gleichbleibend. Daher gibt es dort keine ausgeprägten Jahreszeiten - das Jahr wird in eine Regen- und 
                    eine Trockenzeit eingeteilt.
                    </p>
                    <p style='margin-bottom: 12px;'>
                    An den <b>Polarkreisen</b> (hellblaue Linien bei jeweils ca. 66° Nord/Süd) geht die Sonne zu den Sonnenwenden 
                    gerade nicht mehr auf bzw. unter (Polarnacht/Polartag). Zum Beispiel herrscht zur Dezember-Sonnenwende nördlich des nördlichen
                    Polarkreises Polarnacht. Zur Juni-Sonnenwende hingegen ist die Sonne dort 24 Stunden am Tag oberhalb des Horizonts - es herrscht Polartag.
                    <p style='margin-bottom: 12px;'>
                    Die Sonnenwenden werden auch als <b>Solstitien</b> (Singular Solstitium), und die Tagundnachtgleichen als <b>Äquinoktien</b> (Singular Äquinoktium) bezeichnet.
                    </p>
                </div>
            </details>

            <details style='width: 100%; background-color: #1a1a1a; color: #e0e0e0; padding: 10px; 
                    border-radius: 8px; border: 1px solid #444; cursor: pointer; 
                    box-sizing: border-box;'>
                <summary style='color: #ffcc00; font-weight: bold;'>Hilfe & Steuerung</summary>
        
                <div style='display: flex; flex-wrap: wrap; width: 100%; margin-top: 10px; 
                    border-top: 1px solid #333; padding-top: 10px; gap: 10px;'>
            
                <div style='flex: 1; min-width: 200px; max-width: 100%; white-space: normal;'>
                    <b style="color: #ffcc00;">
                    <p style='margin-bottom: 12px;'>
                    Navigation:</b></p>
                    <p style='margin-bottom: 12px;'>
                    &#x2022; <b>Ansicht drehen</b>: Rechtsklick + Ziehen<br></p>
                    <p style='margin-bottom: 12px;'>
                    &#x2022; <b>Ansicht bewegen</b>: Shift + Linksklick<br></p>
                    <p style='margin-bottom: 12px;'>
                    &#x2022; <b>Zoom</b>: Mausrad</p>
                </div>
            
                <div style='flex: 1; min-width: 200px; max-width: 100%; white-space: normal;'>
                    <b style="color: #ffcc00;">
                    <p style='margin-bottom: 12px;'>
                    Interaktion:</b></p>
                    <p style='margin-bottom: 12px;'>
                    &#x2022; <b>Klick auf Erde/Sonne</b>: Fokus setzen</p>
                    <p style='margin-bottom: 12px;'>
                    &#x2022; <b>Linien</b>: Einblenden von Äquator, Wendekreisen und Polarkreisen</p>
                    <p style='margin-bottom: 12px;'>
                    &#x2022; <b>Springe zu</b>: Simulation auf den entsprechenden Zeitpunkt setzen</p>
                </div>

                </div>
                <div style='width: 100%; white-space: normal; overflow-wrap: break-word; 
                    word-wrap: break-word; word-break: break-word; line-height: 1.4; 
                    margin-top: 10px; display: block;'>
                    Zur einfacheren Übersicht Simulation pausieren, dann die Ansicht auf die Erde zentrieren. 
                    Nun kann man mit "Springe zu" die Positionen wechseln.

                    Aus Gründen der Sichtbarkeit ist die Rotationsgeschwindigkeit der Erde im Modell etwa achtmal langsamer als in der Realität.
                    Erde und Sonne sind im Verhältnis nicht maßstabsgetreu. Die perfekte Kreisbahn des Erdorbits ist ebenfalls eine Vereinfachung.
                </div>
            </details>
        </div>
        """,
        'label_controls': "<b>Steuerung</b>",
        'label_view': "<b>Ansicht</b>",
        'label_speed': "<b>Umlauf/Rotationsgeschwindigkeit</b>",
        'label_jump': "<b>Springe zu</b>",
        'label_expl': "<b>Erklärungen</b>",
        'btn_pause': "Pause", 'btn_start': "Start",
        'btn_reset': "Simulation Zurücksetzen",
        'btn_lines_on': "Breitenkreise: AN", 'btn_lines_off': "Breitenkreise: AUS",
        'btn_fokus_n': "Fokus: NORD", 'btn_fokus_s': "Fokus: SÜD",
        'btn_lang': "Sprache: Deutsch",
        'btn_today': "HEUTE",
        'jump_sep': "Sep (Äquin.)", 'jump_dez': "Dez (Wende)",
        'jump_mar': "Mär (Äquin.)", 'jump_jun': "Jun (Wende)",
        'lines': ["Äquator", "Nördl. Wendekreis", "Südl. Wendekreis", "Nördl. Polarkreis", "Südl. Polarkreis"],
        'stations': ["Tagundnachtgleiche\n(September)", "Sonnenwende\n(Dezember)", "Tagundnachtgleiche\n(März)", "Sonnenwende\n(Juni)"],
        'msg_moving': "Die Erde bewegt sich weiter...",
        'msg_mar_n': "<b>Frühjahrs-Tagundnachtgleiche:</b> Sonne im Zenit über dem Äquator. Weltweit gleiche Tageslänge.",
        'msg_jun_n': "<b>Sommersonnenwende:</b> Sonne im Zenit über dem nördlichen Wendekreis. Sommeranfang. Die Sonne geht nördlich des nördlichen Polarkreises nicht mehr unter - Polartag.",
        'msg_sep_n': "<b>Herbst-Tagundnachtgleiche:</b> Sonne im Zenit über dem Äquator. Weltweit gleiche Tageslänge.",
        'msg_dec_n': "<b>Wintersonnenwende:</b> Sonne im Zenit über dem südlichen Wendekreis. Winteranfang. Die Sonne geht nördlich des nördlichen Polarkreises nicht mehr auf - Polarnacht.",
        'msg_mar_s': "<b>Herbst-Tagundnachtgleiche:</b> Sonne im Zenit über dem Äquator. Weltweit gleiche Tageslänge.",
        'msg_jun_s': "<b>Wintersonnenwende:</b> Sonne im Zenit über dem nördlichen Wendekreis. Winteranfang. Die Sonne geht südlich des südlichen Polarkreises nicht mehr auf - Polarnacht.",
        'msg_sep_s': "<b>Frühjahrs-Tagundnachtgleiche:</b> Sonne im Zenit über dem Äquator. Weltweit gleiche Tageslänge.",
        'msg_dec_s': "<b>Sommersonnenwende:</b> Sonne im Zenit über dem südlichen Wendekreis. Sommeranfang. Die Sonne geht südlich des südlichen Polarkreises nicht mehr unter - Polartag."
        
    },
    'en': {
        'title': "Season-Simulator",
        'header_html': """
        <div style='width: 100%; max-width: 900px; background-color: #1a1a1a; color: white; padding: 15px; 
            border-radius: 8px; border: 1px solid #444; font-family: sans-serif; 
            box-sizing: border-box; margin-bottom: 10px; overflow-x: hidden;'>
    
            <h1 style='margin: 0 0 10px 0; color: #ffcc00; font-size: 22px;'>Season-Simulator v0.9b</h1>

            <details open style='width: 100%; background-color: #1a1a1a; color: #e0e0e0; padding: 10px; 
                         border-radius: 8px; border: 1px solid #444; cursor: pointer; 
                         box-sizing: border-box; margin-bottom: 10px;'>
                <summary style='color: #ffcc00; font-weight: bold;'>Description</summary>
                <div style='width: 100%; white-space: normal; overflow-wrap: break-word; 
                    word-wrap: break-word; word-break: break-word; line-height: 1.4; 
                    margin-top: 10px; display: block;'>
                    <p style='margin-bottom: 12px;'>
                    This tool provides a simplified means of simulating the Earth's motion around the Sun over the course of the year. 
                    The tilt of Earth's rotational axis with respect to the so-called <b>ecliptic</b> 
                    (the plain in which the planets revolve around the Sun) causes a non-uniform illumination with sunlight 
                    at the two hemispheres over the year. What we perceive as the Sun angle is responsible for the seasons.
                    <br></p>
                    <p style='margin-bottom: 12px;'>
                    The <b>tropics</b> lie between the Tropic of Cancer (at about 23° north) and the Tropic of Capricorn (at about 23° south). 
                    The Sun reaches zenith above the Tropic of Cancer at June solstice - summer begins in the northern hemisphere. In December, the Sun reaches zenith
                    at the Tropic of Capricorn - the beginning of winter in the northern hemisphere. The amount of daylight doesn't change by much over the course of the year
                    in the tropics; this is why this regions does not exhibit seasons at all - the year is divided into a rain- and a dry season.
                    <br></p>
                    <p style='margin-bottom: 12px;'>
                    The <b>Arctic Circle</b> and <b>Antarctic Circle</b> (at roughly 66° north and south respectively) mark the positions where the Sun doesn't rise or set at the
                    respective solstice. For example the Sun does not rise north of the Arctic Circle at December solstice. This is called polar night. Respectively at June solstice
                    the Sun won't set, what causes polar day.</p>
                </div>
            </details>

            <details style='width: 100%; background-color: #1a1a1a; color: #e0e0e0; padding: 10px; 
                    border-radius: 8px; border: 1px solid #444; cursor: pointer; 
                    box-sizing: border-box;'>
                <summary style='color: #ffcc00; font-weight: bold;'>Controls</summary>
        
                <div style='display: flex; flex-wrap: wrap; width: 100%; margin-top: 10px; 
                    border-top: 1px solid #333; padding-top: 10px; gap: 10px;'>
            
                <div style='flex: 1; min-width: 200px; max-width: 100%; white-space: normal;'>
                    <b style="color: #ffcc00;">
                    <p style='margin-bottom: 12px;'>
                    Navigation:</b><br></p>
                    <p style='margin-bottom: 12px;'>
                    &#x2022; <b>Tilt</b>: Hold/Draw RMB</p>
                    <p style='margin-bottom: 12px;'>
                    &#x2022; <b>Pan</b>: Shift + LMB</p>
                    <p style='margin-bottom: 12px;'>
                    &#x2022; <b>Zoom</b>: Mousewheel</p>
                </div>
            
                <div style='flex: 1; min-width: 200px; max-width: 100%; white-space: normal;'>
                    <b style="color: #ffcc00;">
                    <p style='margin-bottom: 12px;'>Interaction:</b></p>
                    <p style='margin-bottom: 12px;'>
                    &#x2022; <b>Click Earth/Sun</b>: Shift focus</p>
                    <p style='margin-bottom: 12px;'>
                    &#x2022; <b>Lines</b>: Toggle equator, tropics and Arctic/Antarctic circles</p>
                    <p style='margin-bottom: 12px;'>
                    &#x2022; <b>Go to</b>: Move to respective timestamp</p>
                </div>

                </div>
                <div style='width: 100%; white-space: normal; overflow-wrap: break-word; 
                    word-wrap: break-word; word-break: break-word; line-height: 1.4; 
                    margin-top: 10px; display: block;'>
                    For better visibility pause simulation, then center focus on Earth. You can now easily toggle the solstices and equinoxes via the "Go to" button.

                    Due to reasons of visibility the Earth's rotational period is slowed down by approximately a factor of eight in this simulation. The Sun and Earth
                    are not to scale. The circular orbit (eccentricity of zero) is also a simplification.
                </div>
            </details>
        </div>
        """,
        'label_controls': "<b>Controls</b>",
        'label_view': "<b>View</b>",
        'label_speed': "<b>Orbital/Rotational Velocity</b>",
        'label_jump': "<b>Go to</b>",
        'label_expl': "<b>Description</b>",
        'btn_pause': "Pause", 'btn_start': "Resume",
        'btn_reset': "Reset Simulation",
        'btn_lines_on': "Latitudes: ON", 'btn_lines_off': "Latitudes: OFF",
        'btn_fokus_n': "Focus: N", 'btn_fokus_s': "Focus: S",
        'btn_lang': "Language: English",
        'btn_today': "TODAY",
        'jump_sep': "Sep (Equinox)", 'jump_dez': "Dec (Solstice)",
        'jump_mar': "Mar (Equinox)", 'jump_jun': "Jun (Solstice)",
        'lines': ["Equator", "Tropic of Cancer", "Tropic of Capricorn", "Arctic Circle", "Antarctic Circle"],
        'stations': ["Equinox\n(September)", "Solstice\n(December)", "Equinox\n(March)", "Solstice\n(June)"],
        'msg_moving': "The Earth continues its journey...",
        'msg_mar_n': "<b>Spring Equinox:</b> Sun reaches zenith above the equator. Approximate same day length globally.",
        'msg_jun_n': "<b>Summer Solstice:</b> Sun reaches zenith above the Tropic of Cancer. Beginning of summer. The Sun doesn't set north of the Arctic Circle - polar day.",
        'msg_sep_n': "<b>Autumn Equinox:</b> Sun reaches zenith above the equator. Approximate same day length globally.",
        'msg_dec_n': "<b>Winter Solstice:</b> Sun reaches zenith above the Tropic of Capricorn. Beginning of winter. The Sun doesn't rise north of the Arctic Circle - polar night.",
        'msg_mar_s': "<b>Autumn Equinox:</b> Sun reaches zenith above the equator. Approximate same day length globally.",
        'msg_jun_s': "<b>Winter Solstice:</b> Sun reaches zenith above the Tropic of Cancer. Beginning of winter. The Sun doesn't rise south of the Antarctic Circle - polar night.",
        'msg_sep_s': "<b>Spring Equinox:</b> Sun reaches zenith above the equator. Approximate same day length globally.",
        'msg_dec_s': "<b>Summer Solstice:</b> Sun reaches zenith above the Tropic of Capricorn. Beginning of summer. The Sun doesn't set south of the Antarctic Circle - polar day."
    }
}


# ******************************************************************
#  Global state variables
# ******************************************************************
state = {
    'running': True,
    'orbit_speed': 0.001,
    'show_lines': True,
    'focus_north': True,
    'theta': pi,
    'lang': 'en'
}

ORBIT_RADIUS = 50
DAYS_PER_YEAR = 45 

# ******************************************************************
#  Scene Setup 
# ******************************************************************

scene = canvas(width=1000, height=600, background=color.black)
header_container = wtext(text=LANG_DATA[state['lang']]['header_html'])

scene.lights = []
scene.ambient = color.gray(0.1)
sun_light = local_light(pos=vector(0,0,0), color=color.white)

scene.append_to_caption("<br>")
lbl_controls = wtext(text=LANG_DATA[state['lang']]['label_controls'])
scene.append_to_caption("<br>")


# ******************************************************************
#  Functions setup
# ******************************************************************
def toggle_run(b):
    state['running'] = not state['running']
    L = LANG_DATA[state['lang']]
    b.text = L['btn_pause'] if state['running'] else L['btn_start']
    b.background = color.red if state['running'] else color.green

def set_speed(s):
    state['orbit_speed'] = s.value

def toggle_lines(b):
    state['show_lines'] = not state['show_lines']
    L = LANG_DATA[state['lang']]
    for line in earth_lines: 
        line.visible = state['show_lines']
        if not state['show_lines']: line.my_label.visible = False
    b.text = L['btn_lines_on'] if state['show_lines'] else L['btn_lines_off']

def toggle_hem(b):
    state['focus_north'] = not state['focus_north']
    L = LANG_DATA[state['lang']]
    b.text = L['btn_fokus_n'] if state['focus_north'] else L['btn_fokus_s']

def jump_to(angle):
    state['theta'] = angle

def jump_to_today():
    now = datetime.datetime.now()
    day_of_year = now.timetuple().tm_yday
    sept_equinox_doy = 265
    diff_days = day_of_year - sept_equinox_doy
    state['theta'] = ((diff_days / 365.25) * 2 * math.pi) % (2 * math.pi)

def toggle_lang(b):
    state['lang'] = 'en' if state['lang'] == 'de' else 'de'
    L = LANG_DATA[state['lang']]

    header_container.text = L['header_html']
    lbl_controls.text = L['label_controls']
    lbl_view.text = L['label_view']
    lbl_speed.text = L['label_speed']
    lbl_jump.text = L['label_jump']
    lbl_expl.text = L['label_expl']
    
    b.text = L['btn_lang']
    btn_pause.text = L['btn_pause'] if state['running'] else L['btn_start']
    btn_reset.text = L['btn_reset']
    btn_line_toggle.text = L['btn_lines_on'] if state['show_lines'] else L['btn_lines_off']
    btn_hem_toggle.text = L['btn_fokus_n'] if state['focus_north'] else L['btn_fokus_s']
    btn_j1.text = L['jump_sep']; btn_j2.text = L['jump_dez']
    btn_j3.text = L['jump_mar']; btn_j4.text = L['jump_jun']
    btn_j5.text = L['btn_today']

    for i, line in enumerate(earth_lines):
        line.my_label.text = L['lines'][i] 
    for i, station in enumerate(station_objects):
        station.my_label.text = L['stations'][i]

# ******************************************************************
#  Dashboard Layout
# ******************************************************************

btn_pause = button(text="Pause", bind=toggle_run, background=color.red)
btn_reset = button(text="Reset Simulation", bind=lambda: jump_to(math.pi))
scene.append_to_caption("  ")
btn_lang = button(text="Language: DE/EN", bind=toggle_lang)

scene.append_to_caption("<br><br>")
lbl_view = wtext(text=LANG_DATA[state['lang']]['label_view'])
scene.append_to_caption("<br>")
btn_hem_toggle = button(text="Fokus: NORD", bind=toggle_hem)
btn_line_toggle = button(text="Breitenkreise: AN", bind=toggle_lines)

scene.append_to_caption("<br><br>")
lbl_speed = wtext(text=LANG_DATA[state['lang']]['label_speed'])
scene.append_to_caption("<br>")
speed_slider = slider(min=0, max=0.02, value=0.001, bind=set_speed)

scene.append_to_caption("<br><br>")
lbl_jump = wtext(text=LANG_DATA[state['lang']]['label_jump'])
scene.append_to_caption("<br>")
btn_j1 = button(text="Sep", bind=lambda: jump_to(0))
btn_j2 = button(text="Dez", bind=lambda: jump_to(pi/2))
btn_j3 = button(text="Mär", bind=lambda: jump_to(pi))
btn_j4 = button(text="Jun", bind=lambda: jump_to(1.5*pi))
btn_j5 = button(text="HEUTE", bind=jump_to_today, background=color.orange, color=color.black)

scene.append_to_caption("<br><br><hr>")
lbl_expl = wtext(text=LANG_DATA[state['lang']]['label_expl'])
scene.append_to_caption("<br>")
info_box = wtext(text="") 

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
cols = [color.white, color.yellow, color.yellow, color.cyan, color.cyan]

for i in range(5):
    lat_rad = radians(lats[i])
    L = ring(axis=tilt_axis, radius=(2 * cos(lat_rad)) * 1.01, thickness=0.03, color=cols[i])
    L.my_lat = lats[i] 
    L.my_label = label(text=LANG_DATA[state['lang']]['lines'][i], height=10, box=False, visible=False, color=cols[i])
    earth_lines.append(L)

station_positions = [vector(50,0,0), vector(0,0,50), vector(-50,0,0), vector(0,0,-50)]
station_objects = []

for i, pos in enumerate(station_positions):
    m = sphere(pos=pos, radius=0.5, color=color.white, opacity=0.5)
    m.my_label = label(pos=pos, text=LANG_DATA[state['lang']]['stations'][i], height=12, opacity=0.3, box=False)
    station_objects.append(m)

def handle_click():
    picked = scene.mouse.pick
    if picked == earth: scene.camera.follow(earth)
    elif picked == sun: scene.camera.follow(None); scene.center = vector(0,0,0)
    
    elif hasattr(picked, 'my_label'):
        picked.my_label.visible = not picked.my_label.visible
        
scene.bind('mousedown', handle_click)

toggle_lang(btn_lang)

# ******************************************************************
#  Animation
# ******************************************************************

date_hud = label(pixel_pos=True, pos=vector(20, scene.height - 20, 0), 
                 text="", align='left', height=25, 
                 box=True, background=color.gray(0.1), opacity=0.8,
                 font='sans', color=color.orange)

def get_current_date_str(theta, lang):
    months_dict = {
        'de': ["Januar", "Februar", "März", "April", "Mai", "Juni", 
               "Juli", "August", "September", "Oktober", "November", "Dezember"],
        'en': ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]
    }
    
    base_date = datetime.datetime(2025, 9, 22)
    days_to_add = (theta / (2 * math.pi)) * 365.25
    current_dt = base_date + datetime.timedelta(days=days_to_add)
    
    day = current_dt.day
    month_name = months_dict[lang][current_dt.month - 1]
    
    if lang == 'de':
        return f"{day}. {month_name}"
    else:
        return f"{day} {month_name}"

while True:
    rate(100)
    if state['running']:
        state['theta'] = (state['theta'] + state['orbit_speed']) % (2 * pi)
        earth.rotate(angle=state['orbit_speed'] * DAYS_PER_YEAR, axis=tilt_axis, origin=earth.pos)

    t = state['theta']
    earth.pos = vector(ORBIT_RADIUS * cos(t), 0, ORBIT_RADIUS * sin(t))
    earth_axis.pos = earth.pos - (tilt_axis * 3)

    for line in earth_lines:
        line.pos = earth.pos + tilt_axis * (2 * sin(radians(line.my_lat)))
        line.axis = tilt_axis
        line.my_label.pos = line.pos + vector(1,0,0) * line.radius

    date_hud.pos = vector(20, scene.height - 20, 0)
    #prefix = "Datum: " if state['lang'] == 'de' else "Date: "
    date_hud.text = get_current_date_str(t, state['lang'])

    L = LANG_DATA[state['lang']]

    if      0 <= t < 0.2 or t > 6.1:    msg = L['msg_sep_n'] if state['focus_north'] else L['msg_sep_s']
    elif    1.3 < t < 1.8:              msg = L['msg_dec_n'] if state['focus_north'] else L['msg_dec_s']
    elif    2.9 < t < 3.3:              msg = L['msg_mar_n'] if state['focus_north'] else L['msg_mar_s']
    elif    4.5 < t < 4.9:              msg = L['msg_jun_n'] if state['focus_north'] else L['msg_jun_s']
    else:                               msg = L['msg_moving']    
    
    info_box.text = f"<div style='background-color: #1a1a1a; color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #444;'>{msg}</div>"

# ******************************************************************