import os, shutil, time, itertools, configparser

def read_item(file_name=None, promp=False, extension=None, cf=os.getcwd()):
	"""Reads an .xyz, .gjf, .com or .log item and returns a list of its contents ready for class instantiation"""
	if promp != False:
		if extension is None: extension = [".xyz"]
		print(promp)
		files = file_weeder(extension)
		if len(files) == 0: print("Sorry no such files in current directory!"); return []
		for idx,item in enumerate(files): print("{:<5}{:<25}".format(idx+1,item))
		while True:
			try: file_name = files[int(input())-1]; break
			except: print("Invalid input!")
	with open(os.path.join(cf,file_name),"r") as in_file: in_content = in_file.read().splitlines()
	in_content.insert(0,file_name)
	return in_content

def file_weeder(ext_to_weed,cf=os.getcwd(), promp=True):
	"""Looks up files with the extensions provided in current directory"""
	if type(ext_to_weed) == str: ext_to_weed = [ext_to_weed]
	weeded_list = []
	for a,b in itertools.product(ext_to_weed,os.listdir(cf)):
		if a in b: weeded_list.append(b)
	if promp and len(weeded_list) == 0:
		print("No '{}' files found in current directory!".format("' or '".join(ext_to_weed)))
		print(cf)
		return []
	return sorted(weeded_list)

def is_str_float(i):
	"""Check if a string can be converted into a float"""
	try: float(i); return True
	except ValueError: return False

def mv_up_folder():
	"""Move files with a chossen extension up a folder"""
	while True:
		extensions = [[0, "return"], ["1", ".log"], ["2", ".gjf"],["2", ".com"],["3", ".xyz"]]
		print("Select a file extension to move up a folder")
		for idx, ext in enumerate(extensions):
			if idx == 0: print("0   - Cancel request")
			else: print("{:<3} - {:>10}".format(ext[0], ext[1]))
		extension = {str(i[0]): i[1] for i in extensions}.get(input(), None)
		print(extension)
		if extension == "return": return
		if extension != None: break
		print("Invalid Option")
	folders = [x[0] for x in os.walk(os.getcwd())]
	for folder in folders[1:]:
		for file in file_weeder(extension, folder, promp=False):
			if os.path.isfile(os.path.join(folders[0], file)):
				print("Filename: {}\nFrom: {}\nAlready exists in uper directory:\n{}".format(file, folder, folders[0]))
				break
			shutil.copy2(os.path.join(folder, file), os.path.join(folders[0], file))
def sel_files(weeded_list):
	print("Choose the files you want to operate on:")
	print("(Multiple files can be separated by a space; 'a' for all files)")
	print("{:>3}{:>30}".format("0", "None"))
	for i,a in enumerate(weeded_list): print("{:>3}{:>30}".format(str(i+1),a))
	while True:
		option = input().lower().split()
		if all(b in ["a","0",*[str(a) for a in range(len(weeded_list)+1)]] for b in option): break
	if "0" in option: return False
	else: return weeded_list if "a" in option else [weeded_list[int(i)-1] for i in option]

def timeit(method):
	def timed(*args, **kw):
		ts = time.time()
		result = method(*args, **kw)
		te = time.time()
		print('{}:{:.2f} ms'.format(method.__name__, (te - ts) * 1000))
		return result
	return timed

class Var:
	conf_dir = os.path.dirname(__file__)
	conf_file = os.path.join(conf_dir, "user.init")

	def __init__(self,conf_file=conf_file):
		self.std_config = configparser.ConfigParser()
		self.std_config["SERVERS"] = {"heimdall_user": "heimdall_user",
							 "heimdall_mail": "heimdall_mail",
							 "heimdall_notification": "False",
							 "aguia_user": "aguia_user",
							 "athene_user": "athene_user",
							 "sub_s_name": "sub_s_name"}
		self.std_config["BEHAVIOUR"] = {"heavy_atom": "36",
							   "gjf_overwrite": "False",
							   "folder_op": "True",
							   "gauss_ext": ".com",
							   "comp_software": "gaussian"}
		self.std_config["ANALYSIS"] = {"options": "3 4 5 6 7"}
		if not os.path.isfile(conf_file):
			with open(conf_file, "w") as configfile:
				self.std_config.write(configfile)
		else:
			self.config = configparser.ConfigParser()
			self.config.read(conf_file)

		def pick(args,get_type,valid_keys={},default=None,config=self.config,std_config=self.std_config):
			try:
				if get_type == "str":
					result = config.get(*args)
				elif get_type == "bool":
					result = config.getboolean(*args)
				elif get_type == "int":
					result = config.getint(*args)
			except:
				if get_type == "str":
					result = std_config.get(*args)
				elif get_type == "bool":
					result = std_config.getboolean(*args)
				elif get_type == "int":
					result = std_config.getint(*args)
			finally:
				if valid_keys:
					result = valid_keys.get(result,default)
				return result

		self.heimdall_user = pick(("SERVERS","heimdall_user"),"str")
		self.heimdall_mail = pick(("SERVERS","heimdall_mail"),"str")
		self.heimdall_notification = pick(("SERVERS","heimdall_notification"),"bool")
		self.aguia_user = pick(("SERVERS","aguia_user"),"str")
		self.athene_user = pick(("SERVERS","athene_user"),"str")
		self.sub_s_name = pick(("SERVERS","sub_s_name"),"str")
		keys={n:n for n in range(1,119)}
		self.heavy_atom = pick(("BEHAVIOUR","heavy_atom"),"int",valid_keys=keys,default=36)
		self.gjf_overwrite = pick(("BEHAVIOUR","gjf_overwrite"),"bool")
		self.folder_op = pick(("BEHAVIOUR","folder_op"),"bool")
		keys = {".gjf":".gjf","gjf":".gjf",".com":".com","com":".com"}
		self.gauss_ext = pick(("BEHAVIOUR","gauss_ext"),"str",valid_keys=keys,default=".com")
		keys = {"gaussian":"gaussian","g09":"gaussian","g16":"gaussian","orca":"orca"}
		self.comp_software = pick(("BEHAVIOUR","comp_software"),"str",valid_keys=keys,default="gaussian")
		self.e_options = [
			["Blank column","Blank"],
			["Hartree to kcal/mol conversion factor (627.5)", "Eh to kcal/mol"],
			["Hartree to kJ/mol conversion factor (2625.5)", "Eh to kJ/mol"],
			["Filename","Filename"],
			["Hyperlink to corresponding folder", "Folder"],
			["Hyperlink to Filename.xyz",".xyz"],
			["Hyperlink to Filename{}".format(self.gauss_ext),self.gauss_ext],
			["Route section read from Filename{}".format(self.gauss_ext), self.gauss_ext + "_#"],
			["Hyperlink to Filename.log",".log"],
			["Route section read from Filename.log",".log_#"],
			["Energy from last SCF cycle", "E0"],
			["Number of imaginary frequencies found on Filename.log","iFreq"],
			["Zero-point correction","E_ZPE"],
			["Thermal correction to Energy","E_tot"],
			["Thermal correction to Enthalpy","H_corr"],
			["Thermal correction to Gibbs Free Energy","G_corr"],
			["Sum of electronic and zero-point Energies","E0+E_ZPE"],
			["Sum of electronic and thermal Energies","E0+E_tot"],
			["Sum of electronic and thermal Enthalpies","E0+H_corr"],
			["Sum of electronic and thermal Free Energies","E0+G_corr"],
			["Filename.log gaussian normal termination status","Done?"],
			["Error messages found on Filename.log","Error"],
			["HOMO from Filename.log","HOMO"],
			["LUMO from Filename.log","LUMO"],
			["HOMO-LUMO gap from Filename.log","HOMO-LUMO"],
			["Charge from Filename.log","Charge"],
			["Starting multiplicity from Filename.log","Mult"],
			["Number of 'SCF Done:' keywords found","n_SCF"],
			["Number of atoms on Filename.log","n_atoms"],
			["Filename.log calculation type (This may be unreliable)","TYP"],
			["Filename.log calculation type consistency with iFreq","Needs refinement?"],
			["Filename.log last spin densities before anihilation", "S**2 BA"],
			["Filename.log last spin densities after anihilation", "S**2 After"],
			["Filename.log last geometry", "LG"],
			["Filename.log last Muliken charge and spin density","MulkSpinDens"],
			["Filename.log last Internal coordinates", "LastIntCoord"],
			["Filename.log last Muliken charge", "MulkCharges"],
			["Filename.log last ESP charge", "ESPCharges"],
			["Filename.log last population analysis", "POPAnalysis"],
			["Filename.log last NPA analysis", "NPAAnalysis"]

		]
		self.valid_e_keys = [str(n) for n in range(len(self.e_options))]
		self.e_analysis_opt = [int(a) for a in pick(("ANALYSIS","options"),"str").split() if a in self.valid_e_keys]
		#self.e_analysis_opt = [int(a) for a in self.valid_e_keys]
		global preferences
		preferences = self
	def set_variables(self):
		print("Please type 'chave' and press enter")
		if input().strip().lower() != "chave": return
		try: import raapbs;	pbs = True
		except ImportError:	pbs = False
		options = [
			["To return", None],
			["Set program BEHAVIOUR options", self.set_behaviour],
			["Set preferences related to the creation of xls files via energy analysis function",self.xls_creation]
		]
		if pbs:	options.insert(1,["Set SERVER related options", self.set_server])
		while True:
			option = self.get_option(options)
			if option == 0: return
			else: options[option][-1]()
	def get_option(self,options):
		print("Which variables do you want to set?")
		for i, v in enumerate(options):
			if v[1] is None: print("{} - {}".format(i, v[0]))
			else: print("{} - {} {}".format(i, v[0], "" if callable(v[1]) else getattr(self, v[1])))
		while True:
			option = input().strip()
			if option in [str(n) for n in range(len(options))]:	break
			else: print("Invalid Input!")
		return int(option)
	def set_server(self,conf_file=conf_file):
		options = [
			["To return", None],
			["HEIMDALL USER:", "heimdall_user"],
			["HEIMDALL MAIL:", "heimdall_mail"],
			["HEIMDALL SEND EMAIL (true/false):", "heimdall_notification"],
			["AGUIA USER:", "aguia_user"],
			["ATHENE USER:", "athene_user"],
			["SUBMISSION SCRIPT NAME:", "sub_s_name"]
		]
		while True:
			option = self.get_option(options)
			if option == 0: return
			else:
				variable = input("Enter variable '{}' value: ".format(options[option][-1]))
				self.config["SERVERS"][options[option][-1]]=variable.strip()
				with open(conf_file, "w") as configfile: self.config.write(configfile)
				self.__init__()
	def set_behaviour(self,conf_file=conf_file):
		options = [
			["To return", None],
			["ECP IS ADVISED FOR ELEMENTS LARGER THAN:", "heavy_atom"],
			["OVERWRITE .GJF FILES WITH NO PROMP (true/false):", "gjf_overwrite"],
			["AUTO OPERATE ON ALL FILES IN THE CWD (true/false):", "folder_op"],
			["GAUSSIAN INPUT FILE EXTENSION ('.gjf' or '.com'):", "gauss_ext"],
			["COMPUTATIONAL CHEMISTRY SOFTWARE (orca/gaussian):", "comp_software"]
		]
		while True:
			option = self.get_option(options)
			if option == 0: return
			else:
				variable = input("Enter variable '{}' value: ".format(options[option][-1]))
				self.config["BEHAVIOUR"][options[option][-1]]=variable.strip()
				with open(conf_file, "w") as configfile: self.config.write(configfile)
				self.__init__()
	def xls_creation(self,conf_file=conf_file):
		while True:
			print("=============================CURRENTLY INCLUDED COLUMNS=============================")
			correspondence = {}
			for i,a in enumerate(self.e_analysis_opt,start=1):
				print("{:>3} {:<59} {:>20}".format(i,*self.e_options[a]))
				correspondence.update({str(i):a})
			unused = [a for a in self.valid_e_keys if int(a) not in self.e_analysis_opt]
			start = len(correspondence)+1
			if unused:
				print("============================CURRENTLY UNINCLUDED COLUMNS============================")
			for i,a in enumerate(unused,start=start):
				print("{:>3} {:<59} {:>20}".format(i,*self.e_options[int(a)]))
				correspondence.update({str(i):int(a)})
			print("====================================================================================")
			print()
			print("xls analysis columns can be added with '+N' or removed with '-N':")
			print("Multiple operations can be separated with a space character. Enter '0' to go back")
			option = input().split()
			if "0" in option: return
			else:
				add_keys = [correspondence[a[1:]] for a in option if a[0] == "+" and a[1:] in correspondence.keys()]
				rem_keys = [correspondence[a[1:]] for a in option if a[0] == "-" and a[1:] in correspondence.keys()]
				all_keys = [a for a in self.e_analysis_opt if a not in rem_keys]
				all_keys.extend([a for a in add_keys if a not in rem_keys])
				self.config["ANALYSIS"]["options"] = " ".join([str(a) for a in all_keys])
				with open(conf_file, "w") as configfile:
					self.config.write(configfile)
				self.__init__()
preferences = Var()


