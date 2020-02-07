from pathlib import Path

from openpyxl import Workbook
from models import Session
from settings import OUTPUTS_FOLDER


def get_excel_wb_path(suffix=None, index=0):
	file_name = f'db_dump{suffix}_{index}'
	if Path.joinpath(OUTPUTS_FOLDER, f'{file_name}.xlsx').exists():
		new_index = int(file_name.split('_')[-1]) + 1
		return get_excel_wb_path(suffix, new_index)
	else:
		return Path.joinpath(OUTPUTS_FOLDER, f'{file_name}.xlsx')


def write_model_to_worksheet(wb, model, query):
	ws = wb.create_sheet(model.__tablename__)
	ws.append(model.__table__.columns.keys())
	for i in query:
		data = list(map(i.__dict__.get, model.__table__.columns.keys()))
		ws.append(data)


def dump_to_excel(model, query, suffix='', write_only=True):
	wb = Workbook(write_only=write_only)
	write_model_to_worksheet(wb, model, query)
	wb.save(get_excel_wb_path(suffix))


if __name__ == '__main__':
	s = Session()
	dump_to_excel(suffix='_VK')











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
