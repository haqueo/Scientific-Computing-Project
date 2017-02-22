from solution_final import away_from_52

def test_away_from_52():
    assert  away_from_52([55,56]) == True
    assert away_from_52([23,12]) == True
    assert  away_from_52([4,1]) == True
    assert away_from_52([47,48]) == False
    assert away_from_52([45,46]) == False

