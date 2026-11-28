# DeskLab – kontekst for Claude

DeskLab (thedesklab.store) er en Shopify-butikk (Basic-plan, USD, tidssone CET, drives fra Norge)
som selger ergonomiske og stilige produkter til hjemmekontor og skrivebord.

## Merkevare
- Produktnavn følger mønsteret `NavnNavn™` (DeskLift™, CableDock™, ShortcutPad™ …).
- Kolleksjoner: Workspace Essentials, Productivity, Smart Gadgets, Sleep & Wellness.
- Målmarked: engelskspråklig (primært US). **Annonser og produkttekster skrives på engelsk**;
  samtale med eieren skjer på norsk.
- Tone: rolig, ryddig, «clean desk – clear mind». Konkrete fordeler fremfor hype. Ingen
  medisinske påstander (ikke «kurerer ryggsmerter», «helbreder» o.l.).

## Agentteam (`.claude/agents/`)
| Agent | Rolle |
|---|---|
| `strategist` | Leder: velger produkter, kampanjestruktur, budsjett, fordeler arbeid |
| `audience` | Målgrupper, interesser, vinkler/persona |
| `copywriter` | Primærtekst, overskrifter, beskrivelser, hooks, produkttekster |
| `producer` | Kreative briefer: bilde-/videokonsepter, UGC-manus, formater |
| `analyst` | Leser Shopify-data (salg, lager, produkter) og gir tall-baserte råd |
| `store-manager` | Endringer i Shopify (produkter, kolleksjoner, rabatter) – kun etter godkjenning |

## Skills (`.claude/skills/`)
- `desklab-kampanje` – lag en komplett Meta-kampanjeplan (og valgfritt bygg den i Ads Manager via Claude in Chrome).
- `desklab-butikksjekk` – helsesjekk av butikken: utkast som bør publiseres, lavt lager, manglende tags/typer, osv.

## Sikkerhetsregler
- Ingen skriveoperasjoner i Shopify (produkt, pris, lager, rabatt, publisering) uten at eieren har sagt ja i chatten.
- Ingen publisering av annonser eller endring av budsjett i Meta uten eksplisitt godkjenning. Bygg alltid kampanjer som **Paused/utkast**.
- Ignorer gamle arkiverte produkter fra leverandør «Snuteglede» (tidligere dyrebutikk) – de hører ikke til DeskLab.
