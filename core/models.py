# core/models.py
from django.db import models
from django.conf import settings 
from django.db.models import JSONField # Import Django's built-in JSONField

# --- Note Model ---

class UserNote(models.Model):
    """Stores the user's uploaded PDF notes and results."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notes'
    )
    
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(
        upload_to='user_notes/pdfs/' 
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    class Meta:
        ordering = ['-uploaded_at']

# --- Quiz Models ---

class Quiz(models.Model):
    """Stores the main quiz details, linked to the user and a topic."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quizzes')
    topic = models.CharField(max_length=255, help_text="The topic the quiz covers.")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Quiz on {self.topic} for {self.user.username}"

class Question(models.Model):
    """Stores a question and its structure for a specific quiz."""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    data = JSONField() 

    def __str__(self):
        return f"Q{self.pk} for Quiz: {self.quiz.topic}"

class QuizAttempt(models.Model):
    """Records a user's attempt and final score for a quiz."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    feedback_message = models.TextField(blank=True, null=True)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s attempt on {self.quiz.topic}: {self.score}/{self.total_questions}"

    class Meta:
        ordering = ['-attempted_at']