import requests

# Define your API key
API_KEY = "YzkzZTkwY2U0NTBlNDFmOWFmNjA5MGJmMGRjMDg2YWUtMTc0MDgzMzk5Ng=="

# Set the API endpoint URL
API_URL = "https://api.heygen.com/v2/avatars"

# Set the headers, including the API key
headers = {
    "Content-Type": "application/json",
    "X-Api-Key": API_KEY
}

try:
    # Make the API request
    response = requests.get(API_URL, headers=headers)

    # Print full response for debugging
    print("\nFull API Response:")
    print(response.text)

    print("Full Response JSON:", response.json())  # Add this before checking "avatars"

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Check if avatars are present in the response
        
        if "avatars" in data and data["avatars"]:
            print("\nAvailable Avatars:")
            for avatar in data["avatars"]:
                print(f"Avatar ID: {avatar['avatar_id']}")
                print(f"Avatar Name: {avatar['avatar_name']}")
                print("----------------------------")
        else:
            print("No avatars found in the response.")

    else:
        print(f"Error: Unable to fetch avatars (Status Code: {response.status_code})")

except Exception as e:
    print(f"An error occurred: {e}")
