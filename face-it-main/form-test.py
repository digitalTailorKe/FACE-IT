import requests

url = "http://139.162.90.90/compare"

# Paths to the image files
known_image_path = "known_images/austin.jpeg"
compared_image_path = "compared_images/obama.jpg"

# Open the image files in binary mode
with open(known_image_path, 'rb') as known_image, open(compared_image_path, 'rb') as compared_image:
    files = {
        'known_image': known_image,
        'compared_image': compared_image,
    }
    
    # Send the POST request
    response = requests.post(url, files=files)
    
    # Print the response from the server
    print(response.text)
