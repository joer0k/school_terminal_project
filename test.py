from requests import get, post, put, delete

print(get('http://localhost:5000/api/teachers').json())
print(post('http://localhost:5000/api/teachers', json={
    'teacher_name' : 'Тест №2',
    'way_to_photo': 'путь',
    'additional_information':'что то',
    'post_id':'1'
}).json())
print(get('http://localhost:5000/api/teachers').json())
print(put('http://localhost:5000/api/teachers/2', json={
    'way_to_photo': 'измененный путь',
}).json())
print(get('http://localhost:5000/api/teachers').json())
print(delete('http://localhost:5000/api/teachers/2').json())
print(get('http://localhost:5000/api/teachers').json())