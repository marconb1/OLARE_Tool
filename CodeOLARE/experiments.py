# -*- coding: utf-8 -*-

from PyQt4.QtGui import * 
from PyQt4.QtSql import * 
from PyQt4.QtCore import *
import sys
import csv
import os
import re

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s:s    
    
class Ui_MainWindow(QMainWindow):

    def copyWord(self):
        selectedWord = self.word.toPlainText()
        self.loadExamplesScoreFreqWordDB(selectedWord)

    def clearComboV(self):
        self.comboV.blockSignals(True)
        self.comboV.setCurrentIndex(-1)
        self.comboV.blockSignals(False)
             
    def clearComboADJ(self):
        self.comboADJ.blockSignals(True)
        self.comboADJ.setCurrentIndex(-1)
        self.comboADJ.blockSignals(False)
    
    def clearComboADV(self):
        self.comboADV.blockSignals(True)
        self.comboADV.setCurrentIndex(-1)
        self.comboADV.blockSignals(False)
      
    def clearComboSUBST(self):
        self.comboSUBST.blockSignals(True)
        self.comboSUBST.setCurrentIndex(-1)
        self.comboSUBST.blockSignals(False)
        
    def clearAllCombos(self):
        self.comboV.blockSignals(True)
        self.comboV.setCurrentIndex(-1)
        self.comboV.blockSignals(False)
        
        self.comboSUBST.blockSignals(True)
        self.comboSUBST.setCurrentIndex(-1)
        self.comboSUBST.blockSignals(False)
        
        self.comboADV.blockSignals(True)
        self.comboADV.setCurrentIndex(-1)
        self.comboADV.blockSignals(False)
        
        self.comboADJ.blockSignals(True)
        self.comboADJ.setCurrentIndex(-1)
        self.comboADJ.blockSignals(False)
        
        self.comboNewPolarity.blockSignals(True)
        self.comboNewPolarity.setCurrentIndex(-1)
        self.comboNewPolarity.blockSignals(False)
        
        self.comboQC.blockSignals(True)
        self.comboQC.setCurrentIndex(-1)
        self.comboQC.blockSignals(False)
      
    def loadCategoriesDB(self):
        db = QSqlDatabase.addDatabase("QMYSQL")
        db.setHostName('localhost')
        db.setDatabaseName('GloboNoticias')
        db.setUserName('root')
        db.setPassword('pln')

        if (db.open()==False):     
            QMessageBox.critical(None, "Database Error", db.lastError().text())   
 
        query1 = QSqlQuery ("SELECT DISTINCT Palavra FROM TabelaVAdjAdvSubst WHERE Categoria='Adv.' ORDER BY Palavra ASC;")   
        query2 = QSqlQuery ("SELECT DISTINCT Palavra FROM TabelaVAdjAdvSubst WHERE Categoria='Adj.' ORDER BY Palavra ASC;")
        query3 = QSqlQuery ("SELECT DISTINCT Palavra FROM TabelaVAdjAdvSubst WHERE Categoria='Subst.' ORDER BY Palavra ASC;")
        query4 = QSqlQuery ("SELECT DISTINCT Palavra FROM TabelaVAdjAdvSubst WHERE Categoria='V.' ORDER BY Palavra ASC;")

        index=0
        while (query1.next()):
	    self.comboADV.addItem(query1.value(0).toString())
	    index = index+1
	while (query2.next()):
	    self.comboADJ.addItem(query2.value(0).toString())
	    index = index+1    
        while (query3.next()):
	    self.comboSUBST.addItem(query3.value(0).toString())
	    index = index+1
	while (query4.next()):
	    self.comboV.addItem(query4.value(0).toString())
	    index = index+1
        return db
               
    def loadExamplesScoreFreqWordDB(self,selectedWord_withQuotationMark):
        selectedWord_withoutQuotationMark = self.word.toPlainText()
        selectedWord_withQuotationMark = "'%s'" % selectedWord_withQuotationMark 
  
        queryExampleADV = QSqlQuery ("SELECT DISTINCT Exemplo FROM TabelaAdv WHERE Palavra="+selectedWord_withQuotationMark +";")   
        queryExampleADJ = QSqlQuery ("SELECT DISTINCT Exemplo FROM TabelaAdj WHERE Palavra=" +selectedWord_withQuotationMark + ";")
        queryExampleSUBST = QSqlQuery ("SELECT DISTINCT Exemplo FROM TabelaSubst WHERE Palavra="+selectedWord_withQuotationMark +";")
        queryExampleV = QSqlQuery ("SELECT DISTINCT Exemplo FROM tabelav WHERE Palavra= "+selectedWord_withQuotationMark +" ;")

        queryScore = QSqlQuery ("SELECT Pontuacao FROM TabelaVAdjAdvSubst WHERE Palavra="+selectedWord_withQuotationMark +";")
       
        queryFreqADV = QSqlQuery ("SELECT DISTINCT Frequencia FROM TabelaAdv WHERE Palavra ="+selectedWord_withQuotationMark +";")
        queryFreqV = QSqlQuery ("SELECT DISTINCT Frequencia FROM tabelav WHERE Palavra ="+selectedWord_withQuotationMark +";")
        queryFreqSUBST = QSqlQuery ("SELECT DISTINCT Frequencia FROM TabelaSubst WHERE Palavra ="+selectedWord_withQuotationMark +";")
        queryFreqADJ = QSqlQuery ("SELECT DISTINCT Frequencia FROM TabelaAdj WHERE Palavra ="+selectedWord_withQuotationMark +";")
        
        queryWord = QSqlQuery ("SELECT DISTINCT Palavra FROM TabelaVAdjAdvSubst WHERE Palavra ="+selectedWord_withQuotationMark +";")

        if queryScore.next() == True:
            recebequery = queryScore.value(0).toString()
            self.textoPolaridade.setText(recebequery)
        if queryFreqADV.next() == True:
            freqs = queryFreqADV.value(0).toString()
            self.textoFreq.setText(freqs)
            tag = 'ADV'
            self.textoVariavel.setText(tag)
        if queryFreqV.next() == True:
            freqs = queryFreqV.value(0).toString()        
            self.textoFreq.setText(freqs)
            tag = 'VERB'
            self.textoVariavel.setText(tag)
        if queryFreqADJ.next() == True:
            freqs = queryFreqADJ.value(0).toString()
            self.textoFreq.setText(freqs)
            tag = 'ADJ'
            self.textoVariavel.setText(tag)            
        if queryFreqSUBST.next() == True:
            freqs = queryFreqSUBST.value(0).toString()
            self.textoFreq.setText(freqs)
            tag = 'NOUN'
            self.textoVariavel.setText(tag)
                
        indexADV=0
        indexADJ=0
        indexSUBST=0
        indexV=0
        
        if queryExampleADV.next() == False:
            if queryExampleADJ.next() == False:
	        if queryExampleSUBST.next() == False:
		    if queryExampleV.next() == False:		        
		        self.tableWidget.clearContents()
		        freqs = "It was not found!"
		        self.textoFreq.setText(freqs)
		        self.textoPolaridade.setText(freqs)        
        queryExampleSUBST.previous()
        while (queryExampleSUBST.next() == True):      
            self.tableWidget.setColumnCount(queryExampleSUBST.record().count())
            self.tableWidget.setRowCount(queryExampleSUBST.size())
            self.tableWidget.setItem(indexSUBST,0,QTableWidgetItem(queryExampleSUBST.value(0).toString()))  
            indexSUBST = indexSUBST+1
        queryExampleADV.previous()    
        while (queryExampleADV.next() == True):
            self.tableWidget.setColumnCount(queryExampleADV.record().count())
            self.tableWidget.setRowCount(queryExampleADV.size())
            self.tableWidget.setItem(indexADV,0,QTableWidgetItem(queryExampleADV.value(0).toString()))  
	    indexADV = indexADV+1
        queryExampleADJ.previous()    
        while (queryExampleADJ.next() == True):
            self.tableWidget.setColumnCount(queryExampleADJ.record().count())
            self.tableWidget.setRowCount(queryExampleADJ.size())
            self.tableWidget.setItem(indexADJ,0,QTableWidgetItem(queryExampleADJ.value(0).toString()))            
	    indexADJ = indexADJ+1
        queryExampleV.previous()
        while (queryExampleV.next() == True):
            self.tableWidget.setColumnCount(queryExampleV.record().count())
            self.tableWidget.setRowCount(queryExampleV.size())
            self.tableWidget.setItem(indexV,0,QTableWidgetItem(queryExampleV.value(0).toString()))  
            indexV = indexV+1
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.resizeRowsToContents()
        numsRows = self.tableWidget.rowCount()
        for i in range(numsRows):
	    wordInText = self.tableWidget.item(i,0).text()
	    wordInTextSplit = wordInText.split(' ')
	    for k in range(0,len(wordInTextSplit)):	      
	        wordInTable = wordInTextSplit[k].split(' ')
	        for j in range(0,len(wordInTable)):
	            if wordInTable[j]==selectedWord_withoutQuotationMark:
	                self.tableWidget.item(i,0).setForeground(QBrush(QColor(100,5,130,200)))        
        return selectedWord_withoutQuotationMark
               
    def exportCSV(self):
        path = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV(*.csv)')
        if not path.isEmpty():
            with open(unicode(path), 'wb') as stream:
                writer = csv.writer(stream)
                for row in range(self.table2Widget.rowCount()):
                    rowdata = []
                    for column in range(self.table2Widget.columnCount()):
                        item = self.table2Widget.item(row, column)
                        if item is not None:
                            rowdata.append(unicode(item.text()).encode('utf8'))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
        
    def saveSQL(self):
        saveQC = self.comboQC.currentText()
        saveWord = self.word.toPlainText()
        saveNewPolarity = self.comboNewPolarity.currentText()
        
        textoPalavra = self.word.toPlainText()
        textoPolaridade = self.textoPolaridade.toPlainText()
        textoFreq = self.textoFreq.toPlainText()
        textoQC = self.textoQC.toPlainText()
        textoVariavelCategoria = self.textoVariavel.toPlainText()
        
        lastrow = self.table2Widget.rowCount()

        self.table2Widget.insertRow(lastrow)
        null = ''
        item0 = QTableWidgetItem(textoPalavra)
        item1 = QTableWidgetItem(textoVariavelCategoria)
        item2 = QTableWidgetItem(null)
        item3 = QTableWidgetItem(textoPolaridade)
        item4 = QTableWidgetItem(saveNewPolarity)
        item5 = QTableWidgetItem(textoFreq)        
        item6 = QTableWidgetItem(saveQC)
        item7 = QTableWidgetItem(null)
        item8 = QTableWidgetItem(null)
                
        self.table2Widget.setItem(lastrow,0,item0)
        self.table2Widget.setItem(lastrow,1,item1)
        self.table2Widget.setItem(lastrow,2,item2)
        self.table2Widget.setItem(lastrow,3,item3)
        self.table2Widget.setItem(lastrow,4,item4)
        self.table2Widget.setItem(lastrow,5,item5)
        self.table2Widget.setItem(lastrow,6,item6)
        self.table2Widget.setItem(lastrow,7,item7)
        self.table2Widget.setItem(lastrow,8,item8)        
        
        if (lastrow%2==0):
            self.table2Widget.item(lastrow, 0).setData(Qt.BackgroundRole, QColor(255, 250, 205))
            self.table2Widget.item(lastrow, 1).setData(Qt.BackgroundRole, QColor(255, 250, 205))
            self.table2Widget.item(lastrow, 2).setData(Qt.BackgroundRole, QColor(255, 250, 205))
            self.table2Widget.item(lastrow, 3).setData(Qt.BackgroundRole, QColor(255, 250, 205))
            self.table2Widget.item(lastrow, 4).setData(Qt.BackgroundRole, QColor(255, 250, 205))
            self.table2Widget.item(lastrow, 5).setData(Qt.BackgroundRole, QColor(255, 250, 205))
            self.table2Widget.item(lastrow, 6).setData(Qt.BackgroundRole, QColor(255, 250, 205))
            self.table2Widget.item(lastrow, 7).setData(Qt.BackgroundRole, QColor(255, 250, 205))
            self.table2Widget.item(lastrow, 8).setData(Qt.BackgroundRole, QColor(255, 250, 205))
        else: 
            self.table2Widget.item(lastrow, 0).setData(Qt.BackgroundRole, QColor(238, 221, 130))
            self.table2Widget.item(lastrow, 1).setData(Qt.BackgroundRole, QColor(238, 221, 130))
            self.table2Widget.item(lastrow, 2).setData(Qt.BackgroundRole, QColor(238, 221, 130))
            self.table2Widget.item(lastrow, 3).setData(Qt.BackgroundRole, QColor(238, 221, 130))
            self.table2Widget.item(lastrow, 4).setData(Qt.BackgroundRole, QColor(238, 221, 130))
            self.table2Widget.item(lastrow, 5).setData(Qt.BackgroundRole, QColor(238, 221, 130))
            self.table2Widget.item(lastrow, 6).setData(Qt.BackgroundRole, QColor(238, 221, 130))
            self.table2Widget.item(lastrow, 7).setData(Qt.BackgroundRole, QColor(238, 221, 130))
            self.table2Widget.item(lastrow, 8).setData(Qt.BackgroundRole, QColor(238, 221, 130))

        saveWord = "'%s'" % saveWord
        saveNewPolarity = "'%s'" % saveNewPolarity
        if saveQC != '/':
            query = QSqlQuery ("UPDATE TabelaVAdjAdvSubst SET NovaPolaridade = "+saveNewPolarity+" WHERE Palavra="+saveWord+";")
        saveQC = "'%s'" % saveQC
        if saveQC != '/':
            query = QSqlQuery ("UPDATE TabelaVAdjAdvSubst SET ColunaQC = "+saveQC+" WHERE Palavra="+saveWord+";")
        self.table2Widget.horizontalHeader().setStretchLastSection(True)
        self.table2Widget.resizeRowsToContents()    
        
    def remove(self):
         self.table2Widget.removeRow(self.table2Widget.currentRow())
         
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(2000, 1000)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.ButOpenBanco = QPushButton(self.centralwidget)
        self.ButOpenBanco.setGeometry(QRect(50,55,475,40))
        self.ButOpenBanco.setObjectName(_fromUtf8("re"))
        self.ButOpenBanco.setStyleSheet('color:#274257;font: bold;background-color:#D4E7ED;border:1px solid black;')
        
        self.ButClearTabela = QPushButton(self.centralwidget)
        self.ButClearTabela.setGeometry(QRect(1070,55,180,40))
        self.ButClearTabela.setObjectName(_fromUtf8("re3"))
        self.ButClearTabela.setStyleSheet('color:#274257;font: bold;background-color:#D4E7ED;border:1px solid black;')

        self.ButREMOVE = QPushButton(self.centralwidget)
        self.ButREMOVE.setGeometry(QRect(50,565,145,30))
        self.ButREMOVE.setObjectName(_fromUtf8("op"))
        self.ButREMOVE.setStyleSheet('color:#274257;font: bold;background-color:#D4E7ED;border: 1px solid black;')
        
        self.ExportCsV = QPushButton(self.centralwidget)
        self.ExportCsV.setGeometry(QRect(1070,140,180,40))
        self.ExportCsV.setObjectName(_fromUtf8("op"))
        self.ExportCsV.setStyleSheet('color:#274257;font: bold;background-color:#D4E7ED;border: 1px solid black;')
        
        self.SaveSqL = QPushButton(self.centralwidget)
        self.SaveSqL.setGeometry(QRect(1070,97,180,40))
        self.SaveSqL.setObjectName(_fromUtf8("op2"))
        self.SaveSqL.setStyleSheet('color:#274257;font: bold;background-color:#D4E7ED;border: 1px solid black;')

        self.comboADV = QComboBox(self.centralwidget)
        self.comboADV.setGeometry(QRect(50, 145, 111, 31))
        self.comboADV.setObjectName(_fromUtf8("comboADV"))
        self.comboADV.addItem(_fromUtf8(""))
        self.comboADV.setStyleSheet('color:rgb(10);border:1px solid black;')

        self.comboADJ = QComboBox(self.centralwidget)
        self.comboADJ.setGeometry(QRect(170, 145, 111, 31))
        self.comboADJ.setObjectName(_fromUtf8("comboADJ"))
        self.comboADJ.addItem(_fromUtf8(""))
        self.comboADJ.setStyleSheet('color:rgb(10);border:1px solid black;')
        
        self.comboSUBST = QComboBox(self.centralwidget)
        self.comboSUBST.setGeometry(QRect(290, 145, 111, 31))
        self.comboSUBST.setObjectName(_fromUtf8("comboSUBST"))
        self.comboSUBST.addItem(_fromUtf8(""))
        self.comboSUBST.setStyleSheet('color:rgb(10);border:1px solid black;')
        
        self.comboV = QComboBox(self.centralwidget)
        self.comboV.setGeometry(QRect(410, 145, 111, 31))
        self.comboV.setObjectName(_fromUtf8("comboV"))
        self.comboV.addItem(_fromUtf8(""))
        self.comboV.setStyleSheet('color:rgb(10);border:1px solid black;')
        
        self.comboQC = QComboBox(self.centralwidget)
        self.comboQC.setGeometry(QRect(721, 145, 111, 31))
        self.comboQC.setObjectName(_fromUtf8("comboQC"))
        self.comboQC.addItem(_fromUtf8(""))
        self.comboQC.setStyleSheet('color:rgb(10);border:1px solid black;')
        
        self.comboNewPolarity = QComboBox(self.centralwidget)
        self.comboNewPolarity.setGeometry(QRect(600, 145, 111, 31))
        self.comboNewPolarity.setObjectName(_fromUtf8("comboPO"))
        self.comboNewPolarity.addItem(_fromUtf8(""))
        self.comboNewPolarity.setStyleSheet('color:rgb(10);border:1px solid black;')

        self.labelADV = QLabel(self.centralwidget)
        self.labelADV.setGeometry(QRect(65, 125, 75, 17))
        self.labelADV.setObjectName(_fromUtf8("labelADV"))
        self.labelADV.setStyleSheet('color:#274257;font: bold')
        
        self.labelADJ = QLabel(self.centralwidget)
        self.labelADJ.setGeometry(QRect(175, 125, 83, 17))
        self.labelADJ.setObjectName(_fromUtf8("labelADJ"))
        self.labelADJ.setStyleSheet('color:#274257;font: bold')
        
        self.labelSUBST = QLabel(self.centralwidget)
        self.labelSUBST.setGeometry(QRect(315, 125, 60, 17))
        self.labelSUBST.setObjectName(_fromUtf8("labelSUBST"))
        self.labelSUBST.setStyleSheet('color:#274257;font: bold')
        
        self.labelV = QLabel(self.centralwidget)
        self.labelV.setGeometry(QRect(435, 125, 60, 17))
        self.labelV.setObjectName(_fromUtf8("labelV"))
        self.labelV.setStyleSheet('color:#274257;font: bold')
        
        self.labelPalavra = QLabel(self.centralwidget)
        self.labelPalavra.setGeometry(QRect(600, 55, 60, 20))
        self.labelPalavra.setObjectName(_fromUtf8("labelPalavra"))
        self.labelPalavra.setStyleSheet('color:#274257;font: bold')
        
        self.labelPolaridade = QLabel(self.centralwidget)
        self.labelPolaridade.setGeometry(QRect(721, 55, 80, 20))
        self.labelPolaridade.setObjectName(_fromUtf8("labelPolaridade"))
        self.labelPolaridade.setStyleSheet('color:#274257;font: bold')

        self.labelFrequencia = QLabel(self.centralwidget)
        self.labelFrequencia.setGeometry(QRect(842, 55, 80, 20))
        self.labelFrequencia.setObjectName(_fromUtf8("labelFrequencia"))
        self.labelFrequencia.setStyleSheet('color:#274257;font: bold')
        
        self.labelNewPolarity = QLabel(self.centralwidget)
        self.labelNewPolarity.setGeometry(QRect(600,125 , 100, 20))
        self.labelNewPolarity.setObjectName(_fromUtf8("labelNewPolarity"))
        self.labelNewPolarity.setStyleSheet('color:#274257;font: bold')
        
        self.labelQC = QLabel(self.centralwidget)
        self.labelQC.setGeometry(QRect(721, 125, 80, 20))
        self.labelQC.setObjectName(_fromUtf8("labelQC"))
        self.labelQC.setStyleSheet('color:#274257;font: bold')
        
        self.word = QTextEdit(self.centralwidget)
        self.word.setGeometry(QRect(600,80,111,30))
        self.word.setObjectName(_fromUtf8("text"))
        self.word.setStyleSheet('color:rgb(10);border:1px solid black;')
        
        self.textoQC = QTextEdit(self.centralwidget)
        self.textoQC.setGeometry(QRect(0,0,0,0))
        
        self.textoVariavel = QTextEdit(self.centralwidget)
        self.textoVariavel.setGeometry(QRect(0,0,0,0))

        self.textoPolaridade = QTextEdit(self.centralwidget)
        self.textoPolaridade.setGeometry(QRect(721,80,111,30))
        self.textoPolaridade.setObjectName(_fromUtf8("polaridade"))
        self.textoPolaridade.setStyleSheet('color:rgb(10);border:1px solid black;')
        
        self.textoFreq = QTextEdit(self.centralwidget)
        self.textoFreq.setGeometry(QRect(842,80,140,50))
        self.textoFreq.setObjectName(_fromUtf8("frequencia"))
        self.textoFreq.setStyleSheet('color:rgb(10);border:1px solid black;')
           
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QRect(50, 180, 1200, 380))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setStyleSheet('color:rgb(10);border:1px solid black;')
        self.tableWidget.setColumnCount(1)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        
        self.table2Widget = QTableWidget(self.centralwidget)
        self.table2Widget.setGeometry(QRect(50, 600, 1200, 210))
        self.table2Widget.setObjectName(_fromUtf8("table2Widget"))
        self.table2Widget.setStyleSheet('color:rgb(10);border:1px solid black;')
        self.table2Widget.setColumnCount(9)  
        
        item = QTableWidgetItem()
        self.table2Widget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.table2Widget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.table2Widget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.table2Widget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.table2Widget.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.table2Widget.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.table2Widget.setHorizontalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.table2Widget.setHorizontalHeaderItem(7, item)
        item = QTableWidgetItem()
        self.table2Widget.setHorizontalHeaderItem(8, item)
        
        item = QTableWidgetItem()
        self.table2Widget.setItem(0,0, item)
        item = QTableWidgetItem()
        self.table2Widget.setItem(1,1, item)
        item = QTableWidgetItem()
        self.table2Widget.setItem(2,2, item)
        item = QTableWidgetItem()
        self.table2Widget.setItem(3,3, item)
        item = QTableWidgetItem()
        self.table2Widget.setItem(4,4, item)
        item = QTableWidgetItem()
        self.table2Widget.setItem(5,5, item)
        item = QTableWidgetItem()
        self.table2Widget.setItem(6,6, item)
        item = QTableWidgetItem()
        self.table2Widget.setItem(7,7, item)
        item = QTableWidgetItem()
        self.table2Widget.setItem(8,8, item)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.labelPolaridade.setText(QApplication.translate("MainWindow", "Polarity", None, QApplication.UnicodeUTF8))
        self.labelPalavra.setText(QApplication.translate("MainWindow", "Word", None, QApplication.UnicodeUTF8))
        self.labelADV.setText(QApplication.translate("MainWindow", "ADV", None, QApplication.UnicodeUTF8))
        self.labelADJ.setText(QApplication.translate("MainWindow", "ADJ", None, QApplication.UnicodeUTF8))
        self.labelSUBST.setText(QApplication.translate("MainWindow", "NOUN", None, QApplication.UnicodeUTF8))
        self.labelV.setText(QApplication.translate("MainWindow", "VERB", None, QApplication.UnicodeUTF8))
        self.labelNewPolarity.setText(QApplication.translate("MainWindow", "NewPolarity", None, QApplication.UnicodeUTF8))
        self.labelQC.setText(QApplication.translate("MainWindow", "Q/C", None, QApplication.UnicodeUTF8))
        self.labelFrequencia.setText(QApplication.translate("MainWindow", "Frequency", None, QApplication.UnicodeUTF8))
        self.ExportCsV.setText(QApplication.translate("MainWindow", "Export as CSV", None, QApplication.UnicodeUTF8))
        self.SaveSqL.setText(QApplication.translate("MainWindow", "Save SQL", None, QApplication.UnicodeUTF8))
        self.ButOpenBanco.setText(QApplication.translate("MainWindow", "Load Categories", None, QApplication.UnicodeUTF8))
        self.ButClearTabela.setText(QApplication.translate("MainWindow", "Clean All!", None, QApplication.UnicodeUTF8))
        self.ButREMOVE.setText(QApplication.translate("MainWindow", "Remove Line", None, QApplication.UnicodeUTF8))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(QApplication.translate("MainWindow", "Examples", None, QApplication.UnicodeUTF8))
        
        item = self.table2Widget.horizontalHeaderItem(0)
        item.setText(QApplication.translate("MainWindow", "Words", None, QApplication.UnicodeUTF8))
        
        item = self.table2Widget.horizontalHeaderItem(3)
        item.setText(QApplication.translate("MainWindow", "Polarity", None, QApplication.UnicodeUTF8))
        
        item = self.table2Widget.horizontalHeaderItem(5)
        item.setText(QApplication.translate("MainWindow", "Frequency", None, QApplication.UnicodeUTF8))
        
        item = self.table2Widget.horizontalHeaderItem(4)
        item.setText(QApplication.translate("MainWindow", "NewPolarity", None, QApplication.UnicodeUTF8))
        
        item = self.table2Widget.horizontalHeaderItem(6)
        item.setText(QApplication.translate("MainWindow", "Q/C", None, QApplication.UnicodeUTF8))
        
        item = self.table2Widget.horizontalHeaderItem(1)
        item.setText(QApplication.translate("MainWindow", "Category", None, QApplication.UnicodeUTF8))
        
        item = self.table2Widget.horizontalHeaderItem(2)
        item.setText(QApplication.translate("MainWindow", "NewCategory", None, QApplication.UnicodeUTF8))
        
        item = self.table2Widget.horizontalHeaderItem(7)
        item.setText(QApplication.translate("MainWindow", "Expression", None, QApplication.UnicodeUTF8))
        
        item = self.table2Widget.horizontalHeaderItem(8)
        item.setText(QApplication.translate("MainWindow", "PS", None, QApplication.UnicodeUTF8))

        QMetaObject.connectSlotsByName(MainWindow)
        QObject.connect(self.ButOpenBanco , SIGNAL("clicked()"), self.loadCategoriesDB)
        QObject.connect(self.comboQC, SIGNAL(_fromUtf8("activated(QString)")), self.textoQC.setText)
        QObject.connect(self.comboADJ, SIGNAL(_fromUtf8("activated(QString)")), self.word.setText)
        QObject.connect(self.comboADV, SIGNAL(_fromUtf8("activated(QString)")), self.word.setText)
        QObject.connect(self.comboV, SIGNAL(_fromUtf8("activated(QString)")), self.word.setText)
        QObject.connect(self.comboSUBST, SIGNAL(_fromUtf8("activated(QString)")), self.word.setText)
        QObject.connect(self.word, SIGNAL(_fromUtf8("textChanged()")), self.copyWord)     
        QObject.connect(self.ButClearTabela, SIGNAL(_fromUtf8("clicked()")), self.tableWidget.clearContents)
        QObject.connect(self.ButClearTabela, SIGNAL(_fromUtf8("clicked()")), self.clearAllCombos)
        QObject.connect(self.ButClearTabela, SIGNAL(_fromUtf8("clicked()")), self.word.clear)
        QObject.connect(self.ButClearTabela, SIGNAL(_fromUtf8("clicked()")), self.textoFreq.clear) 
        QObject.connect(self.ButClearTabela, SIGNAL(_fromUtf8("clicked()")), self.textoPolaridade.clear)
        QObject.connect(self.comboADJ, SIGNAL("currentIndexChanged(const QString&)"), self.clearComboV)
        QObject.connect(self.comboADV, SIGNAL("currentIndexChanged(const QString&)"), self.clearComboV)
        QObject.connect(self.comboSUBST, SIGNAL("currentIndexChanged(const QString&)"), self.clearComboV)       
        QObject.connect(self.comboV, SIGNAL("currentIndexChanged(const QString&)"), self.clearComboADJ)
        QObject.connect(self.comboADV, SIGNAL("currentIndexChanged(const QString&)"), self.clearComboADJ)
        QObject.connect(self.comboSUBST, SIGNAL("currentIndexChanged(const QString&)"), self.clearComboADJ)  
        QObject.connect(self.comboADJ, SIGNAL("currentIndexChanged(const QString&)"), self.clearComboADV)
        QObject.connect(self.comboV, SIGNAL("currentIndexChanged(const QString&)"), self.clearComboADV)
        QObject.connect(self.comboSUBST, SIGNAL("currentIndexChanged(const QString&)"), self.clearComboADV)      
        QObject.connect(self.comboADJ, SIGNAL("currentIndexChanged(const QString&)"), self.clearComboSUBST)
        QObject.connect(self.comboADV, SIGNAL("currentIndexChanged(const QString&)"), self.clearComboSUBST)
        QObject.connect(self.comboV, SIGNAL("currentIndexChanged(const QString&)"), self.clearComboSUBST)
        QObject.connect(self.ExportCsV , SIGNAL("clicked()"), self.exportCSV)
        QObject.connect(self.SaveSqL , SIGNAL("clicked()"), self.saveSQL)
        QObject.connect(self.ButREMOVE , SIGNAL("clicked()"), self.remove)
        
        listQC = [self.tr('Q'),self.tr('C'),]
        self.comboQC.clear()
        self.comboQC.addItems(listQC)
        
        listNewPolarity = [self.tr('+'),self.tr('-'),self.tr('0'),]
        self.comboNewPolarity.clear()
        self.comboNewPolarity.addItems(listNewPolarity)
        
def isAlive(qobj):    
    import sip
    try:        
        sip.unwrapinstance(qobj)
    except RuntimeError:
        return False
    return True
    
if __name__ == "__main__":
    import sys
 
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    MainWindow.show()
    sys.exit(app.exec_())
