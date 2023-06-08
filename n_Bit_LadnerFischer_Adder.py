def int_to_binary_array(number, num_bits):  # Int to Binary Table
    binary_array = []
    for _ in range(num_bits):
        binary_array.insert(0, number & 1)
        number = number >> 1

    return binary_array


def binary_array_to_int(bit_array):
    decimal_value = 0
    for bit in bit_array:
        decimal_value = (decimal_value << 1) | bit
    return decimal_value


def preprocessing(n, a, b):
    g_0 = [0] * n
    p_0 = [0] * n
    h_0 = [0] * n

    for i in range(n):
        g_0[i] = a[i] and b[i]
        p_0[i] = a[i] or b[i]
        h_0[i] = not (g_0[i]) and p_0[i]

    return g_0, p_0, h_0


def parallel_prefix(n, g_0, p_0):
    p_prime = [0] * n
    g_prime = [0] * n

    for i in range(n):
        p_prime[i] = p_0[i]
        g_prime[i] = g_0[i]

    white_cells = 0
    black_cells = 0
    counter = 0

    k = 0

    while (2**k) < n:
        k = k + 1


    for i in range(0, k):

        for j in range((n - 1), -1, -1):

            if white_cells >= (2 ** i):

                if black_cells < (2 ** i):

                    g_prime[j] = g_prime[j] or (g_prime[j + 1] and p_prime[j])

                    if counter < (2 ** i):
                        p_prime[j] = p_prime[j] and p_prime[j + 1]
                        counter = counter + 1

                    black_cells = black_cells + 1

                else:
                    white_cells = 0
                    black_cells = 0

            else:
                white_cells = white_cells + 1

            if j == 0:
                white_cells = 0
                black_cells = 0
                counter = 0

    return g_prime


def sum_computation(n, h_0, g_prime):
    s = [0] * (n + 1)

    s[n] = h_0[n - 1]
    s[0] = g_prime[0]

    for i in range(1, n):
        s[i] = g_prime[i] ^ h_0[i - 1]

    return s


def binary_adder(n, a, b):
    # Converting DEC to BIN
    a_bin = int_to_binary_array(a, n)
    b_bin = int_to_binary_array(b, n)

    # Preprocessing stage
    g_0, p_0, h_0 = preprocessing(n, a_bin, b_bin)

    # Parallel-prefix stage
    g_prime = parallel_prefix(n, g_0, p_0)

    # Sum computation stage
    s = sum_computation(n, h_0, g_prime)

    return s


# Example numbers
A = 63
B = 21
n = 3
# print("S : ", binary_array_to_int(7, binary_adder(7, A, B))) # Example of A+B
# print("S : ", binary_adder(7, A, B))

for i in range(0, (2**n)):
    for j in range(0, (2**n)):
        print(i, "+", j, "=", binary_array_to_int(binary_adder(n, i, j)))
        if (i+j) != (binary_array_to_int(binary_adder(n, i, j))):
            print("Error!")
