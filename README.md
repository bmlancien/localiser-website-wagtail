# Localiser Website

A Wagtail/Django website.

## Requirements

- Python 3.12
- Node.js 20+

## Setup

### Python dependencies

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Node dependencies

```bash
npm install
```

## Development

Start both the Django dev server and the Tailwind CSS watcher with a single command:

```bash
npm run dev
```

Output is colour-coded — **blue** for Django, **yellow** for Tailwind. Tailwind automatically rebuilds the CSS whenever you edit a template.

## CSS / Tailwind

The project uses [Tailwind CSS v4](https://tailwindcss.com).

| File | Purpose |
|---|---|
| `localiser_website/static/css/input.css` | Tailwind source — add custom styles here |
| `localiser_website/static/css/localiser_website.css` | Compiled output — do not edit directly |

## Content blocks & StreamField

Wagtail's StreamField lets content creators freely add, remove, and reorder content modules on a page — without touching code. Think of it as a lightweight page builder built into the CMS.

### How a block is built (button as example)

A block has three parts, each in one place:

**1. Styling — `localiser_website/static/css/input.css`**

Defines the visual variants as named CSS classes. This is the only place styling lives — change it here and it updates everywhere the button is used.

```css
@layer components {
  .btn-primary { @apply bg-blue-600 text-white px-6 py-3 rounded-lg ...; }
  .btn-outline { @apply border-2 border-blue-600 text-blue-600 px-6 py-3 ...; }
}
```

**2. Block definition — `home/models.py`**

Defines what fields the block exposes to the content creator (text, link, style dropdown, etc.).

```python
class ButtonBlock(StructBlock):
    text  = CharBlock(label="Button text")
    link  = PageChooserBlock(label="Link to page")
    style = ChoiceBlock(choices=BUTTON_STYLE_CHOICES, label="Style")

    class Meta:
        template = "home/blocks/button_block.html"
```

**3. Template — `home/templates/home/blocks/button_block.html`**

Renders the block's output. `value` holds the fields defined above.

```html
<a href="{% pageurl value.link %}" class="{{ value.style }}">{{ value.text }}</a>
```

---

### Two ways a dev can use a block

**Fixed position** — the block is hardcoded into a specific spot in a template. The content creator can only edit its fields, not move or remove it. Example: the hero CTA button in `home_page.html`.

**Inside a StreamField** — the block is added to a StreamField alongside other blocks. The content creator can add it anywhere on the page, reorder it, duplicate it, or remove it entirely. Example: the `content` StreamField on the home page.

To add a new block to the StreamField, register it in the `StreamField` definition in `models.py`, then run a migration:

```python
content = StreamField([
    ("rich_text", RichTextBlock()),
    ("image",     ImageChooserBlock(...)),
    ("button",    ButtonBlock()),          # ← add new blocks here
])
```

The block then appears automatically in the admin's block picker — no further changes needed.

### Other CSS commands

```bash
# Watch only (no Django server)
npm run watch:css

# Production build (minified)
npm run build:css
```
