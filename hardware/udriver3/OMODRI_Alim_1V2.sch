EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 5 19
Title "Open MOtor DRiver Initiative (OMODRI)"
Date "2020-12-16"
Rev "1.1"
Comp "LAAS/CNRS"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Wire Wire Line
	6300 3500 6700 3500
Text Label 5950 3950 0    50   ~ 0
FB_1V2
Wire Wire Line
	5900 3500 6050 3500
Wire Wire Line
	5900 3600 6050 3600
Text Label 6450 3500 0    50   ~ 0
1V2
Wire Wire Line
	6700 4050 6700 3500
Wire Wire Line
	6700 4400 6700 4350
$Comp
L power:GND #PWR?
U 1 1 5F75EA33
P 6700 4400
AR Path="/5F3A3F16/5F75EA33" Ref="#PWR?"  Part="1" 
AR Path="/5F3A3F16/5F5BF412/5F75EA33" Ref="#PWR035"  Part="1" 
F 0 "#PWR035" H 6700 4150 50  0001 C CNN
F 1 "GND" H 6705 4227 50  0000 C CNN
F 2 "" H 6700 4400 50  0001 C CNN
F 3 "" H 6700 4400 50  0001 C CNN
	1    6700 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	6300 4400 6300 4350
$Comp
L power:GND #PWR?
U 1 1 5F75EA3A
P 6300 4400
AR Path="/5F3A3F16/5F75EA3A" Ref="#PWR?"  Part="1" 
AR Path="/5F3A3F16/5F5BF412/5F75EA3A" Ref="#PWR034"  Part="1" 
F 0 "#PWR034" H 6300 4150 50  0001 C CNN
F 1 "GND" H 6305 4227 50  0000 C CNN
F 2 "" H 6300 4400 50  0001 C CNN
F 3 "" H 6300 4400 50  0001 C CNN
	1    6300 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	6300 3500 6300 3550
Text GLabel 4725 3500 0    50   Input ~ 0
5V0
$Comp
L power:GND #PWR?
U 1 1 5F75EA49
P 5350 4400
AR Path="/5F3A3F16/5F75EA49" Ref="#PWR?"  Part="1" 
AR Path="/5F3A3F16/5F5BF412/5F75EA49" Ref="#PWR033"  Part="1" 
F 0 "#PWR033" H 5350 4150 50  0001 C CNN
F 1 "GND" H 5355 4227 50  0000 C CNN
F 2 "" H 5350 4400 50  0001 C CNN
F 3 "" H 5350 4400 50  0001 C CNN
	1    5350 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	5350 4200 5350 4400
Wire Wire Line
	5900 3700 6050 3700
Wire Wire Line
	6050 3700 6050 3600
Connection ~ 6050 3600
Wire Wire Line
	6050 3600 6050 3500
Wire Wire Line
	6300 3850 6300 3950
Wire Wire Line
	6050 3500 6300 3500
Connection ~ 6050 3500
Connection ~ 6300 3500
Wire Wire Line
	5900 3950 6300 3950
Connection ~ 6300 3950
Wire Wire Line
	6300 3950 6300 4050
Text GLabel 7700 3500 2    50   Output ~ 0
VDD_1V2
Connection ~ 7150 3500
$Comp
L Device:R R?
U 1 1 5F75EA6A
P 6300 4200
AR Path="/5F3A3F16/5F75EA6A" Ref="R?"  Part="1" 
AR Path="/5F3A3F16/5F5BF412/5F75EA6A" Ref="R9"  Part="1" 
F 0 "R9" H 6370 4246 50  0000 L CNN
F 1 "100k" H 6370 4155 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric" V 6230 4200 50  0001 C CNN
F 3 "https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf" H 6300 4200 50  0001 C CNN
F 4 "P122655CT-ND" H 6300 4200 50  0001 C CNN "DigiKey"
F 5 "2302389" H 6300 4200 50  0001 C CNN "Farnell"
F 6 "667-ERJ-1GNF1003C" H 6300 4200 50  0001 C CNN "Mouser"
F 7 "ERJ-1GNF1003C" H 6300 4200 50  0001 C CNN "Part No"
F 8 "179-7130" H 6300 4200 50  0001 C CNN "RS"
	1    6300 4200
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5F75EA75
P 6300 3700
AR Path="/5F3A3F16/5F75EA75" Ref="R?"  Part="1" 
AR Path="/5F3A3F16/5F5BF412/5F75EA75" Ref="R8"  Part="1" 
F 0 "R8" H 6370 3746 50  0000 L CNN
F 1 "100k" H 6370 3655 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric" V 6230 3700 50  0001 C CNN
F 3 "https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf" H 6300 3700 50  0001 C CNN
F 4 "P122655CT-ND" H 6300 3700 50  0001 C CNN "DigiKey"
F 5 "2302389" H 6300 3700 50  0001 C CNN "Farnell"
F 6 "667-ERJ-1GNF1003C" H 6300 3700 50  0001 C CNN "Mouser"
F 7 "ERJ-1GNF1003C" H 6300 3700 50  0001 C CNN "Part No"
F 8 "179-7130" H 6300 3700 50  0001 C CNN "RS"
	1    6300 3700
	1    0    0    -1  
$EndComp
$Comp
L omodri_lib:MPM3804GG U?
U 1 1 5F75EA7F
P 5350 3750
AR Path="/5F3A3F16/5F75EA7F" Ref="U?"  Part="1" 
AR Path="/5F3A3F16/5F5BF412/5F75EA7F" Ref="U4"  Part="1" 
F 0 "U4" H 5050 3450 50  0000 C CNN
F 1 "MPM3804GG" H 5250 4100 50  0000 C CNN
F 2 "udriver3:QFN-10_2x2mm_P0.5mm" H 5350 3750 50  0001 C CNN
F 3 "https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MPM3804GG/document_id/2122/" H 5350 3750 50  0001 C CNN
F 4 "1589-1982-1-ND" H 5350 3750 50  0001 C CNN "DigiKey"
F 5 "3358188" H 5350 3750 50  0001 C CNN "Farnell"
F 6 "946-MPM3804GG-Z" H 5350 3750 50  0001 C CNN "Mouser"
F 7 "MPM3804GG" H 5350 3750 50  0001 C CNN "Part No"
	1    5350 3750
	1    0    0    -1  
$EndComp
$Comp
L Device:Ferrite_Bead_Small FB?
U 1 1 5F75EA96
P 6925 3500
AR Path="/5F3A3F16/5F75EA96" Ref="FB?"  Part="1" 
AR Path="/5F3A3F16/5F5BF412/5F75EA96" Ref="FB3"  Part="1" 
F 0 "FB3" V 6875 3650 50  0000 C CNN
F 1 "220R@100MHz" V 7050 3500 50  0000 C CNN
F 2 "Inductor_SMD:L_0603_1608Metric" V 6855 3500 50  0001 C CNN
F 3 "https://www.murata.com/-/media/webrenewal/support/library/catalog/products/emc/emifil/c51e.ashx?la=en-gb&cvid=20190315071402699800" H 6925 3500 50  0001 C CNN
F 4 "490-5225-1-ND" H 6925 3500 50  0001 C CNN "DigiKey"
F 5 "1515753" H 6925 3500 50  0001 C CNN "Farnell"
F 6 "81-BLM18SG221TN1D" H 6925 3500 50  0001 C CNN "Mouser"
F 7 "BLM18SG221TN1D" H 6925 3500 50  0001 C CNN "Part No"
F 8 "792-6271" H 6925 3500 50  0001 C CNN "RS"
	1    6925 3500
	0    1    1    0   
$EndComp
$Comp
L Device:C C?
U 1 1 5F75EAA2
P 6700 4200
AR Path="/5F3A3F16/5F75EAA2" Ref="C?"  Part="1" 
AR Path="/5F3A3F16/5F5BF412/5F75EAA2" Ref="C21"  Part="1" 
F 0 "C21" H 6815 4246 50  0000 L CNN
F 1 "10uF" H 6815 4155 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6738 4050 50  0001 C CNN
F 3 "https://www.murata.com/en-eu/products/productdetail?partno=GRM188R61A106ME69%23" H 6700 4200 50  0001 C CNN
F 4 "490-10475-1-ND" H 6700 4200 50  0001 C CNN "DigiKey"
F 5 "2456110" H 6700 4200 50  0001 C CNN "Farnell"
F 6 "81-GRM188R61A106ME9D" H 6700 4200 50  0001 C CNN "Mouser"
F 7 "GRM188R61A106ME69D" H 6700 4200 50  0001 C CNN "Part No"
F 8 "113-8702" H 6700 4200 50  0001 C CNN "RS"
F 9 "10V" H 6700 4200 50  0001 C CNN "Rated Voltage"
	1    6700 4200
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 5F75EAAE
P 7150 4200
AR Path="/5F3A3F16/5F75EAAE" Ref="C?"  Part="1" 
AR Path="/5F3A3F16/5F5BF412/5F75EAAE" Ref="C22"  Part="1" 
F 0 "C22" H 7265 4246 50  0000 L CNN
F 1 "10uF" H 7265 4155 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 7188 4050 50  0001 C CNN
F 3 "https://www.murata.com/en-eu/products/productdetail?partno=GRM188R61A106ME69%23" H 7150 4200 50  0001 C CNN
F 4 "490-10475-1-ND" H 7150 4200 50  0001 C CNN "DigiKey"
F 5 "2456110" H 7150 4200 50  0001 C CNN "Farnell"
F 6 "81-GRM188R61A106ME9D" H 7150 4200 50  0001 C CNN "Mouser"
F 7 "GRM188R61A106ME69D" H 7150 4200 50  0001 C CNN "Part No"
F 8 "113-8702" H 7150 4200 50  0001 C CNN "RS"
F 9 "10V" H 7150 4200 50  0001 C CNN "Rated Voltage"
	1    7150 4200
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 5F75EABA
P 7625 4200
AR Path="/5F3A3F16/5F75EABA" Ref="C?"  Part="1" 
AR Path="/5F3A3F16/5F5BF412/5F75EABA" Ref="C23"  Part="1" 
F 0 "C23" H 7740 4246 50  0000 L CNN
F 1 "1uF" H 7740 4155 50  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 7663 4050 50  0001 C CNN
F 3 "https://www.murata.com/en-eu/products/productdetail?partno=GRM033C81A105ME05%23" H 7625 4200 50  0001 C CNN
F 4 "490-13219-1-ND" H 7625 4200 50  0001 C CNN "DigiKey"
F 5 "3238032" H 7625 4200 50  0001 C CNN "Farnell"
F 6 "81-GRM033C81A105ME5D" H 7625 4200 50  0001 C CNN "Mouser"
F 7 "GRM033C81A105ME05D" H 7625 4200 50  0001 C CNN "Part No"
F 8 "" H 7625 4200 50  0001 C CNN "RS"
F 9 "10V" H 7625 4200 50  0001 C CNN "Rated Voltage"
	1    7625 4200
	1    0    0    -1  
$EndComp
Connection ~ 6700 3500
Wire Wire Line
	7150 4050 7150 3500
$Comp
L power:GND #PWR?
U 1 1 5F75EAC2
P 7150 4425
AR Path="/5F3A3F16/5F75EAC2" Ref="#PWR?"  Part="1" 
AR Path="/5F3A3F16/5F5BF412/5F75EAC2" Ref="#PWR036"  Part="1" 
F 0 "#PWR036" H 7150 4175 50  0001 C CNN
F 1 "GND" H 7155 4252 50  0000 C CNN
F 2 "" H 7150 4425 50  0001 C CNN
F 3 "" H 7150 4425 50  0001 C CNN
	1    7150 4425
	1    0    0    -1  
$EndComp
Wire Wire Line
	7150 4425 7150 4350
$Comp
L power:GND #PWR?
U 1 1 5F75EAC9
P 7625 4425
AR Path="/5F3A3F16/5F75EAC9" Ref="#PWR?"  Part="1" 
AR Path="/5F3A3F16/5F5BF412/5F75EAC9" Ref="#PWR037"  Part="1" 
F 0 "#PWR037" H 7625 4175 50  0001 C CNN
F 1 "GND" H 7630 4252 50  0000 C CNN
F 2 "" H 7625 4425 50  0001 C CNN
F 3 "" H 7625 4425 50  0001 C CNN
	1    7625 4425
	1    0    0    -1  
$EndComp
Wire Wire Line
	7625 4425 7625 4350
Wire Wire Line
	7150 3500 7625 3500
Wire Wire Line
	7625 3500 7700 3500
Connection ~ 7625 3500
Wire Wire Line
	7025 3500 7150 3500
Wire Wire Line
	6700 3500 6825 3500
Text HLabel 4725 3950 0    50   Input ~ 0
PG_5V0
Wire Wire Line
	4725 3950 4800 3950
Wire Wire Line
	4725 3500 4800 3500
Wire Wire Line
	7625 3500 7625 4050
Wire Wire Line
	4900 3600 4825 3600
Wire Wire Line
	4825 3600 4825 3700
Wire Wire Line
	4825 3700 4900 3700
Wire Wire Line
	4900 3800 4825 3800
Wire Wire Line
	4825 3800 4825 3700
Connection ~ 4825 3700
Text Label 4825 3800 1    50   ~ 0
SW
$EndSCHEMATC
