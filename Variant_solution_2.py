import csv
import re


def get_csv():
    '''Функция для преобразования файла csv в список.'''
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list_one = list(rows)
    return contacts_list_one


def find_copy(text):
    '''Функция для поиска одинаковых фамилий.'''
    contacts_set = set()
    contacts_list_two = []
    for one_keep in text:
        contacts_set.add(one_keep[0].split(' ')[0])

    for surname in contacts_set:
        no_copy_list = []

        for i in text:
            if surname == i[0].split(' ')[0]:
                no_copy_list.extend(i)
        contacts_list_two.append(no_copy_list)
    contacts_list_two = ([' '.join(i) for i in contacts_list_two])
    return contacts_list_two


def edit_phone(text):
    '''Функция для редактирования номеров телефонов.'''
    contact_list_three = []
    # print(text)
    for number in text:
        number_update = re.sub(
            r'([8|\+7]+\s*)\(?(\d{3})\)?[-\s]?(\d{3})-?(\d{2})-?(\d{2})\s*\(?(доб\.)?\s?(('
            r'?<=доб\.\s)\d+)?', r'+7(\2)\3-\4-\5 \6\7', number)
        contact_list_three.append(number_update)
    return contact_list_three


def edit_data(text):
    '''Функция для редактирования текста для файла csv.'''
    contact_list_four = []
    patt = (
        r'(^\w+)\s(\w+)\s(\w+)\s+(\w+)\s+([А-ЯЁа-я\s\–]+)?([a-z]+)?\s([\+\d\(\d+\)\-]+)?(\sдоб\.\d+)?\)?\s*[А-ЯЁа-яё]*\s*[А-ЯЁа-яё]*\s*[А-ЯЁа-яё]*\s*[А-ЯЁ]*(\w[а-яё]+)*\s?([a-z][А-ЯЁа-яё\s]+\b)?\s*(\w+\.)?(\w+@\w+\.\w+)?([a-z]+)?\s?([a-z]+$)?')
    change_patt = r'\1,\2,\3,\4,\5\6\10,\7\8\13,\11\12\14'
    for employee in text:
        edit_employee = (re.sub(patt, change_patt, employee)).split(',')
        if edit_employee[0] != 'lastname':
            contact_list_four.append(edit_employee)
        else:
            contact_list_four.insert(0, edit_employee)
    return contact_list_four


if __name__ == '__main__':
    contacts_list_one = get_csv()
    contact_list_two = find_copy(contacts_list_one)
    contact_list_three = edit_phone(contact_list_two)
    contact_list_four = edit_data(contact_list_three)

    with open("phonebook_2.csv", "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')

        datawriter.writerows(contact_list_four)
