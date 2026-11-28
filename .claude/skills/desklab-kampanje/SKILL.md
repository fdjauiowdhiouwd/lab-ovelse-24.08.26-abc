---
name: desklab-kampanje
description: Lag en komplett Meta Ads-kampanje (Facebook/Instagram) for DeskLab – produktvalg, målgrupper, tekster, kreative briefer og navnestruktur – og bygg den eventuelt som pauset utkast i Ads Manager via Claude in Chrome. Bruk når eieren ber om kampanje, annonser, «ads», ny test eller Black Friday/jul-kampanje.
---
# DeskLab-kampanje

Kjør stegene i rekkefølge. Lever underveis korte statuslinjer på norsk.

## 1. Brief (spør kun om det som mangler)
- Mål: salg / test nye produkter / retargeting
- Daglig budsjett (USD) – standard $20–30/dag på testfase
- Marked – standard US
- Ev. tilbud (rabattkode, fri frakt) – bruk kun tilbud som faktisk finnes

## 2. Data → `analyst`
Hent aktive produkter, pris, lager og salg siste 30 dager. Utelukk lager < 20 og arkiverte «Snuteglede»-produkter.

## 3. Plan → `strategist`
Velg 2–4 produkter og struktur med navnemalen:
- Kampanje `US | SALES | {tema} | {ÅÅÅÅ-MM}`
- Annonsesett `US | BROAD | Advantage+`, `US | INT | {interesse-stack}`, `US | RT | Visitors 30d + ATC 14d`
- Annonse `C{n}-V{n} | {IMG|VID|UGC} | {vinkel}`

## 4. Parallelt → `audience`, så `copywriter` og `producer`
Kjør `copywriter` og `producer` parallelt når vinklene fra `audience` er klare.

## 5. Leveranse
Skriv planen til `kampanjer/{ÅÅÅÅ-MM-DD}-{tema}.md` med:
1. Sammendrag (mål, budsjett, produkter, KPI-er)
2. Struktur-tabell (kampanje → sett → annonser)
3. Per annonse: primary text, headline, description, CTA, kreativ brief, filnavn
4. Sjekkliste før lansering (pixel/Conversions API aktiv, UTM `utm_source=meta&utm_campaign={kampanjenavn}`, domene verifisert, rabattkode testet)

## 6. Bygge i Ads Manager (valgfritt)
Kun hvis eieren ber om det **og** Claude in Chrome er tilgjengelig (krever eierens egen maskin):
- Last inn skillen `anthropic-skills:chrome-browser` først.
- Bygg alt med status **Paused**. Publiser aldri, og endre aldri betalingsinfo.
- Stopp og spør ved innlogging, 2FA, betalingsdialoger eller policy-advarsler.
Er Chrome ikke tilgjengelig: lever planen og si at den kan bygges når en maskin er koblet til.
