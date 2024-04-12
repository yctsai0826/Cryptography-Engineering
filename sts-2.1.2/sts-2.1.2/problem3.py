import random

print('')
random.seed(12345)
print([random.random() for _ in range(5)])

random.seed(12345)
print([random.random() for _ in range(5)])
