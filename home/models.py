from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import RichTextBlock, StructBlock, CharBlock, PageChooserBlock, ChoiceBlock
from wagtail.images.blocks import ImageChooserBlock

BUTTON_STYLE_CHOICES = [
    ("btn-primary", "Primary — solid blue"),
    ("btn-secondary", "Secondary — solid dark"),
    ("btn-outline", "Outline — bordered"),
    ("btn-ghost", "Ghost — text only"),
]


class ButtonBlock(StructBlock):
    text = CharBlock(label="Button text")
    link = PageChooserBlock(label="Link to page")
    style = ChoiceBlock(choices=BUTTON_STYLE_CHOICES, default="btn-primary", label="Style")

    class Meta:
        template = "home/blocks/button_block.html"
        icon = "link"
        label = "Button"


class HomePage(Page):
    CTA_STYLE_CHOICES = BUTTON_STYLE_CHOICES

    # add the Hero section of HomePage:
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage image",
    )
    hero_text = models.CharField(
        blank=True,
        max_length=255, help_text="Write an introduction for the site"
    )
    hero_cta = models.CharField(
        blank=True,
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Text to display on Call to Action",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )
    hero_cta_style = models.CharField(
        verbose_name="Hero CTA style",
        max_length=20,
        choices=CTA_STYLE_CHOICES,
        default="btn-primary",
        help_text="Visual style of the Call to Action button",
    )

    body = RichTextField(blank=True)

    content = StreamField(
        [
            ("rich_text", RichTextBlock(label="Rich text")),
            ("image", ImageChooserBlock(template="home/blocks/image_block.html", label="Image")),
            ("button", ButtonBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Content blocks",
    )

    # modify your content_panels:
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("hero_text"),
                FieldPanel("hero_cta"),
                FieldPanel("hero_cta_link"),
                FieldPanel("hero_cta_style"),
            ],
            heading="Hero section",
        ),
        FieldPanel('body'),
        FieldPanel('content'),
    ]


class HydrogenPage(Page):
    pass
