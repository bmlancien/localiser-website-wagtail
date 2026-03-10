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

---

- [CSS](#css)
- [Components](#components)
- [Create a new page](#create-a-new-page)
- [Create a new component](#create-a-new-component)
- [Localization](#localization)

---

## CSS

The project uses [Tailwind CSS v4](https://tailwindcss.com).

| File | Purpose |
|---|---|
| `localiser_website/static/css/input.css` | Tailwind source — add custom styles here |
| `localiser_website/static/css/localiser_website.css` | Compiled output — do not edit directly |

### Brand colors

Defined in `@theme` in `input.css` and available as Tailwind utilities everywhere:

| Token | Hex | Utilities |
|---|---|---|
| `primary` | `#07679F` | `bg-primary`, `text-primary`, `border-primary` |
| `secondary` | `#D82B50` | `bg-secondary`, `text-secondary`, `border-secondary` |
| `body-text` | `#004066` | `bg-body-text`, `text-body-text`, `border-body-text` |

### Utility classes vs component classes

Put Tailwind utility classes directly in templates for one-off styles. Use `@layer components` in `input.css` only for styles reused across many places (buttons, cards, badges):

```css
@layer components {
  .my-class { @apply px-6 py-3 bg-primary text-white rounded-full; }
}
```

### Other commands

```bash
npm run watch:css   # watch only (no Django server)
npm run build:css   # production build (minified)
```

---

## Components

Before building something new, check if it already exists.

### Buttons

Always combine `.btn` + a variant + a size. Icons (SVG elements) inside the button align automatically.

```html
<a class="btn btn-primary btn-md">Label</a>
<a class="btn btn-secondary btn-md">Label</a>
<a class="btn btn-white btn-md">Label</a>
<a class="btn btn-outline btn-md">Label</a>

<!-- Sizes -->
<a class="btn btn-primary btn-sm">Small</a>

<!-- With icon at start or end -->
<a class="btn btn-primary btn-md"><svg ...></svg> Label</a>
<a class="btn btn-outline btn-sm">Label <svg ...></svg></a>
```

| Class | Description |
|---|---|
| `btn-primary` | Blue background, white text |
| `btn-secondary` | Pink/red background, white text |
| `btn-white` | White background, blue text |
| `btn-outline` | Blue border and text, transparent bg |
| `btn-md` | Base size — `px-6 py-3 text-lg` |
| `btn-sm` | Small — `px-4 py-2 text-sm` |

Content creators can choose the variant via the admin. Size is set by the developer in the template.

---

### Horizontal card (`horizontal_card`)

**Block** — used inside a `StreamField`. Template: `home/templates/home/blocks/card_block.html`.

| Field | Type | Required |
|---|---|---|
| Text above title | Short text | No |
| Title | Short text | Yes |
| Body text | Rich text | Yes |
| Image | Image | No — when set, renders on the left side |

CSS class: `.card` — white background, rounded corners, `shadow-card` glow.

Admin: add via the **Cards** StreamField on any page that includes it.

---

## Create a new page

1. Add a model in `home/models.py`:

```python
class MyPage(Page):
    pass  # add fields here later
```

2. Create a template at `home/templates/home/my_page.html` (snake_case of the class name, `_page.html` suffix required):

```html
{% extends "base.html" %}

{% block content %}
{% endblock %}
```

3. Run migrations:

```bash
python manage.py makemigrations home
python manage.py migrate
```

4. In the Wagtail admin — go to Pages, pick a parent, click **Add child page**, select your new page type.

### Navbar

The navbar (`localiser_website/templates/partials/navbar.html`) is included on every page via `base.html`.

A page appears in the navbar when it is **live** and has **Show in menus** ticked (edit page → Promote tab).

**Dropdown grouping** is defined in `NAV_GROUPS` in `home/context_processors.py`:

```python
NAV_GROUPS = {
    "hydrogen": ["hydrogen-registration"],        # key = parent slug, values = child slugs
    "your-parent-slug": ["child-one", "child-two"],
}
```

Page tree position does not affect the navbar — grouping is controlled entirely by `NAV_GROUPS`.

---

## Create a new component

### Principle

**Design in HTML first. Add Python only for what content creators need to edit.**

Layout, spacing, colours, font sizes → Tailwind utility classes in the template.
Text, links, images a content creator would change → model fields.

### Workflow

**1. Build the HTML**

Use Tailwind utility classes directly with placeholder text:

```html
<section class="py-24 px-6 bg-primary text-white">
  <h1 class="text-5xl font-bold">Your headline here</h1>
  <p class="text-xl font-light mt-4">Supporting text</p>
</section>
```

**2. Decide what is editable**

Yes: headline, body copy, CTA label, CTA link, images.
No: layout, colours, spacing, font sizes.

**3. Add model fields**

```python
class MyPage(Page):
    hero_title = models.CharField(blank=True, max_length=255)
    hero_cta_text = models.CharField(blank=True, max_length=100)
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_title"),
            FieldPanel("hero_cta_text"),
            FieldPanel("hero_cta_link"),
        ], heading="Hero section"),
    ]
```

**4. Wire the template**

```html
<h1 class="text-5xl font-bold">{{ page.hero_title }}</h1>
{% if page.hero_cta_text %}
  <a href="{% if page.hero_cta_link %}{% pageurl page.hero_cta_link %}{% endif %}"
     class="btn btn-secondary btn-md">
    {{ page.hero_cta_text }}
  </a>
{% endif %}
```

**5. Migrate and rebuild**

```bash
python manage.py makemigrations && python manage.py migrate
npm run build:css
```

### Flat fields vs StreamField

Use **flat fields** when a page has a fixed layout (sections always in the same order).

Use **StreamField** when content creators need to freely add, reorder, or remove blocks. Add the block to `home/models.py`, create its template in `home/templates/home/blocks/`, and register it in the page's `StreamField`.

> **Important:** Never rename a StreamField block key without also updating the stored JSON in the database. The key is stored as-is and Wagtail will silently skip blocks with an unrecognised key.

---

## Localization

The site uses [wagtail-localize](https://github.com/wagtail/wagtail-localize) for multilingual content.

**Languages:** German `de` (source/default), English `en`, French `fr`, Spanish `es`.

German pages have no URL prefix (`/`). Other languages: `/en/`, `/fr/`, `/es/`.

### Translation workflow

1. Create and publish the page in German as normal
2. In the page editor, click **Translate** → select target languages
3. Translators edit field by field in the translation editor — untranslated fields fall back to German
4. Publish the translation

### What can and cannot differ per language

| | Supported |
|---|---|
| Different text per language | ✅ |
| Different image per language | ✅ |
| Page exists in some languages only | ✅ — just don't translate it |
| Different block structure per language | ❌ — structure always mirrors the German source |

### Country-specific pages

Pages that only make sense in one language (e.g. a German legal notice) are created directly in that language's page tree and never submitted for translation. They simply don't appear in other language trees.

### Language switcher

Only shows languages where a live translation of the current page exists. Managed via the `get_page_translations` template tag in `home/templatetags/i18n_tags.py`.
