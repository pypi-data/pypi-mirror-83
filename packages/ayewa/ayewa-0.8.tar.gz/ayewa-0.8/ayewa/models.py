from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalManyToManyField

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, FieldRowPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.core.fields import StreamField

from .blocks import BaseStreamBlock



class IndexPage(Page):
    intro = RichTextField(blank=True)
    nav_description = models.CharField(_('Navigation Description'), max_length=255, blank=True, default='')
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )


class AyewaIndexPage(IndexPage):
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        StreamFieldPanel('body'),
    ]


class ActionApproachIndexPage(IndexPage):
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('nav_description', classname="full"),
        StreamFieldPanel('body'),
    ]
    subpage_types = ['ayewa.ActionApproach']


class SolutionIndexPage(IndexPage):
    content_panels = Page.content_panels + [
        FieldPanel('nav_description', classname="full"),
        StreamFieldPanel('body'),
    ]
    subpage_types = ['ayewa.Solution']


class PeopleIndexPage(IndexPage):
    content_panels = Page.content_panels + [
        FieldPanel('nav_description', classname="full"),
        StreamFieldPanel('body'),
    ]
    subpage_types = ['ayewa.People']

class ResourceIndexPage(IndexPage):
    content_panels = Page.content_panels + [
        FieldPanel('nav_description', classname="full"),
        StreamFieldPanel('body'),
    ]
    subpage_types = ['ayewa.Resource']

class ScienceIndexPage(IndexPage):
    content_panels = Page.content_panels + [
        FieldPanel('nav_description', classname="full"),
        StreamFieldPanel('body'),
    ]

class OtherIndexPage(IndexPage):
    content_panels = Page.content_panels + [
        FieldPanel('nav_description', classname="full"),
        StreamFieldPanel('body'),
    ]


class Solution(Page):
    description = RichTextField('Description', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),

    ]

    def __str__(self):
        try:
            return '{name}'.format(
                name=self.name,
            )
        except AttributeError:
            return 'unassigned'


class ActionApproach(Page):
    name = models.CharField(_('name'), max_length=40, blank=True, default='')
    description = RichTextField('Description', blank=True)

    class Meta:
        app_label = 'ayewa'
        verbose_name = _("Action Approach")
        verbose_name_plural = _("Action Approaches")

    def __str__(self):
        return '{name}'.format(
            name=self.name,
        )


@register_snippet
class Scope(models.Model):
    name = models.CharField(_('name'), max_length=40, blank=True, default='')
    description = RichTextField('Description', blank=True)

    class Meta:
        verbose_name_plural = "Scopes"
        verbose_name = "Scope"
        app_label = 'ayewa'

    def __str__(self):
        try:
            return '{name}'.format(
                name=self.name,
            )
        except AttributeError:
            return 'unassigned'


@register_snippet
class Rank(models.Model):
    name = models.CharField(_('name'), max_length=40, blank=True, default='')
    description = RichTextField('Description', blank=True)

    class Meta:
        verbose_name_plural = "Ranks"
        verbose_name = "Rank"
        app_label = 'ayewa'

    def __str__(self):
        try:
            return '{name}'.format(
                name=self.name,
            )
        except AttributeError:
            return 'unassigned'


@register_snippet
class UserRating(models.Model):
    name = models.CharField(_('name'), max_length=40, blank=True, default='')
    description = RichTextField('Description', blank=True)

    class Meta:
        verbose_name_plural = "User Ratings"
        verbose_name = "User Rating"
        app_label = 'ayewa'

    def __str__(self):
        try:
            return '{name}'.format(
                name=self.name,
            )
        except AttributeError:
            return 'unassigned'


@register_snippet
class InternalRating(models.Model):
    name = models.CharField(_('name'), max_length=40, blank=True, default='')
    description = RichTextField('Description', blank=True)

    class Meta:
        verbose_name_plural = "Internal Ratings"
        verbose_name = "Internal Rating"
        app_label = 'ayewa'


@register_snippet
class Role(models.Model):

    def __str__(self):
        try:
            return '{name}'.format(
                name=self.name,
            )
        except AttributeError:
            return 'unassigned'

    name = models.CharField(_('name'), max_length=255, blank=False, null=True, )


class People(Page):
    first_name = models.CharField(_('first_name'), max_length=40, blank=True, default='')
    last_name = models.CharField(_('last_name'), max_length=40, blank=True, default='')
    role = ParentalManyToManyField('Role', blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('first_name', ),
                FieldPanel('last_name', ),
            ],
            heading="Personal Details",
            classname="collapsible expanded"),
        MultiFieldPanel(
            [
                FieldPanel('role', ),
            ],
            heading="Roles/Other",
            classname="collapsible collapsed"),
    ]

    class Meta:
        app_label = 'ayewa'
        verbose_name = _("Person")

    def __str__(self):
        return '{first} {last}'.format(
            first=self.first_name,
            last=self.last_name
        )

    def list_roles(self):
        return ['{name}, {resource}'.format(name=i.name, resource=i.resource.name) for i in self.role.all()]


@register_snippet
class ResourceNeed(models.Model):
    name = models.CharField(_('name'), max_length=40, blank=True, default='')
    description = RichTextField('Description', blank=True)

    class Meta:
        verbose_name_plural = "Resource Needs"
        verbose_name = "Resource Need"
        app_label = 'ayewa'

    def __str__(self):
        try:
            return '{name}'.format(
                name=self.name,
            )
        except AttributeError:
            return 'unassigned'


@register_snippet
class ResourceType(models.Model):
    name = models.CharField(_('name'), max_length=40, blank=True, default='')
    description = RichTextField('Description', blank=True)

    class Meta:
        verbose_name_plural = "Resource Types"
        verbose_name = "Resource Type"
        app_label = 'ayewa'

    def __str__(self):
        try:
            return '{name}'.format(
                name=self.name,
            )
        except AttributeError:
            return 'unassigned'


@register_snippet
class ResourceClass(models.Model):
    name = models.CharField(_('name'), max_length=40, blank=True, default='')
    description = RichTextField('Description', blank=True)

    class Meta:
        verbose_name_plural = "Resource Classes"
        verbose_name = "Resource Class"
        app_label = 'ayewa'

    def __str__(self):
        try:
            return '{name}'.format(
                name=self.name,
            )
        except AttributeError:
            return 'unassigned'


class Resource(Page):
    summary = models.TextField(_('Summary'), default='', blank=True, null=True)
    description = RichTextField('Description', blank=True)
    resource_type = models.ForeignKey(ResourceType, blank=True, on_delete=models.SET_NULL, null=True,
                                      related_name='resource_type')
    user_rating = models.ForeignKey(UserRating, blank=True, on_delete=models.SET_NULL, null=True, )
    internal_rating = models.ForeignKey(InternalRating, blank=True, on_delete=models.SET_NULL, null=True, )
    rank = models.ForeignKey(Rank, blank=True, on_delete=models.SET_NULL, null=True, )
    resource_class = ParentalManyToManyField('ResourceClass', blank=True)
    resource_need = ParentalManyToManyField('ResourceNeed', blank=True)
    scope = ParentalManyToManyField('Scope', blank=True)
    solution = ParentalManyToManyField('Solution', blank=True)
    people = ParentalManyToManyField('People', blank=True)
    email_address = models.CharField(_('Email Address'), max_length=64, blank=True, default='')
    primary_phone = models.CharField(_('Primary Phone'), max_length=50, blank=True, null=True, default=None)
    address_1 = models.CharField(_('Address 1'), max_length=64, blank=True, null=True, default='')
    address_2 = models.CharField(_('Address 2'), max_length=64, blank=True, null=True, default=None)
    city = models.CharField(_('City'), max_length=64, blank=True, null=True, default='')
    state = models.CharField(_('State'), max_length=20, blank=True, default='')
    postal_code = models.CharField(_('Postal (Zip) Code'), max_length=10, blank=True, null=True, default='',
                                   validators=[])  # TODO: Add a validator
    country = models.CharField(_('Country'), max_length=30, blank=True, null=True, default='',
                               validators=[])  # TODO: Add a validator
    website = models.CharField(_('Website'), max_length=30, blank=True, null=True, default='',
                               validators=[])  # TODO: Add a validator

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('summary', ),
                FieldPanel('description', ),
            ],
            heading="Summary/Description",
            classname="collapsible collapsed"),
        MultiFieldPanel(
            [
                FieldPanel('email_address', ),
                FieldPanel('primary_phone', ),
                FieldPanel('website', ),
            ],
            heading="Contact Info",
            classname="collapsible collapsed"),
        MultiFieldPanel(
            [
                FieldPanel('address_1', ),
                FieldPanel('address_2', ),
                FieldPanel('city', ),
                FieldRowPanel([
                    FieldPanel('state', ),
                    FieldPanel('postal_code', ),
                    FieldPanel('country', ),

                ])
            ],
            heading="Address Info",
            classname="collapsible collapsed"),

        MultiFieldPanel(
            [
                FieldPanel('people', ),
            ],
            heading="People",
            classname="collapsible collapsed"),

        MultiFieldPanel(
            [
                FieldRowPanel([
                    FieldPanel(
                        'resource_class',
                        widget=forms.CheckboxSelectMultiple,
                    ),
                    FieldPanel(
                        'resource_type',
                        widget=forms.CheckboxSelectMultiple,
                    ),
                ]),
                FieldRowPanel([
                    FieldPanel(
                        'solution',
                        widget=forms.CheckboxSelectMultiple,
                    ),
                ]),
                FieldPanel(
                    'user_rating',
                    widget=forms.Select,
                ),
                FieldPanel(
                    'internal_rating',
                    widget=forms.Select,
                ),
                FieldPanel(
                    'rank',
                    widget=forms.Select,
                ),

            ],
            heading="Categorization",
            classname="collapsible collapsed"
        ),
    ]

    def __str__(self):
        try:
            classes = ', '.join(self.list_resource_classes())
            if classes:
                classes = '({classes})'.format(classes=classes)
            return '{name} {classes}'.format(
                name=self.name,
                classes=classes
            )
        except AttributeError:
            return 'unassigned'

    def list_resource_classes(self):
        return ['{name}'.format(name=i.name) for i in self.resource_class.all()]

    def list_resource_classes_as_str(self):
        classes = ', '.join(self.list_resource_classes())
        return '{classes}'.format(
            classes=classes
        )

    def list_scopes(self):
        return ['{name}'.format(name=i.name) for i in self.scope.all()]

    def list_scopes_as_str(self):
        scopes = ', '.join(self.list_scopes())
        return '{scopes}'.format(
            scopes=scopes
        )

    def list_solutions(self):
        return ['{name}'.format(name=i.name) for i in self.solution.all()]

    def list_solutions_as_str(self):
        solutions = ', '.join(self.list_solutions())
        return '{solutions}'.format(
            solutions=solutions
        )

    def list_needs(self):
        return ['{name}'.format(name=i.name) for i in self.resource_need.all()]

    def list_needs_as_str(self):
        needs = ', '.join(self.list_needs())
        return '{needs}'.format(
            needs=needs
        )

    def is_project(self):
        if len(self.resource_class.filter(is_project=True)) > 0:
            return True
        else:
            return False

    def is_organization(self):
        if len(self.resource_class.filter(is_organization=True)) > 0:
            return True
        else:
            return False

    list_resource_classes_as_str.short_description = 'Class(es)'
    list_scopes_as_str.short_description = 'Scope(s)'
    list_solutions_as_str.short_description = 'Solution(s)'
    list_needs_as_str.short_description = 'Need(s)'
    is_project.short_description = 'Proj?'
    is_project.boolean = True
    is_organization.short_description = 'Org?'
    is_organization.boolean = True
