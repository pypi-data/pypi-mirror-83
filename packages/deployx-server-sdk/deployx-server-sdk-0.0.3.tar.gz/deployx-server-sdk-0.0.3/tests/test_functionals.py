from . import *
import src as dxclient


# Все ок

# user пустой
# identifier капсом
# identifier = '' (пустой)
# поля больше 255 символов

# выключен redis
# точка не сохранена, нет подключения к сети
# точка сохранена, отключилась сеть

@pytest.mark.incremental
class TestNormalExperiment:

    def test_all_valid_data_and_point_enabled(self):
        user = {
            'unique_identifier': 'MYIDENTIFIER123',
            'username': 'captainkryuk',
            'first_name': 'andrey',
            'email': 'bestrongwb@gmail.com',
            'last_name': 'kryukov'  
        }

        dxclient.set_sdk_key("6ee4189e763c2742465eaa90294f6e3f19b2f91258d084f88905c3135486e6c8")

        feature = dxclient.get('test', user, False)

        assert feature == True

    def test_caps_user_and_point_disabled(self):
        user = {
            'UNIQUE_IDENTIFIER': 'TEST'
        }

        dxclient.set_sdk_key("6ee4189e763c2742465eaa90294f6e3f19b2f91258d084f88905c3135486e6c8")

        feature = dxclient.get('test', user, False)

        assert feature == True

    def test_blank_dict_user_and_point_enabled(self):
        """ 
        * should create user with unique_identifier == '-' 
        * if user already created just get point from redis
        """

        user = {}

        dxclient.set_sdk_key("6ee4189e763c2742465eaa90294f6e3f19b2f91258d084f88905c3135486e6c8")

        feature = dxclient.get('test', user, False)

        assert feature == True

    def test_blank_identifier_user_and_point_enabled(self):
        """ 
        * should create user with unique_identifier == '-' 
        * if user already created just get point from redis
        """
        user = {
            'UNIQUE_IDENTIFIER': ''
        }

        dxclient.set_sdk_key("6ee4189e763c2742465eaa90294f6e3f19b2f91258d084f88905c3135486e6c8")

        feature = dxclient.get('test', user, False)

        assert feature == True

    def test_all_blank_user_and_point_enabled(self):
        user = {
            'unique_identifier': '',
            'username': '',
            'first_name': '',
            'email': '',
            'last_name': ''          
        }

        dxclient.set_sdk_key("6ee4189e763c2742465eaa90294f6e3f19b2f91258d084f88905c3135486e6c8")

        feature = dxclient.get('test', user, False)

        assert feature == True

    def test_blank_identifire_fill_user_and_point_enabled(self):
        user = {
            'unique_identifier': '',
            'username': 'username',
            'first_name': 'andrey',
            'email': 'bestrongwb@gmail.com',
            'last_name': 'kryukov'          
        }

        dxclient.set_sdk_key("6ee4189e763c2742465eaa90294f6e3f19b2f91258d084f88905c3135486e6c8")

        feature = dxclient.get('test', user, False)

        assert feature == True