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

### Other CSS commands

```bash
# Watch only (no Django server)
npm run watch:css

# Production build (minified)
npm run build:css
```

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

**Fixed position** — the block is hardcoded into a specific spot in a template. The content creator can only edit its fields, not move or remove it.

**Inside a StreamField** — the block is added to a StreamField alongside other blocks. The content creator can add it anywhere on the page, reorder it, duplicate it, or remove it entirely.

To add a new block to the StreamField, register it in the `StreamField` definition in `models.py`, then run a migration:

```python
content = StreamField([
    ("rich_text", RichTextBlock()),
    ("image",     ImageChooserBlock(...)),
    ("button",    ButtonBlock()),          # ← add new blocks here
])
```

The block then appears automatically in the admin's block picker — no further changes needed.

---

## How to create a new Wagtail page

1. Add a model in home/models.py:

```python
class MyPage(Page):
    pass  # add fields here later
```

For a page with content fields, subclass Page, add Django/Wagtail fields, and list them in content_panels.

2. Create a template at home/templates/home/my_page.html (snake_case of the class name). `_page.html` is necessary`:

```html
{% extends "base.html" %}

{% block content %}
{% endblock %}
```

3. Run migrations:

```python
python manage.py makemigrations home
python manage.py migrate
```

4. Add it in Wagtail admin — go to Pages, pick a parent, click "Add child page", and select your new page type.

---

## Top navbar

The navbar is rendered from `localiser_website/templates/partials/navbar.html` and included in every page via `base.html`.

### How items appear in the navbar

Two conditions must both be true for a page to appear:

1. The page is **live** in the Wagtail admin
2. The page has **Show in menus** enabled (Wagtail admin → edit page → Promote tab → tick "Show in menus")

The navbar is driven by `home/context_processors.py`, which fetches all live in-menu pages across the site.

---

### Add a top-level nav item

1. Create your page in the Wagtail admin under **Home**
2. Edit the page → Promote tab → tick **Show in menus** → save

The page will appear in the navbar automatically. No code changes needed.

---

### Remove a nav item

Untick **Show in menus** on the page in the Wagtail admin. The item disappears from the navbar immediately. The page itself remains live and accessible via its URL.

---

### Add a dropdown under an existing nav item

The dropdown grouping is defined in `NAV_GROUPS` at the top of `home/context_processors.py`:

```python
NAV_GROUPS = {
    "hydrogen": ["hydrogen-registration"],
}
```

- The **key** is the slug of the parent nav item (the one that gets the dropdown)
- The **values** are slugs of pages that appear as dropdown children

To add a new dropdown child:

1. Create the page in Wagtail admin under **Home** (not under the parent page — the URL stays flat)
2. Tick **Show in menus** on the new page
3. Add its slug to `NAV_GROUPS` in `context_processors.py`:

```python
NAV_GROUPS = {
    "hydrogen": ["hydrogen-registration", "your-new-slug"],
}
```

No migration needed — this is a Python config change only.

---

### Add a dropdown to a new parent item

Add a new key to `NAV_GROUPS`:

```python
NAV_GROUPS = {
    "hydrogen": ["hydrogen-registration"],
    "your-parent-slug": ["child-slug-one", "child-slug-two"],
}
```

The parent page will render as a link + chevron with a hover dropdown. All listed child pages must have **Show in menus** ticked.

---

### Important: page tree position does not affect the navbar

The navbar grouping is controlled entirely by `NAV_GROUPS` — **not** by the Wagtail page tree. A page can be a child of any parent in the tree and still appear wherever you place it in the nav. This keeps URLs flat regardless of how the nav is structured.