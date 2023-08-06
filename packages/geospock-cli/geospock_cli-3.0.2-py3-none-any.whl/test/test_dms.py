import base64
import json
import http.client

from urllib.parse import urlparse


def parse_and_make_request(url: str, method: str, body: str, headers) -> dict:
    parsed_url = urlparse(url)
    response = make_request(parsed_url.netloc, parsed_url.path, parsed_url.query, method, body, headers,
                                          parsed_url.scheme == "https")
    return response


def make_request(endpoint: str, path: str, query: str, method: str, body: str, headers, ssl=True) -> dict:
    if ssl:
        conn = http.client.HTTPSConnection(endpoint)
    else:
        conn = http.client.HTTPConnection(endpoint)
    conn.request(method, path + (("?" + query) if (query != "") else ""), body, headers)
    response = conn.getresponse()

    print(str(response.status) + ":", end='')

    if response.status >= 500:
        print("Could not communicate with the GeoSpock management service - error code {}"
                       .format(response.status))

    response_body = response.read().decode()

    if response_body == "Authentication Error":
        print(response_body)
    return response_body


def get_header(user: str, password: str) -> dict:
    basic_unencoded = user + ":" + password
    basic_encoded = base64.b64encode(basic_unencoded.encode("ascii"))
    basic_final = basic_encoded.decode('ascii')
    headers = {"content-type": "application/json", "authorization": "Basic %s" % basic_final}
    return headers


request_address = "http://localhost:8080/groups"
request = ""
header = get_header("user1", "user1Pass")

response = parse_and_make_request(request_address, "GET", json.dumps(request), header)
print(response)

response = parse_and_make_request(request_address + "/testGroup", "PUT", json.dumps(request), header)
print(response)

response = parse_and_make_request(request_address + "/testGroup", "PUT", json.dumps(request), header)
print(response)

response = parse_and_make_request(request_address + "/testGroup/users/testUser1", "PUT", json.dumps(request), header)
print(response)

response = parse_and_make_request(request_address + "/testGroup/users/testUser2", "PUT", json.dumps(request), header)
print(response)

response = parse_and_make_request(request_address, "GET", json.dumps(request), header)
print(response)

response = parse_and_make_request(request_address + "/testGroup/users/testUser2", "DELETE", json.dumps(request), header)
print(response)

response = parse_and_make_request(request_address, "GET", json.dumps(request), header)
print(response)

response = parse_and_make_request(request_address + "/testGroup", "DELETE", json.dumps(request), header)
print(response)
