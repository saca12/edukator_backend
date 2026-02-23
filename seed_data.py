import os
import django
import uuid
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TuteurIA.settings')
django.setup()

from education.models import Grade, Subject, Chapter, Lesson, LessonContent
from exercises.models import Exercise, Question, Answer, Difficulty, ExerciseType

def populate():
    print("Début du peuplement de la base de données (Mode Mise à jour)...")

    grade, _ = Grade.objects.get_or_create(name="2nde C", level="Lycée")
    diff_normal, _ = Difficulty.objects.get_or_create(level_name="Normal", value=1)
    
    # CORRECTION : Le type doit être QCM (selon models.py) et non "Quiz"
    type_qcm, _ = ExerciseType.objects.get_or_create(name="QCM")

    programme = {
        "Mathématiques": [
            ("Calcul dans R", ["Ensembles de nombres", "Intervalles et voisinages", "Valeur absolue"]),
            ("Fonctions", ["Généralités sur les fonctions", "Fonctions affines", "Fonctions de référence"]),
        ],
        "Physique-Chimie": [
            ("Chimie", ["L'atome et l'élément chimique", "La mole : quantité de matière", "Les solutions aqueuses"]),
            ("Physique", ["Mouvement et vitesse", "Forces et équilibre", "Lois de Newton (Introduction)"]),
        ],
        "SVT": [
            ("La Terre", ["La Terre dans le système solaire", "La biosphère", "Structure interne de la Terre"]),
            ("Écosystèmes", ["Flux de matière et d'énergie", "Biodiversité", "Cycles de la matière"]),
        ],
        "Français": [
            ("Littérature", ["Le texte argumentatif", "L'analyse du roman", "La poésie"]),
            ("Méthodologie", ["Le résumé de texte", "La dissertation", "Le commentaire composé"]),
        ],
        "Histoire-Géo": [
            ("Histoire", ["La Renaissance", "La révolution industrielle", "L'Afrique avant la colonisation"]),
            ("Géographie", ["La population mondiale", "Les climats", "L'urbanisation mondiale"]),
        ],
        "Anglais": [
            ("Grammar", ["Present Perfect vs Past Simple", "Passive Voice", "Conditionals"]),
            ("Communication", ["Environment & Ecology", "Technology & Progress", "Jobs and Future"]),
        ],
        "Philosophie": [
            ("Introduction", ["La conscience", "Le désir", "La vérité"]),
            ("Morale et Politique", ["La liberté", "Le devoir", "La justice"]),
        ]
    }

    for subject_name, chapters in programme.items():
        subject, _ = Subject.objects.get_or_create(name=subject_name, grade=grade)

        for i, (chapter_title, lessons) in enumerate(chapters):
            chapter, _ = Chapter.objects.get_or_create(
                subject=subject, 
                order_index=i + 1,
                defaults={'id': uuid.uuid4(), 'title': chapter_title}
            )
            if chapter.title != chapter_title:
                chapter.title = chapter_title
                chapter.save()

            for j, lesson_title in enumerate(lessons):
                lesson, created = Lesson.objects.get_or_create(
                    chapter=chapter,
                    order_index=j + 1,
                    defaults={'id': uuid.uuid4(), 'title': lesson_title, 'is_completed': False}
                )
                
                if not created and lesson.title != lesson_title:
                    lesson.title = lesson_title
                    lesson.save()

                LessonContent.objects.get_or_create(
                    lesson=lesson,
                    defaults={
                        'id': uuid.uuid4(),
                        'rich_text_content': f"<h1>{lesson_title}</h1><p>Cours complet sur {lesson_title}.</p>",
                        'illustrations_url': "/images/placeholder.jpg",
                        'audio_url': "/audio/placeholder.mp3"
                    }
                )

                exercise, _ = Exercise.objects.get_or_create(
                    lesson=lesson,
                    defaults={
                        'id': uuid.uuid4(),
                        # CORRECTION : On met un titre plus explicite
                        'title': f"{subject_name} - QCM : {lesson_title}",
                        'type': type_qcm,
                        'difficulty': diff_normal,
                        'instructions': f"Test de connaissances sur {lesson_title}."
                    }
                )

                for k in range(1, 4):
                    question, q_created = Question.objects.get_or_create(
                        exercise=exercise,
                        question_text=f"Concernant la leçon '{lesson_title}', l'affirmation {k} est-elle exacte ?",
                        defaults={'id': uuid.uuid4(), 'points': 5.0}
                    )
                    
                    # NOUVEAU : Création des choix de réponses pour que le frontend React puisse les afficher
                    if q_created:
                        Answer.objects.create(question=question, choice_text="Oui, tout à fait", is_correct_option=True)
                        Answer.objects.create(question=question, choice_text="Non, c'est faux", is_correct_option=False)
                        Answer.objects.create(question=question, choice_text="Je ne sais pas", is_correct_option=False)

    print("Population terminée ! Les QCM sont maintenant jouables.")

if __name__ == '__main__':
    populate()