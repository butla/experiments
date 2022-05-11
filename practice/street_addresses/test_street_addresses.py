import pytest

from street_addresses import extract_parts


@pytest.mark.parametrize('address_string, address_dict', [
    ('Winterallee 3', {'Winterallee', '3'}),
    ('Musterstrasse 45', {'Musterstrasse', '45'}),
    ('Blaufeldweg 123B', {'Blaufeldweg', '123B'}),
    ('Am Bächle 23', {'Am Bächle', '23'}),
    ('Auf der Vogelwiese 23 b', {'Auf der Vogelwiese', '23 b'}),
    ('4, rue de la revolution', {'rue de la revolution', '4'}),
    ('200 Broadway Av', {'Broadway Av', '200'}),
    ('Calle Aduana, 29', {'Calle Aduana', '29'}),
    ('Calle 39 No 1540', {'Calle 39', 'No 1540'}),
    ('ul. 22 Stycznia 35', {'ul. 22 Stycznia', '35'}),
])
def test_extract_parts(address_string, address_dict):
    assert extract_parts(address_string) == address_dict


def test_extract_parts_without_number():
    with pytest.raises(ValueError):
        extract_parts('some address without a number')