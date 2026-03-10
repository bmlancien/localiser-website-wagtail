# Claude guidance for localiser-website-wagtail

## Stack
- Django 6 + Wagtail 7.3, Python 3.12
- Tailwind CSS v4, Node 20
- Start dev: `npm run dev` (Django on :8000 + Tailwind watch)
- After any model change: `python manage.py makemigrations && python manage.py migrate`
- After adding new Tailwind classes (when not using `npm run dev`): `npm run build:css`

---

## Core principle

**Design in HTML first. Add Python only for what content creators need to edit.**

Layout, spacing, colours, font sizes → Tailwind utility classes in the template.
Text, links, images a content creator would change → model fields.

---

## Styling conventions

### Brand colors
Always use theme tokens. Never hardcode hex values in templates or CSS.

| Token | Hex | Use |
|---|---|---|
| `primary` | `#07679F` | Primary blue — CTAs, accent labels, links |
| `secondary` | `#D82B50` | Pink/red — secondary CTAs |
| `body-text` | `#004066` | Body copy, headings |

Use as: `text-primary`, `bg-secondary`, `border-body-text`, etc.

### Buttons
Always: `.btn` + variant + size. Never write raw button utility classes.

```html
<a class="btn btn-primary btn-md">Label</a>
<a class="btn btn-outline btn-sm">Label <svg ...></svg></a>
```

Variants: `btn-primary`, `btn-secondary`, `btn-white`, `btn-outline`
Sizes: `btn-md` (base), `btn-sm`
Icons: place SVG inside — `inline-flex` handles alignment automatically.

### `@layer components`
Only for styles used in multiple places (buttons, cards, badges).
One-off section styles → utility classes directly in the template.

---

## Models & admin

### Flat fields vs StreamField
- **Flat fields** — page has a fixed layout (sections always in the same order). Simple, no migration complexity.
- **StreamField** — content creators need to freely add, reorder, or remove blocks. Only use when that flexibility is genuinely needed.

Don't reach for StreamField just because a section contains structured data.

### What belongs in a model field
Yes: headline text, body copy, CTA label, CTA link, images.
No: layout, spacing, colours, font sizes, anything only a developer would change.

### After adding a new block type to a StreamField
Use a descriptive snake_case key: `horizontal_card`, not `card`. This key is stored in the database and cannot be renamed without a data migration.

---

## Component inventory

Before building something new, check if it already exists.

| Component | Type | Location |
|---|---|---|
| Button | CSS component | `input.css` → `.btn` + variant + size |
| Horizontal card | StreamField block (`horizontal_card`) | `home/models.py` → `CardBlock`, template `home/blocks/card_block.html` |

Fields for horizontal card: `supertitle` (optional), `title`, `text` (rich text), `image` (optional, renders left).

---

## File map

| File | Purpose |
|---|---|
| `home/models.py` | All page models and block definitions |
| `home/templates/home/` | Page templates |
| `home/templates/home/blocks/` | Block templates |
| `localiser_website/templates/base.html` | Base template — navbar included here |
| `localiser_website/templates/partials/navbar.html` | Top navbar |
| `localiser_website/static/css/input.css` | Tailwind source — brand tokens, component classes |
| `localiser_website/static/css/localiser_website.css` | Compiled CSS — do not edit |
| `home/static/fonts/` | Roboto font files |
| `home/static/images/` | Static images (e.g. hero background) |
| `home/context_processors.py` | Navbar items and dropdown groups |

---

## Navbar
- Items appear when a page is **live** and has **Show in menus** ticked (Promote tab).
- Dropdown grouping is defined in `NAV_GROUPS` in `home/context_processors.py` — keyed by parent slug.
- Page tree position does not affect the navbar.

See README for full navbar documentation.
