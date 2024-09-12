import json

def find_values_by_key(data, target_key):

    values = []
    # если словарь
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                values.append(value)
            elif isinstance(value, (dict, list)):
                values.extend(find_values_by_key(value, target_key))
    # если список
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                values.extend(find_values_by_key(item, target_key))
    
    return values

# Загрузка JSON из файла
with open('response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Поиск значений по ключу
key_to_find = 'full_text'
values = find_values_by_key(data, key_to_find)
# вывод первых 10 твитов Илона
for value in range(10):
    print(f"Твит № {value+1}. {values[value]}")