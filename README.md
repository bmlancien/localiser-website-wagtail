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
