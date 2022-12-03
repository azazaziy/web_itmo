import json
import inspect

class SetArticle:
    def __init__(self, json_article):
        article = json.loads(json_article)
        self.author = article.get('author')
        self.title = article.get('title')
        self.text = article.get('text')
        self.image = article.get('image')
        self.timestamp = article.get('timestamp')
        self.tags = article.get('tags')
        self.article_id = None
        self.editors = article.get('editors')
        self.moderators = article.get('moderators')

    def set_article_id(self, article_id):
        self.article_id = article_id

    def to_dict(self):
        return {
            'author': f"'{self.author}'",
            'title': f"'{self.title}'",
            'text': f"'{self.text}'",
            'image': f"'{self.image}'",
            'timestamp': f"'{self.timestamp}'",
            'tags': None,
            'article_id': str(self.article_id),
            'editors': None,
            'moderators': None
        }