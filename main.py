def calculate_bmi(height, weight):
  # Calculate the BMI value and return it
  bmi = weight / (height ** 2) * 703
  return bmi

def calculate_max_heart_rate(intensity, resting_hr, age):
  # Calculate the maximum heart rate using the Karvonen formula and return it
  max_hr = (((220 - age) - resting_hr) * intensity) + resting_hr
  return max_hr

# Prompt the user for their height and weight until they provide valid input
while True:
  try:
    height = float(input("Enter your height in inches: "))
    if height <= 0:
      print("Height must be a positive number.")
      continue
    break
  except ValueError:
    print("Invalid input. Please enter a valid number.")

while True:
  try:
    weight = float(input("Enter your weight in pounds: "))
    if weight <= 0:
      print("Weight must be a positive number.")
      continue
    break
  except ValueError:
    print("Invalid input. Please enter a valid number.")

# Calculate the BMI and print the result
bmi = calculate_bmi(height, weight)
print("Your BMI is", bmi)

# Prompt the user for their age, resting heart rate, and intensity level until they provide valid input
while True:
  try:
    age = int(input("Enter your age: "))
    if age <= 0:
      print("Age must be a positive number.")
      continue
    break
  except ValueError:
    print("Invalid input. Please enter a valid number.")

while True:
  try:
    resting_hr = int(input("Enter your resting heart rate: "))
    if resting_hr <= 0:
      print("Resting heart rate must be a positive number.")
      continue
    break
  except ValueError:
    print("Invalid input. Please enter a valid number.")

while True:
  try:
    intensity = float(input("Enter the intensity level (as a percentage): "))
    if intensity <= 0 or intensity > 100:
      print("Intensity must be a positive number between 0 and 100.")
      continue
    break
  except ValueError:
    print("Invalid input. Please enter a valid number.")

# Calculate the maximum heart rate and print the result
max_hr = calculate_max_heart_rate(intensity, resting_hr, age)
print("Your maximum heart rate at this intensity level is", max_hr)
