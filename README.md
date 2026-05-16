# Spillover Risk × AI Datacenters

An interactive world map exploring whether the geographic footprint of large AI datacenters — existing and publicly announced — coincides with regions at elevated zoonotic-pathogen spillover risk.

**Live map:** https://ivetyorda.github.io/spillover-vs-datacenters/

## What it shows

Two overlays on a world map with country borders:

1. **Spillover-risk heatmap** — a stylized synthesis of four peer-reviewed studies on the spatial distribution of zoonotic-pathogen spillover risk. Hotspot regions are sampled with weighted points and rendered as a smooth Leaflet.heat surface.
2. **Major AI datacenters** — circles for existing facilities, triangles for publicly announced (planned) facilities. Click any marker for operator, location, and a short context note.

Layer toggles in the top-right let you turn heatmap, existing, planned, and country borders on or off independently.

## Source papers (spillover risk)

1. Simkin R.D. et al. (2025). *Zoonotic Host Richness in the Global Wildland–Urban Interface.* Global Change Biology 31:e70039. DOI: 10.1111/gcb.70039
2. Lancet Planetary Health (2024). *Mapping hotspots of zoonotic pathogen emergence: an integrated model-based and participatory-based approach.* PIIS2542-5196(24)00309-7
3. Plowright et al. (2024). *Prediction of viral spillover risk based on the mass action principle.* PMC11061335
4. Choo J. et al. (2023). *Hotspots of zoonotic disease risk from wildlife hunting and trade in the tropics.* Integrative Conservation 2:165–175. DOI: 10.1002/inc3.34

## A note on fidelity

The heatmap is a **stylized synthesis**, not a calibrated model output. The raw rasters behind these papers are not all publicly available as downloadable layers. Hotspot regions and intensity gradients are seeded from the papers' described findings; Leaflet.heat then interpolates the surface. For quantitative work, read the source papers directly.

The datacenter list is curated from public sources (hyperscaler data-center pages, Reuters / AP / company press releases) and is not exhaustive — many smaller AI training clusters live in colocation space without published coordinates.

## Repo contents

- `index.html` — the single-file interactive map.
- `data/spillover_risk.json` — weighted points for the heatmap with regional metadata.
- `data/datacenters.json` — datacenter list with coordinates, status, operator, notes.

## License

MIT — see [LICENSE](LICENSE).
