import datetime #<- will be used to set default dates on models
import sqlalchemy as sa #<- provides access to sqlalchemy constructs

from webhelpers2.text import urlify #<- will generate slugs
from webhelpers2.date import time_ago_in_words #<- human friendly dates
from paginate_sqlalchemy import SqlalchemyOrmPage #<- provides pagination

from pyramid_blogr.models import Base, DBSession  #<- we need to import our sqlalchemy metadata for model classes to inherit from

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,     #<- will provide unicode field,
    UnicodeText, #<- will provide unicode text field,
    DateTime     #<- time abstraction field,
)

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def all(cls):
        return DBSession.query(Entry).order_by(sa.desc(Entry.created))

    @classmethod
    def by_id(cls, id):
        return DBSession.query(Entry).filter(Entry.id == id).first()

    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)

    @classmethod
    def get_paginator(cls, request, page=1):
        query = DBSession.query(Entry).order_by(sa.desc(Entry.created))
        query_params = request.GET.mixed()

        def url_maker(link_page):
            query_params['page'] = link_page
            return request.current_route_url(_query=query_params)
        return SqlalchemyOrmPage(query, page, items_per_page=5,
                                 url_maker=url_maker)