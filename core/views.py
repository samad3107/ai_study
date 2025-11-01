# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login 
from django.contrib.auth.views import LoginView
from markdown import markdown
import json # <--- JSON IS CORRECTLY IMPORTED HERE (Module Level)

# Imports rely on other files being correct
from .forms import PDFUploadForm, TopicForm 
from .models import UserNote, Quiz, Question, QuizAttempt
from .ai_utils import (
    extract_text_from_pdf, summarize_notes, explain_topic_and_focus, 
    generate_quiz_json, generate_feedback
)

# ----------------------------------------------------------------------
# Core & Custom Authentication Views (Public)
# ----------------------------------------------------------------------

def home_view(request):
    """Renders the main landing page, found at templates/core/home.html."""
    return render(request, 'core/home.html', {'title': 'Home'})

class CustomLoginView(LoginView):
    """Uses Django's official LoginView but points to your custom nested template."""
    template_name = 'core/registration/login.html' 


def register_view(request):
    """Handles user registration. (Path: templates/core/registration/register.html)"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
    else:
        form = UserCreationForm()
        
    context = {'form': form, 'title': 'Register'}
    return render(request, 'core/registration/register.html', context)


# ----------------------------------------------------------------------
# Protected Feature Views
# ----------------------------------------------------------------------

# core/views.py (Find and REPLACE the pdf_upload_view function)

@login_required 
def pdf_upload_view(request):
    """Handles PDF file upload, text extraction, and AI summarization."""
    
    # Ensure necessary imports are available at the top of views.py:
    # from .ai_utils import extract_text_from_pdf, summarize_notes
    
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Save the model instance without committing
            note = form.save(commit=False)
            note.user = request.user 
            note.save() # Save the object, which saves the file to MEDIA_ROOT
            
            # --- AI PROCESSING LOGIC ADDED HERE ---
            
            # 2. Get the absolute path to the saved PDF file
            pdf_path = note.pdf_file.path 
            
            # 3. Extract text from the PDF using the helper function
            pdf_text = extract_text_from_pdf(pdf_path)
            
            if pdf_text and len(pdf_text) > 100: # Ensure enough text was extracted
                # 4. Generate the summary using the AI utility
                summary = summarize_notes(pdf_text, note.title)
                
                # 5. Save the summary back to the database model
                note.summary_text = summary
                note.save() 
            else:
                note.summary_text = "ERROR: Could not extract sufficient text from PDF. File may be encrypted or empty."
                note.save()
            
            # --- END AI PROCESSING LOGIC ---

            return redirect('note_detail', pk=note.pk)
    else:
        form = PDFUploadForm()
        
    context = {'form': form, 'title': 'Upload Notes for Summarization'}
    return render(request, 'core/pdf_upload.html', context)

# core/views.py (Find and REPLACE the note_detail_view function)

@login_required 
def note_detail_view(request, pk):
    """Displays the uploaded note and its AI-generated summary."""
    # This view must be fully implemented to prevent redirection loops.
    from .models import UserNote # Ensure this is imported

    try:
        note = get_object_or_404(UserNote, pk=pk, user=request.user)
        # Assuming summary_text was populated in the previous step
        context = {'note': note, 'title': f'Note: {note.title}', 'error': None}
        return render(request, 'core/note_detail.html', context)
    except Exception as e:
        # If fetching the note fails, log and redirect gracefully
        print(f"Note detail view crashed: {e}")
        return redirect('home')

@login_required 
def topic_explanation_view(request):
    """Handles topic input, calls AI for explanation, and renders result."""

    form = TopicForm()
    explanation_html = None
    topic = None

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic_name']

            raw_explanation = explain_topic_and_focus(topic)
            explanation_html = markdown(raw_explanation)

    context = {
        'form': form, 
        'title': 'Topic Explainer',
        'topic': topic,
        'explanation_html': explanation_html
    }
    return render(request, 'core/topic_explanation.html', context)


@login_required
def quiz_list_view(request):
    """Displays user's existing quizzes and handles new quiz generation request."""
    user_quizzes = Quiz.objects.filter(user=request.user)
    form = TopicForm() 
    
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic_name']
            
            quiz_id = generate_and_save_quiz(request.user, topic)
            
            if quiz_id:
                return redirect('take_quiz', pk=quiz_id)
            else:
                context = {
                    'form': form, 
                    'user_quizzes': user_quizzes, 
                    'error': 'Quiz generation failed! The AI may have timed out or returned invalid data. Please try a simpler topic.'
                }
                return render(request, 'core/quiz_list.html', context)
    
    context = {'form': form, 'user_quizzes': user_quizzes, 'title': 'My Quizzes'}
    return render(request, 'core/quiz_list.html', context)

# ----------------------------------------------------------------------
# Quiz Redirection Views
# ----------------------------------------------------------------------

# core/views.py (Find and REPLACE the take_quiz_view function)

@login_required
def take_quiz_view(request, pk):
    """Fetches and displays the quiz questions for the user to answer."""
    from .models import Quiz, Question # Ensure these are imported

    # 1. Fetch the Quiz object and its Questions
    # NOTE: pk is the Quiz ID passed from the 'Retake Quiz' button
    quiz = get_object_or_404(Quiz, pk=pk, user=request.user)
    questions = quiz.questions.all()
    
    # Structure the data for the template
    question_data = []
    for q in questions:
        question_data.append({
            'id': q.pk,
            'text': q.data.get('text'),
            'options': q.data.get('options'),
        })

    if request.method == 'POST':
        # Submission handled by grade_quiz_view (Task 6)
        return redirect('grade_quiz', pk=quiz.pk)
        
    context = {
        'quiz': quiz,
        'question_data': question_data,
        'title': f'Take Quiz: {quiz.topic}'
    }
    # Template path: core/take_quiz.html
    return render(request, 'core/take_quiz.html', context)
# core/views.py (Find and REPLACE the grade_quiz_view function)

@login_required
def grade_quiz_view(request, pk):
    """Grades the submitted quiz, generates AI feedback, and saves the attempt."""
    
    # Ensure necessary imports are present inside the file:
    # from .models import Quiz, Question, QuizAttempt
    # from .ai_utils import generate_feedback
    
    if request.method != 'POST':
        # Safety check: if accessed via GET, redirect to take quiz
        return redirect('take_quiz', pk=pk) 

    # 1. Fetch the Quiz and Questions
    quiz = get_object_or_404(Quiz, pk=pk, user=request.user)
    questions = quiz.questions.all()
    
    score = 0
    total_questions = questions.count()
    
    # 2. Iterate through submitted answers and grade them
    for question in questions:
        # The submitted field name is 'question_{id}' from the HTML form
        submitted_answer_index = request.POST.get(f'question_{question.pk}')
        
        # The correct answer index is stored in the Question model's JSON data
        correct_index = question.data.get('correct_answer_index')
        
        # Compare submitted answer (as a string) to the correct index (as an int/str)
        try:
            # We convert both to strings for safe comparison
            if str(submitted_answer_index) == str(correct_index):
                score += 1
        except Exception:
            # Ignore cases where the user didn't select an answer
            pass 

    # 3. Generate Encouraging Message (via AI utility)
    feedback_message = generate_feedback(quiz.topic, score, total_questions)

    # 4. Save the Quiz Attempt to the database
    # This records the final result and feedback
    attempt, created = QuizAttempt.objects.update_or_create(
        user=request.user,
        quiz=quiz,
        defaults={'score': score, 'total_questions': total_questions, 'feedback_message': feedback_message}
    )

    # 5. CRITICAL FIX: Redirect to the RESULTS page, not the list page.
    return redirect('quiz_results', pk=attempt.pk)
# core/views.py (Find and REPLACE the quiz_results_view function)

@login_required
def quiz_results_view(request, pk):
    """Displays the final quiz results, score, and AI feedback."""
    
    # Ensure QuizAttempt is imported
    from .models import QuizAttempt

    # Fetch the specific QuizAttempt using the primary key (pk)
    attempt = get_object_or_404(QuizAttempt, pk=pk, user=request.user)
    
    # Calculate the percentage score
    if attempt.total_questions > 0:
        percentage = round((attempt.score / attempt.total_questions) * 100)
    else:
        percentage = 0
        
    # Find all questions related to the quiz for review
    questions = attempt.quiz.questions.all()

    context = {
        'attempt': attempt,
        'percentage': percentage,
        'questions': questions,
        'title': f'Results for {attempt.quiz.topic}'
    }
    # Template path: core/quiz_results.html
    return render(request, 'core/quiz_results.html', context)
# ----------------------------------------------------------------------
# Quiz Helper Function (Full Definition)
# ----------------------------------------------------------------------

# core/views.py (inside generate_and_save_quiz)
# core/views.py (Find and REPLACE the entire generate_and_save_quiz function)

# core/ai_utils.py (Find and REPLACE the generate_quiz_json function)

# core/views.py (Add this entire function definition)

# --- Quiz Helper Function (Full Definition) ---

def generate_and_save_quiz(user, topic):
    """Generates quiz JSON using AI and saves Quiz and Question objects."""
    
    # Imports are defined inside the function scope to ensure they are found 
    import json
    from .ai_utils import generate_quiz_json
    from .models import Quiz, Question
    
    json_str, error = generate_quiz_json(topic)
    
    if error:
        print(f"Quiz Generation Error: {error}")
        return None
    
    try:
        quiz_data = json.loads(json_str) 
        questions_list = quiz_data.get('quiz_questions', [])
        
        if not questions_list:
            print("AI returned valid JSON but no questions.")
            return None
        
        new_quiz = Quiz.objects.create(
            user=user,
            topic=topic
        )
        
        questions_to_create = [
            Question(
                quiz=new_quiz, 
                data=q_data
            ) for q_data in questions_list
        ]
        Question.objects.bulk_create(questions_to_create)
        
        return new_quiz.pk
        
    except json.JSONDecodeError:
        print(f"AI returned invalid JSON: {json_str[:200]}...")
        return None
    except Exception as e:
        print(f"Error saving quiz to DB: {e}")
        return None