

class CreateDeliveryResponse:
    def __init__(self, jsonResponse):
        """
        Initialize new instance from CreateDeliveryResponse class

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        instance from CreateDeliveryResponse

        """
        self._id, self.trackingNumber, self.message = self.fromJSONPayload(
            jsonResponse)

    def fromJSONPayload(self, jsonResponse):
        """
        Extract _id, trackingNumber and message fields from json response object

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        _id (str): Delivery Id
        trackingNumber (str): Delivery trackingNumber
        message (str): Create delivery response message
        """
        _id = jsonResponse["_id"]
        trackingNumber = jsonResponse["trackingNumber"]
        message = jsonResponse["message"]

        return _id, trackingNumber, message

    def get_deliveryId(self):
        return self._id

    def get_trackingNumber(self):
        return self.trackingNumber

    def get_message(self):
        return self.message

    def __str__(self):
        return self._id
