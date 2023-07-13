import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import serial

#initialize serial port
ser = serial.Serial()
ser.port = 'COM3' #Arduino serial port
ser.baudrate = 115200
ser.timeout = 1 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n") #print serial parametetemp_list

# Create figure for plotting
fig, ax = plt.subplots(2, 2)
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
time = [] #store trials here
hum_list = []
temp_list = []
ping_list = []
degrees_list = []
gas_list = []
P3Recent = 0
P5Recent = 0
P10Recent = 0
P25Recent = 0
P50Recent = 0
P100Recent = 0
runs = 0
# This function is called periodically from FuncAnimation
def animate(runs, time, hum_list, temp_list, ping_list, degrees_list, gas_list, P3Recent, P5Recent, P10Recent, P25Recent, P50Recent, P100Recent):
    #Aquire and patemp_liste data from serial port
    line_as_list = []
    while len(line_as_list) != 11:
        line = str(ser.readline()) 
        line = line.replace('b', '').replace("'", '').replace("\\n" , '').replace("\\t", ' ')
        line_as_list = line.split(' ')
    runs += 1
    if (runs-20) < 0:
        temp_gas_start = 0
    else:
        temp_gas_start = runs - 20
    if (runs-15) < 0:
        ping_start = 0
    else:
        ping_start = runs - 15
    #Set variables to their values read from the ser port   
    ping = int(line_as_list[0])
    degrees = int(line_as_list[1])
    temp = float(line_as_list[2])
    hum = float(line_as_list[3])
    gas = int(line_as_list[4])
    P3 = int(line_as_list[5])
    P5 = int(line_as_list[6])
    P10 = int(line_as_list[7])
    P25 = int(line_as_list[8])
    P50 = int(line_as_list[9])
    P100 = int(line_as_list[10])
    
	# Add data to lists
    time.append(runs)

    ping_list.append(ping)
    degrees_list.append(degrees)
    temp_list.append(temp)
    hum_list.append(hum)
    gas_list.append(gas)

    if runs == 1:
        P3Recent = P3
        P5Recent = P5
        P10Recent = P10
        P25Recent = P25
        P50Recent = P50
        P100Recent = P100
    elif P3 != 0 or P5 != 0 or P10 != 0 or P25 != 0 or P50 != 0 or P100 != 0:
        P3Recent = P3
        P5Recent = P5
        P10Recent = P10
        P25Recent = P25
        P50Recent = P50
        P100Recent = P100

    
    ping_list = ping_list[ping_start : runs+1]
    degrees_list = degrees_list[ping_start : runs+1]
    hum_list = hum_list[temp_gas_start : runs+1]
    temp_list = temp_list[temp_gas_start : runs+1]
    gas_list = gas_list[temp_gas_start : runs+1]

    # Draw x and y lists
    ax[0,0].clear()
    ax[0,1].clear()
    ax[1,0].clear()
    labels = ["Humidity(%)","Temperature(Celsius)", "Gas(Normal Air ~ 100-150)"]
    # Format plots
    ax[0,0].set_title("Temp and Hum Sensors")
    ax[0,0].set_xlabel('Trials')
    ax[0,0].set_ylabel('Sensor Values')

    ax[0,1].set_title("Ultrasonic Turret")
    ax[0,1].set_xlabel("Degrees°")
    ax[0,1].set_ylabel("Distance(cm)")

    ax[1,0].set_title("Gas Sensor")
    ax[1,0].set_xlabel('Trials')
    ax[1,0].set_ylabel('Sensor Values')

    ax[1,1].set_title("Particulate Sensor")
    ax[1,1].set_xlabel('Range 0.1L of air(um)')
    ax[1,1].set_ylabel('Particles')

    humPlot = ax[0,0].plot(time[temp_gas_start: None], hum_list, color = "green")
    tempPlot = ax[0,0].plot(time[temp_gas_start: None], temp_list, color = "red")
    ax[0,1].plot(degrees_list, ping_list, color = "blue")
    gasPlot = ax[1,0].plot(time[temp_gas_start : None], gas_list, color = "yellow")
    ax[1,1].bar(1, P3Recent, width=1, color = "orange")
    ax[1,1].bar(5, P5Recent, width=1, color = "purple")
    ax[1,1].bar(10, P10Recent, width=1, color = "cyan")
    ax[1,1].bar(25, P25Recent, width=1, color = "pink")
    ax[1,1].bar(50, P50Recent, width=0.8, color = "olive")
    ax[1,1].bar(100, P100Recent, width=0.8, color = "gray")

    ax[0,1].set_ylim([0, 314])
    ax[0,1].set_xlim([20, 160])

    fig.legend([humPlot, tempPlot, gasPlot], labels = labels,
           loc="upper right")
# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(time, hum_list, temp_list, ping_list, degrees_list, gas_list, P3Recent, P5Recent, P10Recent, P25Recent, P50Recent, P100Recent), interval=1000)
plt.subplots_adjust(hspace=0.5, wspace=0.3) #h and w space is the distance between subplots
plt.show()