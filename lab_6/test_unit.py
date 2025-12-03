import pytest

from library import Book, Library, Reader

def test_book_creation():
    """Тест создания книги"""
    book = Book("Преступление и наказание", "Достоевский")
    assert book.title == "Преступление и наказание"
    assert book.author == "Достоевский"
    assert book.is_borrowed == False


def test_book_borrow():
    """Тест взятия книги"""
    book = Book("Война и мир", "Толстой")
    # Первый раз берем - успешно
    assert book.borrow() == True
    assert book.is_borrowed == True
    # Второй раз берем - неуспешно (уже выдана)
    assert book.borrow() == False


def test_book_return():
    """Тест возврата книги"""
    book = Book("Мастер и Маргарита", "Булгаков")
    book.borrow()  # Сначала берем книгу

    # Возвращаем - успешно
    assert book.return_book() == True
    assert book.is_borrowed == False
    # Пытаемся вернуть еще раз - неуспешно (не была выдана)
    assert book.return_book() == False


def test_library_find_book():
    """Тест поиска книги"""
    library = Library("Тестовая")
    library.add_book("Гарри Поттер", "Роулинг")

    # Находим существующую книгу
    found = library.find_book("Гарри Поттер")
    assert found is not None
    assert found.title == "Гарри Поттер"

    # Не находим несуществующую
    not_found = library.find_book("Несуществующая книга")
    assert not_found is None


def test_library_borrow_book():
    """Тест выдачи книги"""
    library = Library("Тестовая")
    library.add_book("1984", "Оруэлл Дж.")

    # Выдаем книгу
    assert library.borrow_book("1984", "Иван Иванов") == True

    # Проверяем, что книга теперь выдана
    book = library.find_book("1984")
    assert book.is_borrowed == True

    # Пытаемся выдать ту же книгу еще раз
    assert library.borrow_book("1984", "Петр Петров") == False


