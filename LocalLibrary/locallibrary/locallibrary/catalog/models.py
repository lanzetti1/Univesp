from django.db import models
from django.contrib.auth.models import user
from django.urls import reverse

from datetime import date

# Create your models here.

class Genre(models.Model):
    """Modelo representando um genero de livro."""
    name = models.CharField(max_length=200, help_text='Entre com um genero de livro(e.g. Science Fiction)')

    def __str__(self):
        """String para representar o Modelo do objeto."""
        return self.name
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Book(models.Model):
    """Modelo representando um livro (mas nao uma copia especifica de um livro)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Entre com uma descricao resumida do livro')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Caractereres <a href="https://www.isbn-international.org/content/what-isbn">numero ISBN</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Selecione o genero do livro')

    def __str__(self):
        """String para representar o Modelo do objeto."""
        return self.title

    def get_absolute_url(self):
        """Returne a url para acessar o detalhe do registro do livro."""
        return reverse('book-detail', args=[str(self.id)])




import uuid # Required for unique book instances

class BookInstance(models.Model):
    """Modelo representando uma copia especifica de um livro (i.e. isto pode ser emprestado da bibioteca)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID unico para este livro em particular em toda a biblioteca')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
@property
def is_overdue(self):
    if self.due_back and date.today() > self.due_back:
        return True
    return False



    LOAN_STATUS = (
        ('m', 'Manutencao'),
        ('e', 'Emprestado'),
        ('d', 'Disponivel'),
        ('r', 'Reservedo'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Disponibilidade do libro',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String para representar o Modelo do objeto."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Modelo representando um autor."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Falecido', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returna a url para acessar uma instancia de um autor especifico."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String para representar o Model do objeto."""
        return f'{self.last_name}, {self.first_name}'


