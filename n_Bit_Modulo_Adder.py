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


def preprocessing(n, a, b, k):
    g_0 = [0] * n  # G_0[i]
    p_0 = [0] * n  # P_0[i]
    h_0 = [0] * n  # H_0[i]

    a_prime = [0] * n  # A'[i]
    b_prime = [0] * (n + 1)  # B'[i+1]

    g_prime = [0] * n  # G'[i]
    p_prime = [0] * n  # P'[i]
    h_prime = [0] * n  # H'[i]

    k_bin = int_to_binary_array(k, n)
    k_bin[0] = 0  # Last bit of K is always 0

    b_prime[n] = 0  # First bit o B' is always 0

    for i in range(0, n):  # Creating vectors: G, P, H, A', B'

        g_0[i] = a[i] and b[i]
        p_0[i] = a[i] or b[i]
        h_0[i] = not (g_0[i]) and p_0[i]

        if k_bin[i]:

            a_prime[i] = not (a[i] ^ b[i])
            b_prime[i] = a[i] or b[i]

        else:

            a_prime[i] = a[i] ^ b[i]
            b_prime[i] = a[i] and b[i]

        g_prime[i] = a_prime[i] and b_prime[i + 1]
        p_prime[i] = a_prime[i] or b_prime[i + 1]
        h_prime[i] = a_prime[i] ^ b_prime[i + 1]

    return g_0, p_0, h_0, a_prime, b_prime, k_bin, g_prime, p_prime, h_prime


def parallel_prefix(n, a_prime, b_prime, g_0, p_0, h_0, g_prime, p_prime, h_prime):
    g_out = [0] * n  # G_out vector tab
    p_out = [0] * n  # P_out vector tab

    g_prime_out = [0] * n  # G'_out vector tab
    p_prime_out = [0] * n  # P'_out vector tab

    for i in range(0, n):  # Copying G, P, G', P' values to G_out, P_out, G'_out, P'_out tabs

        g_out[i] = g_0[i]
        p_out[i] = p_0[i]

        g_prime_out[i] = g_prime[i]
        p_prime_out[i] = p_prime[i]

    white_cells = 0
    black_cells = 0
    counter = 0

    p = 0

    while (2 ** p) < n:  # Computing number of layers
        p = p + 1

    for i in range(0, p):

        for j in range((n - 1), -1, -1):

            if white_cells >= (2 ** i):

                if black_cells < (2 ** i):

                    g_out[j] = g_out[j] or (g_out[j + 1] and p_out[j])
                    g_prime_out[j] = g_prime_out[j] or (g_prime_out[j + 1] and p_prime_out[j])

                    if counter < (2 ** i):
                        p_out[j] = p_out[j] and p_out[j + 1]
                        p_prime_out[j] = p_prime_out[j] and p_prime_out[j + 1]

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

    c_out = not (g_out[0] or g_prime_out[0])

    return g_out, p_out, g_prime_out, c_out


def multiplexing(n, c_out, h_0, h_prime, g_out, g_prime_out):
    h_multi = [0] * n
    g_multi = [0] * n

    for i in range(0, (n - 1)):

        if c_out:

            h_multi[i] = h_0[i]
            g_multi[i] = g_out[i + 1]

        else:

            h_multi[i] = h_prime[i]
            g_multi[i] = g_prime_out[i + 1]

    h_multi[n - 1] = 0  # First bit of multiplexed vector H is always 0

    if c_out:

        g_multi[n - 1] = h_0[n-1]

    else:

        g_multi[i] = h_prime[n-1]


    return  h_multi, g_multi

def sum_computation(n, h_multi, g_multi):

    s = [0] * n

    for i in range(n):

        s[i] = h_multi[i] ^ g_multi[i]

    return s


def modulo_adder(n, a, b, k):
    # Converting DEC to BIN
    a_bin = int_to_binary_array(a, n)
    b_bin = int_to_binary_array(b, n)

    # Preprocessing stage
    g_0, p_0, h_0, a_prime, b_prime, k_bin, g_prime, p_prime, h_prime = preprocessing(n, a_bin, b_bin, k)

    # Parallel-prefix stage
    g_out, p_out, g_prime_out, c_out = parallel_prefix(n, a_prime, b_prime, g_0, p_0, h_0, g_prime, p_prime, h_prime)

    # Multiplexing stage
    h_multi, g_multi = multiplexing(n, c_out, h_0, h_prime, g_out, g_prime_out)

    # Sum computation stage
    s = sum_computation(n, h_multi, g_multi)

    return s


# Example numbers
A = 1  # A < 2^n - 1
B = 98  # B < 2^n - 1
n = 7
K = 5  # 3 <= K <= 2^(n-1) - 1

#result = modulo_adder(n, A, B, K)
#print("S : ", binary_array_to_int(result))  # Example of A+B
#print("S : ", result)

for i in range(0, (2 ** n)):
    for j in range(0, (2 ** n)):
        print(i, "+", j, "=", binary_array_to_int(modulo_adder(n, i, j, K)))
        if (i + j) != (binary_array_to_int(modulo_adder(n, i, j, K))):
            print("Error!")
