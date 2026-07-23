# -*- coding: utf-8 -*-
"""Civil 3D site for 899 Virginia Park: crisp 3in aerial + neighbor parcel lines +
extruded building footprints, Jeff's parcel + house highlighted, labels. EPSG:2253."""
import ezdxf, json, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
GIS = os.path.join(HERE, "gis")
CX, CY, R = 13469759.5, 320851.0, 260.0
JEFF_PID = "04001887."
OUT = os.path.join(HERE, "899VP_Site.dxf")

def outer(g):
    c = g["coordinates"]
    if g["type"] == "MultiPolygon": c = c[0]
    return c[0]
def cen(r):
    xs = [p[0] for p in r]; ys = [p[1] for p in r]; return sum(xs)/len(xs), sum(ys)/len(ys)
def height(pr):
    h = pr.get("MEDIAN_HGT")
    try:
        if h and float(h) > 6: return float(h)
    except: pass
    s = pr.get("STORIES")
    try:
        if s and float(s) > 0: return float(s)*11.0
    except: pass
    return 22.0

doc = ezdxf.new("R2018"); msp = doc.modelspace()
for n, c in (("AERIAL", 250), ("PARCELS", 8), ("PARCEL-JEFF", 1), ("BLDG-3D", 9),
             ("BLDG-JEFF", 30), ("LABELS", 2)):
    doc.layers.add(n, color=c)

# aerial
minx, miny = CX-R, CY-R
img = os.path.join(GIS, "aerial_899vp.jpg")
idef = doc.add_image_def(filename=img, size_in_pixel=(int(R*2*4), int(R*2*4)))
msp.add_image(insert=(minx, miny, -0.5), size_in_units=(R*2, R*2), image_def=idef,
              rotation=0, dxfattribs={"layer": "AERIAL"})

# parcels (property lines)
par = json.load(open(os.path.join(GIS, "neighbors_parcels.geojson")))
jeff_pr = None
for f in par["features"]:
    pr = f["properties"]; r = outer(f["geometry"])
    isj = (pr.get("parcel_id") == JEFF_PID)
    msp.add_lwpolyline([(p[0], p[1]) for p in r], close=True,
                       dxfattribs={"layer": "PARCEL-JEFF" if isj else "PARCELS", "elevation": 0.1})
    if isj: jeff_pr = pr
    # neighbor id label (small)
    cx, cy = cen(r)
    msp.add_text(pr.get("parcel_id", ""), height=3,
                 dxfattribs={"layer": "LABELS"}).set_placement((cx-10, cy))

# buildings
fp = json.load(open(os.path.join(GIS, "neighbors_footprints.geojson")))
for f in fp["features"]:
    r = [(p[0], p[1]) for p in outer(f["geometry"])]
    if len(r) < 3: continue
    h = height(f["properties"])
    bc = cen(r); isj = math.hypot(bc[0]-CX, bc[1]-CY) < 45   # Jeff's house = nearest footprint
    lyr = "BLDG-JEFF" if isj else "BLDG-3D"
    for i in range(len(r)-1):
        x0, y0 = r[i]; x1, y1 = r[i+1]
        msp.add_3dface([(x0, y0, 0), (x1, y1, 0), (x1, y1, h), (x0, y0, h)], dxfattribs={"layer": lyr})
    cx0, cy0 = bc
    for i in range(len(r)-1):
        x0, y0 = r[i]; x1, y1 = r[i+1]
        msp.add_3dface([(cx0, cy0, h), (x0, y0, h), (x1, y1, h), (cx0, cy0, h)], dxfattribs={"layer": lyr})

# Jeff label
if jeff_pr:
    t = ("899 VIRGINIA PARK  (parcel %s)\\Powner %s\\P%s  built %s\\P%s ac  %sx%s lot" % (
        jeff_pr.get("parcel_id"), jeff_pr.get("taxpayer_1"), jeff_pr.get("property_class_description"),
        jeff_pr.get("year_built"), jeff_pr.get("total_acreage"), jeff_pr.get("frontage"), jeff_pr.get("depth")))
    m = msp.add_mtext(t, dxfattribs={"layer": "LABELS", "char_height": 5}); m.set_location((CX+20, CY+30, 40))

doc.saveas(OUT)
print("SAVED", OUT, "| Jeff parcel found:", jeff_pr is not None)
