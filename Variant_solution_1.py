import csv
import re


def get_csv():
    '''Функция для преобразования файла csv в список.'''
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")

        contacts_list_new = list(rows)

    contacts_list_one = []
    for person in contacts_list_new:
        contacts_list_one.append([j for j in person if j != ''])
    return contacts_list_one


def find_copy(text):
    '''Функция для поиска одинаковых фамилий.'''
    contacts_set = set()
    contacts_list_no_copy = []
    for one_keep in text[1:]:
        contacts_set.add(one_keep[0].split(' ')[0])

    for surname in contacts_set:
        no_copy_list = []

        for i in text:
            if surname == i[0].split(' ')[0]:
                no_copy_list.extend(i)
        contacts_list_no_copy.append(no_copy_list)
    contacts_list_two = ([' '.join(i) for i in contacts_list_no_copy])
    return contacts_list_two


def gradation(text):
    '''Функция для редактирования текста для файла csv.'''
    contact_list_three = []
    for person in text:
        list_ = []
        list_.append(re.findall(r'^([А-ЯЁ][а-я]+)', person))
        person = (person[re.search(r'^[А-ЯЁ][а-я]+', person).end():]).strip()
        list_.append(re.findall(r'^([А-ЯЁ][а-яё]+)', person))
        person = (person[re.search(r'[А-ЯЁ][а-я]+', person).end():]).strip()
        list_.append((re.findall(r'^([А-ЯЁ][а-яё]+)', person)))
        person = (person[re.search(r'[А-ЯЁ][а-я]+', person).end():]).strip()
        list_.append((re.findall(r'^([А-ЯЁа-яё]+)', person)))
        person = (person[re.search(r'[А-ЯЁа-я]+', person).end():]).strip()
        person = re.sub(
            r'([8|\+7]+\s*)\(?(\d{3})\)?[-\s]?(\d{3})-?(\d{2})-?(\d{2})\s*\(?(доб\.)?\s?(('
            r'?<=доб\.\s)\d+)?', r'+7(\2)\3-\4-\5 \6\7', person)
        list_.append(
            (re.findall(
                r'(\+7\(\d{3}\)\d{3}-\d\d-\d\d(?:\sдоб\.\d+)?)',
                person)))
        person = (
            re.sub(
                r'\+7\(\d{3}\)\d{3}-\d\d-\d\d(?:\sдоб\.\d+)?',
                '',
                person)).strip()
        list_.append((re.findall(r'\w*\.?\w+@\w+\.\w{2,3}', person)))
        person = (re.sub(r'[\.\w]+@\w+\.\w{2,3}', '', person)).strip()
        list_.append(
            (re.findall(
                r'(\b[а-яёa-z][а-я]+.*[А-ЯЁа-яё][а-я]+)',
                person)))
        contact_list_three.append(list_)
    return contact_list_three


def edit_contact_list(text):
    '''Корректирую список, переставляю местами нужные элементы и добавляю в пустые строки запись об отсутствии данных.'''
    contact_list_four = []
    for num, el in enumerate(text):
        el[-1], el[-2] = el[-2], el[-1]
        el[4], el[5] = el[5], el[4]
        contact_list_four.append(el)
        for num_, el_ in enumerate(el):
            if len(el_) == 0:
                text[num][num_] = ['нет данных']
    return contact_list_four


def end_edit(text):
    '''Добавляем оглавление и разглаживаем список.'''
    contact_list_end = []
    for i in text:
        contact_list_end.append(sum(i, []))
    contact_list_end.insert(0, contacts_one[0])
    return contact_list_end


if __name__ == '__main__':
    contacts_one = get_csv()
    contact_list_two = find_copy(contacts_one)
    contact_list_three = gradation(contact_list_two)
    contact_list_four = edit_contact_list(contact_list_three)
    contact_list_end = end_edit(contact_list_four)

    with open("phonebook_1.csv", "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')

        datawriter.writerows(contact_list_end)
