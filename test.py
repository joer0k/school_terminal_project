from requests import get, post, put, delete

from requests import get, post, put, delete

print(get('http://localhost:5000/api/teachers').json())
# print(post('http://localhost:5000/api/posts', json={
#     'title':'Учитель русского языка',
#     'post': 'middle_school'
# }).json())
#
# print(post('http://localhost:5000/api/teachers', json={
#     'teacher_name':'Подварко Елена Юрьевна',
#     'way_to_photo': 'images/podvarko.jpg',
#     'additional_information':'njnjnnjnnjj',
#     'post_id': 1
# }).json())
#
# print(post('http://localhost:5000/api/teachers', json={
#     'teacher_name':'Мастерова Ксения Юрьевна',
#     'way_to_photo': '',
#     'additional_information':'njnjnnjnnjj',
#     'post_id': 4
# }).json())
#
# print(post('http://localhost:5000/api/teachers', json={
#     'teacher_name':'Руденко Ксения Николаевна',
#     'way_to_photo': '',
#     'additional_information':'njnjnnjnnjj',
#     'post_id': 3
# }).json())


print(get('http://localhost:5000/api/teachers/post/1'))

# print(get('http://localhost:5000/api/posts').json())

# print(put('http://localhost:5000/api/posts/2', json={
#     'title': 'Завуч',
# }).json())
# print(get('http://localhost:5000/api/teachers').json())
# print(delete('http://localhost:5000/api/teachers/2').json())
# print(get('http://localhost:5000/api/posts').json())