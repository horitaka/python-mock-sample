from cgitb import text
import unittest
from unittest.mock import MagicMock, patch
from sample import main
import api
import requests_mock

class ResponseMock:
    def __init__(self, text):
        self.text = text

class TestSample(unittest.TestCase):
    def test_mock_called(self):
        # api.call_apiをmockにする
        mock = MagicMock()
        api.call_api = mock
        
        url = "https://example.com"
        main(url)

        # call_apiが、"https://example.com"の引数で呼ばれたことを検証する
        mock.assert_called_with("https://example.com")


    def test_mock_return_value(self):
        # call_apiをモック化して、戻り値をResponseMock("mocked_text")に設定する
        mock = MagicMock(return_value=ResponseMock("mocked_text"))
        api.call_api = mock

        url = "https://example.com"
        result = main(url)

        self.assertEqual(result, "mocked_text")


    def test_mock_side_effect(self):
        # argsにはcall_apiを呼び出したときの引数が入る
        # 引数によって戻り値を変える
        def mock_return_value(*args, **kwargs):
            if args[0] == "https://example.com":
                result = "mocked_text"
            else:
                result = "not_found_text"
            return ResponseMock(result)
        mock = MagicMock(side_effect=mock_return_value)
        api.call_api = mock

        # test1
        url = "https://example.com"
        result = main(url)

        self.assertEqual(result, "mocked_text")

        # test2
        url = "https://notfound.com"
        result = main(url)

        self.assertEqual(result, "not_found_text")


class TestSamplePatch(unittest.TestCase):
    def test_mock_patch(self):
        mock = MagicMock(return_value=ResponseMock("mocked_text"))
        with patch('api.call_api', mock):
            print(api.call_api)
            # output: <MagicMock id='xxxxxxxxxx'>
            url = "https://example.com"
            result = main(url)

            self.assertEqual(result, "mocked_text")

        print(api.call_api)
        # output: <function call_api at xxxxxxxxx>


    mock = MagicMock(return_value=ResponseMock("mocked_text"))
    @patch('api.call_api', mock)
    def test_mock_patch_decorator(self):
        url = "https://example.com"
        result = main(url)

        self.assertEqual(result, "mocked_text")


if __name__ == '__main__':
    unittest.main()