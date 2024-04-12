import hashlib
import time

# List of hash functions to be tested
hash_functions = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha224': hashlib.sha224,
    'sha256': hashlib.sha256,
    'sha512': hashlib.sha512,
    'sha3_224': hashlib.sha3_224,
    'sha3_256': hashlib.sha3_256,
    'sha3_512': hashlib.sha3_512,
}

def calculate_hash(hash_function, file_path):
    hasher = hash_function()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def time_hash_function(hash_function, file_path):
    start_time = time.time()
    hash_value = calculate_hash(hash_function, file_path)
    duration = time.time() - start_time
    return hash_value, duration

def compare_hash_speeds(file_path):
    times = {}
    for name, function in hash_functions.items():
        hash_value, duration = time_hash_function(function, file_path)
        times[name] = duration
        print(f"{name} hash: {hash_value}\nTime taken: {duration} seconds\n")
    return times

# Example usage:
file_path = './video.mp4'
times = compare_hash_speeds(file_path)

# To rank the hash functions by speed
sorted_times = sorted(times.items(), key=lambda kv: kv[1])
print("Ranking of hash functions by speed:")
for rank, (name, time_taken) in enumerate(sorted_times, start=1):
    print(f"{rank}. {name}: {time_taken} seconds")
