

def AES(plain, key):
    keys = keyExpansion(key)

    #round 0 add round key 0
    state0 = format( (int(plain, 2)^int(keys[0], 2)), "b")    
    matrix = [state0[0:4], state0[4:8], state0[8:12], state0[12:16]]
               

    #round 1 -> subnibbles -> shift row -> mix column -> add round key 1
    for i in range(0, len(matrix)):
        matrix[i] = subnibbles(matrix[i])

    shiftRow(matrix)
    
    mixColumns(matrix)
    
def mixColumns(matrix):
    E = ["0001", "0100", "0001", "0100"] #[1, x^2, 1, x^2]
    mixed = [ (int(E[0],2) * int(matrix[0],2) ^ int(E[1],2) * int(matrix[2],2)),
              (int(E[0],2) * int(matrix[1],2) ^ int(E[1],2) * int(matrix[3],2)),
               ]
    print(format(mixed[0], "b").zfill(4))
    print(format(mixed[1], "b").zfill(4))


def keyExpansion(key):
    '''
    key is a string of 16 bits
    '''
    keys = [key]

    #separte key into two words
    w0 = key[0:8]
    w1 = key[8:len(key)]

    #compute g(W1)
    gw1 = calcGwx(w1, 1)

    w2 = format( (int(w0, 2) ^ int(gw1, 2)) , "b").zfill(8) 

    w3 = format( (int(w2, 2) ^ int(w1, 2)), "b").zfill(8)

    #key1
    keys.append( (w2+w3) )
    
    #compute g(W3)
    gw3 = calcGwx(w3, 2)
    
    w4 = format( (int(w2, 2) ^ int(gw3, 2)), "b").zfill(8)
    w5 = format( (int(w4, 2) ^ int(w3, 2)), "b").zfill(8)

    #key2
    keys.append( (w4+w5) )

    return keys

def calcGwx(wordx, index):
    #swap the nibbles
    nibbles = [wordx[4:8], wordx[0:4]]
    
    nibbles[0] = subnibbles(nibbles[0])
    nibbles[1] = subnibbles(nibbles[1])
    #print(nibbles)
    

    if index >= 2:
        poly = 19%pow(2,(index+2)) 
        poly *= pow(2, (8-len(format(poly, "b").zfill(4))))
    else:
        poly = pow(2, (index+2))*pow(2, 4)
    
    
    #print(format(poly, "b"))
    xorsum = int((nibbles[0]+nibbles[1]), 2) ^ poly
    return format(xorsum, "b").zfill(8)

def subnibbles(nibble):
    sBox = {"0000":"1001", "0001":"0100", "0010":"1010", "0011":"1011", "0100":"1101", 
            "0101":"0001", "0110":"1000", "0111":"0101", "1000":"0110", "1001":"0010", 
            "1010":"0000", "1011":"0011", "1100":"1100", "1101":"1110", "1110":"1111", "1111":"0111"}
    return sBox[nibble]

def shiftRow(nibbles):
    temp = nibbles[1]
    nibbles[1] = nibbles[3]
    nibbles[3] = temp


if __name__ == "__main__":
    nibbles = ["1001", "0111", "1000", "1010"]
    print(f"nibbles before shift row {nibbles}")
    shiftRow(nibbles)
    print(f"nibbles after shift row {nibbles}")
    nib = "1101"
    print(f"Nibble sub for 1101 is {subnibbles(nib)}")

    print("Testing g(w1)\n")
    word = "11010000"
    gword = calcGwx(word, 1)
    print(f"g(W1) is {gword}")

    print("Testing g(w3)\n")
    word = "11100000"
    gword = calcGwx(word, 2)
    print(f"g(W3) is {gword}")

    #print(keyExpansion("0010111011010000"))

    #AES("1010110011010101", "0010111011010000")

    matrix = ["0110", "1001", "0001", "1010"]
    print("testing mixed column")
    mixColumns(matrix)