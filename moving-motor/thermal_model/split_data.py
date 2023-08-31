import sys
sys.path.append('../')  # Adiciona o diretório pai (pasta_principal) ao PATH
from utils import get_data

filename = "rolling_data_PID_SIN_0.txt"
times_temp, ids_temp, iqs_temp, vds_temp, vqs_temp, velocitys_temp, temps_measured_temp, positions_temp = get_data(filename)

times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = [], [], [], [], [], [], [], []

for i in range(len(times_temp)):
    if i % 2 == 0:
        times.append(times_temp)
        ids.append(ids_temp)
        iqs.append(iqs_temp)
        vqs.append(vqs_temp)
        vds.append(vds_temp)
        velocitys.append(velocitys_temp)
        temps_measured.append(temps_measured_temp)
        positions.append(positions_temp)

# Save data in file
f = open("rolling_data_PID_SIN_0_new.txt", "w")
f.write("Time, Id, Iq, Ud, Uq, Velocity, Temperature, Position\n")

for i in range(len(times)):
    f.write(str(times[i]) + ", " 
            + str(ids[i]) + ", " 
            + str(iqs[i]) + ", "
            + str(vds[i]) + ", " 
            + str(vqs[i]) + ", " 
            + str(velocitys[i]) + ", " 
            + str(temps_measured[i]) + ", " 
            + str(positions[i])
            + "\n")
f.close()
