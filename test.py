import requests

'''
возвращает всех пользователей 
{'users': [{'email': 'test@test.com', 'id': 1, 'name': 'Test', 'surname': 'Test'}]}
'''
print(requests.get('http://127.0.0.1:8080/admin/api/users').json())

'''
возвращает об одном пользователе по айди:
{'users': [{'email': 'test@test.com', 'id': 1, 'name': 'Test', 'surname': 'Test'}]}
'''
print(requests.get('http://127.0.0.1:8080/admin/api/user/1').json())

'''
создает пользователя. ответ - {'email': 'test2@test.com', 'id': 2, 'name': 'Test2', 'surname': 'Test2'}'''
print(requests.post('http://127.0.0.1:8080/admin/api/users',
                    json={'email': 'test2@test.com', 'name': 'Test2', 'surname': 'Test2', "password": '12345678',
                          'repeat_password': '12345678'}).json())

'''изменяет пользователя ответ - {'email': 'test3@test.com', 'id': 3, 'name': 'Test2', 'surname': 'Test2'}'''
print(requests.put('http://127.0.0.1:8080/admin/api/user/3', json={'email': 'test3@test.com'}).json())

'''удаляет пользователя: ответ - {'status': 'Успешно'}
'''
print(requests.delete('http://127.0.0.1:8080/admin/api/user/2').json())
