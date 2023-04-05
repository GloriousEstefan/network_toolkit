def is_ip_valid(ip_address):
    if not ip_address:
        print("No IP address provided")
        return False
    
    octet_list = ip_address.rstrip("\n").split('.')

    if len(octet_list) != 4:
        print(f"{ip_address} returned false during octet count check")
        return False

    first_octet = int(octet_list[0])
    if first_octet == 127 or (first_octet == 169 and int(octet_list[1]) == 254):
        print(f"{ip_address} returned false during loopback and apipa check")
        return False

    if not (1 <= first_octet <= 223):
        print(f"{ip_address} returned false during multicast check")
        return False
    
    for octet in octet_list:
        try:
            int(octet)

        except ValueError:
            print(f"{ip_address} returned false during octet integer check")
            return False

    return all(0 <= int(octet) <= 255 for octet in octet_list[1:])