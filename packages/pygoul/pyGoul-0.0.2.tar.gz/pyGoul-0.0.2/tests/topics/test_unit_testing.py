#import pytest
import pytest, os
#from models.train import model_test
from ... import only_six_or_A, onlyHookersAndBlackJack, file_to_string
#@pytest.mark.skip
class TestOnlySixOrA(object):
    def test_with_a_five_int(self):
        test_arg = 5
        with pytest.raises(ValueError) as exc_info:
            only_six_or_A(test_arg)
        expected_error_msg ="Expect 6 or A, got 5"
        assert exc_info.match(expected_error_msg)

    def test_with_a_B_string(self):
        test_arg = "B"
        with pytest.raises(ValueError) as exc_info:
            only_six_or_A(test_arg)
        expected_error_msg ="Expect 6 or A, got B"
        assert exc_info.match(expected_error_msg)

    def test_with_a_A_string(self):
        test_arg = "A"
        result = only_six_or_A(test_arg)
        expected_value = True
        assert result==expected_value

#@pytest.mark.skip
#@pytest.mark.skipif(True)
# @pytest.mark.xfail(reason="“Using TDD, onlyHookersAndBlackJack() is not implemented")
# @pytest.mark.skipif(sys.version_info > (2, 7), reason="requires Python 2.7")
class TestOnlyHookersAndBlackJack(object):
    def test_onlyHookersAndBlackJack(self):
        test_arg = 5
        with pytest.raises(ValueError) as exc_info:
            onlyHookersAndBlackJack(test_arg)
        expected_error_msg ="Expect 21 but got 5"
        print(exc_info)
        assert exc_info.match(expected_error_msg)



# Add a decorator to make this function a fixture
@pytest.fixture
def a_fixture_file(tmpdir):
    file_path = tmpdir.join("fixture_file.txt")
    with open(file_path, "w") as f:
        f.write("A")
    yield file_path
    #don't have to remove file if tmpdir is used
    #os.remove(file_path)
    
# Pass the correct argument so that the test can use the fixture
def test_file_to_string(a_fixture_file):
    expected = "A"
    # Pass the clean data file path yielded by the fixture as the first argument
    actual = file_to_string(a_fixture_file)
    assert actual == expected, "Expected: {0}, Actual: {1}".format(expected, actual) 




# Define a function convert_to_int_bug_free
def convert_to_int_bug_free(comma_separated_integer_string):
    # Assign to the dictionary holding the correct return values 
    return_values = {"1,801": 1801, "201,411": 201411, "2,002": 2002, "333,209": 333209, "1990": None, "782,911": 782911, "1,285": 1285, "389129": None}
    # Return the correct result using the dictionary return_values
    return return_values[comma_separated_integer_string]

# Add the correct argument to use the mocking fixture in this test
@pytest.mark.xfail(reason="“Mocking test, not implemented yet")
def test_on_raw_data(self, raw_and_clean_data_file, mocker):
    raw_path, clean_path = raw_and_clean_data_file
    # Replace the dependency with the bug-free mock
    convert_to_int_mock = mocker.patch("data.preprocessing_helpers.convert_to_int",
                                    side_effect = convert_to_int_bug_free)
    preprocess(raw_path, clean_path)
    # Check if preprocess() called the dependency correctly
    assert convert_to_int_mock.call_args_list == [call("1,801"), call("201,411"),call("2,002"), call("333,209"),call("1990"), call("782,911"),call("1,285"), call("389129")]
    with open(clean_path, "r") as f:
        lines = f.readlines()
    first_line = lines[0]
    assert first_line == "1801\\t201411\\n"
    second_line = lines[1]
    assert second_line == "2002\\t333209\\n" 

import numpy as np
import pytest

@pytest.mark.xfail(reason="Model test, not implemented yet")
def test_on_perfect_fit():
    # Assign to a NumPy array containing a linear testing set
    test_argument = np.array([[1.0,3.0], [2.0,	5.0], [3.0,	7.0]])
    # Fill in with the expected value of r^2 in the case of perfect fit
    expected = 1.0
    # Fill in with the slope and intercept of the model
    actual = model_test(test_argument, slope=2, intercept=1)
    # Complete the assert statement
    assert actual == pytest.approx(expected), "Expected: {0}, Actual: {1}".format(expected, actual)


        # def test_onlyHookersAndBlackJack(self):
    #     test_arg = 21
    #     with pytest.raises(ValueError) as exc_info:
    #         result = onlyHookersAndBlackJack(test_arg)
    #         expected_error_msg ="Expect 21 but got {}".format(result)
    #         assert exc_info.match(expected_error_msg)
