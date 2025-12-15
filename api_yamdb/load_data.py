import os
import django
import csv

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

from django.contrib.auth import get_user_model
from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()

def clean_value(value):
    """Очищает значение от NULL и лишних пробелов"""
    if value == 'NULL' or value is None or value == '':
        return ''
    return str(value).strip()

print("="*50)
print("НАЧАЛО ЗАГРУЗКИ ДАННЫХ ИЗ CSV ФАЙЛОВ")
print("="*50)

# 1. Загрузка пользователей (users.csv)
print("\n1. ЗАГРУЗКА ПОЛЬЗОВАТЕЛЕЙ...")
users_path = os.path.join('static', 'data', 'users.csv')
try:
    with open(users_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        user_count = 0
        for row in reader:
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
                if created:
                    user_count += 1
            except Exception as e:
                print(f"  Ошибка при загрузке пользователя ID {row.get('id', 'N/A')}: {e}")
    
    print(f"  ✓ Загружено пользователей: {user_count} (всего в БД: {User.objects.count()})")
except FileNotFoundError:
    print(f"  ✗ Файл не найден: {users_path}")
except Exception as e:
    print(f"  ✗ Ошибка при чтении файла пользователей: {e}")

# 2. Загрузка категорий (category.csv)
print("\n2. ЗАГРУЗКА КАТЕГОРИЙ...")
categories_path = os.path.join('static', 'data', 'category.csv')
try:
    with open(categories_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        category_count = 0
        for row in reader:
            try:
                category, created = Category.objects.get_or_create(
                    id=int(clean_value(row['id'])),
                    defaults={
                        'name': clean_value(row['name']),
                        'slug': clean_value(row['slug']),
                    }
                )
                if created:
                    category_count += 1
            except Exception as e:
                print(f"  Ошибка при загрузке категории ID {row.get('id', 'N/A')}: {e}")
    
    print(f"  ✓ Загружено категорий: {category_count} (всего в БД: {Category.objects.count()})")
except FileNotFoundError:
    print(f"  ✗ Файл не найден: {categories_path}")
except Exception as e:
    print(f"  ✗ Ошибка при чтении файла категорий: {e}")

# 3. Загрузка жанров (genre.csv)
print("\n3. ЗАГРУЗКА ЖАНРОВ...")
genres_path = os.path.join('static', 'data', 'genre.csv')
try:
    with open(genres_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        genre_count = 0
        for row in reader:
            try:
                genre, created = Genre.objects.get_or_create(
                    id=int(clean_value(row['id'])),
                    defaults={
                        'name': clean_value(row['name']),
                        'slug': clean_value(row['slug']),
                    }
                )
                if created:
                    genre_count += 1
            except Exception as e:
                print(f"  Ошибка при загрузке жанра ID {row.get('id', 'N/A')}: {e}")
    
    print(f"  ✓ Загружено жанров: {genre_count} (всего в БД: {Genre.objects.count()})")
except FileNotFoundError:
    print(f"  ✗ Файл не найден: {genres_path}")
except Exception as e:
    print(f"  ✗ Ошибка при чтении файла жанров: {e}")

# 4. Загрузка произведений (titles.csv)
print("\n4. ЗАГРУЗКА ПРОИЗВЕДЕНИЙ...")
titles_path = os.path.join('static', 'data', 'titles.csv')
try:
    with open(titles_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        title_count = 0
        for row in reader:
            try:
                category_id = clean_value(row['category'])
                category = None
                if category_id:
                    try:
                        category = Category.objects.get(id=int(category_id))
                    except Category.DoesNotExist:
                        print(f"  ⚠ Категория с id {category_id} не найдена для произведения {row['id']}")
                        continue
                
                description = clean_value(row['description']) if 'description' in row else ''
                year = int(clean_value(row['year'])) if clean_value(row['year']) else None
                
                title, created = Title.objects.get_or_create(
                    id=int(clean_value(row['id'])),
                    defaults={
                        'name': clean_value(row['name']),
                        'year': year,
                        'category': category,
                        'description': description,
                    }
                )
                if created:
                    title_count += 1
            except Exception as e:
                print(f"  Ошибка при загрузке произведения ID {row.get('id', 'N/A')}: {e}")
    
    print(f"  ✓ Загружено произведений: {title_count} (всего в БД: {Title.objects.count()})")
except FileNotFoundError:
    print(f"  ✗ Файл не найден: {titles_path}")
except Exception as e:
    print(f"  ✗ Ошибка при чтении файла произведений: {e}")

# 5. Загрузка связей жанров и произведений (genre_title.csv)
print("\n5. ЗАГРУЗКА СВЯЗЕЙ ЖАНРОВ И ПРОИЗВЕДЕНИЙ...")
genre_title_path = os.path.join('static', 'data', 'genre_title.csv')
try:
    with open(genre_title_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        relation_count = 0
        for row in reader:
            try:
                title_id = int(clean_value(row['title_id']))
                genre_id = int(clean_value(row['genre_id']))
                
                title = Title.objects.get(id=title_id)
                genre = Genre.objects.get(id=genre_id)
                
                # Проверяем, есть ли уже такая связь
                if not title.genre.filter(id=genre_id).exists():
                    title.genre.add(genre)
                    relation_count += 1
            except Title.DoesNotExist:
                print(f"  ⚠ Произведение с id {title_id} не найдено")
            except Genre.DoesNotExist:
                print(f"  ⚠ Жанр с id {genre_id} не найден")
            except Exception as e:
                print(f"  Ошибка при загрузке связи: {e}")
    
    print(f"  ✓ Загружено связей: {relation_count}")
except FileNotFoundError:
    print(f"  ✗ Файл не найден: {genre_title_path}")
except Exception as e:
    print(f"  ✗ Ошибка при чтении файла связей: {e}")

# 6. Загрузка отзывов (review.csv)
print("\n6. ЗАГРУЗКА ОТЗЫВОВ...")
reviews_path = os.path.join('static', 'data', 'review.csv')
try:
    with open(reviews_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        review_count = 0
        for row in reader:
            try:
                title_id = int(clean_value(row['title_id']))
                author_id = int(clean_value(row['author']))
                
                title = Title.objects.get(id=title_id)
                author = User.objects.get(id=author_id)
                
                score = int(clean_value(row['score'])) if clean_value(row['score']) else 1
                score = max(1, min(10, score))  # Ограничиваем оценку от 1 до 10
                
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
                if created:
                    review_count += 1
            except Title.DoesNotExist:
                print(f"  ⚠ Произведение с id {title_id} не найдено для отзыва {row.get('id', 'N/A')}")
            except User.DoesNotExist:
                print(f"  ⚠ Пользователь с id {author_id} не найден для отзыва {row.get('id', 'N/A')}")
            except Exception as e:
                print(f"  Ошибка при загрузке отзыва ID {row.get('id', 'N/A')}: {e}")
    
    print(f"  ✓ Загружено отзывов: {review_count} (всего в БД: {Review.objects.count()})")
except FileNotFoundError:
    print(f"  ✗ Файл не найден: {reviews_path}")
except Exception as e:
    print(f"  ✗ Ошибка при чтении файла отзывов: {e}")

# 7. Загрузка комментариев (comments.csv)
print("\n7. ЗАГРУЗКА КОММЕНТАРИЕВ...")
comments_path = os.path.join('static', 'data', 'comments.csv')
try:
    with open(comments_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        comment_count = 0
        for row in reader:
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
                if created:
                    comment_count += 1
            except Review.DoesNotExist:
                print(f"  ⚠ Отзыв с id {review_id} не найден для комментария {row.get('id', 'N/A')}")
            except User.DoesNotExist:
                print(f"  ⚠ Пользователь с id {author_id} не найден для комментария {row.get('id', 'N/A')}")
            except Exception as e:
                print(f"  Ошибка при загрузке комментария ID {row.get('id', 'N/A')}: {e}")
    
    print(f"  ✓ Загружено комментариев: {comment_count} (всего в БД: {Comment.objects.count()})")
except FileNotFoundError:
    print(f"  ✗ Файл не найден: {comments_path}")
except Exception as e:
    print(f"  ✗ Ошибка при чтении файла комментариев: {e}")

print("\n" + "="*50)
print("ЗАГРУЗКА ДАННЫХ ЗАВЕРШЕНА!")
print("="*50)
print("ИТОГОВАЯ СТАТИСТИКА:")
print(f"  📊 Пользователи: {User.objects.count()}")
print(f"  📊 Категории: {Category.objects.count()}")
print(f"  📊 Жанры: {Genre.objects.count()}")
print(f"  📊 Произведения: {Title.objects.count()}")
print(f"  📊 Отзывы: {Review.objects.count()}")
print(f"  📊 Комментарии: {Comment.objects.count()}")

# Проверка связей
print("\nПРОВЕРКА СВЯЗЕЙ:")
for title in Title.objects.all()[:3]:  # Показываем первые 3 произведения
    genres = ", ".join([g.name for g in title.genre.all()])
    print(f"  '{title.name}': {genres or 'нет жанров'}")
