class Book:
    """Книга в библиотеке"""

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False

    def __str__(self):
        if self.is_borrowed:
            return f'"{self.title}" - {self.author} (выдана)'
        return f'"{self.title}" - {self.author} (в наличии)'

    def borrow(self):
        """Взять книгу"""
        if not self.is_borrowed:
            self.is_borrowed = True
            return True
        return False

    def return_book(self):
        """Вернуть книгу"""
        if self.is_borrowed:
            self.is_borrowed = False
            return True
        return False


class Library:
    """Библиотека"""

    def __init__(self, name):
        self.name = name
        self.books = []
        self.readers = {}

    def add_book(self, title, author):
        """Добавить новую книгу"""
        book = Book(title, author)
        self.books.append(book)
        return book

    def find_book(self, title):
        """Найти книгу по названию"""
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def borrow_book(self, title, reader_name):
        """Выдать книгу читателю"""
        book = self.find_book(title)
        if book and book.borrow():
            # Записываем, кто взял книгу
            if reader_name not in self.readers:
                self.readers[reader_name] = []
            self.readers[reader_name].append(title)
            return True
        return False

    def return_book(self, title):
        """Принять книгу обратно"""
        book = self.find_book(title)
        if book:
            return book.return_book()
        return False

    def get_available_books(self):
        """Получить список доступных книг"""
        return [book for book in self.books if not book.is_borrowed]

    def get_borrowed_books(self):
        """Получить список выданных книг"""
        return [book for book in self.books if book.is_borrowed]

    def get_statistics(self):
        """Получить статистику"""
        total = len(self.books)
        borrowed = len(self.get_borrowed_books())
        available = total - borrowed

        # Найти самого популярного автора
        author_count = {}
        for book in self.books:
            author_count[book.author] = author_count.get(book.author, 0) + 1

        if author_count:
            popular_author = max(author_count, key=author_count.get)
        else:
            popular_author = "Нет авторов"

        return {
            'total': total,
            'borrowed': borrowed,
            'available': available,
            'popular_author': popular_author
        }


class Reader:
    """Читатель библиотеки"""

    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow(self, library, book_title):
        """Взять книгу из библиотеки"""
        if library.borrow_book(book_title, self.name):
            self.borrowed_books.append(book_title)
            return True
        return False

    def return_book(self, library, book_title):
        """Вернуть книгу в библиотеку"""
        if book_title in self.borrowed_books and library.return_book(book_title):
            self.borrowed_books.remove(book_title)
            return True
        return False

    def get_info(self):
        """Получить информацию о читателе"""
        return {
            'name': self.name,
            'books_count': len(self.borrowed_books),
            'books': self.borrowed_books.copy()
        }


# УТИЛИТЫ
def validate_book_data(title, author):
    """Проверить корректность данных книги"""
    if not title or len(title.strip()) < 2:
        return False, "Название слишком короткое"

    if not author or len(author.strip()) < 2:
        return False, "Имя автора слишком короткое"

    return True, "Данные корректны"


def format_book_list(books):
    """Отформатировать список книг для вывода"""
    if not books:
        return "Книги не найдены"

    result = []
    for i, book in enumerate(books, 1):
        result.append(f"{i}. {book}")
    return "\n".join(result)


# ДЕМОНСТРАЦИЯ РАБОТЫ
def perfomance():
    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ БИБЛИОТЕЧНОЙ СИСТЕМЫ")
    print("=" * 50)

    # 1. Создаем библиотеку
    library = Library("Городская библиотека")
    print(f"\nСоздана библиотека: {library.name}")

    # 2. Добавляем книги
    print("\nДобавляем книги:")
    books_data = [
        ("Преступление и наказание", "Достоевский Ф.М."),
        ("Война и мир", "Толстой Л.Н."),
        ("Мастер и Маргарита", "Булгаков М.А."),
        ("Гарри Поттер", "Роулинг Дж.К."),
        ("1984", "Оруэлл Дж.")
    ]

    for title, author in books_data:
        book = library.add_book(title, author)
        print(f"   ✓ {book}")

    # 3. Создаем читателя
    reader = Reader("Анна Петрова")
    print(f"\nСоздан читатель: {reader.name}")

    # 4. Читатель берет книги
    print("\nЧитатель берет книги:")
    books_to_borrow = ["Война и мир", "Гарри Поттер"]
    for book_title in books_to_borrow:
        if reader.borrow(library, book_title):
            print(f"Взята: '{book_title}'")
        else:
            print(f"Не удалось взять: '{book_title}'")

    # 5. Показываем состояние библиотеки
    print("\nСостояние библиотеки:")
    stats = library.get_statistics()
    print(f"   Всего книг: {stats['total']}")
    print(f"   Выдано: {stats['borrowed']}")
    print(f"   Доступно: {stats['available']}")
    print(f"   Популярный автор: {stats['popular_author']}")

    # 6. Показываем доступные книги
    print("\nДоступные книги:")
    available = library.get_available_books()
    for book in available:
        print(f"   - {book}")

    # 7. Читатель возвращает книгу
    print("\nЧитатель возвращает книгу:")
    if reader.return_book(library, "Война и мир"):
        print("   ✓ 'Война и мир' возвращена")

    # 8. Информация о читателе
    print("\nИнформация о читателе:")
    info = reader.get_info()
    print(f"   Имя: {info['name']}")
    print(f"   Книг на руках: {info['books_count']}")
    if info['books']:
        print(f"   Список: {', '.join(info['books'])}")

    # 9. Проверка валидации
    print("\nПроверка валидации данных:")
    test_cases = [
        ("Книга", "Автор"),
        ("К", "Автор"),
        ("Книга", "А"),
        ("", "Автор"),
        ("Книга", "")
    ]

    for title, author in test_cases:
        is_valid, message = validate_book_data(title, author)
        status = "✓" if is_valid else "✗"
        print(f"   {status} '{title}' / '{author}': {message}")


if __name__ == "__main__":
    perfomance()