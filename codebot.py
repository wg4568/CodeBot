import sys, re

def base_type(string):
	string = str(string)
	if string.lower() == "true":
		return True
	if string.lower() == "false":
		return False
	try:
		return float(string)
	except ValueError: pass
	try:
		return int(string)
	except ValueError: pass
	return string

LOG = ""

def do_log(s):
	global LOG
	LOG += s + "\n"
	print s

class Command:
	def __init__(self, first, args, raw=""):
		self.first = first
		self.args = args
		self.raw = raw
		self.type = self.first[0]
		self.code = ""

	def __str__(self):
		return "%s %s" % (self.first, self.args)

	def disp_code(self):
		if self.type == "auton":
			return "autonomous code"
		else:
			return self.code.replace("\n","").replace("?","").replace("&","").replace("@","")

	def differentiate(self):
		if self.type == "define":
			if self.first[1] == "motor":
				self.name = self.first[2]
				self.reversed = ("reversed" in self.args)
				for arg in self.args:
					if "port" in arg.split():
						self.port = int(arg.split()[1])
				if self.reversed: rv = ",reversed"
				else: rv = ""
				self.code = "#pragma config(Motor,port%s,MOTOR_%s,tmotorVex393_MC29,openLoop%s)\n" % (self.port, self.name, rv)

		if self.type == "group":
			if self.first[1] == "motor":
				self.name = self.first[2]
				self.motors = self.args
				mrs = ""
				for m in self.motors:
					mrs += "@motor(MOTOR_%s)?=?s;&" % (m)
				self.code = "void GROUP_%s(float s)?{&%s}&" % (self.name, mrs)

		if self.type == "bind":
			self.bindtype = self.first[1]
			if self.bindtype == "group":
				self.boundtotype = self.first[3]
				self.boundto = self.first[2]
				self.inputs = []
				self.rest = 0.0
				self.sensitivity = 1.0
				for argument in self.args:
					s = argument.split()
					if s[0] == "input":
						self.inputs.append(s)
					if s[0] == "sensitivity":
						self.sensitivity = float(s[1])
					if s[0] == "rest":
						self.rest = float(s[1])
				self.loopcode = "@@BIND_%s();&" % (self.boundto)
				if self.boundtotype == "channel":
					self.code = "void BIND_%s()?{&@GROUP_%s(vexRT[Ch%s]?*?%s);&}&" % (self.boundto, self.boundto, self.inputs[0][1], self.sensitivity)
				if self.boundtotype == "button":
					ifs = ""
					for ip in self.inputs:
						button = ip[1]
						speed = float(ip[2])
						bnd = "@GROUP_%s(%s);&" % (self.boundto, speed)
						ifs += "if?(vexRT[Btn%s])?{&@%s@}?else " % (button, bnd)
					ifs += "{&@@GROUP_%s(%s);&@}" % (self.boundto, self.rest)
					self.code += "void BIND_%s()?{&@%s&}&" % (self.boundto, ifs)
					self.loopcode = "@@BIND_%s();&" % (self.boundto)

		if self.type == "auton":
			self.duration = 0.0
			for arg in self.args:
				s = arg.split()
				if s[0] == "run":
					groups = s[1:-2]
					speed = float(s[-2:][0])
					delay = float(s[-1:][0])
					self.duration += delay
					g1 = ""
					g2 = ""
					for g in groups:
						g1 += "@GROUP_%s(%s);&" % (g, speed)
						g2 += "@GROUP_%s(%s);&" % (g, 0.0)
					self.code += "%s@wait1Msec(%s);&%s" % (g1, delay, g2)

		if self.type == "raw":
			self.rawtype = self.first[1]
			for n in self.args:
				self.code += "@" + n + "&"

class Code:
	def __init__(self, *args, **kwargs):
		self.commands = []
		self.raw = ""
		self.raw_split = []
		self.code = None
		self.log = ("log" in kwargs and kwargs["log"])
		self.comments = []
		self.args = {"competition":False, "tidy": False, "custom":False, "logcomment":True}

		if args:
			self.parse(args[0])

	def write_to_file(self, path):
		with open(path, "w+") as file:
			file.write(self.code)
			do_log("[written to file] %s - %s bytes" % (path, len(self.code)))

	def parse(self, raw):
		try:
			rargs = re.findall(r"!\*.*\*!", raw, re.DOTALL)
			for argseg in rargs:
				argseg = argseg.strip("!*").strip("*!").split(",")
				for arg in argseg:
					arg = arg.replace(" ","")
					arg = arg.split("=")
					self.args[arg[0]] = base_type(arg[1])
			raw = re.sub(r"!\*.*\*!", "", raw, re.DOTALL)
			do_log("[extracted arguments] %s" % (self.args))
		except Exception as e:
			do_log("[arg extract failed] %s" % (e))

		self.comments = re.findall(r"\/\*.*\*\/", raw, re.DOTALL)
		raw = re.sub(r"\/\*.*\*\/", "", raw, re.DOTALL)
		do_log("[removed comments] %s" % (self.comments))
		self.raw = raw.replace("\n","").replace("\t","")
		self.raw_split = self.raw.split(";")
		for command in self.raw_split:
			if command:
				first = command.split("{")[0].strip().split()
				args = re.findall(r'\{([^]]*)\}', command)[0].split(",")
				cmd = Command(first, args, raw=command)
				do_log("[parsed command] %s" % (cmd))
				self.commands.append(cmd)

	def build(self):
		loopcode = ""
		header = ""
		auton = ""
		body = ""
		initcode = ""
		self.code = "/* Code auto generated from %s - CodeBot language by William Gardner (https://github.com/wg4568/CodeBot/) */\n" % self.src

		rawloop = ""
		rawinit = ""

		for cmd in self.commands:
			cmd.differentiate()
			if cmd.code: do_log("[built command] %s" % (cmd.disp_code()))
			else: do_log("[built command] skipping because no code created - %s" % (cmd))
			if hasattr(cmd, "loopcode"):
				loopcode += cmd.loopcode
			elif cmd.type == "define":
				header += cmd.code
			elif cmd.type == "auton":
				do_log("[build autonomous] %s steps, takes %s seconds" % (len(cmd.args), cmd.duration/1000))
				auton += cmd.code
			elif cmd.type == "raw":
				if cmd.rawtype == "loop":
					rawloop += cmd.code
				else:
					rawinit += cmd.code
			else:
				body += cmd.code

		# rawloop = "void raw_loop()?{&%s}&" % (rawloop)
		# rawinit = "void raw_init()?&%s}&" % (rawinit)
		# self.code += rawloop
		# self.code += rawinit

		if self.args["competition"]:
			header += "#pragma platform(VEX2)\n#pragma competitionControl(Competition)\n#include \"Vex_Competition_Includes.c\"\nvoid pre_auton()?{&@/*?preauton?*/&}&"
			main = "task usercontrol"
		else:
			main = "task main"

		self.code += header
		auton = "task autonomous()?{&%s}&" % (auton)
		self.code += body
		self.code += auton
		if self.args["custom"]:
			self.code += "\n\nvoid custom_init() {\n\t//init code\n}\n"
			self.code += "void custom_loop() {\n\t//loop code\n}\n\n"
			loopcode += "@custom_loop();&"
			initcode += "@custom_init();&"
			# loopcode += "@raw_loop();&"
			# initcode += "@raw_init();&"
		loopcode = "%s()?{&@%s@while?(true)?{&%s@}&}" % (main, initcode, loopcode)
		self.code += loopcode
		if self.args["tidy"]:
			self.code = self.code.replace("?"," ").replace("&","\n").replace("@","\t")
		else:
			self.code = self.code.replace("?","").replace("&","").replace("@","")

		return self.code

with open(sys.argv[1], "r") as file:
	OUTPUT = sys.argv[1].split(".")[0] + ".c"
	RAW = file.read()
	do_log("[loaded file] %s - %s bytes" % (sys.argv[1], len(RAW)))

code = Code(log=True)
code.src = sys.argv[1]
code.parse(RAW)
code.build()

if code.args["logcomment"]:
		code.code += "\n\n/" + ("* ===== BUILD LOG =====\n\n%s\n ===== END LOG ===== *" % (LOG)).replace("/","") + "/"
		code.code += "\n\n/" + ("* ===== SOURCE CODE =====\n\n%s\n ===== END CODE ===== *" % (RAW)).replace("/","") + "/"

code.write_to_file(OUTPUT)

# # [PackageDev] target_format: plist, ext: tmLanguage
# ---
# name: CodeBot
# scopeName: codebot.cb
# fileTypes: [cb]
# uuid: c7e16b37-8c2d-4fc5-9c01-4bf0f5b803a9

# patterns:
# - name: entity.name.function.python
#   match: ^(define|group|bind|auton)

# - name: keyword.control.flow.python
#   match: (motor|channel|button|group|servo)

# - name: constant.numeric.integer.decimal.python
#   match: ([0-9|\.|\-][A-Z]|[0-9|\.|\-]|\$[a-zA-Z\_]+)

# - name: constant.numeric.integer.decimal.python
#   match: \!\*.*\*\!

# - begin: /\*
#   captures:
#     '0':
#       name: comment.line.number-sign.python
#   end: \*/
#   name: comment.line.number-sign.python

# - name: support.function.builtin.python
#   match: (input|port|sensitivity|reversed|run|rest)

# - name: meta.preprocessor.c
#   match: ([a-zA-Z\_]+)
# ...


# !* competition=True, tidy=True *!

# define motor arm_right_upper {
# 	port 2,
# 	reversed
# };
# define motor arm_right_lower {
# 	port 3,
# 	reversed
# };
# define motor arm_left_upper {
# 	port 4
# };
# define motor arm_left_lower {
# 	port 5
# };
# define motor base_front_left {
# 	port 6
# };
# define motor base_back_left {
# 	port 7
# };
# define motor base_right_all {
# 	port 8
# };
# define motor latch_motor {
# 	port 9,
# 	reversed
# };

# group motor latch {
# 	latch_motor
# };
# group motor base_left {
# 	base_front_left,
# 	base_back_left
# };
# group motor base_right {
# 	base_right_all
# };
# group motor arm_unit {
# 	arm_right_upper,
# 	arm_right_lower,
# 	arm_left_upper,
# 	arm_left_lower
# };

# bind group arm_unit button {
# 	input 6U 127,
# 	input 6D -50,
# 	rest 20
# };
# bind group latch button {
# 	input 8D -25,
# 	input 8R 25
# };
# bind group base_left channel {
# 	input 3
# };
# bind group base_right channel {
# 	input 2
# };