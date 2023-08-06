import os, shutil
from raachem.file_class.log import LogFile
from raachem.file_class.gjf import GjfFile
from raachem.util.gen_purp import file_weeder, read_item, preferences, timeit, is_str_float


def e_analysis(weeded_list):
	"""Analyses Gaussian log files in weeded_list and prints out a txt file with results in current directory"""
	file_name = "Extracted_data.txt"
	out = []
	out.append("{} File(s) were analyzed in total.".format(len(weeded_list)))
	out.append("{:^29}|{:^20}|{:^20}|{:^20}".format("Name", "Sum of Elet an TC", "Thermal Correct", "last SCF"))
	rel_e = []
	for i in weeded_list:
		log = LogFile(read_item(i))
		t = log.thermal
		try: last_SCF = log.scf_done[-1][-1]
		except: last_SCF = "None"
		if t == False: out.append("{:<30} no_thermo_data_found_Last_SCF: {:>20}".format(i, last_SCF)); continue
		out.append("{:<30}{:>20}{:>20}{:>20}".format(str(i), str(t[7]), str(t[3]), str(last_SCF)))
		rel_e.append([i, float(t[7]) * 627.5095, float(last_SCF) * 627.5095, float(t[3]) * 627.5095])
	if len(rel_e) > 1:
		print("Do you want the free energies to be reported relative to which item?")
		print("Enter 0 if you don't want to analyze them)")
		for idx, entry in enumerate(rel_e):
			print(" {:<4}{:<20}{:>25}".format(idx + 1, entry[0], round(entry[1], 2)))
		while True:
			option = input()
			if option in [str(a) for a in range(len(rel_e)+1)]: option = int(option); break
			else: print("Could notunderstand request")
		if option == 0: print("Leaving analysis\n")
		else:
			out.append("\nFree energies relative to {}, (Name,G,H,TC):".format(rel_e[option-1][0]))
			for i in rel_e:
				a = [i[0], *[round(i[n] - rel_e[option-1][n], 2) for n in [1,2,3]]]
				out.append("{:<26}{:>26}{:>10}{:>10}".format(*a))
			out.append("\n")
	with open(file_name,mode="w",newline="\n") as file: file.write("\n".join(out))
	print("\nDone! \nPlease lookup:\n\n" + os.path.join(os.getcwd(), file_name), "\n")

def rel_scf(list=False):
	energies = []
	for i in file_weeder([".log"]):
		log = LogFile(read_item(i))
		energies.append([log.name, log.scf_done[-1][1], log.normal_termin])
	if len(energies) == 0: print("No .log files in current folder"); return
	energies = [[i[0], float(i[1]), i[2]] for i in energies]
	energies.sort(key=lambda x: x[1])
	min_e = energies[0][1]
	energies = [[i[0], (i[1] - min_e) * 627.509, i[2]] for i in energies]
	if list == False: print("\n".join(["{:>30}{:>15f}{:>5}".format(*l) for l in energies]))
	elif list == True: return energies

@timeit
def csv_e_analysis():
	def evaluate_list(folder, files=set()):
		for file in os.listdir(folder):
			if os.path.isdir(os.path.join(folder, file)):
				evaluate_list(os.path.join(folder, file), files)
			elif any([file.endswith(".log"),file.endswith(".xyz"),file.endswith(preferences.gauss_ext)]):
				files.add(os.path.join(folder, os.path.splitext(file)[0]))
		return files
	def evaluate_file(a, i,last):
		row = {a[1]:"-" for a in preferences.e_options}
		try:
			#BLANK
			row.update({"Blank": "-"})
			row.update({"Eh to kcal/mol":"627.5095"})
			row.update({"Eh to kJ/mol": "2625.5002"})

			#FILE PROPERTIES
			row.update({"Filename":os.path.basename(a)})

			#FOLDER PROPERTIES
			fold_name = os.path.dirname(a)
			row.update({"rel_path":os.path.relpath(fold_name, os.getcwd())})
			row.update({"Folder": 'HYPERLINK("{}";"{}")'.format(fold_name,os.path.relpath(fold_name, os.getcwd()))})

			#XYZ PROPERTIES
			xyz_name = a + ".xyz"
			is_xyz = os.path.isfile(os.path.relpath(xyz_name, os.getcwd()))
			row.update({".xyz":'HYPERLINK("{}";"Link")'.format(xyz_name) if is_xyz else "-"})

			#INPUT PROPERTIES
			inp_name = a + preferences.gauss_ext
			is_inp = os.path.isfile(os.path.relpath(inp_name, os.getcwd()))
			inp = GjfFile(read_item(os.path.relpath(inp_name, os.getcwd()))) if is_inp else False
			if inp:
				row.update({preferences.gauss_ext:'HYPERLINK("{}";"Link")'.format(inp_name) if is_inp else "-"})
				row.update({preferences.gauss_ext + "_#": inp.route_text() if inp else "-"})

			#LOG PROPERTIES
			log_name = a + ".log"
			is_log = os.path.isfile(os.path.relpath(log_name, os.getcwd()))
			log = LogFile(read_item(os.path.relpath(log_name, os.getcwd()))) if is_log else False
			if log:
				row.update({".log": 'HYPERLINK("{}";"Link")'.format(log_name) if log else "-"})
				row.update({".log_#": log.raw_route if log.raw_route else "-"})
				row.update({"E0":str(log.scf_done[-1][-1]) if log.scf_done else "-"})
				row.update({"iFreq": log.last_freq.n_ifreq() if log.last_freq else "-"})
				row.update({"E_ZPE": str(log.thermal[4]) if log.thermal else "-"})
				row.update({"E_tot": str(log.thermal[5]) if log.thermal else "-"})
				row.update({"H_corr": str(log.thermal[6]) if log.thermal else "-"})
				row.update({"G_corr": str(log.thermal[7]) if log.thermal else "-"})
				row.update({"E0+E_ZPE": str(log.thermal[0]) if log.thermal else "-"})
				row.update({"E0+E_tot": str(log.thermal[1]) if log.thermal else "-"})
				row.update({"E0+H_corr": str(log.thermal[2]) if log.thermal else "-"})
				row.update({"E0+G_corr": str(log.thermal[3]) if log.thermal else "-"})
				row.update({"Done?":"Yes" if log.normal_termin else "No"})
				row.update({"Error":log.error_msg if log else "-"})
				row.update({"HOMO": log.homo if log.homo else "-"})
				row.update({"LUMO": log.lumo if log.homo else "-"})
				row.update({"HOMO-LUMO": log.homo_lumo_gap if log.homo else "-"})
				row.update({"Charge": log.charge_mult[0] if log.charge_mult else "-"})
				row.update({"Mult": log.charge_mult[1] if log.charge_mult else "-"})
				row.update({"n_SCF":len(log.scf_done) if log.scf_done else "-"})
				row.update({"n_atoms": log.n_atoms if log.n_atoms else "-"})
				row.update({"TYP": log.calc_type if log.calc_type else "-"})
				row.update({"Needs refinement?": log.needs_ref()})
				row.update({"S**2 BA": log.s_squared[-1][1] if log.s_squared else "-"})
				row.update({"S**2 After": log.s_squared[-1][2] if log.s_squared else "-"})
				row.update({"LG": "\n".join(log.last_xyz_obj().return_print() if log.last_xyz_obj() else "-")})
				row.update({"LG": "-"})
				row.update({"MulkSpinDens": log.last_muliken_spin_density})
				row.update({"LastIntCoord": log.last_internal_coord})
				row.update({"MulkCharges": log.last_muliken_charges})
				row.update({"ESPCharges":log.last_chelpg_charges})
				row.update({"POPAnalysis":log.pop_analysis})
				row.update({"NPAAnalysis": log.npa_analysis})

		except Exception as e:
			print()
			print("\nError on file:\n{}\n".format(a));
			print(e, "\n")
		finally:
			if i+1 < last: print("\rEvaluating... {}/{}".format(i+1,last),end=" ")
			else: print("\rEvaluation done ({}/{}), saving '.xls' file...".format(i+1,last))
			return row
	aux_files_needed = ["LG","MulkSpinDens","LastIntCoord","MulkCharges","ESPCharges","POPAnalysis","NPAAnalysis"]
	folder_name = os.path.join(os.getcwd(), "linked_analysis_suplementary_files")
	if os.path.exists(os.path.join(folder_name)):
		if any(a in (preferences.e_options[n][1] for n in preferences.e_analysis_opt) for a in aux_files_needed):
			print("The following directory will be OVERWRITTEN!")
			print(folder_name)
			print("Are you sure? (y/n)")
			while True:
				if input() == "y": break
				else: print("Canceling...");return

	files = evaluate_list(os.getcwd())
	csv_list = [evaluate_file(file,i,len(files)) for i,file in enumerate(files)]
	if not csv_list: print("No .log files in {} directory".format(os.getcwd())); return
	csv_list.sort(key=lambda x: x["Folder"])
	try:
		import xlwt
		from xlwt import Workbook
	except ImportError:
		print("xlwt module is needed")
		return
	wb = Workbook()
	sheet1 = wb.add_sheet('Data')
	sheet2 = wb.add_sheet('Labels')
	style0 = xlwt.easyxf("", "#.0000000")

	for i_b,b in enumerate(preferences.e_options[n] for n in preferences.e_analysis_opt):
		sheet2.write(i_b, 0, b[1])
		sheet2.write(i_b, 1, b[0])
	for i_b,b in enumerate(preferences.e_options[n][1] for n in preferences.e_analysis_opt):
		sheet1.write(0, i_b, b)
	for i_a,a in enumerate(csv_list,start=1):
		for i_b,b in enumerate(preferences.e_options[n][1] for n in preferences.e_analysis_opt):
			if b in ("E0+G_corr", "E0", "E0+H_corr"):
				sheet1.write(i_a, i_b, float(a[b]) if is_str_float(a[b]) else a[b],style0)
			elif b in ("Folder",".xyz",preferences.gauss_ext,".log"):
				try: sheet1.write(i_a, i_b, xlwt.Formula(a[b]))
				except Exception: sheet1.write(i_a, i_b, a[b])
			elif b in aux_files_needed:
				if a[b] and a[b] != "-":
					filename = os.path.join(folder_name,a["rel_path"],a["Filename"]+"_"+b+".txt")
					try:
						os.makedirs(os.path.dirname(filename), exist_ok=True)
						if type(a[b]) == str:
								with open(filename, "w") as f:
									f.write(a[b])
								sheet1.write(i_a, i_b, xlwt.Formula('HYPERLINK("{}";"Link")'.format(filename)))
					except FileExistsError:
						print("Error while creating the following file:")
						print(filename)
						print("File already exists!")
				else:
					sheet1.write(i_a, i_b, "-")
			else: sheet1.write(i_a, i_b, a[b])
	try:
		wb.save("linked_analysis.xls")
	except PermissionError:
		print("Error while saving file!\nIs the file '{}' already open?".format("linked_analysis.xls"))

def deduplicate():
	print("Analyzing energies...")
	energies = [[b.name,float(b.scf_done[-1][1]),b.normal_termin,b.last_xyz_obj()] for i in file_weeder([".log"]) for b in [LogFile(read_item(i))]]
	unique = energies
	if not unique: print("No log files to be analyzed"); return
	black_list, folder_mov = [], []
	print("Starting analysis...")
	for file in sorted(unique,key=lambda x: (x[2],-x[1]),reverse=True):
		if file[0] in black_list: continue
		black_list.append(file[0])
		sim_en = [i for i in unique if i[0] not in black_list and  i[1] + 1 > file[1] > i[1] - 1]
		if sim_en:
			duplicates = []
			for obj in sim_en:
				if obj[3].superimpose(file[3], ret="max_d",conv=6):
					print("{} is a duplicate of {}".format(obj[3].name(), file[3].name()))
					duplicates.append(obj[3].name())
					black_list.append(obj[3].name())
			if duplicates: folder_mov.append([file[3].name(),duplicates])
	for folder in folder_mov:
		subfolder = os.path.join(os.getcwd(),"duplicates_of_{}".format(folder[0].replace(".log","")))
		try: os.mkdir(subfolder)
		except FileExistsError:	pass
		print("Moving duplicates of {} to the following directory:\n{}".format(folder[0], subfolder))
		for file in folder[1]:
			for alt_file in file_weeder([file.replace(".log",".")]):
				try:
					shutil.move(os.path.join(os.getcwd(),alt_file),os.path.join(subfolder,alt_file))
					print("Moved: {}".format(alt_file))
				except PermissionError:
					print("Error while moving log files:")
					print("Maybe {} already exists in the following directory:\n{}".format(alt_file,subfolder))
				except FileNotFoundError:
					print("File {} not found in the following directory:\n{}".format(alt_file,subfolder))
	print("Done!")
