from PyQt5 import QtCore, QtGui, QtWidgets #, QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
import sys
import os
import helloworld
from OSGridConverter import grid2latlong
from decimal import Decimal
import webbrowser
import folium
import io
import csv
from string import ascii_letters

class ConverterApp(QtWidgets.QMainWindow, helloworld.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ConverterApp, self).__init__(parent)
        self.setupUi(self)
        self.convert_btn.clicked.connect(self.calculatelatlon)
        self.pushButton.clicked.connect(self.map_button)
        self.exit_btn.clicked.connect(self.exit_button)
        self.clear_btn.clicked.connect(self.clear_button)
        self.fileopen_btn.clicked.connect(self.fileopen_button)
        self.outputcsv_btn.clicked.connect(self.generatecsv)
        global prefix_dict
        prefix_dict = {
            "00": "SV",
            "01": "SQ",
            "02": "SL",
            "03": "SF",
            "04": "SA",
            "05": "NV",
            "06": "NQ",
            "07": "NL",
            "08": "NF",
            "09": "NA",
            "010": "HV",
            "011": "HQ",
            "012": "HL",
            "10": "SW",
            "11": "SR",
            "12": "SM",
            "13": "SG",
            "14": "SB",
            "15": "NW",
            "16": "NR",
            "17": "NM",
            "18": "NG",
            "19": "NB",
            "110": "HW",
            "111": "HR",
            "112": "HM",
            "20": "SX",
            "21": "SS",
            "22": "SN",
            "23": "SH",
            "24": "SC",
            "25": "NX",
            "26": "NS",
            "27": "NN",
            "28": "NH",
            "29": "NC",
            "210": "HX",
            "211": "HS",
            "212": "HN",
            "30": "HY",
            "31": "ST",
            "32": "SO",
            "33": "SJ",
            "34": "SD",
            "35": "NY",
            "36": "NT",
            "37": "NO",
            "38": "NJ",
            "39": "ND",
            "310": "HY",
            "311": "HT",
            "312": "HO",
            "40": "SZ",
            "41": "SU",
            "42": "SP",
            "43": "SK",
            "44": "SE",
            "45": "NZ",
            "46": "NU",
            "47": "NP",
            "48": "NK",
            "49": "NE",
            "410": "HZ",
            "411": "HU",
            "412": "HP",
            "50": "TV",
            "51": "TQ",
            "52": "TL",
            "53": "TF",
            "54": "TA",
            "55": "OV",
            "56": "OQ",
            "57": "OL",
            "58": "OF",
            "59": "OA",
            "510": "JV",
            "511": "JQ",
            "512": "JL",
            "60": "TW",
            "61": "TR",
            "62": "TM",
            "63": "TG",
            "64": "TB",
            "65": "OW",
            "66": "OR",
            "67": "OM",
            "68": "OG",
            "69": "OB",
            "610": "JW",
            "611": "JR",
            "612": "JM",
            "70": "TX",
            "71": "TS",
            "72": "TN",
            "73": "TH",
            "74": "TC",
            "75": "OX",
            "76": "OS",
            "77": "ON",
            "78": "OH",
            "79": "OC",
            "710": "JX",
            "711": "JS",
            "712": "JN"
        }

    def calculatelatlon(self):
        east_in = self.eastings_input.text()
        north_in = self.northings_input.text()
        if str(east_in).isdigit() and len(str(east_in)) == 6 and str(north_in).isdigit() and len(str(north_in)) in [6,7]:
            if len(str(north_in)) == 7:
                prefix_one = east_in[0] + north_in[0:2]
                northing = north_in[2:7]
            else:
                prefix_one = east_in[0] + north_in[0]
                northing = north_in[1:7]
            prefix = prefix_dict[prefix_one]
            easting = east_in[1:7]
            l = grid2latlong(prefix + ' ' + easting + ' ' + northing)
            self.result_lat.setText(str(l.latitude))
            self.result_lon.setText(str(l.longitude))
            global latitude
            latitude = str(l.latitude)
            global longitude
            longitude = str(l.longitude)
            global googleurl
            googleurl ='https://maps.google.com/?q=' + str(l.latitude) + ',' + str(l.longitude)
            self.google_url_box.setText(str(googleurl))
        else:
            errormsg = QMessageBox()
            errormsg.setIcon(QMessageBox.Critical)
            errormsg.setText("Error")
            errormsg.setInformativeText('Please Check the Easting and Northings.')
            errormsg.setWindowTitle("Error")
            errormsg.exec_()

    def map_button(self):
        if 'latitude' in globals() or 'longitude' in globals():
            m = folium.Map(location=[latitude, longitude], zoom_start=15)
            folium.Marker([latitude, longitude]).add_to(m)
            data = io.BytesIO()
            m.save(data, close_file=False)
            web_engine = QWebEngineView() #QtWebEngineWidgets.QWebEngineView()
            self.web_engine.setHtml(data.getvalue().decode())
            #self.web_engine.load(QtCore.QUrl(googleurl))
        else:
            errormsg = QMessageBox()
            errormsg.setIcon(QMessageBox.Critical)
            errormsg.setText("Error")
            errormsg.setInformativeText('Please Check the Easting and Northings.')
            errormsg.setWindowTitle("Error")
            errormsg.exec_()

    def fileopen_button(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        global fileName
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "csv(*.csv)", options=options)
        out_file = "Chosen Input File: " + os.path.basename(fileName)
        self.text_output.setText(str(out_file))
        global dropdown
        with open(fileName, "r") as f:
            reader = csv.DictReader(f)
            dropdown = reader.fieldnames
        f.close()
        self.choose_eastings.addItems(dropdown)
        global eastingsfield
        self.choose_northings.addItems(dropdown)
        global northingsfield

    def generatecsv(self):
        outputfilename = self.output_filename.text()
        if set(outputfilename).difference(ascii_letters):
            errormsg = QMessageBox()
            errormsg.setIcon(QMessageBox.Critical)
            errormsg.setText("Error")
            errormsg.setInformativeText('Please check your filename for special characters.')
            errormsg.setWindowTitle("Error")
            errormsg.exec_()
        else:
            #eastingsfield = self.choose_eastings.currentText()
            eastings_index = self.choose_eastings.currentIndex()
            #northingsfield = self.choose_northings.currentText()
            northings_index = self.choose_northings.currentIndex()
            working_dir = os.path.dirname(fileName)
            out = working_dir + "/" + outputfilename + ".csv"
            with open(fileName, "r") as csv_input:
                with open(out, 'w') as csv_output:
                    writer = csv.writer(csv_output, lineterminator='\n')
                    reader = csv.reader(csv_input, delimiter=',')
                    all =[]
                    row = next(reader)
                    row.append('latitude')
                    row.append('longitude')
                    all.append(row)
                    for row in reader:
                        east = row[eastings_index]
                        north = row[northings_index]
                        if str(east).isdigit() and len(str(east)) == 6 and str(north).isdigit() and len(str(north)) in [6, 7]:
                            if len (str(north)) == 7:
                                prefix_one = east[0] + north[0:2]
                                northing = north[1:7]
                            else:
                                prefix_one = east[0] + north[0]
                                northing = north[1:7]
                            prefix = prefix_dict[prefix_one]
                            easting = east[1:7]
                            l = grid2latlong(prefix + ' ' + easting + ' ' + northing)
                            latitude = str(l.latitude)
                            longitude = str(l.longitude)
                            row.append(latitude)
                            row.append(longitude)
                            all.append(row)
                        else:
                            latitude = "##ERROR##"
                            longitude = "##ERROR##"
                            row.append(latitude)
                            row.append(longitude)
                            all.append(row)
                    writer.writerows(all)
                    self.text_output.setText("Complete.")
         
    def exit_button(self):
         QtCore.QCoreApplication.instance().quit()
         
    def clear_button(self):
         self.eastings_input.clear()
         self.northings_input.clear()
         self.result_lat.clear()
         self.result_lon.clear()
         self.google_url_box.clear()
		

def main():
    app = QApplication(sys.argv)
    form = ConverterApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
