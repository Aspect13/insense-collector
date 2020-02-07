from pathlib import Path
from openpyxl import Workbook

from logger_custom import logger
from settings import OUTPUTS_FOLDER


def get_excel_wb_path(suffix=None, index=0):
	file_name = f'db_dump{suffix}_{index}'
	if Path.joinpath(OUTPUTS_FOLDER, f'{file_name}.xlsx').exists():
		new_index = int(file_name.split('_')[-1]) + 1
		return get_excel_wb_path(suffix, new_index)
	else:
		return Path.joinpath(OUTPUTS_FOLDER, f'{file_name}.xlsx')


def write_model_to_worksheet(worksheet, query):
	worksheet.append([i['name'] for i in query.column_descriptions])
	for group_data in query.all():
		worksheet.append(group_data)


def dump_to_excel(query, worksheet_name='Sheet1', suffix='', write_only=True):
	log_query = str(query).replace("\n", "  ")
	logger.info(f'Writing data to excel with query {log_query}')
	wb = Workbook(write_only=write_only)
	ws = wb.create_sheet(worksheet_name)
	write_model_to_worksheet(ws, query)
	save_path = get_excel_wb_path(suffix)
	logger.info(f'Saving workbook at: {save_path}')
	wb.save(save_path)


if __name__ == '__main__':
	from dbshell import vk_query
	dump_to_excel(vk_query, suffix='_VK', worksheet_name='vk_groups')











# def requests_auth():
# 	headers = {
# 		'Referer': 'https://m.vk.com/login?role=fast&to=&s=1&m=1&email={}'.format(LOGIN),
# 		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'
# 	}
#
# 	payload = {
# 		'email': LOGIN,
# 		'pass': PASSWORD
# 	}
#
# 	with requests.Session() as S:
# 		page = S.get('https://m.vk.com/login')
# 		soup = BeautifulSoup(page.content, 'html.parser')
# 		url = soup.find('form')['action']
# 		p = S.post(url, data=payload, headers=headers)
# 		# NOW YOU ARE SUCCESSFULLY LOGGED IN
# 		x = S.get('https://vk.com/volleyzenit')
# 		with open('tmp.html', 'w') as out:
# 			out.write(x.text)
