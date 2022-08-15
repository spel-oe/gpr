EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:R R1
U 1 1 5F6D3A6C
P 3100 2200
F 0 "R1" H 3170 2246 50  0000 L CNN
F 1 "R" H 3170 2155 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 3030 2200 50  0001 C CNN
F 3 "~" H 3100 2200 50  0001 C CNN
	1    3100 2200
	1    0    0    -1  
$EndComp
$Comp
L Device:R R3
U 1 1 5F6D3FC6
P 3550 2200
F 0 "R3" H 3620 2246 50  0000 L CNN
F 1 "R" H 3620 2155 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 3480 2200 50  0001 C CNN
F 3 "~" H 3550 2200 50  0001 C CNN
	1    3550 2200
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 5F6D41B1
P 3100 3000
F 0 "R2" H 3170 3046 50  0000 L CNN
F 1 "R" H 3170 2955 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 3030 3000 50  0001 C CNN
F 3 "~" H 3100 3000 50  0001 C CNN
	1    3100 3000
	1    0    0    -1  
$EndComp
$Comp
L Device:R R4
U 1 1 5F6D4564
P 3600 3000
F 0 "R4" H 3670 3046 50  0000 L CNN
F 1 "R" H 3670 2955 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 3530 3000 50  0001 C CNN
F 3 "~" H 3600 3000 50  0001 C CNN
	1    3600 3000
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 3150 3100 3200
Wire Wire Line
	3100 3200 3600 3200
Wire Wire Line
	3600 2850 3600 2800
Wire Wire Line
	3600 2800 3450 2800
Wire Wire Line
	3100 2800 3100 2850
Wire Wire Line
	3550 2050 3550 2000
Wire Wire Line
	3550 2000 3100 2000
Wire Wire Line
	3100 2000 3100 2050
Wire Wire Line
	3100 2350 3100 2400
Wire Wire Line
	3100 2400 3250 2400
Wire Wire Line
	3550 2400 3550 2350
Wire Wire Line
	3600 3200 3600 3150
$Comp
L Connector:Conn_Coaxial J1
U 1 1 5F6D6885
P 3450 2550
F 0 "J1" H 3550 2525 50  0000 L CNN
F 1 "Conn_Coaxial" H 3550 2434 50  0000 L CNN
F 2 "Connector_Coaxial:SMA_Amphenol_901-144_Vertical" H 3450 2550 50  0001 C CNN
F 3 " ~" H 3450 2550 50  0001 C CNN
	1    3450 2550
	1    0    0    -1  
$EndComp
Wire Wire Line
	3250 2550 3250 2400
Connection ~ 3250 2400
Wire Wire Line
	3250 2400 3550 2400
Wire Wire Line
	3450 2750 3450 2800
Connection ~ 3450 2800
Wire Wire Line
	3450 2800 3100 2800
$EndSCHEMATC
