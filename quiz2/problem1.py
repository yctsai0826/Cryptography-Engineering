import hashlib
import time


def sha1_hash(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()


def crack_sha1_hash(hash_to_crack, password_list):
    attempts = 0
    start_time = time.time()

    with open(password_list, 'r') as file:
        for password in file:
            attempts += 1
            hashed_password = sha1_hash(password.strip())

            if hashed_password == hash_to_crack:
                time_taken = time.time() - start_time
                return (password.strip(), attempts, time_taken)

    return (None, attempts, time.time() - start_time)


def crack_sha1_hash_2(hash_to_crack, password_list):
    attempts = 0
    start_time = time.time()

    with open(password_list, 'r') as file:
        for password in file:
            attempts += 1
            hashed_password = sha1_hash((s_password+password).strip())

            if hashed_password == hash_to_crack:
                time_taken = time.time() - start_time
                return (password.strip(), attempts, time_taken)

    return (None, attempts, time.time() - start_time)



# Example usage:
hash_to_crack_a = 'ef0ebbb77298e1fbd81f756a4efc35b977c93dae'
hash_to_crack_b = '0bc2f4f2e1f8944866c2e952a5b59acabd1cebf2'
hash_to_crack_c = '9d6b628c1f81b4795c0266c0f12123c1e09a7ad3'
salt = 'dfc3e4f0b9b5fb047e9be9fb89016f290d2abb06'
password_list_file = './password.txt'

password_a, attempts, time_taken = crack_sha1_hash(hash_to_crack_a, password_list_file)

if password_a:
    print(
        f'Hash: {hash_to_crack_a}\nPassword: {password_a}\nTook {attempts} attempts to crack input hash. Time Taken: {time_taken}')
else:
    print(f'Failed to crack hash after {attempts} attempts.')
print("")


password_b, attempts, time_taken = crack_sha1_hash(hash_to_crack_b, password_list_file)

if password_b:
    print(
        f'Hash: {hash_to_crack_b}\nPassword: {password_b}\nTook {attempts} attempts to crack input hash. Time Taken: {time_taken}')
else:
    print(f'Failed to crack hash after {attempts} attempts.')
print("")


s_password, s_attempts, s_time_taken = crack_sha1_hash(salt, password_list_file)
password, attempts, time_taken = crack_sha1_hash_2(hash_to_crack_c, password_list_file)

if password:
    print(
        f'Hash: {hash_to_crack_c}\nPassword: {s_password + password}\nTook {attempts} attempts to crack input hash. Time Taken: {time_taken}')
else:
    print(f'Failed to crack hash after {attempts} attempts.')
print("")
