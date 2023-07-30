from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name_given):
        if not name_given:
            raise ValueError('No name provided')
        author_name_in_use = Author.query.filter(Author.name == name_given).first()
        if author_name_in_use and author_name_in_use.id != self.id:
            raise ValueError('Name is already in use')
        return name_given
    
    @validates('phone_number')
    def validate_number(self, key, phone_given):
        if len(phone_given) != 10:
            raise ValueError('Phone number must be ten digits')
        return phone_given

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self, key, content_given):
        if len(content_given) < 250:
            raise ValueError('Content must be at least 250 characters long)')
        return content_given
    
    @validates('summary')
    def validate_summary(self,key,summary_given):
        if len(summary_given) >= 250:
            raise ValueError('Summary must not be over 250 characters long')
        return summary_given
    
    @validates('category')
    def validate_category(self, key, content_given):
        if content_given != 'Fiction' and content_given != 'Non-Fiction':
            raise ValueError('Content must be of type Fiction or Non-Fiction')
        return content_given
    
    @validates('title')
    def validate_title(self, key, title_given):
        clickbait_words = ['Won\'t Belive', 'Secret', 'Top', 'Guess']
        if not any(word in title_given.lower() for word in clickbait_words):
            raise ValueError('This title needs to be more clickbaitey')
        return title_given


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
