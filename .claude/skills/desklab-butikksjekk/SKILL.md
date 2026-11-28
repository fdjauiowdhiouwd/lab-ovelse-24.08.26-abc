---
name: desklab-butikksjekk
description: Helsesjekk av DeskLab Shopify-butikken – finner produkter i utkast, lavt lager, manglende tags/produkttype/SEO, uryddige titler og gamle arkiverte produkter, og foreslår prioriterte tiltak. Bruk når eieren spør «hvordan står det til med butikken», vil rydde, eller forberede lansering/kampanje.
---
# DeskLab butikksjekk

## 1. Hent data (via `analyst`, kun lesing)
- `get-shop-info`
- Alle produkter (paginér, 100 per side): tittel, status, produkttype, vendor, tags, totalInventory, pris, SEO-tittel/-beskrivelse, antall bilder
- Kolleksjoner med antall produkter
- Salg siste 30 dager (`run-analytics-query`) hvis tilgjengelig

## 2. Sjekk mot DeskLab-standarden
| Sjekk | Regel |
|---|---|
| Status | DRAFT med lager og bilder → kandidat for publisering |
| Lager | < 20 = lavt, 0 = utsolgt |
| Tittel | `Navn™`, ingen lange leverandørtitler (AliExpress-stil) |
| Vendor/tags | vendor `DeskLab`, tag `desklab` + kategori |
| Produkttype | ikke tom |
| SEO | tittel ≤ 60, beskrivelse ≤ 155 tegn, engelsk |
| Bilder | minst 3 |
| Kolleksjon | hvert aktivt produkt i minst én kolleksjon |
| Gamle varer | arkiverte «Snuteglede»-produkter – foreslå sletting kun hvis eieren vil |

## 3. Rapport
Skriv `rapporter/butikksjekk-{ÅÅÅÅ-MM-DD}.md`:
1. Status i tall (aktive/utkast/arkiverte, lavt lager)
2. Topp 5 tiltak, prioritert etter effekt på salg
3. Full tabell over avvik per produkt
4. Forslag til endringer (fra → til)

## 4. Utføre endringer
Bare etter eksplisitt «ja»: overlat til `store-manager`, som viser endringene og utfører dem.
