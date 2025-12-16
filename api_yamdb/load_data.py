import csv
import os

import django
from django.contrib.auth import get_user_model

from reviews.models import Category, Comment, Genre, Review, Title


DATA_DIR = os.path.join('static', 'data')
FILES = {
    'users': 'users.csv',
    'categories': 'category.csv',
    'genres': 'genre.csv',
    'titles': 'titles.csv',
    'genre_title': 'genre_title.csv',
    'reviews': 'review.csv',
    'comments': 'comments.csv'
}

LOAD_FUNCTIONS = [
    ('users', 'load_users'),
    ('categories', 'load_categories'),
    ('genres', 'load_genres'),
    ('titles', 'load_titles'),
    ('genre_title', 'load_genre_title'),
    ('reviews', 'load_reviews'),
    ('comments', 'load_comments')
]


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()


User = get_user_model()


def clean_value(value):
    if value == 'NULL' or value is None or value == '':
        return ''
    return str(value).strip()


def process_user_row(row):
    try:
        user, created = User.objects.get_or_create(
            id=int(clean_value(row['id'])),
            defaults={
                'username': clean_value(row['username']),
                'email': clean_value(row['email']),
                'role': clean_value(row['role']),
                'bio': clean_value(row['bio']),
                'first_name': clean_value(row['first_name']),
                'last_name': clean_value(row['last_name']),
            }
        )
        return created
    except Exception:
        return False


def load_users():
    users_path = os.path.join(DATA_DIR, FILES['users'])
    try:
        with open(users_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return sum(1 for row in reader if process_user_row(row))
    except FileNotFoundError:
        return 0


def process_category_row(row):
    try:
        category, created = Category.objects.get_or_create(
            id=int(clean_value(row['id'])),
            defaults={
                'name': clean_value(row['name']),
                'slug': clean_value(row['slug']),
            }
        )
        return created
    except Exception:
        return False


def load_categories():
    categories_path = os.path.join(DATA_DIR, FILES['categories'])
    try:
        with open(categories_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return sum(1 for row in reader if process_category_row(row))
    except FileNotFoundError:
        return 0


def process_genre_row(row):
    try:
        genre, created = Genre.objects.get_or_create(
            id=int(clean_value(row['id'])),
            defaults={
                'name': clean_value(row['name']),
                'slug': clean_value(row['slug']),
            }
        )
        return created
    except Exception:
        return False


def load_genres():
    genres_path = os.path.join(DATA_DIR, FILES['genres'])
    try:
        with open(genres_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return sum(1 for row in reader if process_genre_row(row))
    except FileNotFoundError:
        return 0


def process_title_row(row):
    try:
        category_id = clean_value(row['category'])
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=int(category_id))
            except Category.DoesNotExist:
                return False

        if 'description' in row:
            description = clean_value(row['description'])
        else:
            description = ''

        if clean_value(row['year']):
            year = int(clean_value(row['year']))
        else:
            year = None

        title, created = Title.objects.get_or_create(
            id=int(clean_value(row['id'])),
            defaults={
                'name': clean_value(row['name']),
                'year': year,
                'category': category,
                'description': description,
            }
        )
        return created
    except Exception:
        return False


def load_titles():
    titles_path = os.path.join(DATA_DIR, FILES['titles'])
    try:
        with open(titles_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return sum(1 for row in reader if process_title_row(row))
    except FileNotFoundError:
        return 0


def process_genre_title_row(row):
    try:
        title_id = int(clean_value(row['title_id']))
        genre_id = int(clean_value(row['genre_id']))

        title = Title.objects.get(id=title_id)
        genre = Genre.objects.get(id=genre_id)

        if not title.genre.filter(id=genre_id).exists():
            title.genre.add(genre)
            return True
        return False
    except (Title.DoesNotExist, Genre.DoesNotExist, Exception):
        return False


def load_genre_title():
    genre_title_path = os.path.join(DATA_DIR, FILES['genre_title'])
    try:
        with open(genre_title_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return sum(1 for row in reader if process_genre_title_row(row))
    except FileNotFoundError:
        return 0


def process_review_row(row):
    try:
        title_id = int(clean_value(row['title_id']))
        author_id = int(clean_value(row['author']))

        title = Title.objects.get(id=title_id)
        author = User.objects.get(id=author_id)

        if clean_value(row['score']):
            score = int(clean_value(row['score']))
        else:
            score = 1
        score = max(1, min(10, score))

        review, created = Review.objects.get_or_create(
            id=int(clean_value(row['id'])),
            defaults={
                'title': title,
                'text': clean_value(row['text']),
                'author': author,
                'score': score,
                'pub_date': clean_value(row['pub_date']),
            }
        )
        return created
    except (Title.DoesNotExist, User.DoesNotExist, Exception):
        return False


def load_reviews():
    reviews_path = os.path.join(DATA_DIR, FILES['reviews'])
    try:
        with open(reviews_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return sum(1 for row in reader if process_review_row(row))
    except FileNotFoundError:
        return 0


def process_comment_row(row):
    try:
        review_id = int(clean_value(row['review_id']))
        author_id = int(clean_value(row['author']))

        review = Review.objects.get(id=review_id)
        author = User.objects.get(id=author_id)

        comment, created = Comment.objects.get_or_create(
            id=int(clean_value(row['id'])),
            defaults={
                'review': review,
                'text': clean_value(row['text']),
                'author': author,
                'pub_date': clean_value(row['pub_date']),
            }
        )
        return created
    except (Review.DoesNotExist, User.DoesNotExist, Exception):
        return False


def load_comments():
    comments_path = os.path.join(DATA_DIR, FILES['comments'])
    try:
        with open(comments_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return sum(1 for row in reader if process_comment_row(row))
    except FileNotFoundError:
        return 0


def main():
    load_results = {}

    for file_name, func_name in LOAD_FUNCTIONS:
        func = globals()[func_name]
        load_results[file_name] = func()

    print("Результаты загрузки данных:")
    for file_name, count in load_results.items():
        print(f"  {file_name}: {count} записей")


if __name__ == "__main__":
    main()
