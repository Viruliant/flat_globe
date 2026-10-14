import numpy as np

arr_a = np.array([1, 2, 3])
arr_b = np.array([4, 5, 6])

# Element-wise addition
add_result = arr_a + arr_b
print("Addition:", add_result)

# Element-wise multiplication
mul_result = arr_a * arr_b
print("Multiplication:", mul_result)

# Scalar multiplication
scalar_mul = arr_a * 2
print("Scalar Multiplication:", scalar_mul)

# Dot product
dot_product = np.dot(arr_a, arr_b)
print("Dot Product:", dot_product)

# Sum of all elements
total_sum = np.sum(arr_a)
print("Total Sum:", total_sum)

# Mean of elements
mean_val = np.mean(arr_a)
print("Mean:", mean_val)
