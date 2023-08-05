from riemann.encoding.addresses import make_p2wpkh_address

def point_to_pubkey(x, y, compressed):
    if compressed:
        int_y = int.from_bytes(y, 'big')
        if int_y & 1:  # odd root
            return b'\x03' + x.rjust(32, b'\x00')
        else:           # even root
            return b'\x02' + x.rjust(32, b'\x00')
    else:
        return b'\x04' + x.rjust(32, b'\x00') + y.rjust(32, b'\x00')


def point_to_p2wpkh_address(x, y):
    return make_p2wpkh_address(point_to_pubkey(x, y, True))