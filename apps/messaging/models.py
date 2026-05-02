from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampMixin
from core.utils import generate_tracking_id


class Conversation(TimestampMixin):
    subject = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='conversations')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject


class Message(TimestampMixin):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    body = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['sender', 'is_read']),
        ]

    def __str__(self):
        return f'Message from {self.sender.username} in {self.conversation.subject}'


class SupportTicket(TimestampMixin):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('waiting_on_customer', 'Waiting on Customer'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    reference = models.CharField(max_length=30, unique=True, db_index=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_tickets'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f'{self.reference} — {self.subject} ({self.status})'

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_tracking_id(prefix='TKT')
        super().save(*args, **kwargs)
