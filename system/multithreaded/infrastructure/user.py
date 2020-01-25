
class User:
    def __init__(self, uid, location, profile, rated_books, age=None):
        self.uid = uid
        self.location = location
        self.age = age
        self.rated_books = rated_books
        self.profile = profile