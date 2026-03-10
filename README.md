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

## Adding a section or component

### The principle

**Design in HTML first, add Python only for what content creators need to edit.**

Layout, spacing, colours, font sizes — keep those as Tailwind utility classes directly in the template. Only extract text, links, or images that a content creator would realistically need to change into model fields.

---

### Workflow

**1. Build the HTML in the template**

Use Tailwind utility classes directly. Hardcode placeholder text to start.

```html
<!-- home/templates/home/home_page.html -->
<section class="py-24 px-6 bg-blue-900 text-white">
  <h1 class="text-5xl font-bold">Your headline here</h1>
  <p class="text-xl font-light mt-4">Supporting text here</p>
  <a href="#" class="mt-8 inline-block px-6 py-3 bg-red-500 rounded-full font-bold">
    CTA button
  </a>
</section>
```

**2. Decide what is editable**

Ask: would a content creator need to change this without a developer? Typical yes: headline text, body copy, CTA label, CTA link, images. Typical no: layout, colours, spacing, font sizes.

**3. Add model fields for editable content**

In `home/models.py`, add only the fields identified above and list them in `content_panels`:

```python
class HomePage(Page):
    hero_title    = models.CharField(blank=True, max_length=255)
    hero_subtitle = models.CharField(blank=True, max_length=500)
    hero_cta_text = models.CharField(blank=True, max_length=100)
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_title"),
            FieldPanel("hero_subtitle"),
            FieldPanel("hero_cta_text"),
            FieldPanel("hero_cta_link"),
        ], heading="Hero section"),
    ]
```

**4. Wire the template to model fields**

Replace hardcoded text with `{{ page.field_name }}`. Wrap optional elements in `{% if %}`:

```html
<h1 class="text-5xl font-bold">{{ page.hero_title }}</h1>
<p class="text-xl font-light mt-4">{{ page.hero_subtitle }}</p>
{% if page.hero_cta_text %}
  <a href="{% if page.hero_cta_link %}{% pageurl page.hero_cta_link %}{% endif %}"
     class="mt-8 inline-block px-6 py-3 bg-red-500 rounded-full font-bold">
    {{ page.hero_cta_text }}
  </a>
{% endif %}
```

**5. Run migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

The fields appear in the Wagtail admin automatically — no further admin configuration needed.

**6. Rebuild CSS (if you added new Tailwind classes)**

```bash
npm run build:css
```

Or just keep `npm run dev` running — it watches and rebuilds automatically.

---

### Reusable CSS classes

For styles used in many places (buttons, badges, tags), define named classes in `input.css` using `@layer components` and `@apply`:

```css
@layer components {
  .btn-primary { @apply inline-block px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold; }
}
```

For one-off sections, put utility classes directly in the template — no need for a named class.

---

### When to use StreamField instead

Use flat model fields (as above) when a page has a **fixed layout** — the sections are always in the same order.

Use `StreamField` when content creators need to **freely add, reorder, or remove sections** (like a flexible landing page builder). StreamField adds complexity, so only reach for it when that flexibility is genuinely needed.

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