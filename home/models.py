from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock


BUTTON_VARIANT_CHOICES = [
    ("btn-secondary", "Secondary — pink/red"),
    ("btn-primary",   "Primary — blue"),
    ("btn-white",     "White — white bg, blue text"),
    ("btn-outline",   "Outline — blue border and text"),
]


class CardBlock(StructBlock):
    supertitle = CharBlock(required=False, label="Text above title (optional)")
    title      = CharBlock(label="Title")
    text       = RichTextBlock(label="Body text", features=["bold", "italic", "ul", "ol", "link"])
    image      = ImageChooserBlock(required=False, label="Image — shown on the left (optional)")

    class Meta:
        template = "home/blocks/card_block.html"
        icon = "doc-full"
        label = "Horizontal card"


class HomePage(Page):
    hero_title = models.CharField(blank=True, max_length=255)
    hero_subtitle = models.CharField(blank=True, max_length=500)
    hero_cta_text = models.CharField(blank=True, max_length=100, verbose_name="CTA button text")
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="CTA button link",
    )
    hero_cta_style = models.CharField(
        max_length=20,
        choices=BUTTON_VARIANT_CHOICES,
        default="btn-secondary",
        verbose_name="CTA button style",
    )
    hero_cta_subtext = models.CharField(blank=True, max_length=255, verbose_name="Text below CTA")

    cards = StreamField(
        [("horizontal_card", CardBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Cards",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_title"),
            FieldPanel("hero_subtitle"),
            FieldPanel("hero_cta_text"),
            FieldPanel("hero_cta_link"),
            FieldPanel("hero_cta_style"),
            FieldPanel("hero_cta_subtext"),
        ], heading="Hero section"),
        FieldPanel("cards"),
    ]


class HydrogenPage(Page):
    pass


class HydrogenRegistrationPage(Page):
    pass
