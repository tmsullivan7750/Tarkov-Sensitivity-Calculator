from PyQt5 import QtWidgets
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QComboBox, QWidget, QVBoxLayout
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate('./tarkovcalculator-firebase-adminsdk-4jy8a-161e7a078c.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
helmets = []
faceshields = []
armors = []
extras = []
inputSensitivity = 0
inputAimingSensitivity = 0
calculatedSensitivity = inputSensitivity
calculatedAimingSensitivity = inputAimingSensitivity
helmetMultiplier = 0
faceshieldMultiplier = 0
armorMultiplier = 0
extraMultiplier = 0

class helmet:
	def __init__(self,name,movement,turning):
		self.name = name
		self.movement = movement
		self.turning = turning

class faceshield:
	def __init__(self,name,movement,turning):
		self.name = name
		self.movement = movement
		self.turning = turning

class armor:
	def __init__(self,name,movement,turning):
		self.name = name
		self.movement = movement
		self.turning = turning

class extra:
	def __init__(self,name,movement,turning):
		self.name = name
		self.movement = movement
		self.turning = turning

###############-POPULATE HELMET LIST-##########################
helmets_ref = db.collection('Helmets')
docs = helmets_ref.stream()

helmets.append(helmet("N/A","0","0"))
for doc in docs:
	tempName = u'{}'.format(doc.to_dict()['name'])
	tempMovement = u'{}'.format(doc.to_dict()['movement'])
	tempTurning = u'{}'.format(doc.to_dict()['turning'])
	helmets.append(helmet(tempName,tempMovement,tempTurning))
##################################################################

###############-POPULATE FACESHIELD LIST-##########################
faceshield_ref = db.collection('Faceshields')
docs2 = faceshield_ref.stream()

faceshields.append(faceshield("N/A","0","0"))
for doc in docs2:
	tempName = u'{}'.format(doc.to_dict()['name'])
	tempMovement = u'{}'.format(doc.to_dict()['movement'])
	tempTurning = u'{}'.format(doc.to_dict()['turning'])
	faceshields.append(faceshield(tempName,tempMovement,tempTurning))
##################################################################

###############-POPULATE ARMOR LIST-##########################
armor_ref = db.collection('Armor')
docs3 = armor_ref.stream()

armors.append(armor("N/A","0","0"))
for doc in docs3:
	tempName = u'{}'.format(doc.to_dict()['name'])
	tempMovement = u'{}'.format(doc.to_dict()['movement'])
	tempTurning = u'{}'.format(doc.to_dict()['turning'])
	armors.append(armor(tempName,tempMovement,tempTurning))
##################################################################

###############-POPULATE ARMOR LIST-##########################
extra_ref = db.collection('Extras')
docs4 = extra_ref.stream()

extras.append(extra("N/A","0","0"))
for doc in docs4:
	tempName = u'{}'.format(doc.to_dict()['name'])
	tempMovement = u'{}'.format(doc.to_dict()['movement'])
	tempTurning = u'{}'.format(doc.to_dict()['turning'])
	extras.append(extra(tempName,tempMovement,tempTurning))
##################################################################

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.helmetSelect = QComboBox()
		for helmet in helmets:
			self.helmetSelect.addItem(helmet.name)

		self.faceshieldSelect = QComboBox()
		for faceshield in faceshields:
			self.faceshieldSelect.addItem(faceshield.name)	

		self.extraSelect = QComboBox()
		for extra in extras:
			self.extraSelect.addItem(extra.name)	

		self.armorSelect = QComboBox()
		for armor in armors:
			self.armorSelect.addItem(armor.name)

		self.userInputSens = QLineEdit()
		self.userInputSens.setValidator(QDoubleValidator(0.00,20.00,2))
		self.userInputSens.setMaxLength(4)

		self.userInputAimSens = QLineEdit()
		self.userInputAimSens.setValidator(QDoubleValidator(0.00,20.00,2))
		self.userInputAimSens.setMaxLength(4)

		self.inputSensTitle = QLabel("Input Sensitivity",self)
		self.inputAimSensTitle = QLabel("Input Aiming Sensitivity",self)
		self.helmetTitle = QLabel("Helmet",self)
		self.faceshieldTitle = QLabel("Faceshield",self)
		self.extraTitle = QLabel("Extras",self)
		self.armorTitle = QLabel("Armor",self)
		self.calcSensTitle = QLabel("Calculated Sensitivity",self)
		self.calcAimSensTitle = QLabel("Calculated Aiming Sensitivity",self)
		self.calcSens = QLabel(str(calculatedSensitivity),self)
		self.calcAimSens = QLabel(str(calculatedAimingSensitivity),self)

		layout = QVBoxLayout()
		layout.addWidget(self.inputSensTitle)
		layout.addWidget(self.userInputSens)
		layout.addWidget(self.inputAimSensTitle)
		layout.addWidget(self.userInputAimSens)
		layout.addWidget(self.helmetTitle)
		layout.addWidget(self.helmetSelect)
		layout.addWidget(self.faceshieldTitle)
		layout.addWidget(self.faceshieldSelect)
		layout.addWidget(self.extraTitle)
		layout.addWidget(self.extraSelect)
		layout.addWidget(self.armorTitle)
		layout.addWidget(self.armorSelect)
		layout.addWidget(self.calcSensTitle)
		layout.addWidget(self.calcSens)
		layout.addWidget(self.calcAimSensTitle)
		layout.addWidget(self.calcAimSens)


		container = QWidget()
		container.setLayout(layout)

		self.userInputSens.textChanged.connect(self.getInputSens)
		self.userInputAimSens.textChanged.connect(self.getInputAimingSens)
		self.helmetSelect.currentIndexChanged.connect(self.checkHelmet)
		self.faceshieldSelect.currentIndexChanged.connect(self.checkFaceshield)
		self.extraSelect.currentIndexChanged.connect(self.checkExtra)
		self.armorSelect.currentIndexChanged.connect(self.checkArmor)

		self.setCentralWidget(container)

	def checkHelmet(self, index):
		global helmetMultiplier
		helmetMultiplier = helmets[int(index)].turning
		self.calculateSens()

	def checkFaceshield(self, index):
		global faceshieldMultiplier
		faceshieldMultiplier = faceshields[int(index)].turning
		self.calculateSens()

	def checkExtra(self, index):
		global extraMultiplier
		extraMultiplier = extras[int(index)].turning
		self.calculateSens()

	def checkArmor(self, index):
		global armorMultiplier
		armorMultiplier = armors[int(index)].turning
		self.calculateSens()

	def getInputSens(self,text):
		global inputSensitivity
		inputSensitivity = text
		self.calculateSens()

	def getInputAimingSens(self,text):
		global inputAimingSensitivity
		inputAimingSensitivity = text
		self.calculateSens()

	def calculateSens(self):
		if inputSensitivity != "."  and inputAimingSensitivity != ".":
			totalSensMultiplier = float(armorMultiplier)+float(faceshieldMultiplier)+float(helmetMultiplier)+float(extraMultiplier)
			sensChange = float(-1) * float(inputSensitivity) * totalSensMultiplier
			aimSensChange= float(-1) * float(inputAimingSensitivity) * totalSensMultiplier
			calculatedSensitivity = float(inputSensitivity) + float(sensChange)
			calculatedAimingSensitivity = float(inputAimingSensitivity) + float(aimSensChange)
			finalcalculatedSensitivity = str(round(calculatedSensitivity,2))
			finalcalculatedAimingSensitivity  = str(round(calculatedAimingSensitivity,2))
			self.calcSens.setText(str(finalcalculatedSensitivity))
			self.calcAimSens.setText(str(finalcalculatedAimingSensitivity))


app = QApplication(sys.argv)
win = MainWindow()
#win.setGeometry(200,200,600,600)
win.setWindowTitle("Tarkov Sensitivity Calculator")
win.show()
sys.exit(app.exec_())