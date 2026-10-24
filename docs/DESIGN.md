# GrantDE visual direction

GrantDE uses a neutral foundation, violet accents and a clear sans/serif typographic balance.

## Visual language

- Black and off-white foundations, with blue/violet and soft colour blocks.
- A rounded header, circular brand mark and pill-shaped actions.
- Bold sans-serif headings with italic serif emphasis in the main message.
- Generous spacing, rounded cards, fine borders and restrained shadows.
- A little visual play in the homepage feature card; aligned cards in results.

GrantDE uses local Helvetica/Arial and Georgia fonts without external font requests.

## Main tokens

| Role | Light | Dark |
| --- | --- | --- |
| Page | `#f7f7f3` | `#101014` |
| Card / control | `#ffffff` | `#1b1b22` |
| Main text | `#080808` | `#f7f7f3` |
| Secondary text | `#5d5d66` | `#b1b1bd` |
| Links and focus | `#4d4bc4` | `#b9baff` |
| Primary action | `#080808` | `#f7f7f3` |
| Primary action text | `#ffffff` | `#101014` |
| Feature panel | `#e8e6ff` | `#29263e` |
| Soft surface | `#eeefff` | `#272735` |

Blue `#6670ff` appears in small decorative details. Text uses
a darker violet in light mode to keep contrast. Dark mode is a GrantDE
adaptation of the same neutral and violet colours.

Tokens live in `static/css/site.css`. Theme bootstrap and the browser's
theme-colour metadata use the same page colours. Static assets have content
versions, so new styles and scripts load together after a rebuild.

## Components and behaviour

- Result cards: 24 px corners; native form controls: 12 px corners.
- Homepage feature card: 32 px corners and a small desktop rotation.
- Header and actions: pill shapes; theme control: 44 px circle.
- Study paths: lilac, violet and aqua surfaces with readable text in both themes.
- Status badges always include words as well as colour.
- Native dropdown options have explicit surface and text colours.
- Mobile navigation stays visible; filters open in the existing modal panel.
- Preserve keyboard focus, reduced motion and layouts down to 320 px.
- Show matching counts only while a filter or search is active; keep catalogue
  totals off the homepage, About page and unfiltered directory.
- Keep nationality conditions on detail pages, without a nationality filter.
