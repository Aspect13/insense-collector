import vk_api
import requests
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError

from logger_custom import logger
from models import VKGroup, VKCounters, Session, VKWallPost
from settings import LOGIN, PASSWORD, POSTS_AMOUNT, UPDATE_GROUP_INFO, UPDATE_COUNTERS, POSTS_DOWNLOAD_MAX, \
	UPDATE_POSTS_INFO


def make_group_wall_id(group):
	return -1 * int(group['id'])


def download_groups(groups):
	assert POSTS_AMOUNT <= 100


	logger.info('Beginning VK auth...')
	vk_session = vk_api.VkApi(
		login=LOGIN, password=PASSWORD,
		token='33927ef133927ef133927ef17233fd261f3339233927ef16dbc8da8c274c7bb6c107c20'
	)
	vk_session.auth()
	vk = vk_session.get_api()
	logger.info('VK auth success!')

	model_session = Session()

	for group in groups:
		START_DATE_FROM_FIRST_POST = False
		group_name, insense_name, insense_description = group
		logger.info(f'Processing group: {group_name}/{insense_name}')
		vk_group = vk.groups.getById(
			group_id=group_name,
			fields=[
				'counters', 'city',
				'country', 'place',
				'description', 'members_count',
				'status', 'contacts',
				'activity', 'start_date']
		)

		vk_group = vk_group[0]

		# for k, v in vk_group.items():
		# 	print(k, ': ', v)

		model_group = VKGroup.from_api(vk_group)
		model_group.insense_name = insense_name
		model_group.insense_description = insense_description
		try:
			logger.info(f'Trying to save group [{group_name}/{insense_name}] into db...')
			model_session.add(model_group)
			model_session.commit()
		except IntegrityError:
			logger.warning(f'Group [{group_name}/{insense_name}] exists!')
			model_session.rollback()
			model_session.flush()
			if not UPDATE_GROUP_INFO:
				logger.warning('Skipping group download and continue with next (to change see "UPDATE_INFO" in settings)')
				continue
			else:
				logger.info('Getting group from database... (to change see "UPDATE_INFO" in settings)')
				model_group = model_session.query(VKGroup).filter(VKGroup.id == vk_group['id']).first()

		if not model_group.start_date:
			logger.warning('No start date specified. Date will be withdrawn from the first comment')
			START_DATE_FROM_FIRST_POST = True

		group_counters = VKCounters.from_api(vk_group['counters'])
		group_counters.group = model_group
		group_counters.members = vk_group['members_count']

		posts_count = vk.wall.get(
			owner_id=make_group_wall_id(vk_group),
			count=1,
			fields=['count']
		)['count']

		logger.info(f'Found {posts_count} posts on group\'s wall')

		group_counters.wall_posts = posts_count
		model_session.add(group_counters)
		try:
			model_session.commit()
		except IntegrityError:
			model_session.rollback()
			model_session.flush()
			if not UPDATE_COUNTERS:
				raise
			else:
				logger.info('Updating counters...')
				group_counters = model_session.query(VKCounters).filter_by(group=model_group).first()
				group_counters.update_from_api({
					**vk_group['counters'],
					'wall_posts': posts_count,
					'members': vk_group['members_count']
				})
				model_session.add(group_counters)
				model_session.commit()
				logger.info('Counters updated!')

		post = None
		for i in range(0, int(min(posts_count, POSTS_DOWNLOAD_MAX)), POSTS_AMOUNT):
			logger.info(f'Fetching next {POSTS_AMOUNT} posts from wall...')
			current_query_count = POSTS_AMOUNT if (posts_count - i) // POSTS_AMOUNT != 0 else posts_count % POSTS_AMOUNT
			group_wall = vk.wall.get(
				owner_id=make_group_wall_id(vk_group),
				count=current_query_count,
				extended=1,
				offset=i
			)
			try:
				for post in group_wall['items']:
					model_post = VKWallPost.from_api(post)
					model_post.group = model_group
					model_session.add(model_post)
						# else:
						# 	model_post = model_session.query(VKWallPost).filter(VKWallPost.id == post['id']).first()
					if post['id'] == group_wall['items'][current_query_count // 4]['id']:
						logger.info(f'{(current_query_count / 4 + i) / posts_count:.2%} complete')
					if post['id'] == group_wall['items'][current_query_count // 2]['id']:
						logger.info(f'{(current_query_count / 2 + i) / posts_count:.2%} complete')
				try:
					model_session.commit()
				except IntegrityError:
					model_session.rollback()
					model_session.flush()
					if not UPDATE_POSTS_INFO:
						raise
			except IntegrityError:
				continue
			finally:
				logger.info(f'{(current_query_count + i) / posts_count:.2%} complete')

		if START_DATE_FROM_FIRST_POST and post:
			model_group.start_date = VKWallPost.date_format(post['date'])
			model_session.add(model_group)
			model_session.commit()
			logger.info(f'Start date for group [{group_name}/{insense_name}] from the first comment update success!')


if __name__ == '__main__':
	groups = [
		('alecbenjaminmusic', 'Какой-то чел', 'Видать музыкант'),
		('tnt', 'CHANNEL TNT', 'some custom description'),
	]
	download_groups(groups)





