class Temperature:
    def __init__(self, celsius: float = 0.0):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """Return temperature in Fahrenheit (from Celsius)."""
        return self._celsius * 9.0 / 5.0 + 32.0

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        """Set temperature by Fahrenheit value. Raises for below absolute zero."""
        celsius_value = (value - 32.0) * 5.0 / 9.0
        if celsius_value < -273.15:
            raise ValueError("Temperature below absolute zero is not allowed")
        self._celsius = celsius_value


if __name__ == '__main__':
    t = Temperature()
    t.celsius = 20
    print("Celsius:", t.celsius)
    print("Fahrenheit:", t.fahrenheit)
    # set via fahrenheit
    t.fahrenheit = 212
    print("After setting Fahrenheit to 212 -> Celsius:", t.celsius)
