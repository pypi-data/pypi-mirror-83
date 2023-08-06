# Bosta Python SDK

This repository contains the open source Python SDK for integrating Bosta's APIs into your Python application.

# Table of Contents

- [APIs Documentation](# apis-documentation)
- [Installation](#installation)
- [Usages](#usages)
- [Contribution](#contribution)
- [License](#license)

# APIs Documentation

- [Staging](https://stg-app.bosta.co/docs) APIs swagger documentation.
- [Production](https://app.bosta.co/docs) APIs swagger documentation.

# Installation

You can install the package via [pip](https://pypi.org/project/pip/). Run the following command:

```bash
pip install bostaSDK
```

# Usage

    ``` python
    import os

    from bostaSDK.apiClient import ApiClient
    from bostaSDK.delivery import list, create, update, track, printAWB, get, terminate
    from bostaSDK.pickup import create, list, get, update, delete
    from bostaSDK.utils import Receiver, Address, ContactPerson


    apiKey=os.environ["BOSTA-API-KEY"]="your api key"
    baseUrl=os.environ["BOSTA-BASE-URL"]="bosta base url"

    apiClient=ApiClient(apiKey, baseUrl)

    # List Deliveries
    apiClient.delivery.listAll(list.ListAllDeliveriesRequest(3, 10))

    # Create new delivery
    reciever=Receiver(
    "firstName",
    "lastName",
    "test@example.com",
     "01090055000")
    dropOffAddress=Address("EG-01", "Maadi", "Maadi", "104")
    createDeliveryReq=create.CreateDeliveryRequest(
        deliveryTypes['SEND']['code'], 100, dropOffAddress, reciever
    )
    deliveryId=apiClient.delivery.create(createDeliveryReq)

    # Print Airway Bill
    apiClient.delivery.printAirWayBill(printAWB.PrintAWBRequest([deliveryId]))

    # Track Delivery
    apiClient.delivery.track(track.TrackDeliveryRequest(deliveryId))

    # Get Delivery
    apiClient.delivery.get(get.GetDeliveryDetailsRequest(deliveryId))

    # Update Delivery
    newReciever=Receiver("user", "test", "test@example.com", "01090055000")
    apiClient.delivery.update(
    update.UpdateDeliveryRequest(
        deliveryId,
        receiver=newReciever,
         cod=120))

    # Terminate Delivery
    apiClient.delivery.terminate(
    terminate.TerminateDeliveryRequest(deliveryId))

    # Create New Pickup
    newPickupId=apiClient.pickup.create(
        create.CreatePickupRequest(
        "Mon Nov 7 2021 00:00:00 GMT+0200", apiClient.pickupTimeSlots[0],
        ContactPerson("userName", "01090000000", "example@bosta.co")
        )
    )

    # List Pickups
    apiClient.pickup.listAll(list.ListAllPickupsRequest(2))

    # Get Pickup
    apiClient.pickup.get(
        get.GetPickupDetailsRequest(newPickupId)
    )

    # Update Pickup
    apiClient.pickup.update(update.UpdatePickupRequest(
        newPickupId, contactPerson=ContactPerson(
    "newUser", "010193155922", "user2@bosta.co")
    ))

    # Delete Pickup
    apiClient.pickup.delete(delete.DeletePickupRequest(newPickupId))

    ```

## Contribution

We are open to, and grateful for, any contributions made by the community.
By contributing to Bosta, you agree to abide by the code of conduct.
- [Contributing Guide](CONTRIBUTING.md) 
- [Code of Conduct](CODE_OF_CONDUCT.md)

## License

The MIT License (MIT) [License](LICENSE).
