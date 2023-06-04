def int_to_binary_array(number, num_bits):
    binary_array = []
    for _ in range(num_bits):
        binary_array.insert(0, number & 1)
        number = number >> 1

    return binary_array

def preprocessing_first_phase(n, A, B, K):
    H = [0] * n  # Half-sum vector
    P = [0] * n  # Carry-propagate vector
    G = [0] * n  # Carry-generate vector

    K[0] = 0

    for i in range(n):
        H[i] = A[i] ^ B[i]
        P[i] = A[i] | B[i]
        G[i] = A[i] & B[i]

    A_prim = [0] * n  # A' vector
    B_prim = [0] * (n + 1)  # B' vector

    B_prim[n] = 0

    for i in range(n):
        if K[i] == 0:
            A_prim[i] = A[i] ^ B[i]
            B_prim[i + 1] = A[i] & B[i]
        else:
            B_prim[i] = A[i] | B[i]
            if not (A[i] ^ B[i]):
                A_prim[i] = 1
            else:
                A_prim[i] = 0

    return K, H, P, G, A_prim, B_prim

def preprocessing_second_phase(n, A_prim, B_prim):
    H_prim = [0] * n  # H' vector
    P_prim = [0] * n  # P' vector
    G_prim = [0] * n  # G' vector

    for i in range(n):
        H_prim[i] = A_prim[i] ^ B_prim[i+1]
        P_prim[i] = A_prim[i] | B_prim[i+1]
        G_prim[i] = A_prim[i] & B_prim[i+1]

    return H_prim, P_prim, G_prim


def preprocessing(n, A, B, K):

    K, H, P, G, A_prim, B_prim = preprocessing_first_phase(n, A, B, K)
    H_prim, P_prim, G_prim = preprocessing_second_phase(n, A_prim, B_prim)

    return  K, H, P, G, A_prim, B_prim, H_prim, P_prim, G_prim

def parallel_prefix(n, P, G, P_prim, G_prim):
    C = [0] * n # Carry vector
    C_prim = [0] * n # C' vector

    for i in range(n):
        C[i] = P[i] & P_prim[i]
        C_prim[i] = G[i] | (G_prim[i] & P[i])

    return C, C_prim

def sum_computation(n, H, H_prim, C, C_prim):
    S = [0] * n

    C_out = C_prim[0]

    for i in range(n):
        if C_out == 0:
            S[i] = H[i] ^ C[i]
        else:
            S[i] = H_prim[i] ^ C_prim[i]

    return S


# Deklaracja zmiennych
n = 4 # Number of bits
A = int_to_binary_array(5, n) # A
B = int_to_binary_array(11, n) # B
K = int_to_binary_array(7, n) # K

K, H, P, G, A_prim, B_prim, H_prim, P_prim, G_prim = preprocessing(n, A, B, K)
C, C_prim = parallel_prefix(n, P, G, P_prim, G_prim)
S = sum_computation(n, H, H_prim, C, C_prim)

print("A", A)
print("B", B)
print("K", K)
print("H", H)
print("P", P)
print("G", G)
print("A'", A_prim)
print("B'", B_prim)
print("H'", H_prim)
print("P'", P_prim)
print("G'", G_prim)
print("C", C)
print("C'", C_prim)
print("S", S)