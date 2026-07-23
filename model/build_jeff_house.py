# -*- coding: utf-8 -*-
"""Headless Revit: 899 Virginia Park house shell from the ArcGIS footprint.
Levels Basement/1st/2nd/3rd/Roof, exterior walls per level, floors, roof slab,
georeferenced to the lot (EPSG:2253 shared coords). Env: none (paths inline)."""
from __future__ import print_function
import os, json, traceback
def log(*a): print("[house] " + " ".join(str(x) for x in a))

TPL = r"C:\ProgramData\Autodesk\RVT 2027\Templates\English-Imperial\Default-Multi-discipline.rte"
FOOT = r"C:\21 Jeff House Fix\model\jeff_footprint_local.json"
OUT = r"C:\21 Jeff House Fix\model\899VP_House.rvt"

try:
    from Autodesk.Revit.DB import (Transaction, XYZ, Line, CurveLoop, ElementId, SaveAsOptions,
        ProjectPosition, FilteredElementCollector, Level, Floor, FloorType, Wall, WallType,
        ElementTypeGroup, BuiltInParameter)
    fj = json.load(open(FOOT)); EW, NS = fj["centroid"]; ring = fj["ring"]
    # de-dup consecutive + drop closing dup
    pts = []
    for p in ring:
        if not pts or (abs(pts[-1][0]-p[0]) > 0.05 or abs(pts[-1][1]-p[1]) > 0.05): pts.append(p)
    if len(pts) > 1 and abs(pts[0][0]-pts[-1][0]) < 0.05 and abs(pts[0][1]-pts[-1][1]) < 0.05: pts = pts[:-1]

    app = __revit__.Application
    doc = app.NewProjectDocument(TPL)

    t = Transaction(doc, "coords"); t.Start()
    doc.ActiveProjectLocation.SetProjectPosition(XYZ.Zero, ProjectPosition(EW, NS, 0.0, 0.0)); t.Commit()

    # levels
    LEVELS = [("Basement", -8.0), ("1st Floor", 0.0), ("2nd Floor", 9.5),
              ("3rd Floor", 18.5), ("Roof", 27.5)]
    t = Transaction(doc, "levels"); t.Start()
    existing = list(FilteredElementCollector(doc).OfClass(Level))
    lvl = {}
    for i, (nm, ev) in enumerate(LEVELS):
        if i < len(existing):
            L = existing[i]; L.Elevation = ev
            try: L.Name = nm
            except: pass
        else:
            L = Level.Create(doc, ev);
            try: L.Name = nm
            except: pass
        lvl[nm] = L
    for extra in existing[len(LEVELS):]:
        try: doc.Delete(extra.Id)
        except: pass
    t.Commit()
    log("levels:", [(n, lvl[n].Elevation) for n, _ in LEVELS])

    wtid = doc.GetDefaultElementTypeId(ElementTypeGroup.WallType)
    if wtid == ElementId.InvalidElementId: wtid = FilteredElementCollector(doc).OfClass(WallType).FirstElementId()
    ftid = doc.GetDefaultElementTypeId(ElementTypeGroup.FloorType)
    if ftid == ElementId.InvalidElementId: ftid = FilteredElementCollector(doc).OfClass(FloorType).FirstElementId()

    def loop():
        cl = CurveLoop()
        for i in range(len(pts)):
            a = pts[i]; b = pts[(i+1) % len(pts)]
            cl.Append(Line.CreateBound(XYZ(a[0], a[1], 0), XYZ(b[0], b[1], 0)))
        return cl

    # exterior walls per storey + floor slab at each level
    STOREYS = [("Basement", "1st Floor"), ("1st Floor", "2nd Floor"),
               ("2nd Floor", "3rd Floor"), ("3rd Floor", "Roof")]
    t = Transaction(doc, "shell"); t.Start()
    for base, top in STOREYS:
        h = lvl[top].Elevation - lvl[base].Elevation
        for i in range(len(pts)):
            a = pts[i]; b = pts[(i+1) % len(pts)]
            Wall.Create(doc, Line.CreateBound(XYZ(a[0], a[1], 0), XYZ(b[0], b[1], 0)),
                        wtid, lvl[base].Id, h, 0.0, False, False)
    for nm in ("Basement", "1st Floor", "2nd Floor", "3rd Floor", "Roof"):
        Floor.Create(doc, [loop()], ftid, lvl[nm].Id)
    t.Commit()
    log("walls + floors built (5 slabs, 4 storeys)")

    so = SaveAsOptions(); so.OverwriteExistingFile = True
    doc.SaveAs(OUT, so); doc.Close(True)
    log("SAVED", OUT)
except Exception as e:
    log("ERR:", e); log(traceback.format_exc())
