def int_to_binary_array(number, num_bits):  # Int to Binary Table
    binary_array = []
    minus = False

    if number < 0:
        minus = True
        number = abs(number)

    for _ in range(num_bits):
        binary_array.insert(0, number & 1)
        number = number >> 1

    if minus:
        carry = 1
        for i in range(len(binary_array) - 1, -1, -1):
            bit = binary_array[i] ^ 1  # invert the bit
            binary_array[i] = bit ^ carry
            carry = bit & carry

    return binary_array


def binary_array_to_int(bit_array):  # Binary table to Int
    decimal_value = 0
    for bit in bit_array:
        decimal_value = (decimal_value << 1) | bit
    return decimal_value


def preprocessing(n, a, b, k):  # Preprocessing stage
    g_0 = [0] * n  # G_0[i]
    p_0 = [0] * n  # P_0[i]
    h_0 = [0] * n  # H_0[i]

    a_prime = [0] * n  # A'[i]
    b_prime = [0] * (n + 1)  # B'[i+1]

    g_prime = [0] * n  # G'[i]
    p_prime = [0] * n  # P'[i]
    h_prime = [0] * n  # H'[i]

    k_bin = int_to_binary_array(k, n)  # Converting K from int to binary
    k_bin[0] = 0  # Last bit of K is always 0

    b_prime[n] = 0  # First bit o B' is always 0

    for i in range(n):  # Creating vectors: G, P, H, A', B'

        g_0[i] = a[i] and b[i]  # G[i] = A[i] and B[i]
        p_0[i] = a[i] or b[i]  # P[i] = A[i] or B[i]
        h_0[i] = not (g_0[i]) and p_0[i]  # H[i] = not(G[i]) and P[i]

        if k_bin[i]:  # Case for K[i] = 1

            a_prime[i] = not (a[i] ^ b[i])  # A'[i] = not(A[i] xor B[i])
            b_prime[i] = a[i] or b[i]  # B'[i] = A[i] or B[i]

        else:  # Case for K[i] = 0

            a_prime[i] = a[i] ^ b[i]  # A'[i] = A[i] xor B[i]
            b_prime[i] = a[i] & b[i]  # B'[i] = A[i] and B[i]

    for i in range(n):  # Additional loop for creating G', P', H' vectors
        g_prime[i] = a_prime[i] and b_prime[i + 1]  # G'[i] = A'[i] and B'[i-1]
        p_prime[i] = a_prime[i] or b_prime[i + 1]  # P'[i] = A'[i] or B'[i-1]
        h_prime[i] = a_prime[i] ^ b_prime[i + 1]  # H'[i] = A'[i] xor B'[i-1]

    return g_0, p_0, h_0, a_prime, b_prime, k_bin, g_prime, p_prime, h_prime


def parallel_prefix(n, g_0, p_0, g_prime, p_prime):  # Parallel-prefix stage
    g_out = [0] * n  # G_out vector tab
    p_out = [0] * n  # P_out vector tab

    g_prime_out = [0] * n  # G'_out vector tab
    p_prime_out = [0] * n  # P'_out vector tab

    for i in range(0, n):  # Copying G, P, G', P' values to G_out, P_out, G'_out, P'_out tabs

        g_out[i] = g_0[i]
        p_out[i] = p_0[i]

        g_prime_out[i] = g_prime[i]
        p_prime_out[i] = p_prime[i]

    white_cells = 0  # Counting buffers
    black_cells = 0  # Counting black-node operators
    counter = 0  # Counting number of computed bn. operators

    p = 0

    while (2 ** p) < n:  # Computing number of layers
        p = p + 1

    for i in range(0, p):  # Parallel-prefix loop

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

    c_out = not (g_out[0] or g_prime_out[0])  # C_out = ~(G[0] or G'[0])

    return g_out, p_out, g_prime_out, c_out


def multiplexing(n, c_out, h_0, h_prime, g_out, g_prime_out):  # Multiplexing stage
    h_multi = [0] * n  # H_multi vector tab
    g_multi = [0] * n  # G_multi vector tab

    for i in range(0, (n - 1)):  # Multiplexing G, H vectors for range from 0 to n-1

        if c_out:  # Case for C_out = 1

            h_multi[i] = h_0[i]
            g_multi[i] = g_out[i + 1]

        else:  # Case for C_out = 0

            h_multi[i] = h_prime[i]
            g_multi[i] = g_prime_out[i + 1]

    h_multi[n - 1] = 0  # First bit of multiplexed vector H is always 0

    # Multiplexing first bit of vectors basing on C_out
    if c_out:

        g_multi[n - 1] = h_0[n - 1]

    else:

        g_multi[n - 1] = h_prime[n - 1]

    return h_multi, g_multi


def sum_computation(n, h_multi, g_multi):  # Sum computation stage
    s = [0] * n  # Creating S vector for computing sum

    for i in range(n):  # Sum computing loop
        s[i] = h_multi[i] ^ g_multi[i]  # S[i] = H_multi[i] xor G_multi[i]

    return s


def modulo_adder(n, a, b, k, minus):  # (A+B) mod (2^n  - K) adder
    # Adding one more bit to n value if the number is below 0
    if minus:
        n = n + 1

    # Converting DEC to BIN
    a_bin = int_to_binary_array(a, n)
    b_bin = int_to_binary_array(b, n)

    # Preprocessing stage
    g_0, p_0, h_0, a_prime, b_prime, k_bin, g_prime, p_prime, h_prime = preprocessing(n, a_bin, b_bin, k)

    # Parallel-prefix stage
    g_out, p_out, g_prime_out, c_out = parallel_prefix(n, g_0, p_0, g_prime, p_prime)

    # Multiplexing stage
    h_multi, g_multi = multiplexing(n, c_out, h_0, h_prime, g_out, g_prime_out)

    # Sum computation stage
    s = sum_computation(n, h_multi, g_multi)

    return s


# Example using for modulo 2^n - K
A = 79  # A < 2^n - 1
B = 85  # B < 2^n - 1
n = 7  # N >= 4
K =37  # 3 <= K <= 2^(n-1) - 1

#  Testing algorithm for selected A, B, n and K
result = modulo_adder(n, A, B, K, False)
print("Sum for (", A, " + ", B, ") mod(", ((2**n)-K), ") : ", binary_array_to_int(result))  # Example of (A+B) mod (
# 2^n - K)
print("Binary : ", result)
print()

# Example using for modulo 2^n + K
A = 160  # A < 2^n - 1
B = 85  # B < 2^n - 1
n = 7  # N >= 4
K =-37  # 3 <= K <= 2^(n-1) - 1 !!! K has to containt '-' before number !!!
result = modulo_adder(n, A, B, K, True)
print("Sum for (", A, " + ", B, ") mod(", ((2**n)-K), ") : ", binary_array_to_int(result))  # Example of (A+B) mod (
# 2^n + K)
print("Binary : ", result)

