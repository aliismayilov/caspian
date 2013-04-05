from django.db import models

import datetime
import re

class Language(models.Model):
    small_name = models.CharField(max_length="3", unique=True)
    long_name = models.CharField(max_length="15")
    priority = models.IntegerField(unique=True)
    
    class Meta:
        ordering = ['priority']
    
    def __unicode__(self):
        return self.small_name
    
    def get_absolute_url(self):
        return "/%s/" % self.small_name

class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
    )
    # Core fields.
    title_ru = models.CharField(max_length=250, help_text="Maximum 250 characters.")
    title_az = models.CharField(max_length=250, help_text="Maximum 250 characters.")
    title_en = models.CharField(max_length=250, help_text="Maximum 250 characters.")
    body_ru = models.TextField()
    body_az = models.TextField()
    body_en = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    last_modified = models.DateTimeField(auto_now=True)
    
    # Metadata.
    slug = models.SlugField(unique_for_date='pub_date', help_text="Suggested value automatically generated from title. Must be unique.")
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS, help_text="Only entries with live status will be publicly displayed.")
    index_ru = models.TextField(editable=False)
    index_az = models.TextField(editable=False)
    index_en = models.TextField(editable=False)
    view_count = models.IntegerField(editable=False, default=0)
    
    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-pub_date']
    
    def __unicode__(self):
        return self.slug
    
    def get_absolute_url_ru(self):
        return "/ru/%s/%s/%s/%s.html" % (
            self.pub_date.strftime("%Y"),
            self.pub_date.strftime("%b").lower(),
            self.pub_date.strftime("%d"),
            self.slug
        )
    def get_absolute_url_az(self):
        return "/az/%s/%s/%s/%s.html" % (
            self.pub_date.strftime("%Y"),
            self.pub_date.strftime("%b").lower(),
            self.pub_date.strftime("%d"),
            self.slug
        )
    def get_absolute_url_en(self):
        return "/en/%s/%s/%s/%s.html" % (
            self.pub_date.strftime("%Y"),
            self.pub_date.strftime("%b").lower(),
            self.pub_date.strftime("%d"),
            self.slug
        )
    def get_absolute_url(self):
        return "/ru/%s/%s/%s/%s.html" % (
            self.pub_date.strftime("%Y"),
            self.pub_date.strftime("%b").lower(),
            self.pub_date.strftime("%d"),
            self.slug
        )
    
    def save(self):
        self.index_ru = strip_html_and_remove_white_spaces(self.title_ru + " " + self.body_ru)
        self.index_az = strip_html_and_remove_white_spaces(self.title_az + " " + self.body_az)
        self.index_en = strip_html_and_remove_white_spaces(self.title_en + " " + self.body_en)
        super(Entry, self).save()

class Page(models.Model):
    TOP = 1
    SIDE = 2
    NONE = 3
    TYPE_CHOICES = (
        (TOP, 'Top'),
        (SIDE, 'Side'),
        (NONE, 'None'),
    )
    title_ru = models.CharField(max_length=100)
    title_az = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)
    body_ru = models.TextField(null=True, blank=True)
    body_az = models.TextField(null=True, blank=True)
    body_en = models.TextField(null=True, blank=True)
    type = models.IntegerField(choices=TYPE_CHOICES, default=TOP, help_text="Page menu position")
    
    slug = models.SlugField(unique=True)
    link_ru = models.CharField(max_length=500, null=True, blank=True)
    link_az = models.CharField(max_length=500, null=True, blank=True)
    link_en = models.CharField(max_length=500, null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    index_ru = models.TextField(editable=False)
    index_az = models.TextField(editable=False)
    index_en = models.TextField(editable=False)
    
    class Meta:
        ordering = ['priority']
    
    def __unicode__(self):
        return self.title_ru
    
    def get_absolute_url_ru(self):
        if self.link_ru:
            return self.link_ru
        else:
            return "/ru/%s.html" % self.slug
    def get_absolute_url_az(self):
        if self.link_az:
            return self.link_az
        else:
            return "/az/%s.html" % self.slug
    def get_absolute_url_en(self):
        if self.link_en:
            return self.link_en
        else:
            return "/en/%s.html" % self.slug
    def get_absolute_url(self):
        return "/ru/%s.html" % self.slug

    def save(self):
        self.index_ru = strip_html_and_remove_white_spaces(self.title_ru + " " + self.body_ru)
        self.index_az = strip_html_and_remove_white_spaces(self.title_az + " " + self.body_az)
        self.index_en = strip_html_and_remove_white_spaces(self.title_en + " " + self.body_en)
        super(Page, self).save()

class Poll(models.Model):
    question_ru = models.CharField(max_length=250)
    question_az = models.CharField(max_length=250)
    question_en = models.CharField(max_length=250)
    
    start_date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.question_ru

class Choice(models.Model):
    choice_ru = models.CharField(max_length=250)
    choice_az = models.CharField(max_length=250)
    choice_en = models.CharField(max_length=250)
    poll = models.ForeignKey(Poll)
    vote = models.IntegerField(default=0, editable=False)
    
    def __unicode__(self):
        return self.choice_ru


def strip_html_and_remove_white_spaces(content):
    html_p = re.compile(r'<.*?>') # pattern for html tags
    white_p = re.compile(r'\s+') # pattern for white spaces
    
    content = html_p.sub(' ', content) # strip html
    content = white_p.sub(' ', content) # remove white spaces
    
    return content