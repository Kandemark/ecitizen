from django.db import models


class Bill(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        FIRST_READING = 'first_reading', 'First Reading'
        SECOND_READING = 'second_reading', 'Second Reading'
        COMMITTEE = 'committee', 'Committee Stage'
        REPORT = 'report', 'Report Stage'
        THIRD_READING = 'third_reading', 'Third Reading'
        PASSED = 'passed', 'Passed'
        ASSENTED = 'assented', 'Assented to'  # Became Act of Parliament
        REJECTED = 'rejected', 'Rejected'
        WITHDRAWN = 'withdrawn', 'Withdrawn'

    class House(models.TextChoices):
        NATIONAL_ASSEMBLY = 'national_assembly', 'National Assembly'
        SENATE = 'senate', 'Senate'

    title = models.CharField(max_length=500)
    number = models.CharField(max_length=50, db_index=True)
    house = models.CharField(max_length=30, choices=House.choices, default=House.NATIONAL_ASSEMBLY)
    sponsor = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT, db_index=True)
    summary = models.TextField(blank=True)
    date_introduced = models.DateField(null=True, blank=True)
    date_passed = models.DateField(null=True, blank=True)
    date_assented = models.DateField(null=True, blank=True)
    full_text_url = models.URLField(max_length=1000, blank=True)
    source_id = models.CharField(max_length=100, blank=True, unique=True, null=True, db_index=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_introduced', '-last_updated']

    def __str__(self):
        return f'{self.get_house_display()} Bill {self.number}: {self.title}'


class Hansard(models.Model):
    class House(models.TextChoices):
        NATIONAL_ASSEMBLY = 'national_assembly', 'National Assembly'
        SENATE = 'senate', 'Senate'

    title = models.CharField(max_length=500)
    date = models.DateField(db_index=True)
    house = models.CharField(max_length=30, choices=House.choices)
    sitting_number = models.CharField(max_length=50, blank=True)
    content = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    source_url = models.URLField(max_length=1000, blank=True)
    source_id = models.CharField(max_length=100, blank=True, unique=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['house', '-date']),
        ]

    def __str__(self):
        return f'{self.get_house_display()} Hansard — {self.date}'


class CommitteeReport(models.Model):
    committee_name = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    date_published = models.DateField(db_index=True)
    summary = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    full_text_url = models.URLField(max_length=1000, blank=True)
    source_id = models.CharField(max_length=100, blank=True, unique=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_published']

    def __str__(self):
        return f'{self.committee_name}: {self.title}'


class ParliamentarySitting(models.Model):
    class House(models.TextChoices):
        NATIONAL_ASSEMBLY = 'national_assembly', 'National Assembly'
        SENATE = 'senate', 'Senate'

    date = models.DateField(db_index=True)
    house = models.CharField(max_length=30, choices=House.choices)
    session = models.CharField(max_length=200, blank=True)
    agenda = models.TextField(blank=True)
    minutes_url = models.URLField(max_length=1000, blank=True)
    order_paper_url = models.URLField(max_length=1000, blank=True)
    source_id = models.CharField(max_length=100, blank=True, unique=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['house', '-date']),
        ]

    def __str__(self):
        return f'{self.get_house_display()} Sitting — {self.date}'
