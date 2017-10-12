from random import shuffle, randint, choice
from copy import copy
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

# Create a rotor of the Enigma


class rotor:
	def create(self):
		self.scrambler = copy(alphabet)
		shuffle(self.scrambler)
		self.notch = alphabet[randint(0, 25)]  # double step notch
		return

	def encode(self, i):
		return self.scrambler[i]

	def encoderev(self, i):
		return self.scrambler.index(i)

	def rotate(self):
		self.scrambler = self.scrambler[1:] + self.scrambler[:1]

	def setrotor(self, s):
		self.scrambler = s

# Enigma Class


class enigma:
	def __init__(self, num_rotors):
		self.rotors = []
		self.original_rotors = []  # backup original rotors
		self.num_rotors = num_rotors

		for i in range(num_rotors):  # intialize rotors
			self.rotors.append(rotor())
			self.rotors[i].create()
			self.original_rotors.append(self.rotors[i].scrambler)

		# Create reflector
		reflector_scramble = copy(alphabet)
		self.reflector = copy(alphabet)
		while len(reflector_scramble) > 0:
			temp1 = choice(reflector_scramble)
			reflector_scramble.remove(temp1)
			temp2 = choice(reflector_scramble)
			reflector_scramble.remove(temp2)
			self.reflector[alphabet.index(temp1)] = temp2
			self.reflector[alphabet.index(temp2)] = temp1

		# Create plugboard
		plugboard = copy(alphabet)
		shuffle(plugboard)
		self.plugboard = plugboard

	# encryption/decryption
	def encrypt(self, text):
		text = text.upper()
		clk = 0
		ciphertext = ""
		for c in text:
			if c not in alphabet:  # ignore special characters
				ciphertext += c
				continue
			clk += 1

			# letter->plugboard
			char = alphabet.index(self.plugboard[alphabet.index(c)])

			# letter->rotors
			for i in range(self.num_rotors):
				char = self.rotors[i].encode(char)
				char = alphabet.index(char)

			# letter->reflector
			char = alphabet.index(self.reflector[char])

			# letter back through rotors
			for i in range(self.num_rotors):
				char = alphabet[char]
				char = self.rotors[self.num_rotors - i - 1].encoderev(char)
			char = alphabet[self.plugboard.index(alphabet[char])]

			# add letter to ciphertext
			ciphertext += char

			# rotate rotors, rotate 1st everytime, 2nd every 26, 3rd every
			# 56...
			for i in range(self.num_rotors):
				# double step
				if self.rotors[i].notch == self.rotors[i].scrambler[0] and i != self.num_rotors - 1:
					self.rotors[i + 1].rotate()
				if(i == 0):
					self.rotors[i].rotate()
				elif(clk % ((i) * 26) == 0):
					self.rotors[i].rotate()
		return ciphertext

	# Reset rotor positions for decryption
	def reset(self):
		for i in range(self.num_rotors):
			self.rotors[i].setrotor(self.original_rotors[i])

	# Print Enigma setup for debugging
	def print_setup(self):
		print("Plugboards:\n", self.plugboard)
		print(
	"Enigma Setup:\nRotors: ",
	self.num_rotors,
	 "\nRotor arrangement:")
		for i in range(0, self.num_rotors):
			print(self.rotors[i].scrambler)
		print("Reflector arrangement:\n", self.reflector, "\n")


if __name__ == '__main__':
	ready = False
	print("  #  Welcome to Py-Enigma. Type HELP for valid commands")
	while True:
		print("+> ")
		command = str(input()).upper()
		if command.startswith("NEW"):
			print(" #  New machine initialized")
			print(" #  Input how many rotors would you like to use: ")
			num = int(str(input()))
			e = enigma(num)
			ready = True
		elif command.startswith("RESET"):
			e.reset()
			ready=True
			print(" #  Machine configuration reset")
		elif command.startswith("ENCRYPT"):
			if ready:
				plaintext = command.replace("ENCRYPT ", "")
				cyphertext = e.encrypt(plaintext)
				ready=False
				print(cyphertext)
			else:
				print(" #  Machine not configured!")
		elif command.startswith("DECRYPT"):
			if ready:
				plaintext = command.replace("DECRYPT ", "")
				cyphertext = e.encrypt(plaintext)
				ready=False
				print(cyphertext)
			else:
				print(" #  Machine not configured!")
		elif command.startswith("HELP"):
			print(""" # Commands:
 #  new          => resets the machine configuration
 #  reset        => resets the machine rotors for decryption
 #  encrypt <plaintext> => encrypts the given plaintext
 #    this will also decrypt a given cyphertext as long as the settings are the same
 #
 #  print        => prints the current setup of the enigma
 #  help         => prints this message
 #  exit         => exits the script""")
		elif command.startswith("PRINT"):
			e.print_setup();
		elif command.startswith("EXIT"):
			exit()
