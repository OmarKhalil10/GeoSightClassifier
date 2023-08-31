import requests

# Open the image file
with open('uploads/uploaded_image.jpg', 'rb') as image_file:
    # Create a dictionary with the file as a tuple
    files = {'file': ('uploaded_image.jpg', image_file, 'image/jpeg')}
    
    # Send the POST request with the image file
    response = requests.post("http://localhost:8080/predict", files=files)

# Check the response status code
if response.status_code == 200:
    # Parse the JSON response if it's a successful response
    response_json = response.json()
    predictions = response_json.get('classes', [])
    print(predictions)
    max_prob = response_json.get('max_prob', 0)
    print(f"Max Probability: {max_prob}")
else:
    # Handle error response
    print(f"Error: {response.status_code}")
    print(response.text)  # This will contain the error message from the server
