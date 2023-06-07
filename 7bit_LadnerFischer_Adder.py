def int_to_binary_array(number, num_bits): # Int to Binary Table
    binary_array = []
    for _ in range(num_bits):
        binary_array.insert(0, number & 1)
        number = number >> 1

    return binary_array


def preprocessing(n, A, B):
    G_0 = [0] * n
    P_0 = [0] * n
    H_0 = [0] * n

    for i in range(n):
        G_0[i] = A[i] and B[i]
        P_0[i] = A[i] or B[i]
        H_0[i] = not(G_0[i]) and P_0[i]

    return G_0, P_0, H_0


def parallel_prefix(n, G_0, P_0):
    P_prime = [0] * n
    G_prime = [0] * n

    for i in range(n):
        P_prime[i] = P_0[i]
        G_prime[i] = G_0[i]

    white_cells = 0
    black_cells = 0
    counter = 0

    for i in range(0, 3):

        for j in range ((n-1), -1, -1):

            if white_cells >= (2**i):
                
                if black_cells < (2**i):

                    G_prime[j] = G_prime[j] or (G_prime[j+1] and P_prime[j])

                    if counter < (2**i):
                        P_prime[j] = P_prime[j] and P_prime[j+1]
                        counter = counter + 1

                    black_cells = black_cells + 1

                else:
                    white_cells = 0
                    black_cells = 0

            else:
                white_cells = white_cells + 1
            

            white_cells = 0
            black_cells = 0
            counter = 0

    
    return P_prime, G_prime


def  sum_computation(n, H_0, P_prime, G_prime):

    S = [0] * (n+1)

    S[n] = H_0[n-1]
    S[0] = G_prime[0]

    for i in range(1, n):
        S[i] = G_prime[i] ^ H_0[i-1]
        

    return S

def binary_adder(n, A, B):

    # Converting DEC to BIN
    A_bin = int_to_binary_array(A, n)
    B_bin = int_to_binary_array(B, n)

    # Preprocessing stage
    G_0, P_0, H_0 = preprocessing(7, A_bin, B_bin)

    # Parallel-prefix stage
    P_prime, G_prime = parallel_prefix(n, G_0, P_0)

    # Sum computation stage
    S = sum_computation(n, H_0, P_prime, G_prime)

    return S

A = 64
B = 64

print("S : ", binary_adder(7, A, B))


