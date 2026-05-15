"""
LASER-STOLPERDRAHT-ALARM v1.0
Generiert Verdrahtungsdiagramm und Schaltplan als PNG
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ================================================================
# DIAGRAMM 1: BREADBOARD-VERDRAHTUNG
# ================================================================

fig, ax = plt.subplots(figsize=(14, 18))
ax.set_xlim(0, 14)
ax.set_ylim(0, 18)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('#F2F2EE')

# ---- Hilfsfunktionen ----
def wire(ax, x1, y1, x2, y2, color, lw=2.2, zorder=5):
    mid_y = (y1 + y2) / 2
    ax.plot([x1, x1, x2, x2], [y1, mid_y, mid_y, y2],
            color=color, lw=lw, zorder=zorder,
            solid_capstyle='round', solid_joinstyle='round')

def wire_h(ax, x1, y1, x2, y2, color, lw=2.2, zorder=5):
    ax.plot([x1, x2, x2], [y1, y1, y2],
            color=color, lw=lw, zorder=zorder,
            solid_capstyle='round', solid_joinstyle='round')

def dot(ax, x, y, color='#111111'):
    ax.plot(x, y, 'o', color=color, markersize=5, zorder=8)

# ---- TITEL ----
title_box = FancyBboxPatch((0.5, 16.7), 13.0, 1.1,
                            boxstyle="round,pad=0.2",
                            facecolor='#1A4A6B', edgecolor='#0D2E45', lw=2.5, zorder=10)
ax.add_patch(title_box)
ax.text(7.0, 17.3, 'LASER-STOLPERDRAHT-ALARM v1.0', ha='center', va='center',
        fontsize=15, fontweight='bold', color='white', zorder=11)
ax.text(7.0, 16.9, 'Verdrahtungsdiagramm  |  Arduino Nano + KY-008 Laser + LDR + Piezo + LEDs',
        ha='center', va='center', fontsize=8, color='#AACCEE', zorder=11)

# ---- BREADBOARD ----
BB_X, BB_Y = 0.8, 9.0
BB_W, BB_H = 12.4, 5.8

bb_main = FancyBboxPatch((BB_X, BB_Y), BB_W, BB_H,
                          boxstyle="round,pad=0.15",
                          facecolor='#DCDCCC', edgecolor='#999988', lw=2.5, zorder=2)
ax.add_patch(bb_main)

# Stromschienen
for rail_y, rail_color, sign in [
    (BB_Y+BB_H-0.42, '#EE3333', '+'),
    (BB_Y+BB_H-0.72, '#3333CC', '−'),
    (BB_Y+0.22, '#EE3333', '+'),
    (BB_Y+0.52, '#3333CC', '−'),
]:
    rail = patches.Rectangle((BB_X+0.3, rail_y), BB_W-0.6, 0.25,
                               facecolor=rail_color, alpha=0.75, zorder=4)
    ax.add_patch(rail)
    ax.text(BB_X+0.15, rail_y+0.12, sign, fontsize=9, color=rail_color,
            fontweight='bold', va='center', zorder=5)

# Löcher
COLS = 30
col_xs = np.linspace(BB_X+0.55, BB_X+BB_W-0.55, COLS)
row_ys_top = np.linspace(BB_Y+BB_H-1.05, BB_Y+BB_H/2+0.25, 5)
row_ys_bot = np.linspace(BB_Y+BB_H/2-0.25, BB_Y+0.95, 5)

for row_y in list(row_ys_top) + list(row_ys_bot):
    for col_x in col_xs:
        ax.plot(col_x, row_y, 'o', color='#888877', markersize=2.8, zorder=4)

mid = patches.Rectangle((BB_X+0.3, BB_Y+BB_H/2-0.18), BB_W-0.6, 0.36,
                          facecolor='#CCCCBC', edgecolor='#AAAAAA', lw=1, zorder=4)
ax.add_patch(mid)

for i, col_x in enumerate(col_xs):
    if i % 5 == 0:
        ax.text(col_x, BB_Y+BB_H-0.12, str(i+1), fontsize=5, ha='center',
                color='#666655', zorder=5)

ax.text(BB_X+BB_W/2, BB_Y+BB_H+0.2, 'Breadboard  (830 Punkte)',
        ha='center', fontsize=9, color='#444433', fontweight='bold')

# ---- ARDUINO NANO ----
AN_X, AN_Y = 3.5, 1.5
AN_W, AN_H = 3.2, 6.8

nano_pcb = FancyBboxPatch((AN_X, AN_Y), AN_W, AN_H,
                           boxstyle="round,pad=0.2",
                           facecolor='#1A6B8A', edgecolor='#0D4A63', lw=3, zorder=6)
ax.add_patch(nano_pcb)
nano_inner = FancyBboxPatch((AN_X+0.25, AN_Y+0.5), AN_W-0.5, AN_H-1.0,
                             boxstyle="round,pad=0.1",
                             facecolor='#1E7A9E', edgecolor='#0D4A63', lw=1, zorder=7)
ax.add_patch(nano_inner)
ax.text(AN_X+AN_W/2, AN_Y+AN_H/2+0.4, '⊖⊕', ha='center', va='center',
        fontsize=14, color='white', zorder=8)
ax.text(AN_X+AN_W/2, AN_Y+AN_H/2-0.1, 'Arduino', ha='center', va='center',
        fontsize=9, color='white', fontweight='bold', zorder=8)
ax.text(AN_X+AN_W/2, AN_Y+AN_H/2-0.6, 'NANO', ha='center', va='center',
        fontsize=12, color='white', fontweight='bold', zorder=8)

usb = FancyBboxPatch((AN_X+AN_W/2-0.4, AN_Y+AN_H-0.05), 0.8, 0.55,
                      boxstyle="round,pad=0.05",
                      facecolor='#999999', edgecolor='#555555', lw=1.5, zorder=8)
ax.add_patch(usb)
ax.text(AN_X+AN_W/2, AN_Y+AN_H+0.25, 'Mini-USB', ha='center', fontsize=7, color='#444444')

left_pins  = ['D13','D12','D11','D10','D9','D8','D7','D6','D5','D4','D3','D2','GND','RST']
right_pins = ['5V','3V3','A7','A6','A5','A4','A3','A2','A1','A0','AREF','3V3','GND','VIN']
pin_spacing = (AN_H - 0.8) / (len(left_pins) + 1)
nano_pins = {}

for i, pin in enumerate(left_pins):
    py = AN_Y + AN_H - 0.4 - (i+1)*pin_spacing
    ax.plot(AN_X - 0.12, py, 's', color='#C8A830', markersize=5, zorder=9)
    ax.text(AN_X - 0.22, py, pin, ha='right', va='center', fontsize=5.5,
            color='#DDDDDD', zorder=9)
    nano_pins[pin] = (AN_X - 0.12, py)

for i, pin in enumerate(right_pins):
    py = AN_Y + AN_H - 0.4 - (i+1)*pin_spacing
    ax.plot(AN_X + AN_W + 0.12, py, 's', color='#C8A830', markersize=5, zorder=9)
    ax.text(AN_X + AN_W + 0.22, py, pin, ha='left', va='center', fontsize=5.5,
            color='#DDDDDD', zorder=9)
    nano_pins[pin] = (AN_X + AN_W + 0.12, py)

ax.text(AN_X+AN_W/2, AN_Y-0.3, 'Arduino Nano', ha='center',
        fontsize=10, color='#0D4A63', fontweight='bold')

# ---- KOMPONENTEN AUF DEM BREADBOARD ----

# KY-008 LASER MODUL (links, Spalten 3-5)
laser_x = col_xs[3]
laser_y = BB_Y + BB_H/2 + 0.8
laser_body = FancyBboxPatch((laser_x-0.55, laser_y-0.28), 1.1, 0.56,
                              boxstyle="round,pad=0.06",
                              facecolor='#1A1A1A', edgecolor='#111111', lw=2, zorder=8)
ax.add_patch(laser_body)
# Laserlinse
laser_lens = plt.Circle((laser_x+0.42, laser_y), 0.14, color='#CC2222', zorder=9)
ax.add_patch(laser_lens)
# Laserstrahl
ax.annotate('', xy=(BB_X+BB_W+0.5, laser_y),
            xytext=(laser_x+0.56, laser_y),
            arrowprops=dict(arrowstyle='->', color='#FF0000', lw=1.5,
                            connectionstyle='arc3,rad=0'))
ax.plot([laser_x+0.56, BB_X+BB_W+0.3], [laser_y, laser_y],
        color='#FF4444', lw=1.5, linestyle='--', zorder=4, alpha=0.7)
ax.text(laser_x, laser_y-0.55, 'KY-008\nLaser', ha='center', fontsize=6.5,
        color='#222211', fontweight='bold')
# Pins
ax.plot(laser_x-0.35, laser_y+0.28, 'o', color='#C8A830', markersize=3.5, zorder=10)
ax.plot(laser_x,      laser_y+0.28, 'o', color='#C8A830', markersize=3.5, zorder=10)
ax.plot(laser_x+0.35, laser_y+0.28, 'o', color='#C8A830', markersize=3.5, zorder=10)
ax.text(laser_x-0.35, laser_y+0.45, 'S', fontsize=5.5, ha='center', color='#DDAA00')
ax.text(laser_x,      laser_y+0.45, '−', fontsize=7,   ha='center', color='blue')
ax.text(laser_x+0.35, laser_y+0.45, '+', fontsize=7,   ha='center', color='red')

# LDR FOTOWIDERSTAND (rechts außen, symbolisch)
ldr_x = BB_X + BB_W + 0.9
ldr_y = laser_y
ldr_body = plt.Circle((ldr_x, ldr_y), 0.38, facecolor='#F5E8C0',
                        edgecolor='#8B6914', lw=2, zorder=8)
ax.add_patch(ldr_body)
# Pfeile für Lichteinfall
for angle in [45, 90, 135]:
    rad = np.radians(angle)
    ax.annotate('', xy=(ldr_x + 0.28*np.cos(rad), ldr_y + 0.28*np.sin(rad)),
                xytext=(ldr_x + 0.6*np.cos(rad), ldr_y + 0.6*np.sin(rad)),
                arrowprops=dict(arrowstyle='->', color='#FFAA00', lw=1.2))
ax.text(ldr_x, ldr_y, 'LDR', ha='center', va='center', fontsize=6,
        color='#333322', fontweight='bold', zorder=9)
ax.text(ldr_x, ldr_y-0.6, 'Fotowiderstand\n(Empfänger)', ha='center', fontsize=6,
        color='#222211', fontweight='bold')
ax.plot(ldr_x-0.25, ldr_y+0.38, 'o', color='#C8A830', markersize=4, zorder=10)
ax.plot(ldr_x+0.25, ldr_y+0.38, 'o', color='#C8A830', markersize=4, zorder=10)

# Spannungsteiler-Widerstand R1 (10kΩ) für LDR
R1_x = col_xs[26]
R1_y = row_ys_top[2]
r1_body = FancyBboxPatch((R1_x-0.45, R1_y-0.14), 0.9, 0.28,
                          boxstyle="round,pad=0.04",
                          facecolor='#D4A843', edgecolor='#8B6914', lw=1.5, zorder=8)
ax.add_patch(r1_body)
for xi, c in zip([-0.22,-0.08,0.06,0.22,0.32],
                  ['#8B0000','#8B0000','#111111','#C0A020','#C0A020']):
    ax.plot(R1_x+xi, R1_y, '|', color=c, markersize=9, markeredgewidth=2, zorder=9)
ax.text(R1_x, R1_y-0.3, 'R1  10kΩ', ha='center', fontsize=6,
        color='#333322', fontweight='bold')
ax.plot(R1_x-0.45, R1_y, 'o', color='#C8A830', markersize=3.5, zorder=10)
ax.plot(R1_x+0.45, R1_y, 'o', color='#C8A830', markersize=3.5, zorder=10)

# ROTE LED (Alarm)
led_rot_x = col_xs[10]
led_rot_y = BB_Y + BB_H + 1.0
led_rot_body = plt.Circle((led_rot_x, led_rot_y), 0.28,
                            facecolor='#FF4444', edgecolor='#CC0000', lw=2, zorder=8)
ax.add_patch(led_rot_body)
# Lichtpfeile
for angle in [30, 60]:
    rad = np.radians(angle)
    ax.annotate('', xy=(led_rot_x+0.45*np.cos(rad), led_rot_y+0.45*np.sin(rad)),
                xytext=(led_rot_x+0.28*np.cos(rad), led_rot_y+0.28*np.sin(rad)),
                arrowprops=dict(arrowstyle='->', color='#FF6666', lw=1.0))
ax.text(led_rot_x, led_rot_y, '▶', ha='center', va='center', fontsize=8,
        color='#CC0000', zorder=9)
ax.text(led_rot_x, led_rot_y-0.55, 'LED1\nRot (Alarm)', ha='center', fontsize=6,
        color='#222211', fontweight='bold')
ax.plot(led_rot_x-0.1, led_rot_y+0.28, 'o', color='#C8A830', markersize=3.5, zorder=10)
ax.plot(led_rot_x+0.1, led_rot_y+0.28, 'o', color='#C8A830', markersize=3.5, zorder=10)
ax.text(led_rot_x-0.22, led_rot_y+0.42, '+', fontsize=7, color='red', fontweight='bold')
ax.text(led_rot_x+0.12, led_rot_y+0.42, '−', fontsize=9, color='blue', fontweight='bold')

# Vorwiderstand R2 (220Ω) für rote LED
R2_x = col_xs[10]
R2_y = row_ys_top[0]
r2_body = FancyBboxPatch((R2_x-0.38, R2_y-0.12), 0.76, 0.24,
                          boxstyle="round,pad=0.04",
                          facecolor='#D4A843', edgecolor='#8B6914', lw=1.5, zorder=8)
ax.add_patch(r2_body)
for xi, c in zip([-0.18,-0.06,0.06,0.2], ['#DD2222','#DD2222','#111111','#C0A020']):
    ax.plot(R2_x+xi, R2_y, '|', color=c, markersize=8, markeredgewidth=2, zorder=9)
ax.text(R2_x, R2_y-0.28, 'R2  220Ω', ha='center', fontsize=6,
        color='#333322', fontweight='bold')

# GRÜNE LED (Status)
led_gruen_x = col_xs[14]
led_gruen_y = BB_Y + BB_H + 1.0
led_gruen_body = plt.Circle((led_gruen_x, led_gruen_y), 0.28,
                              facecolor='#44CC44', edgecolor='#228822', lw=2, zorder=8)
ax.add_patch(led_gruen_body)
for angle in [30, 60]:
    rad = np.radians(angle)
    ax.annotate('', xy=(led_gruen_x+0.45*np.cos(rad), led_gruen_y+0.45*np.sin(rad)),
                xytext=(led_gruen_x+0.28*np.cos(rad), led_gruen_y+0.28*np.sin(rad)),
                arrowprops=dict(arrowstyle='->', color='#66EE66', lw=1.0))
ax.text(led_gruen_x, led_gruen_y, '▶', ha='center', va='center', fontsize=8,
        color='#228822', zorder=9)
ax.text(led_gruen_x, led_gruen_y-0.55, 'LED2\nGrün (Scharf)', ha='center', fontsize=6,
        color='#222211', fontweight='bold')
ax.plot(led_gruen_x-0.1, led_gruen_y+0.28, 'o', color='#C8A830', markersize=3.5, zorder=10)
ax.plot(led_gruen_x+0.1, led_gruen_y+0.28, 'o', color='#C8A830', markersize=3.5, zorder=10)
ax.text(led_gruen_x-0.22, led_gruen_y+0.42, '+', fontsize=7, color='red', fontweight='bold')
ax.text(led_gruen_x+0.12, led_gruen_y+0.42, '−', fontsize=9, color='blue', fontweight='bold')

# Vorwiderstand R3 (220Ω) für grüne LED
R3_x = col_xs[14]
R3_y = row_ys_top[0]
r3_body = FancyBboxPatch((R3_x-0.38, R3_y-0.12), 0.76, 0.24,
                          boxstyle="round,pad=0.04",
                          facecolor='#D4A843', edgecolor='#8B6914', lw=1.5, zorder=8)
ax.add_patch(r3_body)
for xi, c in zip([-0.18,-0.06,0.06,0.2], ['#DD2222','#DD2222','#111111','#C0A020']):
    ax.plot(R3_x+xi, R3_y, '|', color=c, markersize=8, markeredgewidth=2, zorder=9)
ax.text(R3_x, R3_y-0.28, 'R3  220Ω', ha='center', fontsize=6,
        color='#333322', fontweight='bold')

# PIEZO BUZZER
pz_x = col_xs[19]
pz_y = BB_Y + BB_H + 1.0
pz_outer = plt.Circle((pz_x, pz_y), 0.45, color='#1A1A1A', zorder=8)
ax.add_patch(pz_outer)
pz_mid = plt.Circle((pz_x, pz_y), 0.33, color='#444444', zorder=9)
ax.add_patch(pz_mid)
pz_inner = plt.Circle((pz_x, pz_y), 0.14, color='#C8A830', zorder=10)
ax.add_patch(pz_inner)
ax.text(pz_x, pz_y-0.65, 'BZ1\nPiezo (passiv)', ha='center', fontsize=6,
        color='#222211', fontweight='bold')
ax.plot(pz_x-0.15, pz_y+0.45, 'o', color='#C8A830', markersize=3.5, zorder=11)
ax.plot(pz_x+0.15, pz_y+0.45, 'o', color='#C8A830', markersize=3.5, zorder=11)
ax.text(pz_x-0.28, pz_y+0.6, '+', fontsize=7, color='red', fontweight='bold')
ax.text(pz_x+0.15, pz_y+0.6, '−', fontsize=9, color='blue', fontweight='bold')

# RESET-TASTER
btn_x = col_xs[23]
btn_y = BB_Y + BB_H/2 + 0.8
btn_body = FancyBboxPatch((btn_x-0.35, btn_y-0.35), 0.7, 0.7,
                           boxstyle="round,pad=0.08",
                           facecolor='#DDDDDD', edgecolor='#555555', lw=2, zorder=8)
ax.add_patch(btn_body)
btn_cap = plt.Circle((btn_x, btn_y), 0.18, color='#3333CC', zorder=9)
ax.add_patch(btn_cap)
ax.text(btn_x, btn_y-0.6, 'SW1\nReset-Taster', ha='center', fontsize=6,
        color='#222211', fontweight='bold')
ax.plot(btn_x-0.25, btn_y+0.35, 'o', color='#C8A830', markersize=3.5, zorder=10)
ax.plot(btn_x+0.25, btn_y+0.35, 'o', color='#C8A830', markersize=3.5, zorder=10)

# ---- KABELVERBINDUNGEN ----
RED   = '#DD2222'
BLACK = '#222222'
YELLOW= '#CCAA00'
ORANGE= '#EE7700'
GREEN = '#228822'
PURPLE= '#8822CC'
CYAN  = '#0099AA'

# 5V → VCC-Schiene
p5v = nano_pins.get('5V', (AN_X+AN_W+0.12, 7.5))
wire_h(ax, p5v[0], p5v[1], col_xs[1], BB_Y+BB_H-0.3, RED, lw=2.5)

# GND → GND-Schiene
pgnd = nano_pins.get('GND', (AN_X-0.12, 4.5))
wire(ax, pgnd[0], pgnd[1], col_xs[1], BB_Y+BB_H-0.58, BLACK, lw=2.5)

# VCC-Schiene oben ↔ unten verbinden
ax.plot([BB_X+0.4, BB_X+0.4], [BB_Y+BB_H-0.3, BB_Y+0.35],
        color=RED, lw=2.0, zorder=5, solid_capstyle='round')
ax.plot([BB_X+0.55, BB_X+0.55], [BB_Y+BB_H-0.58, BB_Y+0.65],
        color=BLACK, lw=2.0, zorder=5, solid_capstyle='round')

# D7 → Laser S-Pin
pd7 = nano_pins.get('D7', (AN_X-0.12, 5.8))
wire(ax, pd7[0], pd7[1], laser_x-0.35, laser_y+0.28, YELLOW, lw=2.0)

# Laser GND → GND-Schiene
wire_h(ax, laser_x, laser_y+0.28, col_xs[3], BB_Y+BB_H-0.58, BLACK, lw=2.0)

# Laser VCC → VCC-Schiene
wire_h(ax, laser_x+0.35, laser_y+0.28, col_xs[4], BB_Y+BB_H-0.3, RED, lw=2.0)

# LDR Pin1 → A0 (über Spannungsteiler-Knoten)
pa0 = nano_pins.get('A0', (AN_X+AN_W+0.12, 5.2))
# LDR → R1 Knoten → A0
ax.plot([ldr_x-0.25, R1_x+0.45], [ldr_y+0.38, R1_y],
        color=CYAN, lw=2.0, zorder=5, solid_capstyle='round')
wire(ax, R1_x-0.45, R1_y, pa0[0], pa0[1], CYAN, lw=2.0)
dot(ax, R1_x-0.45, R1_y, CYAN)

# LDR Pin2 → VCC
ax.plot([ldr_x+0.25, ldr_x+0.25, BB_X+BB_W-0.3], [ldr_y+0.38, BB_Y+BB_H-0.3, BB_Y+BB_H-0.3],
        color=RED, lw=2.0, zorder=5, solid_capstyle='round')

# R1 unteres Ende → GND
wire_h(ax, R1_x+0.45, R1_y, col_xs[27], BB_Y+BB_H-0.58, BLACK, lw=2.0)

# D6 → R2 → LED Rot
pd6 = nano_pins.get('D6', (AN_X-0.12, 6.1))
wire(ax, pd6[0], pd6[1], R2_x-0.38, R2_y, ORANGE, lw=2.0)
ax.plot([R2_x+0.38, led_rot_x-0.1], [R2_y, led_rot_y+0.28],
        color=ORANGE, lw=2.0, zorder=5, solid_capstyle='round')
wire_h(ax, led_rot_x+0.1, led_rot_y+0.28, col_xs[10], BB_Y+BB_H-0.58, BLACK, lw=2.0)

# D5 → R3 → LED Grün
pd5 = nano_pins.get('D5', (AN_X-0.12, 6.3))
wire(ax, pd5[0], pd5[1], R3_x-0.38, R3_y, GREEN, lw=2.0)
ax.plot([R3_x+0.38, led_gruen_x-0.1], [R3_y, led_gruen_y+0.28],
        color=GREEN, lw=2.0, zorder=5, solid_capstyle='round')
wire_h(ax, led_gruen_x+0.1, led_gruen_y+0.28, col_xs[14], BB_Y+BB_H-0.58, BLACK, lw=2.0)

# D9 → Piezo +
pd9 = nano_pins.get('D9', (AN_X-0.12, 5.5))
wire(ax, pd9[0], pd9[1], pz_x-0.15, pz_y+0.45, PURPLE, lw=2.0)
wire_h(ax, pz_x+0.15, pz_y+0.45, col_xs[19], BB_Y+BB_H-0.58, BLACK, lw=2.0)

# D2 → Taster
pd2 = nano_pins.get('D2', (AN_X-0.12, 4.8))
wire(ax, pd2[0], pd2[1], btn_x-0.25, btn_y+0.35, '#AA2299', lw=2.0)
wire_h(ax, btn_x+0.25, btn_y+0.35, col_xs[23], BB_Y+BB_H-0.58, BLACK, lw=2.0)

# ---- LEGENDE ----
leg_x, leg_y = 0.5, 8.55
ax.text(leg_x, leg_y, 'Legende:', fontsize=8.5, fontweight='bold', color='#222211')
legend_data = [
    (RED,    2.5, 'VCC / +5V'),
    (BLACK,  2.5, 'GND'),
    (YELLOW, 2.0, 'D7 → Laser (Signal)'),
    (CYAN,   2.0, 'A0 ← LDR (Analogsignal)'),
    (ORANGE, 2.0, 'D6 → LED Rot'),
    (GREEN,  2.0, 'D5 → LED Grün'),
    (PURPLE, 2.0, 'D9 → Piezo'),
    ('#AA2299', 2.0, 'D2 → Taster'),
]
for i, (color, lw, label) in enumerate(legend_data):
    lx = leg_x + (i % 4) * 3.3
    ly = leg_y - 0.42 - (i // 4) * 0.42
    ax.plot([lx, lx+0.55], [ly, ly], color=color, lw=float(lw), zorder=10,
            solid_capstyle='round')
    ax.text(lx+0.7, ly, label, fontsize=7, va='center', color='#333322')

# Rahmen
frame = FancyBboxPatch((0.15, 0.15), 13.7, 17.7,
                        boxstyle="round,pad=0.1",
                        fill=False, edgecolor='#4A7A9B', lw=3, zorder=0)
ax.add_patch(frame)
ax.text(7.0, 0.35, 'Projekt: LASER-STOLPERDRAHT-ALARM v1.0  |  Maßstab: nicht maßstabsgetreu',
        ha='center', fontsize=6.5, color='#888877')

plt.tight_layout(pad=0.2)
plt.savefig('/home/ubuntu/arduino-ideen/02_Laser_Stolperdraht/assets/verdrahtung_breadboard.png',
            dpi=200, bbox_inches='tight', facecolor='#F2F2EE')
plt.close()
print("Breadboard-Diagramm gespeichert.")

# ================================================================
# DIAGRAMM 2: SCHEMATISCHER SCHALTPLAN
# ================================================================

fig2, ax2 = plt.subplots(figsize=(15, 10))
ax2.set_xlim(0, 15)
ax2.set_ylim(0, 10)
ax2.set_aspect('equal')
ax2.axis('off')
fig2.patch.set_facecolor('#FAFAF8')

def line2(x1,y1,x2,y2,color='#111111',lw=1.8,zorder=3):
    ax2.plot([x1,x2],[y1,y2],color=color,lw=lw,zorder=zorder,solid_capstyle='round')

def lbl2(x,y,text,ha='center',va='center',fs=8,bold=False,color='#111111'):
    ax2.text(x,y,text,ha=ha,va=va,fontsize=fs,color=color,
             fontweight='bold' if bold else 'normal')

# Titel
tb = FancyBboxPatch((0.3,9.3),14.4,0.55,boxstyle="round,pad=0.1",
                     facecolor='#1A4A6B',edgecolor='#0D2E45',lw=2,zorder=10)
ax2.add_patch(tb)
lbl2(7.5,9.58,'LASER-STOLPERDRAHT-ALARM v1.0  –  Schematischer Schaltplan',
     fs=11,bold=True,color='white')

# VCC / GND Schienen
line2(0.8,8.2,14.2,8.2,'#DD2222',lw=2.0)
line2(0.8,1.2,14.2,1.2,'#111111',lw=2.0)
lbl2(0.5,8.2,'VCC\n+5V',fs=7,bold=True,color='#DD2222')
lbl2(0.5,1.2,'GND',fs=7,bold=True,color='#444444')

# Arduino Nano Block
mc = FancyBboxPatch((1.0,3.0),2.8,5.0,boxstyle="round,pad=0.15",
                     facecolor='#1A6B8A',edgecolor='#0D4A63',lw=2.5,zorder=5)
ax2.add_patch(mc)
lbl2(2.4,5.8,'Arduino\nNANO',fs=10,bold=True,color='white')

# Nano Pins (rechts)
nano_sch_pins = {
    '5V':  (3.8, 7.5), 'GND': (3.8, 6.8),
    'D7':  (3.8, 6.1), 'A0':  (3.8, 5.4),
    'D6':  (3.8, 4.7), 'D5':  (3.8, 4.0),
    'D9':  (3.8, 3.3), 'D2':  (1.0, 4.5),
}
for pin, (px, py) in nano_sch_pins.items():
    if px > 2.0:
        ax2.plot(px, py, 's', color='#C8A830', markersize=5, zorder=7)
        lbl2(px+0.15, py, pin, ha='left', fs=7, bold=True, color='#DDDDDD')
        line2(3.8, py, px, py, '#CCCCCC', lw=1.2)
    else:
        ax2.plot(px, py, 's', color='#C8A830', markersize=5, zorder=7)
        lbl2(px-0.15, py, pin, ha='right', fs=7, bold=True, color='#DDDDDD')

# 5V → VCC
line2(3.8,7.5,4.5,7.5,'#DD2222',lw=1.8)
line2(4.5,7.5,4.5,8.2,'#DD2222',lw=1.8)
ax2.plot(4.5,8.2,'o',color='#DD2222',markersize=5,zorder=6)

# GND → GND
line2(3.8,6.8,5.0,6.8,'#111111',lw=1.8)
line2(5.0,6.8,5.0,1.2,'#111111',lw=1.8)
ax2.plot(5.0,1.2,'o',color='#111111',markersize=5,zorder=6)

# ---- LASER-ZWEIG ----
# D7 → Laser
line2(3.8,6.1,5.8,6.1,'#CCAA00',lw=1.8)
laser_sch = FancyBboxPatch((5.8,5.8),1.2,0.6,boxstyle="round,pad=0.06",
                            facecolor='#1A1A1A',edgecolor='#111111',lw=2,zorder=6)
ax2.add_patch(laser_sch)
lbl2(6.4,6.1,'KY-008\nLaser',fs=7,bold=True,color='white')
# Laserstrahl
ax2.annotate('',xy=(8.5,6.1),xytext=(7.0,6.1),
             arrowprops=dict(arrowstyle='->',color='#FF2222',lw=2.0))
ax2.plot([7.0,8.5],[6.1,6.1],color='#FF4444',lw=1.5,linestyle='--',alpha=0.8,zorder=4)
lbl2(7.75,6.35,'Laserstrahl',fs=6.5,color='#CC0000')
# Laser GND
line2(5.8,5.8,5.8,1.2,'#111111',lw=1.8)
ax2.plot(5.8,1.2,'o',color='#111111',markersize=5,zorder=6)
# Laser VCC
line2(7.0,6.4,7.0,8.2,'#DD2222',lw=1.8)
ax2.plot(7.0,8.2,'o',color='#DD2222',markersize=5,zorder=6)

# ---- LDR-SPANNUNGSTEILER ----
# LDR Symbol
ldr_sch_x, ldr_sch_y = 8.5, 6.1
ldr_sch = FancyBboxPatch((ldr_sch_x-0.35,ldr_sch_y-0.25),0.7,0.5,
                          boxstyle="round,pad=0.04",
                          facecolor='#F5E8C0',edgecolor='#8B6914',lw=2,zorder=6)
ax2.add_patch(ldr_sch)
for xi,c in zip([-0.15,0.05,0.2],['#8B6914','#8B6914','#8B6914']):
    ax2.plot(ldr_sch_x+xi,ldr_sch_y,'|',color=c,markersize=8,markeredgewidth=1.5,zorder=7)
# Lichtpfeile
for angle in [50,70]:
    rad=np.radians(angle)
    ax2.annotate('',xy=(ldr_sch_x+0.5*np.cos(rad),ldr_sch_y+0.5*np.sin(rad)),
                 xytext=(ldr_sch_x+0.8*np.cos(rad),ldr_sch_y+0.8*np.sin(rad)),
                 arrowprops=dict(arrowstyle='->',color='#FFAA00',lw=1.0))
lbl2(ldr_sch_x,ldr_sch_y-0.45,'LDR',fs=7,bold=True)
# LDR → VCC
line2(ldr_sch_x,ldr_sch_y+0.25,ldr_sch_x,8.2,'#DD2222',lw=1.8)
ax2.plot(ldr_sch_x,8.2,'o',color='#DD2222',markersize=5,zorder=6)
# Knoten A0
lbl2(ldr_sch_x+0.5,ldr_sch_y-0.25,'Knoten\n→ A0',fs=6,color='#0099AA')
ax2.plot(ldr_sch_x,ldr_sch_y-0.25,'o',color='#0099AA',markersize=5,zorder=7)
# A0 Verbindung
line2(ldr_sch_x,ldr_sch_y-0.25,3.8,5.4,'#0099AA',lw=1.8)
# R1 (10kΩ) Spannungsteiler
r1_sch_x, r1_sch_y = ldr_sch_x, ldr_sch_y-1.0
r1_sch = FancyBboxPatch((r1_sch_x-0.35,r1_sch_y-0.22),0.7,0.44,
                         boxstyle="round,pad=0.04",
                         facecolor='#F5E8C0',edgecolor='#8B6914',lw=2,zorder=6)
ax2.add_patch(r1_sch)
for xi,c in zip([-0.2,-0.07,0.07,0.2,0.28],
                 ['#8B0000','#8B0000','#111111','#C0A020','#C0A020']):
    ax2.plot(r1_sch_x+xi,r1_sch_y,'|',color=c,markersize=10,markeredgewidth=2,zorder=7)
lbl2(r1_sch_x,r1_sch_y-0.38,'R1  10kΩ',fs=7,bold=True)
line2(ldr_sch_x,ldr_sch_y-0.25,r1_sch_x,r1_sch_y+0.22,lw=1.8)
line2(r1_sch_x,r1_sch_y-0.22,r1_sch_x,1.2,'#111111',lw=1.8)
ax2.plot(r1_sch_x,1.2,'o',color='#111111',markersize=5,zorder=6)

# ---- LED ROT (D6 → R2 → LED → GND) ----
# R2 (220Ω)
r2_x,r2_y = 10.0,6.5
r2_sch = FancyBboxPatch((r2_x-0.38,r2_y-0.18),0.76,0.36,
                         boxstyle="round,pad=0.04",
                         facecolor='#F5E8C0',edgecolor='#8B6914',lw=2,zorder=6)
ax2.add_patch(r2_sch)
for xi,c in zip([-0.18,-0.06,0.06,0.2],['#DD2222','#DD2222','#111111','#C0A020']):
    ax2.plot(r2_x+xi,r2_y,'|',color=c,markersize=9,markeredgewidth=2,zorder=7)
lbl2(r2_x,r2_y+0.35,'R2  220Ω',fs=7,bold=True)
line2(3.8,4.7,r2_x-0.38,r2_y,'#EE7700',lw=1.8)
# LED Rot Symbol
led_r_x,led_r_y = 11.0,6.5
tri_r = plt.Polygon([[led_r_x-0.22,led_r_y+0.22],[led_r_x-0.22,led_r_y-0.22],[led_r_x+0.22,led_r_y]],
                      closed=True,facecolor='#FF4444',edgecolor='#CC0000',lw=2,zorder=6)
ax2.add_patch(tri_r)
line2(led_r_x+0.22,led_r_y+0.28,led_r_x+0.22,led_r_y-0.28,lw=2.5)
line2(r2_x+0.38,r2_y,led_r_x-0.22,led_r_y,lw=1.8)
line2(led_r_x+0.22,led_r_y,led_r_x+0.6,led_r_y)
line2(led_r_x+0.6,led_r_y,led_r_x+0.6,1.2,'#111111',lw=1.8)
ax2.plot(led_r_x+0.6,1.2,'o',color='#111111',markersize=5,zorder=6)
lbl2(led_r_x,led_r_y-0.5,'LED1\nRot',fs=7,bold=True)
# Lichtpfeile
for a in [30,50]:
    rad=np.radians(a)
    ax2.annotate('',xy=(led_r_x+0.5*np.cos(rad),led_r_y+0.5*np.sin(rad)),
                 xytext=(led_r_x+0.28*np.cos(rad),led_r_y+0.28*np.sin(rad)),
                 arrowprops=dict(arrowstyle='->',color='#FF6666',lw=1.0))

# ---- LED GRÜN (D5 → R3 → LED → GND) ----
r3_x,r3_y = 10.0,4.5
r3_sch = FancyBboxPatch((r3_x-0.38,r3_y-0.18),0.76,0.36,
                         boxstyle="round,pad=0.04",
                         facecolor='#F5E8C0',edgecolor='#8B6914',lw=2,zorder=6)
ax2.add_patch(r3_sch)
for xi,c in zip([-0.18,-0.06,0.06,0.2],['#DD2222','#DD2222','#111111','#C0A020']):
    ax2.plot(r3_x+xi,r3_y,'|',color=c,markersize=9,markeredgewidth=2,zorder=7)
lbl2(r3_x,r3_y+0.35,'R3  220Ω',fs=7,bold=True)
line2(3.8,4.0,r3_x-0.38,r3_y,'#228822',lw=1.8)
led_g_x,led_g_y = 11.0,4.5
tri_g = plt.Polygon([[led_g_x-0.22,led_g_y+0.22],[led_g_x-0.22,led_g_y-0.22],[led_g_x+0.22,led_g_y]],
                      closed=True,facecolor='#44CC44',edgecolor='#228822',lw=2,zorder=6)
ax2.add_patch(tri_g)
line2(led_g_x+0.22,led_g_y+0.28,led_g_x+0.22,led_g_y-0.28,lw=2.5)
line2(r3_x+0.38,r3_y,led_g_x-0.22,led_g_y,lw=1.8)
line2(led_g_x+0.22,led_g_y,led_g_x+0.8,led_g_y)
line2(led_g_x+0.8,led_g_y,led_g_x+0.8,1.2,'#111111',lw=1.8)
ax2.plot(led_g_x+0.8,1.2,'o',color='#111111',markersize=5,zorder=6)
lbl2(led_g_x,led_g_y-0.5,'LED2\nGrün',fs=7,bold=True)
for a in [30,50]:
    rad=np.radians(a)
    ax2.annotate('',xy=(led_g_x+0.5*np.cos(rad),led_g_y+0.5*np.sin(rad)),
                 xytext=(led_g_x+0.28*np.cos(rad),led_g_y+0.28*np.sin(rad)),
                 arrowprops=dict(arrowstyle='->',color='#66EE66',lw=1.0))

# ---- PIEZO (D9 → Buzzer → GND) ----
bz_x,bz_y = 13.0,5.5
bz_body = FancyBboxPatch((bz_x-0.4,bz_y-0.32),0.8,0.64,
                          boxstyle="square,pad=0.05",
                          facecolor='#F0F0F0',edgecolor='#333333',lw=2,zorder=6)
ax2.add_patch(bz_body)
for r in [0.55,0.75]:
    arc = patches.Arc((bz_x+0.4,bz_y),r,r*1.2,angle=0,theta1=-60,theta2=60,
                       color='#333333',lw=1.5,zorder=7)
    ax2.add_patch(arc)
lbl2(bz_x-0.6,bz_y,'BZ1\nPiezo',ha='right',fs=7,bold=True)
line2(3.8,3.3,bz_x-0.4,bz_y,'#8822CC',lw=1.8)
line2(bz_x+0.4,bz_y,bz_x+0.8,bz_y)
line2(bz_x+0.8,bz_y,bz_x+0.8,1.2,'#111111',lw=1.8)
ax2.plot(bz_x+0.8,1.2,'o',color='#111111',markersize=5,zorder=6)

# ---- TASTER (D2 → Taster → GND) ----
sw_x,sw_y = 13.0,3.0
ax2.plot([sw_x-0.3,sw_x+0.3],[sw_y,sw_y+0.4],color='#111111',lw=1.8,zorder=6)
ax2.plot(sw_x-0.3,sw_y,'o',color='#111111',markersize=5,zorder=7)
ax2.plot(sw_x+0.3,sw_y+0.4,'o',color='#111111',markersize=5,zorder=7)
lbl2(sw_x,sw_y-0.3,'SW1\nTaster',fs=7,bold=True)
line2(1.0,4.5,sw_x-0.3,sw_y,'#AA2299',lw=1.8)
line2(sw_x+0.3,sw_y+0.4,sw_x+0.6,sw_y+0.4)
line2(sw_x+0.6,sw_y+0.4,sw_x+0.6,1.2,'#111111',lw=1.8)
ax2.plot(sw_x+0.6,1.2,'o',color='#111111',markersize=5,zorder=6)

# GND-Symbole
for gx,gy in [(5.0,1.2),(5.8,1.2),(r1_sch_x,1.2),(led_r_x+0.6,1.2),
              (led_g_x+0.8,1.2),(bz_x+0.8,1.2),(sw_x+0.6,1.2)]:
    for i,(w,dy) in enumerate([(0.25,0),(0.17,-0.1),(0.09,-0.2)]):
        line2(gx-w,gy-0.25-dy,gx+w,gy-0.25-dy,lw=1.5+i*0.3)

# Rahmen
frame2 = FancyBboxPatch((0.1,0.1),14.8,9.8,boxstyle="round,pad=0.1",
                          fill=False,edgecolor='#4A7A9B',lw=3,zorder=0)
ax2.add_patch(frame2)
lbl2(7.5,0.35,'Bauteile: KY-008 Laser | LDR + R1 10kΩ | R2,R3 220Ω | LED rot/grün | Piezo (passiv) | Taster',
     fs=7,color='#444444')

plt.tight_layout(pad=0.2)
plt.savefig('/home/ubuntu/arduino-ideen/02_Laser_Stolperdraht/assets/schaltplan_schematisch.png',
            dpi=200,bbox_inches='tight',facecolor='#FAFAF8')
plt.close()
print("Schematischer Schaltplan gespeichert.")
