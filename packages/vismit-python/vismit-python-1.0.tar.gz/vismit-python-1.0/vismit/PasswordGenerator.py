import hashlib

class PasswordGenerator:
	def __init__(self, websiteName, password, keyLen):
		self.__shuffled_letters = ['!', ';', 'k', 'a', 'i', 'n', '$', '>', 'q', '2',
		'Z', 't', "'", '[', 'w', 'd', 'W', 'z', '*', '^', 'C', '5', 'T', 'F', '-',
		'{', 'I', 'g', 'Q', 'L', ':', '~', '0', '8', 'l', '#', '=', 'o', 'b', 'j',
		'r', '&', '@', 'u', '3', 'X', 'x', ')', ']', 'A', 'e', 'U', 'D', ',', '`',
		'G', '6', 'R', 'J', '/', '}', 'M', 'h', 'O', '"', '<', 'm', '1', '9', 'p',
		'%', '?', 's', 'c', 'Y', 'v', '(', '\\', 'y', '4', 'V', 'B', '+', '_', 'E',
		'f', 'S', 'H', '.', '|', 'K', '7', 'P', 'N']

		self.website_name = websiteName
		self.password = password
		self.key_len = keyLen
		self.fused_words = self.__fusedWords()


	def __fusedWords(self):
		string1 = self.website_name
		string2 = self.password
		passphrase = ""
		if len(string1)>len(string2):
			string1,string2 = string2, string1

		for i in range(len(string1)):
			passphrase += string1[i] + string2[i]

		if(len(string1)!=len(string2)):
			passphrase += string2[:len(string1)-1:-1]
		return passphrase

	def __chunked_hashed_passphrase(self):
		hashed_passphrase = hashlib.sha256(self.fused_words.encode()).hexdigest()[:60]
		chunk_size = 60//self.key_len

		final_chunks = list()
		i = 0
		start = 0
		while(i<self.key_len):
			final_chunks.append(hashed_passphrase[start:start+chunk_size])
			start+=chunk_size
			i+=1
		return final_chunks

	def __encodeList(self, chp):
		encrypted_password = ''
		for element in chp:
			value = 1
			for e in element:
				if e=='0': continue
				value = (value * int(e, 16)) + value
			encrypted_password+=self.__shuffled_letters[value%len(self.__shuffled_letters)]
		return encrypted_password

	def get_secret_key(self):
		chp = self.__chunked_hashed_passphrase()
		encoded_string = self.__encodeList(chp)
		return encoded_string
