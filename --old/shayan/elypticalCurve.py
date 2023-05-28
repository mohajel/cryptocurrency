class Point:
    generator_prime = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1

    @staticmethod
    def get_generator_point():
        generator_point_x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        generator_point_y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        return Point(generator_point_x, generator_point_y)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other): # Double and Add technique
        result = None
        adding_value = self
        for i in range(256):
            if other & (1 << i): # ith bit of "other"
                result = adding_value + result
                
            adding_value = adding_value + adding_value # twice as big
        return result

    def __add__(self, other): #from little fermat theorem x ** (p-2) % p = x^(-1) % p
        if other is None:
            return self
        if self == other: #point Doubling
            delta = pow(3*pow(self.x, 2, Point.generator_prime)*pow(2 * self.y, Point.generator_prime-2, Point.generator_prime), 1, Point.generator_prime)
            new_point_x = pow((pow(delta,2) - 2*self.x), 1, Point.generator_prime)
            new_point_y = pow((delta*(self.x - new_point_x) - self.y), 1, Point.generator_prime)
            return Point(new_point_x, new_point_y)
        else:
            delta = pow(other.x - self.x, Point.generator_prime - 2, Point.generator_prime) * (other.y - self.y) % Point.generator_prime
            new_point_x = pow((pow(delta,2) - self.x - other.x),1 ,Point.generator_prime)
            new_point_y = pow((delta*(self.x - new_point_x) - self.y),1 ,Point.generator_prime)
            return Point(new_point_x, new_point_y)

    def to_bytes(self):
        return b"\x04" + self.x.to_bytes(32, "big") + self.y.to_bytes(32, "big")

    def to_bytes_compressed(self):
        if self.y % 2 == 1:
           return b"\x03" + self.x.to_bytes(32, "big")
        else:
            return b"\x02" + self.x.to_bytes(32, "big")
