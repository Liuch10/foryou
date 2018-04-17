import ipfsapi


def cache(hash, host="127.0.0.1", port="5001"):
    client = ipfsapi.connect(host, port)
    # res = client.add('forms.py')
    return client.pin_add(hash)


def add(file, host="127.0.0.1", port="5001"):
    client = ipfsapi.connect(host, port)
    return client.add(file)  # {'hash':,'name':}
