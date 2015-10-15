__author__ = 'dt'

class Ipv4Address:

    def __init__(self, address: str, mask: str="255.255.255.252"):
        """
        Initializes an Ipv4Address Object
        :param address: The IPv4 address
        :param mask: The subnet mask
        """
        self.__address = self.string_to_ip(address)
        self.__mask = self.string_to_ip(mask)

    @staticmethod
    def string_to_ip(address: str):
        l = address.split(sep='.')
        if len(l) != 4:
            raise ValueError("invalid address")

        result = 0
        for i, el in enumerate(l):
            if not (0 <= int(el) < 256):
                raise ValueError("invalid address")
            result |= (int(el) << 24 - 8*i)
        return result

    @staticmethod
    def ip_to_string(address: int):
        bytes = [
            (address & 0x000000FF),
            (address & 0x0000FF00) >> 8,
            (address & 0x00FF0000) >> 16,
            (address & 0xFF000000) >> 24,
        ]
        return "{3}.{2}.{1}.{0}".format(*bytes)

    @staticmethod
    def slash_to_snm(slash: int):
        if 8 <= slash < 31:
            return 0xFFFFFFFF ^ (1 << 32 - slash) - 1
        else:
            raise ValueError("slash must be in range(8, 31)")

    @staticmethod
    def slash_to_string(slash: int):
        return Ipv4Address.ip_to_string(Ipv4Address.slash_to_snm(slash))

    @staticmethod
    def snm_to_slash(snm: int):
        while snm & 1 == 0:
            snm >>= 1
        count = 0
        while snm & 1 == 1:
            count += 1
            snm >>= 1
        return count

    def __str__(self):
        return self.ip_to_string(self.__address) + "/{}".format(self.snm_to_slash(self.__mask))

    def net(self):
        return self.__address & self.__mask

    def netstr(self):
        return self.ip_to_string(self.net()) + "/{}".format(self.snm_to_slash(self.__mask))

    def broadcast(self):
        return self.__address | (~self.__mask & 0xFFFFFFFF)

    def broadcaststr(self):
        return self.ip_to_string(self.broadcast())

    def hostcount(self):
        return self.broadcast() - self.net() - 1
