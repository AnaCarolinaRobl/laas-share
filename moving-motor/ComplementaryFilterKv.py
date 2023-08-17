import matplotlib.pyplot as plt
import numpy as np
from utils import get_data, LPF_FILTER

filename = "rolling_data_sin_sin_stopped.txt"

times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)

TIME1 = int(len(times)/times[-1])

current = []
temps_fit = []
times_fit = []
vqs_temp = []
iqs_temp = []
ids_temp = []
velocitys_temp = []

KI = 0.2

for i in range(len(vqs)):
    if i > TIME1*8 and abs(iqs[i]) > 2.5:
        current.append(iqs[i]*KI)
        temps_fit.append(temps_measured[i])
        times_fit.append(times[i])
        vqs_temp.append(vqs[i])
        iqs_temp.append(iqs[i])
        ids_temp.append(ids[i])
        velocitys_temp.append(velocitys[i])

velocitys = np.array(velocitys_temp.copy())
vqs = vqs_temp.copy()
iqs = iqs_temp.copy()
ids = iqs_temp.copy()

kv = 0.01818
def calculate_resis(u, kv, v, i):
    return (u - kv*v)/i

resis = [calculate_resis(vqs[i], kv, velocitys[i], iqs[i]) for i in range(len(vqs))]
resis = LPF_FILTER(0.001, resis)


velocitys = [abs(velocitys[i]) for i in range(len(velocitys))]
velocitys = LPF_FILTER(0.001, velocitys)

current = [abs(current[i]) for i in range(len(current))]
current = LPF_FILTER(0.001, current)


k1 = 720
k2 = 98.2
k3 = -33.7
k4 = -272
print(f"t = {round(k1)}*(u - kv*w)/i + {round(k2,1)}*i {round(k3, 1)}*w {round(k4)}")

# plt.plot(times_fit, resis, ".")
# plt.title("resistencia")
# plt.show()

temps_lstq = []
pk1 = np.array([])
pk2 = np.array([])
pk3 = np.array([])

# for i in range(len(resis)):
#     temp_lstq = k1*resis[i] + k2*current[i] + k3*velocitys[i] + k4
#     temps_lstq.append(temp_lstq)
#     np.append(pk1, k1*resis[i])
#     np.append(pk2, k2*current[i])
#     np.append(pk3, k3*velocitys[i])

# plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
# plt.plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with resistance model")
# plt.plot(times_fit, pk1, ',',label="pk1")
# plt.plot(times_fit, pk1 + pk3, ',',label="pk1 + pk3")
# plt.plot(times_fit, pk2, ',',label="pk2")
# plt.plot(times_fit, pk3, ',',label="pk3")
# plt.title("Filename = " + filename)
# plt.xlabel('Time [s]')
# plt.ylabel('Temperature [° Celsius]')
# plt.legend()
# plt.show()


### data prepation
# Limits estimated temperature between 0 or 200
# for i in range(len(temps_lstq)):
#     if temps_lstq[i] > 200 or temps_lstq[i] < 0 or ids[i] < 1.5:
#         temps_lstq[i] = temps_lstq[i-1]

# FILTER FUNTCTION
def LPF_FILTER(tau, xs):
    ys = [0] * len(xs)
    ys[0] = xs[0]
    for i in range(1, len(xs)):
        ys[i] = tau * xs[i] + (1 - tau) * ys[i-1]
    return ys

def MEDIAN_FILTER(arr, LENGTH):

    arr_flt = []

    for i in range(0, len(arr)):
        temps_vec = [round(arr[i], 1)]
        j = i-LENGTH
        k = i+LENGTH
        while len(temps_vec) <= (LENGTH*2+1) and j<i:
            if j>=0:
                temps_vec.append(round(arr[j], 1))
            if k < len(arr):
                temps_vec.append(round(arr[k], 1))
            j+=1
            k+=1

        x = round(sum(temps_vec)/len(temps_vec), 1)
        arr_flt.append(x)


    return arr_flt

def HPF_FILTER(tau, xs):
    ys = [0] * len(xs)
    ys[0] = 0
    for i in range(1, len(xs)):
        ys[i] = tau * (ys[i-1] + xs[i] - xs[i-1])
    return ys

# temps_lstq_flt = MEDIAN_FILTER(temps_lstq, 10)

# Fusion temperatures (thermal and LSTQ)
def complementaryFilter(arr_hp, arr_lp, tau_hp, tau_lp):
    arr_hp = HPF_FILTER(tau_hp, arr_hp)
    arr_lp = LPF_FILTER(tau_lp, arr_lp)
    
    arr_filtered = []
    for i in range(len(arr_hp)):
        arr_filtered.append(arr_hp[i] + arr_lp[i])

    # arr_filtered = MEDIAN_FILTER(arr_filtered, 10)

    return arr_filtered


# calculate termique model
def thermal_model(times_fit):
    K1 = 0.0102
    K2 = 1/529
    K3 = 1 # 45/25
    T_AMBIENT = 25
    temps_model = [T_AMBIENT]
    for i in range(0, len(ids)-1):
        delta_t = temps_model[-1] - T_AMBIENT
        current = ids[i]*ids[i] + iqs[i]*iqs[i]
        temp_derivate = ((current * K1) - (delta_t * K2)) * K3
        DT = times_fit[i+1] - times_fit[i]
        temps_model.append(temps_model[-1] + ((temp_derivate) * DT))
    return temps_model


temps_model = thermal_model(times_fit)

tau = 0.001
plt.plot(times, temps_measured, "b.", label="Measured Temperature")
plt.plot(times_fit, temps_lstq, label=f"Resistance model")
plt.plot(times_fit, complementaryFilter(temps_model, temps_lstq, 1-tau, tau), label=f"Complementary Filter tau_hp = {1-tau}, tau_lp = {tau}")
plt.xlabel('Time [s]')
plt.ylabel('Temperature [° Celsius]')
plt.legend()
plt.show()

filenames = ["rolling_data_sin_increasing_stopped.txt", "rolling_data_sin_3A.txt", "rolling_data_Sin_sampled.txt", "rolling_data_sin_6A.txt", "rolling_data_PID.txt"]
# filenames = []

for filename in filenames:
    times, ids, iqs, vds, vqs, velocitys, temps_measured, positions = get_data(filename)

    current = []
    temps_fit = []
    times_fit = []
    vqs_temp = []
    iqs_temp = []
    ids_temp = []
    velocitys_temp = []

    for i in range(len(vqs)):
        if i > TIME1*8 and abs(iqs[i]) > 2.5:
            current.append(iqs[i])
            temps_fit.append(temps_measured[i])
            times_fit.append(times[i])
            vqs_temp.append(vqs[i])
            iqs_temp.append(iqs[i])
            ids_temp.append(ids[i])
            velocitys_temp.append(velocitys[i])

    velocitys = np.array(velocitys_temp.copy())
    vqs = vqs_temp.copy()
    iqs = iqs_temp.copy()
    ids = iqs_temp.copy()


    resis = [calculate_resis(vqs[i], kv, velocitys[i], iqs[i]) for i in range(len(vqs))]
    resis = LPF_FILTER(0.001, resis)


    velocitys = [abs(velocitys[i]) for i in range(len(velocitys))]
    velocitys = LPF_FILTER(0.001, velocitys)

    current = [abs(current[i]) for i in range(len(current))]
    current = LPF_FILTER(0.001, current)

    temps_lstq = []
    for i in range(len(resis)):
        temp_lstq = k1*resis[i] + k2*current[i] + k3*velocitys[i] + k4
        temps_lstq.append(temp_lstq)

    temps_model = thermal_model(times_fit)

    plt.plot(times_fit, temps_fit, 'g.', label="Measured Temperature")
    plt.plot(times_fit, temps_lstq, 'r,',label="Estimated Temperature with resistance model")
    plt.plot(times_fit, complementaryFilter(temps_model, temps_lstq, 1-tau, tau), label=f"Complementary Filter tau_hp = {1-tau}, tau_lp = {tau}")
    plt.title("Filename = " + filename)
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [° Celsius]')
    plt.legend()
    plt.show()


