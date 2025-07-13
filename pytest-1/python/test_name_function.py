from name_function import get_formatted_name

def test_first_last_name():
    """Do names like 'Ashraf Bateekha' work?"""
    formatted_name = get_formatted_name('ashraf', 'bateekha')
    assert formatted_name == "Ashraf Bateekha"

def test_first_last_middle_name():
    """Do names like 'Hamada Manga Farawla' work?"""
    formatted_name = get_formatted_name('hamada', 'farawla', 'manga')
    assert formatted_name == "Hamada Manga Farawla"

'''
# values ->> a & b
assert a == b
assert a != b
assert a
assert not a
assert a < b
assert item in collection
assert item not in collection
assert 2 in [1,2,3]
assert my_list == [1,2,3]
assert my_dict == {"name": "mahmoud"}


'''