# attempt number 2
# One file cause might fail. seperate if complete.
# 17/10/2021 @ 3:29am  - lexer went very well :)
# 17/10/2021 @ 17:49pm - It is complete for now. I don't have 
#                        brackets but i do have order of operations :D

import reqkMathParser
import reqkMathInterpreter

numbers = '0123456789'
op_T = {  # Token lookup table
	'!':'FACT',
	'^':'EXPO',
	'/':'DIV',
	'*':'MUL',
	'+':'PLUS',
	'-':'MINUS'
	#'(':'LPAREN',
	#')':'RPAREN'
}
INT   = 'INT'
FLOAT = 'FLOAT'


class error():
	def __init__(self, fn, pos, details):
		self.fn = fn
		self.pos     = pos
		self.details = details

	def __repr__(self):
		error_string = ('   '+' '*self.pos) + '^\n' + self.fn +' Col:'+str(self.pos)+' -> Error: ' + self.details
		return error_string

class unkownChar:
	def __init__(self, fn, pos, char):
		self.fn   = fn
		self.pos  = pos
		self.char = char

	def __repr__(self):
		arrow_p = ('   '+' '*self.pos) + '^'
		error_string = arrow_p+'\n'+self.fn+' Col:'+str(self.pos)+' -> Error: Unknown Character - \''+self.char+'\''
		return error_string

class unkownError:
	def __init__(self, fn, pos, details):
		self.fn = str(fn)
		self.pos = pos
		self.details = str(details)

	def __repr__(self):
		arrow_p = ('   '+' '*self.pos) + '^'#'^'*(len(self.fn)+len(str(self.pos))+len(self.details)+31)
		error_string = arrow_p+'\n'+self.fn+' Col:'+str(self.pos)+' -> ! - Unkown Error: '+self.details+" - !"
		return error_string


class Token():
	def __init__(self, Type_, Value, idx, length):
		self.Type_   = Type_
		self.value   = Value
		self.idx     = idx
		self.length  = length

	def __getitem__(self, parameter):
		return parameter

	def __repr__(self):
		if type(self.value) == int | float and self.value >= 0: return f'{self.Type_}, {self.value}, {self.length}, {self.idx}'
		else: return f'{self.Type_}, {self.value}, {self.length}, {self.idx}'


class Lexer():
	def __init__(self, fn, text):
		self.fn     = fn
		self.text   = text
		self.pos    = 0
		self.TK_IDX = 0

	def makeNumber(self, starting_pos):
		n = ''
		dots = 0

		while self.text[self.pos] in numbers + '.':
			currChar = self.text[self.pos]
			if currChar == '.':
				dots += 1
				if dots > 1:
					return error(self.fn, self.pos, "Multiple Decimal Points")

			n += currChar

			if self.pos < len(self.text):
				self.pos += 1
			else:
				break

		if dots == 1: return Token(FLOAT, float(n), starting_pos, len(n))
		return Token(INT, int(n), starting_pos, len(n))


	def Lex(self):
		tokens = []
		self.text += ' '

		while self.pos < len(self.text):
			currChar = self.text[self.pos]

			if currChar in ' \n\t':
				self.pos += 1

			elif currChar in numbers:
				number = self.makeNumber(self.TK_IDX)
				if type(number) == error:
					return number
				else: 
					tokens.append([number])
					self.TK_IDX += 1

			elif currChar in op_T:
				tokens.append([Token(op_T[currChar], currChar, self.TK_IDX, 1)])
				self.pos += 1
				self.TK_IDX += 1

			else:
				return unkownChar(self.fn, self.pos, currChar)


		return tokens


def main(fn, text, showtokens=False):
	run = Lexer(fn, text)
	tokens = run.Lex()
	if type(tokens) in [error, unkownChar]:
		return tokens

	elif showtokens == True:
		print(tokens)

	parser = reqkMathParser.Parser(tokens)
	current_ops = parser.parse()

	interpreter = reqkMathInterpreter.Interpreter(current_ops, tokens)
	try:
		result = interpreter.generate()
	except:
		 return unkownError(fn, 0, "Input not possible")

	return result

def file_opener(text):
	fn, expected_fe = '<stdin>', '.reqk'  # file extension
	text = text.strip()
	fe = text[len(text)-len(expected_fe):]
	if fe != expected_fe: 
		return(error(fn, len(text)-1, "Exptected file extension '.reqk'")), 1

	fn = text[3:]
	try:
		f = open(fn, "r")
		text = f.read()
	except FileNotFoundError:
		return(error(fn, 3, "No such file or directory")), 1

	return text, 0


def help():
	print("\n Commands:")
	print("  ':tk' - Toggles token visiblity")
	print("  ':f'  - Run code from file (:f {file directory}.reqk)")
	print("  ':h'  - Help guide")
	print("  ':q'  - Quits the program")
	print("\n Operations:")
	print("   |\'!\' - Factorial |")
	print("   |\'^\' - Power     | ")
	print("   |\'/\' - Divide    | ")
	print("   |\'*\' - Multiply  | ")
	print("   |\'+\' - Add       | ")
	print("   |\'-\' - subtract  | ")	
	print("\n Data Types:")
	print("  - (INT)")
	print("  - (FLOAT)\n")

