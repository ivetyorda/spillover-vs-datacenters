"""
Generate preview.png for Open Graph card and Substack link preview.
Renders a 1200x630 image showing:
- spillover-risk density field (continents trace themselves)
- existing datacenters as gold circles
- planned datacenters as pink triangles
- title bar + tagline matching the site's dark theme
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patheffects import withStroke
from scipy.ndimage import gaussian_filter
import os

REPO = os.path.dirname(os.path.abspath(__file__))

# ---- Load data ----
with open(os.path.join(REPO, 'data/spillover_risk.json')) as f:
    sp = json.load(f)
with open(os.path.join(REPO, 'data/datacenters.json')) as f:
    dc = json.load(f)

points = sp['points']  # [[lat, lon, weight], ...]
existing = [d for d in dc['datacenters'] if d['status'] == 'existing']
planned  = [d for d in dc['datacenters'] if d['status'] == 'planned']

# ---- Build density field ----
# We'll bin the weighted points into a 2D grid covering -180..180, -60..80,
# then gaussian-blur to get a smooth surface.
LON_MIN, LON_MAX = -180, 180
LAT_MIN, LAT_MAX = -60, 80
NX, NY = 720, 280   # 0.5° resolution

grid = np.zeros((NY, NX), dtype=np.float32)
for lat, lon, w in points:
    if not (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX):
        continue
    xi = int((lon - LON_MIN) / (LON_MAX - LON_MIN) * (NX - 1))
    yi = int((lat - LAT_MIN) / (LAT_MAX - LAT_MIN) * (NY - 1))
    grid[yi, xi] += w

# Smooth — sigma in cells; 0.5°/cell so sigma=8 ≈ 4° of geographic blur
grid_blur = gaussian_filter(grid, sigma=8.0)

# Normalize to 0..1, then nonlinear stretch so faint regions show up
gmax = grid_blur.max()
if gmax > 0:
    grid_norm = grid_blur / gmax
else:
    grid_norm = grid_blur
# soft gamma to lift midtones
grid_show = np.power(grid_norm, 0.75)

# ---- Colormap matching the site (blue → teal → yellow → orange → red) ----
heat_cmap = LinearSegmentedColormap.from_list('spillover', [
    (0.00, (0.043, 0.063, 0.125, 0.0)),     # transparent navy
    (0.05, (0.18, 0.36, 0.55, 0.30)),
    (0.20, (0.27, 0.71, 0.78, 0.55)),
    (0.40, (0.31, 0.82, 0.63, 0.75)),
    (0.60, (0.98, 0.86, 0.31, 0.85)),
    (0.80, (0.98, 0.55, 0.16, 0.92)),
    (1.00, (0.90, 0.16, 0.16, 0.95)),
])

# ---- Figure ----
# OG card: 1200 x 630
W, H = 1200, 630
fig = plt.figure(figsize=(W/100, H/100), dpi=100)
fig.patch.set_facecolor('#0b1020')

# Title strip at top (left 75%) + main map below
# We'll allocate ~ top 110px to header, rest to map
header_h_frac = 0.18

ax = fig.add_axes([0.0, 0.0, 1.0, 1.0 - header_h_frac])
ax.set_facecolor('#0b1020')

# Plot density field
ax.imshow(
    grid_show,
    origin='lower',
    extent=[LON_MIN, LON_MAX, LAT_MIN, LAT_MAX],
    cmap=heat_cmap,
    aspect='auto',
    interpolation='bilinear',
)

# Datacenter markers
ex_lat = [d['lat'] for d in existing]
ex_lon = [d['lon'] for d in existing]
pl_lat = [d['lat'] for d in planned]
pl_lon = [d['lon'] for d in planned]

ax.scatter(ex_lon, ex_lat,
           marker='o', s=42, c='#fbbf24',
           edgecolors='#0b1020', linewidths=1.0,
           zorder=10)
ax.scatter(pl_lon, pl_lat,
           marker='^', s=70, c='#ff6e9c',
           edgecolors='#0b1020', linewidths=1.0,
           zorder=11)

ax.set_xlim(LON_MIN, LON_MAX)
ax.set_ylim(LAT_MIN, LAT_MAX)
ax.set_xticks([]); ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# ---- Header text ----
# Title
fig.text(0.035, 0.88, 'Spillover Risk  ×  AI Datacenters',
         color='#e9ecf7', fontsize=26, fontweight='bold',
         family='DejaVu Sans')
# Tagline
fig.text(0.035, 0.835,
         'Where AI compute build-outs meet zoonotic spillover hotspots',
         color='#9aa3c2', fontsize=13.5,
         family='DejaVu Sans')

# Small attribution chip on the right
fig.text(0.965, 0.86,
         'INTERACTIVE WORLD MAP',
         color='#6ee7ff', fontsize=10.5, fontweight='bold',
         ha='right', family='DejaVu Sans',
         bbox=dict(boxstyle='round,pad=0.4', fc='#161f3f', ec='#263158', lw=0.8))

# Legend strip at the bottom of the map
leg_y = 0.06
# existing
fig.text(0.035, leg_y, '●', color='#fbbf24', fontsize=14,
         path_effects=[withStroke(linewidth=1.5, foreground='#0b1020')])
fig.text(0.055, leg_y, 'Existing datacenter', color='#e9ecf7', fontsize=11,
         family='DejaVu Sans')
# planned
fig.text(0.185, leg_y, '▲', color='#ff6e9c', fontsize=14,
         path_effects=[withStroke(linewidth=1.5, foreground='#0b1020')])
fig.text(0.205, leg_y, 'Planned datacenter', color='#e9ecf7', fontsize=11,
         family='DejaVu Sans')
# heat
fig.text(0.345, leg_y - 0.005, '  ', color='#0b1020', fontsize=11,
         bbox=dict(boxstyle='round,pad=0.2',
                   fc='#e62828', ec='none'))
fig.text(0.378, leg_y, 'Higher spillover risk', color='#e9ecf7', fontsize=11,
         family='DejaVu Sans')

# URL chip on right of footer
fig.text(0.965, leg_y,
         'ivetyorda.github.io/spillover-vs-datacenters',
         color='#9aa3c2', fontsize=10, ha='right',
         family='DejaVu Sans Mono')

out = os.path.join(REPO, 'preview.png')
plt.savefig(out, dpi=100, facecolor='#0b1020', edgecolor='none',
            bbox_inches=None, pad_inches=0)
plt.close()
print('Wrote', out)
print('Dimensions:', W, 'x', H)
