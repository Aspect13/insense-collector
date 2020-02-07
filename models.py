import datetime

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from logger_custom import logger
from settings import DB_PATH

engine = create_engine(f'sqlite:///{DB_PATH}', echo=__name__ == '__main__')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class VKWallPost(Base):
	__tablename__ = 'VKWallPosts'

	pk = Column(Integer, primary_key=True)
	id = Column(Integer, unique=True, )
	from_id = Column(Integer, nullable=False)
	date = Column(Date)
	text_part_500 = Column(String(512), nullable=False)
	comments_count = Column(Integer)
	likes_count = Column(Integer)
	reposts_count = Column(Integer)
	views_count = Column(Integer)

	group = relationship('VKGroup', back_populates='wall_posts', cascade='all,delete')
	group_id = Column(Integer, ForeignKey('VKGroup.pk'), nullable=False)

	@classmethod
	def from_api(cls, api_data):
		return cls(
			id=api_data['id'],
			from_id=api_data['from_id'],
			date=cls.date_format(api_data['date']),
			text_part_500=str(api_data['text'])[:512],
			comments_count=api_data.get('comments', {}).get('count', 0),
			likes_count=api_data.get('likes', {}).get('count', 0),
			reposts_count=api_data.get('reposts', {}).get('count', 0),
			views_count=api_data.get('views', {}).get('count', 0),
		)



	@staticmethod
	def date_format(date):
		return datetime.datetime.fromtimestamp(date)


class VKCounters(Base):
	__tablename__ = 'VKCounters'

	pk = Column(Integer, primary_key=True)
	members = Column(Integer, default=0)
	photos = Column(Integer, default=0)
	albums = Column(Integer, default=0)
	topics = Column(Integer, default=0)
	videos = Column(Integer, default=0)
	audios = Column(Integer, default=0)
	articles = Column(Integer, default=0)
	wall_posts = Column(Integer, default=0)

	group = relationship('VKGroup', back_populates='counters', cascade='all,delete', uselist=False)
	group_id = Column(Integer, ForeignKey('VKGroup.pk'), nullable=False, unique=True)

	@classmethod
	def from_api(cls, api_data):
		# api_data['photos'] = api_data.get('photos', 0)
		# api_data['albums'] = api_data.get('albums', 0)
		# api_data['topics'] = api_data.get('topics', 0)
		# api_data['videos'] = api_data.get('videos', 0)
		# api_data['audios'] = api_data.get('audios', 0)
		# api_data['articles'] = api_data.get('articles', 0)
		k = cls()
		k.update_from_api(api_data)
		return k

	def update_from_api(self, api_data):
		self.members = api_data.get('members', self.members)
		self.photos = api_data.get('photos', self.photos)
		self.albums = api_data.get('albums', self.albums)
		self.topics = api_data.get('topics', self.topics)
		self.videos = api_data.get('videos', self.videos)
		self.audios = api_data.get('audios', self.audios)
		self.articles = api_data.get('articles', self.articles)
		self.wall_posts = api_data.get('wall_posts', self.wall_posts)


class VKGroup(Base):
	__tablename__ = 'VKGroup'

	pk = Column(Integer, primary_key=True)
	id = Column(Integer, unique=True,)
	name = Column(String(128), nullable=False)
	screen_name = Column(String(128), nullable=False)
	counters = relationship(VKCounters, back_populates='group', cascade='all,delete', uselist=False)
	description = Column(String(512))
	start_date = Column(Date, nullable=True)
	avatar = Column(String(256))
	wall_posts = relationship(VKWallPost, back_populates='group', cascade='all,delete')
	insense_name = Column(String(64), nullable=True)
	insense_description = Column(String(128), nullable=True)


	@staticmethod
	def start_date_format(start_date):
		fmt = '%Y%m%d'
		if start_date == 0:
			return
		return datetime.datetime.strptime(str(start_date), fmt)

	@classmethod
	def from_api(cls, api_data):
		return cls(
			id=api_data['id'],
			name=api_data['name'],
			screen_name=api_data['screen_name'],
			description=str(api_data['description'])[:512],
			start_date=cls.start_date_format(api_data['start_date']),
			avatar=api_data['photo_200'],
		)


class ConnectedToModel:
	__session__ = None

	def __init__(self, model):
		self.model = model

	@property
	def session(self):
		if self.__session__:
			return self.__session__
		print(self.model.__tablename__, ' session init')
		logger.debug(f'{self.__class__} session init')
		self.recreate_session()
		return self.__session__

	def recreate_session(self):
		ConnectedToModel.__session__ = Session()
		# self.__session__ = ConnectedToModel.__session__


if __name__ == '__main__':
	Base.metadata.create_all(engine)

