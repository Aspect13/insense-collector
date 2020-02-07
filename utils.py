def write_model_to_worksheet(wb, model, session):
	ws = wb.create_sheet(model.__tablename__)
	ws.append(model.__table__.columns.keys())
	for i in session.query(model).all():
		data = list(map(i.__dict__.get, model.__table__.columns.keys()))
		ws.append(data)


def dump_to_excel(func, suffix='', write_only=True):
	session = Session()
	wb = Workbook(write_only=write_only)
	func(wb, ProductModel, session)
	write_model_to_worksheet(wb, ReviewModel, session)
	write_model_to_worksheet(wb, ImageModel, session)
	wb.save(EXCEL_WB_PATH(suffix))


if __name__ == '__main__':
	dump_to_excel(write_model_to_worksheet, suffix='_VK')











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
