from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image

# open the input image file and read the pixel data
input_image = Image.open("input.jpg")
pixels = input_image.load()

# get the image dimensions
width, height = input_image.size

# define the encryption key (must be 16, 24, or 32 bytes long)
key = b"mysecretpassword"

# create a new AES cipher object
cipher = AES.new(key, AES.MODE_CBC)

# encrypt each pixel in the image using the AES cipher
for x in range(width):
    for y in range(height):
        # extract the red, green, and blue values from the pixel
        r, g, b = pixels[x, y]

        # concatenate the RGB values into a single byte string
        plaintext = bytes([r, g, b])

        # pad the plaintext to a multiple of 16 bytes (the AES block size)
        padded_plaintext = pad(plaintext, AES.block_size)

        # encrypt the padded plaintext using the AES cipher
        ciphertext = cipher.encrypt(padded_plaintext)

        # extract the encrypted red, green, and blue values from the ciphertext
        r, g, b = ciphertext[:1], ciphertext[1:2], ciphertext[2:3]

        # write the encrypted pixel values back to the image
        pixels[x, y] = (r[0], g[0], b[0])

# save the encrypted image to a new file
input_image.save("encrypted.jpg")

# open the encrypted image and decrypt each pixel using the AES cipher
encrypted_image = Image.open("encrypted.jpg")
pixels = encrypted_image.load()

for x in range(width):
    for y in range(height):
        # extract the encrypted red, green, and blue values from the pixel
        r, g, b = pixels[x, y]

        # concatenate the encrypted RGB values into a single byte string
        ciphertext = bytes([r, g, b])

        # decrypt the ciphertext using the AES cipher
        padded_plaintext = cipher.decrypt(ciphertext)

        # unpad the plaintext to remove the padding added during encryption
        plaintext = unpad(padded_plaintext, AES.block_size)

        # extract the red, green, and blue values from the plaintext
        r, g, b = plaintext[:1], plaintext[1:2], plaintext[2:3]

        # write the decrypted pixel values back to the image
        pixels[x, y] = (r[0], g[0], b[0])

# save the decrypted image to a new file
encrypted_image.save("decrypted.jpg")
