# Convert Celsius to Fahrenheit and Vice-Versa

class Temperature:

	def toCelsius(fahrenheit):
		return (fahrenheit - 32) / 1.8

	def toFahrenheit(celsius):
		return (celsius * 1.8) + 32
