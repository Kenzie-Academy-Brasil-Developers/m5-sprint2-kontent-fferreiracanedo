class ContentSerializer:
    valid_inputs = {
        "title": str,
        "module": str,
        "description": str,
        "students": int,
        "is_active": bool,
    }

    def __init__(self, *args, **kwargs):
        self.data = kwargs
        self.errors = {}

    def is_valid(self):

        self.clean_data()

        try:
            self.validate_required_keys()
            self.validate_data_types()

            return True
        except:
            return False

    def clean_data(self):

        data_keys = tuple(self.data.keys())

        for key in data_keys:
            if key not in self.valid_inputs.keys():
                self.data.pop(key)

    def validate_required_keys(self):
        for valid_key in self.valid_inputs.keys():
            if valid_key not in self.data.keys():
                self.errors[valid_key] = "missing key"

        if self.errors:
            return self.errors

    def validate_data_types(self):
        for valid_key, valid_type in self.valid_inputs.items():
            if type(self.data[valid_key]) is not valid_type:
                self.errors[valid_key] = f"wrong data type {valid_type.__name__}"

        if self.errors:
            return self.errors
