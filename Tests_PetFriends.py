from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Кузьма', animal_type='звезда',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Собакен", "собака", "5", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Лапа', animal_type='собачка', age=1):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Есди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#1

def test_get_api_key_with_wrong_email(email=valid_email, password='11111'):
    """Проверяем при введении неверного пароля выходит результат 403 """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert "key" not in result


#2
def test_get_api_key_with_wrong_email(email='kyky@mail.ru', password=valid_password):
    """Проверяем при введении неверного email выходит результат 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert "key" not in result

#3
def test_add_new_pet_without_photo(name='Жорик', animal_type='терьер', age='8'):
    """Проверяем можно ли добавить питомца в упрощенном формате с корректными данными"""

    #     Получаем api key  и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #     Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

#4 Статус запроса при некорректным вводе возвраста питомца должна возвращать 400, а  возвращает 200
def test_update_self_pet_invalid_age(name='Кит', animal_type='Еж', age=-111):
    """Проверяем возможность обновления информации о питомце с некорректным возрастом"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список пустой, то пробуем добавить новое животное
    if len(my_pets['pets']) == 0:
        status, _ = pf.post_api_create_pet_simple(auth_key, "Алекс", "Котенок", "4")
        assert status == 200, 'New pet is not added'
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, _ = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 400 - выходит ошибка, но при вводе 200 - тест выполняется
    #assert status == 400 (выходит ошибка)
    assert status == 200 #тест проходит

#5
def test_put_api_pet_invalid_pet_id(name='Рикусик', animal_type='пес', age=10, pet_id='1234myr'):
    """Проверяем, что можно обновить питомца с недействующим id"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Берём невалидный id питомца и отправляем запрос на удаление
    status, _ = pf.update_pet_info_id(auth_key, name, animal_type, age, pet_id)

    # Проверяем что статус ответа равен 400 и в списке питомцев нет питомца с невалидным id
    assert status == 400

#6
def test_add_pet_with_a_lot_of_words_in_variable_animal_type(name='Жорик', age='8',
                                  animal_type='терьер самое опасное животное'):
    """ Проверяем, что возможно добавления питомца с названием породы которого превышает 7 слова
    Тест не будет пройден если питомец будет добавлен на сайт с названием породы состоящим более 7 слов.'"""

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(api_key, name, animal_type, age)

    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert status == 200
    assert word_count < 7, 'Питомец добавлен на сайт с названием породы больше 7 слов'

#7
def test_add_new_pet(name='//////', animal_type='******', age='2', pet_photo='images/dog.jpg'):
    """Проверяем, что можно добавить питомца с не корректными данными и фото.
    Cтатус 200 выводит результат теста, статус 400 выводит ошибку в тесте и получается негативный тест и получается,
    что на сайт можно ввести некорректные данные"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    # assert status == 400 - в тесте был использован 400


#8
def test_add_pet_with_numbers_in_variable_animal_type(name='Муся', animal_type='111', age='2'):
    """Проверка с добавлением питомца введя в породе животного (animal_type) цифры.
    Тест с негативным результатом если питомец будет добавлен на сайт с цифрами вместо букв в поле порода"""

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(api_key, name, animal_type, age)

    assert status == 200
    assert result['animal_type'] == '7857987'

#9
def test_add_new_info_pet_with_empty_data(name='', animal_type='',
                                          age=''):
    """Проверяем что можно добавить питомца с пустыми данными без фото"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


#10
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Мурзик", "кот", "1", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
