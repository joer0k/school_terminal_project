import requests

print(requests.post('http://127.0.0.1:8080/admin/api/schedule',
                    json={'subject_id': '1', 'class_id': '2', 'classroom': '1',
                          'day_of_week': '2', 'number_lesson': '1'}).text)
