from models import Session, VKWallPost, VKGroup, VKCounters
from sqlalchemy.sql import func

s = Session()


min_comments = func.min(VKWallPost.comments_count).label('min_comments')
max_comments = func.max(VKWallPost.comments_count).label('max_comments')
avg_comments = func.avg(VKWallPost.comments_count).label('avg_comments')

min_likes = func.min(VKWallPost.likes_count).label('min_likes')
max_likes = func.max(VKWallPost.likes_count).label('max_likes')
avg_likes = func.avg(VKWallPost.likes_count).label('avg_likes')

min_reposts = func.min(VKWallPost.reposts_count).label('min_reposts')
max_reposts = func.max(VKWallPost.reposts_count).label('max_reposts')
avg_reposts = func.avg(VKWallPost.reposts_count).label('avg_reposts')

vk_query = s.query(
	VKGroup.insense_name, VKGroup.insense_description,
	VKGroup.pk, VKGroup.id, VKGroup.name, VKGroup.screen_name,
	VKGroup.description, VKGroup.start_date, VKGroup.avatar,
	min_comments, max_comments, avg_comments,
	min_likes, max_likes, avg_likes,
	min_reposts, max_reposts, avg_reposts,
	VKCounters.pk, VKCounters.members, VKCounters.photos,
	VKCounters.albums, VKCounters.topics, VKCounters.videos,
	VKCounters.audios, VKCounters.articles, VKCounters.wall_posts,
).filter(VKWallPost.group_id == VKGroup.pk, VKCounters.group_id == VKGroup.pk).group_by(VKGroup.pk)
