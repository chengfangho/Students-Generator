import requests
import logging
from getpass import getpass


def authenticate(session):
    """
    Authenticates the user and returns the authentication token.
    """
    url = "https://vprovision.vcamera.net/user/login"
    email = input("Enter your email: ")
    password = getpass("Enter your password: ")
    org_short_name = input("Enter your organization short name: ")

    payload = {"email": email, "password": password, "orgShortName": org_short_name}

    try:
        with session.post(url, json=payload) as login:
            login.raise_for_status()

            response = login.json()
            user_token = response.get("userToken")

            if not user_token:
                logging.error("Error: 'userToken' is missing in the response.")
                return None

            return user_token

    except requests.HTTPError as e:
        handle_http_error(login, e)

    except Exception as e:
        logging.error(f"Error: {e}")
        return None


def handle_http_error(response, error):
    """
    Handles HTTP errors and logs appropriate messages.
    """
    status_code = response.status_code

    if status_code == 400:
        error_message = response.json().get("message", "Invalid request")
        logging.error(f"Error {status_code}: {error_message}")

    elif status_code == 403:
        logging.error(
            "Authentication Error 403: Unauthorized - wrong email, password, or orgShortName"
        )

    else:
        logging.error(f"Error {status_code}: {response.text}")


def get_init(session):
    try:
        data = session.get(
            "https://vcerberus.command.verkada.com/user/photos/fb033db9-28d9-4359-bd08-bef451125e99/2d3e65d7-62e1-439f-bf76-f9585e5f9482/128.jpg"
        ).content
        with open("output_image.jpg", "wb") as image_file:
            image_file.write(data)
        if not data:
            raise ValueError("No Data in Init...")
        return data
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
    except ValueError as e:
        print(f"Error with the response: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


def main():
    session = requests.Session()
    # Set up logging configuration
    logging.basicConfig(level=logging.INFO)

    # Create a session for making HTTP requests
    with requests.Session() as session:
        token = authenticate(session)

        if token:
            logging.info("Authentication successful. Token: %s", token)
            # Further actions using the obtained token
    session.headers.update(
        {"X-VERKADA-AUTH": token, "Content-Type": "application/json"}
    )
    init = get_init(session)
    print(init)


if __name__ == "__main__":
    main()
