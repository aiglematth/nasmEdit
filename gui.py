#Auteur --> aiglematth

#Imports
import tkinter              as tk
import tkinter.scrolledtext as scroll
import tkinter.filedialog   as tkFile
import tkinter.messagebox   as tkMess
from   time             import sleep
from   colors           import *

#Constantes
REGISTERS = [
	"rax", "rcx", "rdx", "rbx", "rsp", "rbp", "rsi", "rdi",
	"eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi",
	"ax", "cx", "dx", "bx", "sp", "bp", "si", "di",
	"ah", "al", "ch", "cl", "dh", "dl", "bh", "bl", "spl", "bpl", "sil", "dil",
	"cr", "dr", "tr"]

for x in range(8, 16):
	REGISTERS.append(f"r{x}")
	REGISTERS.append(f"r{x}d")
	REGISTERS.append(f"r{x}w")
	REGISTERS.append(f"r{x}b")

REGISTERS.sort(key=len, reverse=True)

INSTRUCTIONS = [
	"aaa", "aad", "aam", "aas", "adc", "add", "and", "call", "cbw", "clc", "cld", "cli", "cmc", "cmp", "cmpsb", "cmpsw",
	"cwd", "daa", "das", "dec", "div", "esc", "hlt", "idiv", "imul", "in", "inc", "int", "into", "iret", "ja", "jae", "jb", 
	"JBE", "JC", "JE", "JG", "JGE", "JL", "JLE", "JNA", "JNAE", "JNB", "JNBE", "JNC", "JNE", "JNG", "JNGE", "JNL", "JNLE",
	"JNO", "JNP", "JNS", "JNZ", "JO", "JP", "JPE", "JPO", "JS", "JZ", "jcxz", "jmp", "lahf", "lds", "lea", "les", "lock",
	"lodsb", "lodsw", "loop", "LOOPE", "LOOPNE", "LOOPNZ", "LOOPZ", "mov", "movsb", "movsw", "mul", "neg", "nop", "not", "or",
	"out", "pop", "popf", "push", "pushf", "rcl", "rcr", "REP", "REPE", "REPNE", "REPNZ", "REPZ", "ret", "retn", "retf", "rol",
	"ror", "sahf", "sal", "sar", "sbb", "scasb", "scasw", "shl", "shr", "stc", "std", "sti", "stosb", "stosw", "sub", "test",
	"wait", "xchg", "xlat", "xor", "bound", "enter", "ins", "leave", "outs", "popa", "pusha", "arpl", "clts", "lar", "lgdt",
	"lidt", "lldt", "lmsw", "loadall", "lsl", "ltr", "sgdt", "sidt", "sldt", "smsw", "str", "verr", "verw", "bsf", "bsr", "bt",
	"btc", "btr", "bts", "cdq", "cmpsd", "cwde", "ibts", "insd", "iretd", "iret", "iretq", "jecxz", "lfs", "lgs", "lss", "lodsd",
	"loopw", "LOOPEw", "LOOPNEw", "LOOPNZw", "LOOPZw", "loopd", "LOOPEd", "LOOPNEd", "LOOPNZd", "LOOPZd", "movsd", "movsx",
	"movzx", "outsd", "popad", "popfd", "pushad", "pushfd", "scasd", "SETA", "SETAE", "SETB", "SETBE", "SETC", "SETE", 
	"SETG", "SETGE", "SETL", "SETLE", "SETNA", "SETNAE", "SETNB", "SETNBE", "SETNC", "SETNE", "SETNG", "SETNGE", "SETNL", 
	"SETNLE", "SETNO", "SETNP", "SETNS", "SETNZ", "SETO", "SETP", "SETPE", "SETPO", "SETS", "SETZ", "shld", "shrd", "stosd", 
	"xbts", "bswap", "cmpxchg", "invd", "invlpg", "wbinvd", "xadd", "cpuid", "cmpxchg8b", "rdmsr", "rdtsc", "wrmsr", "rsm",
	"rdpmc", "syscall", "sysret", "CMOVA", "CMOVAE", "CMOVB", "CMOVBE", "CMOVC", "CMOVE", "CMOVG", "CMOVGE", "CMOVL", 
	"CMOVLE", "CMOVNA", "CMOVNAE", "CMOVNB", "CMOVNBE", "CMOVNC", "CMOVNE", "CMOVNG", "CMOVNGE", "CMOVNL", "CMOVNLE", 
	"CMOVNO", "CMOVNP", "CMOVNS", "CMOVNZ", "CMOVO", "CMOVP", "CMOVPE", "CMOVPO", "CMOVS", "CMOVZ", "ud2", "sysenter", "sysexit",
	"prefetcht0", "prefetcht1", "prefetcht2", "prefetchnta", "sfence", "clflush", "lfence", "mfence", "movnti", "pause",
	"monitor", "mwait", "crc32", "cdqe", "cqo", "cmpsq", "cmpxchg16b", "jrcxz", "lodsq", "movsxd", "popfq", "pushfq", "rdtscp",
	"scasq", "stosq", "swapgs", "clgi", "invlpga", "skinit", "stgi", "vmload", "vmmcall", "vmrun", "vmsave", "invept", "invvpid",
	"vmfunc", "vmptrld", "vmptrst", "vmclear", "vmread", "vmwrite", "vmcall", "vmlaunch", "vmresume", "vmxoff", "vmxon",
	"lzcnt", "popcnt", "andn", "bextr", "blsi", "blsmsk", "blsr", "tzcnt", "BZHI", "MULX", "PDEP", "PEXT", "RORX", "SARX", 
	"SHRX", "SHLX", "bextr", "blcfill", "blci", "blcic", "blcmsk", "blcs", "blsfill", "blsic", "t1mskc", "tzmsk",
	"PCLMULQDQ", "PCLMULLQLQDQ", "PCLMULHQLQDQ", "PCLMULLQHQDQ", "PCLMULHQHQDQ", "adcx", "adox", "f2xm1", "fabs", "fadd",
	"faddp", "fbld", "fbstp", "fchs", "fclex", "fcom", "fcomp", "fcompp", "fdecstp", "fdisi", "fdiv", "fdivp", "fdivr", "fdivrp",
	"feni", "ffree", "fiadd", "ficom", "ficomp", "fidiv", "fidivr", "fild", "fimul", "fincstp", "finit", "fist", "fistp",
	"fisub", "fisubr", "fld", "fld1", "fldcw", "fldenv", "fldenvw", "fldl2e", "fldl2t", "fldlg2", "fldln2", "fldpi", "fldz", 
	"fmul", "fmulp", "fnclex", "fndisi", "fneni", "fninit", "fnop", "fnsave", "fnsavew", "fnstcw", "fnstenv", "fnstenw", "fnstw",
	"fpatan", "fprem", "fptan", "frndint", "frstor", "frstorw", "fsave", "fsavew", "fscale", "fsqrt", "fst", "fstcw", "fstenv",
	"fsternvw", "fstp", "fstsw", "fsub", "fsubp", "fsubr", "fsubrp", "ftst", "fwait", "fxam", "fxch", "fxtract", "fyl2x", 
	"fyl2xp1", "fsetpm", "fcos", "fldenvd", "fsaved", "fprem1", "frstord", "fsin", "fsincos", "fstenvd", "fucom", "fucomp", 
	"fucompp", "fcmov", "fcomi", "FCMOVB", "FCMOVBE", "FCMOVE", "FCMOVNB", "FCMOVNBE", "FCMOVNE", "FCMOVNU", "FCMOVU",
	"FCOMI", "FCOMIP", "FUCOMI", "FUCOMIP", "fxrstor", "fxsave", "fisttp", "emms", "movd", "movq"]

INSTRUCTIONS.sort(key=len, reverse=True)

CLEFS = [
	"section", "%macro", "%endmacro", "equ", "$", "$$", "times"]

for end in "bwdqt":
	CLEFS.append(f"res{end}")
	CLEFS.append(f"d{end}")
		
CLEFS.sort(key=len, reverse=True)

"""
A CONTINUER :
SIMD instructions
MMX instructions

MMX instructions operate on the mm registers, which are 64 bits wide. They are shared with the FPU registers.
Original MMX instructions

Added with Pentium MMX 
https://en.wikipedia.org/wiki/X86_instruction_listings
"""


#Classes
class ColorParser():
	"""
	Classe de notre parser
	"""
	def __init__(self, ref):
		"""
		Constructeur de la classe
		:param ref: La ref du parent (on va agir sur l'attribut edit)
		"""
		self.ref = ref
		self.colors = []
	
	def parse(self):
		"""
		Va remplir self.colors de tuples (tag, indexDebut, indexEnd)
		"""
		self.colors = []
		text   = self.ref.edit.get(1.0, tk.END).split("\n")
		
		for ligne in range(len(text)):
			#Coloration des registres
			for register in REGISTERS:
				indexs = self.findAll(text[ligne], register)
				for index in indexs:
					rep = ("registre", f"{str(ligne+1)}.{str(index)}", f"{str(ligne+1)}.{str(index+len(register))}")
					self.colors.append(rep)
					
			#Puis des instructions
			for instruction in INSTRUCTIONS:
				indexs = self.findAll(text[ligne], instruction)
				for index in indexs:
					rep = ("instruction", f"{str(ligne+1)}.{str(index)}", f"{str(ligne+1)}.{str(index+len(instruction))}")
					self.colors.append(rep)
					
			#Maintenant des mots clefs de nasm
			for clef in CLEFS:
				indexs = self.findAll(text[ligne], clef)
				for index in indexs:
					rep = ("clef", f"{str(ligne+1)}.{str(index)}", f"{str(ligne+1)}.{str(index+len(clef))}")
					self.colors.append(rep)
			
			#Des strings
			indexs = self.findAll(text[ligne], "'")
			for index in range(0, len(indexs), 2):
				try:
					rep = ("str", f"{str(ligne+1)}.{str(indexs[index])}", f"{str(ligne+1)}.{str(indexs[index+1]+1)}")
				except:
					rep = ("str", f"{str(ligne+1)}.{str(indexs[index])}", f"{str(ligne+1)}.{str(len(text[ligne]))}")
				self.colors.append(rep)
			
			indexs = self.findAll(text[ligne], '"')
			for index in range(0, len(indexs), 2):
				try:
					rep = ("str", f"{str(ligne+1)}.{str(indexs[index])}", f"{str(ligne+1)}.{str(indexs[index+1]+1)}")
				except:
					rep = ("str", f"{str(ligne+1)}.{str(indexs[index])}", f"{str(ligne+1)}.{str(len(text[ligne]))}")
				self.colors.append(rep)
				print(rep)
			
			#Et des commentaires		
			commentaire = text[ligne].find(";")
			if commentaire >= 0:
				rep = ("commentaire", f"{str(ligne+1)}.{str(commentaire)}", f"{str(ligne+1)}.{str(len(text[ligne])-commentaire)}")
				self.colors.append(rep)
		
	def findAll(self, texte, match):
		"""
		Permet de trouver toutes les occurences d'un mot
		:param texte: Le texte total
		:param match: Le pattern à trouver
		:return:      Une liste d'index
		"""
		debut    = 0
		indexs   = []
		lenMatch = len(match)
		
		while True:
			index = texte.find(match, debut)
			if index < 0:
				return indexs
			indexs.append(index)
			debut += index + lenMatch
			
class EditorGui(tk.Tk):
	"""
	Gui de l'application
	"""
	def __init__(self, nom="NASM EDITOR", taille="720x640"):
		"""
		Constructeur
		:param nom:    Le nom de notre screen
		:param taille: La taille de la fenetre
		"""
		self.colorParser = ColorParser(self)
		self.active = True
		self.taille = taille
		tk.Tk.__init__(self)
		self.title(nom)
		self.geometry(taille)
		self.resizable(False, False)
		
		#Attributs
		self.widgets  = []
		self.fileName = tk.StringVar()
		
		#Parametrage
		self.editor()
		self.update()

	def killWidgets(self):
		"""
		Détruit tout les widgets
		"""
		for widget in self.widgets:
			widget.destroy()
		self.widgets = []

	def editor(self):
		"""
		L'éditeur est lancé
		"""
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		
		#Menu
		self.menu = tk.Menu(self)

		self.menuFile = tk.Menu(self.menu, tearoff=0)
		self.menuFile.add_command(label="New", command=self.new)
		self.menuFile.add_command(label="Open", command=self.open)
		self.menuFile.add_command(label="Save", command=self.save)
		self.menuFile.add_separator()
		self.menuFile.add_command(label="Exit", command=self.destroy)
		self.menu.add_cascade(label="File", menu=self.menuFile)

		self.config(menu=self.menu)

		#Fenêtre d'édition
		self.edit = scroll.ScrolledText(self, undo=True, background=bgColor)
		self.widgets.append(self.edit)
		self.edit.grid(row=0, column=0, sticky="nesw")
		
		#On ajoute les tags
		self.addTags()
		
		#Puis les raccourcis (Ctrl + z et Ctrl + mak + z sont déjè actifs)
		self.bind("<Control-s>", self.save)
		self.edit.bind("<Any-KeyPress>", self.color)
	
	def color(self, event=None):
		"""
		Fonction de coloration syntaxique
		"""
		self.colorParser.parse()

		#On enlève les anciens tags
		for tag in self.edit.tag_names():
			self.edit.tag_remove(tag, 1.0, tk.END)
		
		for (tag, debut, fin) in self.colorParser.colors:
			self.edit.tag_add(tag, debut, fin)
		
	
	def addTags(self):
		"""
		Configure correctement les tags
		"""
		self.edit.tag_config("instruction", foreground=instructionColor)
		self.edit.tag_config("registre", foreground=registreColor)
		self.edit.tag_config("commentaire", foreground=commentaireColor)
		self.edit.tag_config("clef", foreground=clefColor)
		self.edit.tag_config("str", foreground=strColor)

	def new(self):
		"""
		Permet de créer un nouveau fichier
		"""
		fileName = tkFile.asksaveasfilename(title="Enregistrer le nouveau fichier sous", defaultextension=".asm")
		try:
			if fileName != "":
				with open(fileName, "w") as myFile:
					self.fileName.set(fileName)
		except:
			tkMess.showerror("Erreur", "Le fichier ne peut pas être écrit")
	
	def open(self):
		"""
		Permet d'ouvrir un fichier
		"""
		fileName = tkFile.askopenfilename(title="Ouvrir le fichier")
		try:
			if fileName != "":
				with open(fileName, "r") as myFile:
					self.fileName.set(fileName)
					self.edit.insert(1.0, myFile.read())			
		except:
			tkMess.showerror("Erreur", "Le fichier ne peut pas être ouvert")

	def save(self, event=None):
		"""
		Permet de sauvegarder le fichier courant
		"""
		try:
			if self.fileName.get() != "":
				with open(self.fileName.get(), "w") as myFile:
					myFile.write(self.edit.get(1.0, tk.END))
				tkMess.showinfo("Sauvegarde", "Le fichier est sauvegardé")
			else:
				self.new()				
		except:
			tkMess.showerror("Erreur", "Le fichier ne peut pas être sauvegardé")

	def clear(self, event=None):
		"""
		On clear les messages
		"""
		self.edit.delete(1.0, tk.END)

	def destroy(self):
		"""
		A la destruction de la fenêtre, on surcharge destroy
		"""
		try:
			self._variable.trace_vdelete('w', self.__tracecb)
		except AttributeError:
			pass
		else:
			del self._variable
		super().destroy()
		self.label  = None
		self.scale  = None
		self.active = False

if __name__ == "__main__":
	c = EditorGui()
	c.mainloop()
