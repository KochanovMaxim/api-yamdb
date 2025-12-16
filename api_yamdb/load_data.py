import csv
import os
import sys

import django
from django.contrib.auth import get_user_model

from reviews.models import Category, Comment, Genre, Review, Title


project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()


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


User = get_user_model()


def clean_value(value):
    """Очистка значения от лишних пробелов и обработка NULL."""
    if value == 'NULL' or value is None or value == '':
        return ''
    return str(value).strip()


def process_user_row(row):
    """Обработка одной строки данных пользователя."""
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
    except Exception as e:
        print(f"Ошибка при обработке пользователя {row.get('id', 'N/A')}: {e}")
        return False


def load_users():
    """Загрузка пользователей из CSV."""
    users_path = os.path.join(DATA_DIR, FILES['users'])
    try:
        with open(users_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            loaded_count = 0
            for row in reader:
                if process_user_row(row):
                    loaded_count += 1
            return loaded_count
    except FileNotFoundError:
        print(f"Файл {users_path} не найден!")
        return 0
    except Exception as e:
        print(f"Ошибка при загрузке пользователей: {e}")
        return 0


def process_category_row(row):
    """Обработка одной строки данных категории."""
    try:
        category, created = Category.objects.get_or_create(
            id=int(clean_value(row['id'])),
            defaults={
                'name': clean_value(row['name']),
                'slug': clean_value(row['slug']),
            }
        )
        return created
    except Exception as e:
        print(f"Ошибка при обработке категории {row.get('id', 'N/A')}: {e}")
        return False


def load_categories():
    """Загрузка категорий из CSV."""
    categories_path = os.path.join(DATA_DIR, FILES['categories'])
    try:
        with open(categories_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            loaded_count = 0
            for row in reader:
                if process_category_row(row):
                    loaded_count += 1
            return loaded_count
    except FileNotFoundError:
        print(f"Файл {categories_path} не найден!")
        return 0
    except Exception as e:
        print(f"Ошибка при загрузке категорий: {e}")
        return 0


def process_genre_row(row):
    """Обработка одной строки данных жанра."""
    try:
        genre, created = Genre.objects.get_or_create(
            id=int(clean_value(row['id'])),
            defaults={
                'name': clean_value(row['name']),
                'slug': clean_value(row['slug']),
            }
        )
        return created
    except Exception as e:
        print(f"Ошибка при обработке жанра {row.get('id', 'N/A')}: {e}")
        return False


def load_genres():
    """Загрузка жанров из CSV."""
    genres_path = os.path.join(DATA_DIR, FILES['genres'])
    try:
        with open(genres_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            loaded_count = 0
            for row in reader:
                if process_genre_row(row):
                    loaded_count += 1
            return loaded_count
    except FileNotFoundError:
        print(f"Файл {genres_path} не найден!")
        return 0
    except Exception as e:
        print(f"Ошибка при загрузке жанров: {e}")
        return 0


def process_title_row(row):
    """Обработка одной строки данных произведения."""
    try:
        category_id = clean_value(row['category'])
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=int(category_id))
            except Category.DoesNotExist:
                print(f"Категория с id={category_id} не найдена!")
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
    except Exception as e:
        print(f"Ошибка при обработке произведения {row.get('id', 'N/A')}: {e}")
        return False


def load_titles():
    """Загрузка произведений из CSV."""
    titles_path = os.path.join(DATA_DIR, FILES['titles'])
    try:
        with open(titles_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            loaded_count = 0
            for row in reader:
                if process_title_row(row):
                    loaded_count += 1
            return loaded_count
    except FileNotFoundError:
        print(f"Файл {titles_path} не найден!")
        return 0
    except Exception as e:
        print(f"Ошибка при загрузке произведений: {e}")
        return 0


def process_genre_title_row(row):
    """Обработка одной строки связи жанр-произведение."""
    try:
        title_id = int(clean_value(row['title_id']))
        genre_id = int(clean_value(row['genre_id']))

        title = Title.objects.get(id=title_id)
        genre = Genre.objects.get(id=genre_id)

        if not title.genre.filter(id=genre_id).exists():
            title.genre.add(genre)
            return True
        return False
    except Title.DoesNotExist:
        print(f"Произведение с id={title_id} не найдено!")
        return False
    except Genre.DoesNotExist:
        print(f"Жанр с id={genre_id} не найден!")
        return False
    except Exception as e:
        print(f"Ошибка при обработке связи жанр-произведение: {e}")
        return False


def load_genre_title():
    """Загрузка связей жанр-произведение из CSV."""
    genre_title_path = os.path.join(DATA_DIR, FILES['genre_title'])
    try:
        with open(genre_title_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            loaded_count = 0
            for row in reader:
                if process_genre_title_row(row):
                    loaded_count += 1
            return loaded_count
    except FileNotFoundError:
        print(f"Файл {genre_title_path} не найден!")
        return 0
    except Exception as e:
        print(f"Ошибка при загрузке связей жанр-произведение: {e}")
        return 0


def process_review_row(row):
    """Обработка одной строки данных отзыва."""
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
    except Title.DoesNotExist:
        print(f"Произведение с id={title_id} не найдено!")
        return False
    except User.DoesNotExist:
        print(f"Пользователь с id={author_id} не найден!")
        return False
    except Exception as e:
        print(f"Ошибка при обработке отзыва {row.get('id', 'N/A')}: {e}")
        return False


def load_reviews():
    """Загрузка отзывов из CSV."""
    reviews_path = os.path.join(DATA_DIR, FILES['reviews'])
    try:
        with open(reviews_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            loaded_count = 0
            for row in reader:
                if process_review_row(row):
                    loaded_count += 1
            return loaded_count
    except FileNotFoundError:
        print(f"Файл {reviews_path} не найден!")
        return 0
    except Exception as e:
        print(f"Ошибка при загрузке отзывов: {e}")
        return 0


def process_comment_row(row):
    """Обработка одной строки данных комментария."""
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
    except Review.DoesNotExist:
        print(f"Отзыв с id={review_id} не найден!")
        return False
    except User.DoesNotExist:
        print(f"Пользователь с id={author_id} не найден!")
        return False
    except Exception as e:
        print(f"Ошибка при обработке комментария {row.get('id', 'N/A')}: {e}")
        return False


def load_comments():
    """Загрузка комментариев из CSV."""
    comments_path = os.path.join(DATA_DIR, FILES['comments'])
    try:
        with open(comments_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            loaded_count = 0
            for row in reader:
                if process_comment_row(row):
                    loaded_count += 1
            return loaded_count
    except FileNotFoundError:
        print(f"Файл {comments_path} не найден!")
        return 0
    except Exception as e:
        print(f"Ошибка при загрузке комментариев: {e}")
        return 0


def main():
    """Основная функция загрузки данных."""
    load_results = {}

    for file_name, func_name in LOAD_FUNCTIONS:
        func = globals()[func_name]
        count = func()
        load_results[file_name] = count

    total = 0
    for file_name, count in load_results.items():
        total += count


if __name__ == "__main__":
    main()
