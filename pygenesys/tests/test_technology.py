from pygenesys import technology
test = technology.Technology('Chambana', 'Tech',
                             'Label', 'Units',
                             'Input', 7,
                             'Output', 7, 7,
                             7, 7, 7)


def test_attributes():
    exp = ['Chambana', 'Tech', 'Label',
           'Units', 'Input', 7, 'Output', 7,
           7, 7, 7, 7]
    obs = [test.region_name, test.technology_name,
           test.technology_label, test.capacity_units,
           test.input_commodity, test.efficiency,
           test.output_commodity,
           test.capacity_to_activity,
           test.capacity_factor, test.lifetime,
           test.lifetime_loan, test.existing_capacity]
    assert(exp == obs)

    return


def test_technology_placeholder_is_none():
    ret_value = technology.Technology.placeholder(test)

    assert(ret_value is None)

    return
