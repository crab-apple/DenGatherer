def common_entry_assertions(entries):
    assert len(entries) > 0
    for attribute in ['id', 'title', 'price', 'size', 'rooms', 'address']:
        assert_required_attribute(attribute, entries)


def common_expose_assertions(exposes):
    for attr in ['title', 'price', 'size', 'rooms', 'address', 'from']:
        assert_required_attribute(attr, exposes)


def assert_required_attribute(attribute, elements):
    assert all(map(lambda entry: attribute in entry and entry[attribute] is not None, elements)), \
        f'Attribute "{attribute}" not found'


def assert_common_attribute(attribute, elements):
    assert any(map(lambda entry: entry[attribute] is not None, elements)), \
        f'Attribute "{attribute}" not found in any entry'
