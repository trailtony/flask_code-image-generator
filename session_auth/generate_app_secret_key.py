import secrets


def create_flask_secret_key():
    # .token_hex() method returns a hexadecimal string containing random numbers and letters from 0 to 9 and a to f
    secret_key = secrets.token_hex()
    return secret_key


if __name__ == "__main__":
    create_flask_secret_key()