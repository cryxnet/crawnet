class Model:
    def get_data(self):
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Model):
                if hasattr(value, 'get_data'):
                    data[key] = value.get_data()
                else:
                    data[key] = value.__dict__
            else:
                data[key] = value
        return data
