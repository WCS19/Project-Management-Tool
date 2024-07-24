import os
import binascii

# Generate a secret key for Flask app
flask_secret_key = binascii.hexlify(os.urandom(24)).decode()
print("FLASK_SECRET_KEY:", flask_secret_key)

# Generate a JWT secret key
jwt_secret_key = binascii.hexlify(os.urandom(24)).decode()
print("JWT_SECRET_KEY:", jwt_secret_key)