class Type:
    def __init__(self, type_id, type_name, type_description, type_vars):
        """
        Class storing Time Series type data
        """
        self.type_id = type_id
        self.type_name = type_name
        self.type_description = type_description
        self.type_vars = type_vars

    def __repr__(self):
        return f'<Time Series Type {self.type_name} with ID {self.type_id}>'
