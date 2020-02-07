options = {
	0: 'Download data from VK',
	1: 'Export data from database to excel',
}

for k, v in options.items():
	print(k, ': ', v)

try:
	choice = int(input())
except Exception as e:
	exit(e)

if choice == 0:
	from vk_collector import run
	run()
elif choice == 1:
	from dbshell import vk_query
	from utils import dump_to_excel
	dump_to_excel(vk_query, suffix='_VK', worksheet_name='vk_groups')
else:
	print('No such option, try again')
