import secrets

# Generate 1 million bytes of cryptographically secure random numbers
random_bytes = secrets.token_bytes(1000000)

# If you need to save this to a file
with open("ran.bin", "wb") as file:
    file.write(random_bytes)
