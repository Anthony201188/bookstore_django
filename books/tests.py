from django.test import TestCase
from .models import Book
from datetime import date
from decimal import Decimal # used as floats for prices arent exact numbers


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        classmethod_testbook = Book.objects.create(
            title='global testing book',
            author='Myself',
            description='a book about me',
            published_date='2023-11-23',
            price='2.99'
        )

    def setUp(self): # function based setup
        #create two test instances of the Book model (these will be destroyed at the end of testing)
        functionbased_testbook = Book.objects.create(
            title='Harry Potter',
            author='JK Rowling',
            description='a book about stuff and things',
            published_date='2000-10-21',
            price='25.00')
        
        functionbased_testbook2 = Book.objects.create(
            title='The Hobbit',
            author='JRR Tolkien',
            description='a book about different stuff and things',
            published_date='1998-10-22',
            price='9.00')

    def test_book_model_read(self): #naming convention must icnlude 'test' at the start.
        #retrieve the model instance  by title
        harry_potter_book = Book.objects.get(title='Harry Potter')
        the_hobbit_book = Book.objects.get(title='The Hobbit')


        self.assertEqual(harry_potter_book.title, 'Harry Potter')
        self.assertEqual(harry_potter_book.author, 'JK Rowling')
        self.assertEqual(harry_potter_book.description, 'a book about stuff and things')
        self.assertEqual(harry_potter_book.published_date, date(2000,10,21))
        self.assertEqual(harry_potter_book.price, Decimal('25.00'))


        self.assertEqual(the_hobbit_book.title, 'The Hobbit')
        self.assertEqual(the_hobbit_book.author, 'JRR Tolkien')
        self.assertEqual(the_hobbit_book.description, 'a book about different stuff and things')
        self.assertEqual(the_hobbit_book.published_date, date(1998,10,22))
        self.assertEqual(the_hobbit_book.price, Decimal('9.00'))

    def test_book_create_view(self): # uses view 
        # more integrated test of the functioning of the website as a whole
        response = self.client.post('/create/',{"title":'new title', #post creates a new model instance object direclty using the url
                                               "author":'new author',
                                               "description":'new description',
                                               "published_date":'2001-10-11',
                                               "price":'5.89'
                                               })
        new_book = (Book.objects.last()) 

        self.assertEqual(response.status_code,302) #check for re-direct always happens after a post (create)
        self.assertEqual(new_book.title,"new title") 
        self.assertEqual(new_book.author,"new author")
        self.assertEqual (float(new_book.price), 5.89)

    def test_book_update_view(self): 
        response = self.client.post('/update/confirm/3/',
        {
            "title":'new1 title', 
            "author":'new1 author',
            "description":'new description',
            "published_date":'2001-10-11',
            "price":'5.89'
        })
        testing = response.content
        print("response content",testing)
        new_book = (Book.objects.last()) 
        
        self.assertEqual(response.status_code,302) #check for re-direct always happens after a post (create)
        self.assertEqual(new_book.title,"new1 title") 
        self.assertEqual(new_book.author,"new1 author") 
        self.assertEqual (float(new_book.price), 5.89)       




    #version 2
    #     retrived_book_from_db = Book.objects.all() # returns queryset
    #     self.assertEqual(retrived_book_from_db.count(),3)
        
        
        
            





""" NOTE- using class mehtods for log in and book data
from django.test import TestCase
from .models import Book
from django.contrib.auth.models import User

class YourTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user
        cls.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a book
        cls.book = Book.objects.create(
            title='Harry Potter',
            author='JK Rowling',
            description='A book about magic',
            published_date='2000-10-21',
            price='25.00'
        )

    def test_user_can_access_book(self):
        # You can access cls.user and cls.book here
        self.client.login(username=cls.user.username, password='testpassword')
        response = self.client.get('/book/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')

    def test_book_has_correct_author(self):
        # You can access cls.book here
        self.assertEqual(cls.book.author, 'JK Rowling')

    def test_book_has_valid_price(self):
        # You can access cls.book here
        self.assertTrue(cls.book.price > 0)

    #fixtures can also be used to load test data in the following way

    class MyModelTestCase(TestCase):
        fixtures = ['mydata.json'] 
 """

""" NOTE - reasons for using class methods for test data
Efficiency: The setUpTestData method is run once for the entire test case class.
It's called when the test case class is set up but before any individual test methods are run.
This means that the data setup is done more efficiently, as it's not repeated for each test
method within the class.

Consistency: By setting up the test data in setUpTestData, you ensure that the same data is 
used across all test methods within the class. This consistency is crucial for accurate testing,
as all test methods operate on the same data.

Isolation: Test data created in setUpTestData is isolated from the individual test methods.
 Each test method doesn't affect the data used in other test methods, which is important for 
 maintaining test independence and ensuring that changes made during one test method don't impact 
 subsequent tests.

Performance: In some cases, creating test data for every test method can be slow, especially if it 
involves database operations. setUpTestData can improve test performance by reducing the overhead of
data setup for each test method.

also if you assign the classbased setup up data to a varible theey become accessable by all the test
methods within the class parent testing class i.e. all tests within that class

however if you just create the book without assinging a varible its only local and therefore negates the purpose
of this class based method

EXAMPLE 1
class BookTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_book = Book.objects.create(
            title='global testing book',
            author='Myself',
            description='a book about me',
            published_date='2023-11-23',
            price='2.99'
        )

    def test_method_1(self):
        # Access self.test_book and perform assertions

    def test_method_2(self):
        # Access self.test_book and perform assertions
---------------------------------------------------------
EXAMPLE2
class BookTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Book.objects.create(
            title='global testing book',
            author='Myself',
            description='a book about me',
            published_date='2023-11-23',
            price='2.99'
        )

    def test_method_1(self):
        # Cannot access the book created in setUpTestData

    def test_method_2(self):
        # Cannot access the book created in setUpTestData

 """
        

    

