import hashlib
import time
import matplotlib.pyplot as plt

# algorithm implementation with jaccard compare method for text files


def min_hashes_file(file_path, hash_functions_amount, chars_to_hash):
    """
    Calculates the minhash values for a file.

    :param file_path: The path to the file.
    :param hash_functions_amount: The number of hash functions to use.
    :param chars_to_hash: The number of characters to hash at a time.
    :return: The minhash values for the file.
    """
    min_hashes_values = [float('inf')] * hash_functions_amount

    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = file.read()

    for i in range(len(text_data) - chars_to_hash + 1):
        text_data_part = text_data[i:i+chars_to_hash]

        for j in range(hash_functions_amount):
            hash_value = int(hashlib.md5(str(j).encode('utf-8') + text_data_part.encode('utf-8')).hexdigest(), 16)
            min_hashes_values[j] = min(min_hashes_values[j], hash_value)

    return min_hashes_values


def jaccard_compare(minhash_values1, minhash_values2):
    """
    Calculates the Jaccard similarity between two sets of minhash values.

    :param minhash_values1: The first set of minhash values.
    :param minhash_values2: The second set of minhash values.
    :return: The Jaccard similarity between the two sets.
    """
    len_intersect = len(set(minhash_values1).intersection(set(minhash_values2)))
    len_union = len(set(minhash_values1)) + len(set(minhash_values2)) - len_intersect

    return float(len_intersect) / float(len_union)


# comparing two texts

print("Please wait, calculating...")

hash_functions_amount = 200
chars_to_hash = 20

start_test = time.time()
sienkiewicz_1 = min_hashes_file("Sienkiewicz_1.txt", hash_functions_amount, chars_to_hash)
sienkiewicz_2 = min_hashes_file("Sienkiewicz_2.txt", hash_functions_amount, chars_to_hash)
print(f"Sienkiewicz 1 and 2: {jaccard_compare(sienkiewicz_1, sienkiewicz_2):.5f}")
end_test = time.time()
print(f"Runtime: {end_test - start_test:.2f} [s]")

start_test = time.time()
sienkiewicz_1_cp = min_hashes_file("Sienkiewicz_1.txt", hash_functions_amount, chars_to_hash)
prus_1 = min_hashes_file("Prus_1.txt", hash_functions_amount, chars_to_hash)
print(f"Sienkiewicz 1 and Prus 1: {jaccard_compare(sienkiewicz_1_cp, prus_1):.5f}")
end_test = time.time()
print(f"Runtime: {end_test - start_test:.2f} [s]")

# testing amount of hashing functions and characters to be hashed

jaccard_compare_results = []
chars_to_hash_values = [10, 20, 40]
hash_functions_amount_values = [100, 200]
labels = ["10/100", "10/200", "20/100", "20/200", "40/100", "40/200"]

for chars_to_hash in chars_to_hash_values:
    for hash_functions_amount in hash_functions_amount_values:
        sienkiewicz_1_cp = min_hashes_file("Sienkiewicz_1.txt", hash_functions_amount, chars_to_hash)
        prus_1 = min_hashes_file("Prus_1.txt", hash_functions_amount, chars_to_hash)
        jaccard_compare_results.append(jaccard_compare(sienkiewicz_1_cp, prus_1))


x = range(len(jaccard_compare_results))
width = 0.5

fig, axis_x = plt.subplots()
rects = axis_x.bar(x, jaccard_compare_results, width)

axis_x.set_xlabel('Number of characters to be hashed/hashing functions')
axis_x.set_ylabel('Result of comparison')
axis_x.set_title('Comparison of results (Sienkiewicz_1 and Prus_1) for different parameters')

axis_x.set_xticks(x)
axis_x.set_xticklabels(labels)

axis_x.tick_params(axis='x', pad=10)

for rect in rects:
    height = rect.get_height()
    axis_x.annotate("{:.5f}".format(height), xy=(rect.get_x() + rect.get_width() / 2, height))

plt.show()
