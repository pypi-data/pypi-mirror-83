class TimeSeriesInstance:
    def __init__(self, client, series_type, series_id, series_name, series_description):
        """
        Time Series Instance object
        """
        self.__client = client
        self.series_type = series_type
        self.series_id = series_id
        self.series_name = series_name
        self.series_description = series_description

    def delete(self):
        """
        Delete this Time Series Instance

        Returns:
            The deserialized server response, if any
        """
        return self.__client._instances_api.delete_instances_by_id([self.series_id])

    def __repr__(self):
        if len(self.series_id) == 1:
            return f'<Time Series Instance with ID {self.series_id} ' \
                   f'({self.series_description}) of type ' \
                   f'`{self.series_type.type_name}`>'
        else:
            return f'<Time Series Instance with IDs {self.series_id} ' \
                   f'({self.series_description}) of type ' \
                   f'`{self.series_type.type_name}`>'
