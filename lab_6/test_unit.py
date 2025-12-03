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


