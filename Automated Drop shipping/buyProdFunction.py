import hashlib
import requests

def buyProd(product_ids, quantities, address, payment_method, currency, app_key, app_secret, start_date="2022-01-01 00:00:00", end_date="2023-03-31 23:59:59"):
    # Set the API endpoint URL to retrieve orders within the specified date range
    order_list_url = "http://gw.api.alibaba.com/openapi/param2/2/portals.open/api.order.list"

    # Set the API request parameters to retrieve the latest order ID within the date range
    order_list_params = {
        "createStartTime": start_date,
        "createEndTime": end_date,
        "page": 1,
        "pageSize": 1,
        "orderStatus": "success"
    }

    # Sign the request with the app key and app secret
    order_list_sign_str = app_secret
    for k in sorted(order_list_params.keys()):
        order_list_sign_str += k + str(order_list_params[k])
    order_list_sign_str += app_secret

    # Encode the sign string as UTF-8 and calculate the MD5 hash
    order_list_sign = hashlib.md5(order_list_sign_str.encode("utf-8")).hexdigest()

    # Add the authentication parameters to the request to retrieve the latest order ID
    order_list_params.update({
        "app_key": app_key,
        "sign": order_list_sign
    })

    # Send the request to the AliExpress API endpoint to retrieve the latest order ID
    order_list_response = requests.post(order_list_url, data=order_list_params)

    # Check if the request was successful and retrieve the latest order ID
    if order_list_response.status_code == 200 and "orders" in order_list_response.json():
        order_id = order_list_response.json()["orders"][0]["orderId"]

        # Set the API endpoint URL to create a new order
        order_create_url = "http://gw.api.alibaba.com/openapi/param2/2/portals.open/api.order.create"

        # Set the API request parameters to create a new order
        order_create_params = {
            "orderId": order_id,
            "productIds": product_ids,
            "quantities": quantities,
            "address": address,
            "paymentMethod": payment_method,
            "currency": currency
        }

        # Sign the request with the app key and app secret
        order_create_sign_str = app_secret
        for k in sorted(order_create_params.keys()):
            order_create_sign_str += k + str(order_create_params[k])
        order_create_sign_str += app_secret

        # Encode the sign string as UTF-8 and calculate the MD5 hash
        order_create_sign = hashlib.md5(order_create_sign_str.encode("utf-8")).hexdigest()

        # Add the authentication parameters to the request to create a new order
        order_create_params.update({
            "app_key": app_key,
            "sign": order_create_sign
        })

        # Send the request to the AliExpress API endpoint to create a new order
        order_create_response = requests.post(order_create_url, data=order_create_params)

        # Check if the request was successful and return the API response
        if order_create_response.status_code == 200 and "success" in order_create_response.json():
            return order_create_response.json()["success"]
        else:
            return None
    else:
        return None
