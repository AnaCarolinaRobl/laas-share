import os

def get_data(filename):
    # Matrix para armazenar os valores
    datas = [[] for i in range(8)]

    filename = "data/" + filename
    # Leitura do arquivo de texto
    with open(filename, "r") as arquivo:
        # Ignora a primeira linha (cabeçalho)
        next(arquivo)
        # Lê as linhas restantes do arquivo
        for linha in arquivo:
            # Divide a linha em comando e corrente
            linha = linha.strip().split(",")
            for i in range(len(datas)):
                datas[i].append(float(linha[i]))

    return datas

def LPF_FILTER(tau, xs):
    ys = [0] * len(xs)
    ys[0] = xs[0]
    for i in range(1, len(xs)):
        ys[i] = tau * xs[i] + (1 - tau) * ys[i-1]
    return ys

def HPF_FILTER(tau, xs):
    ys = [0] * len(xs)
    ys[0] = 0
    for i in range(1, len(xs)):
        ys[i] = tau * (ys[i-1] + xs[i] - xs[i-1])
    return ys

# Fusion temperatures (thermal and LSTQ)
def complementaryFilter(arr_hp, arr_lp, tau_hp, tau_lp):
    arr_hp = HPF_FILTER(tau_hp, arr_hp)
    arr_lp = LPF_FILTER(tau_lp, arr_lp)
    
    arr_filtered = []
    for i in range(len(arr_hp)):
        arr_filtered.append(arr_hp[i] + arr_lp[i])

    # arr_filtered = MEDIAN_FILTER(arr_filtered, 10)

    return arr_filtered

# Fusion temperatures (thermal and LSTQ)
def fusion_model(temps_lstq, times, ids, iqs):
    K1 = 0.0102
    K2 = 1/529
    T_AMBIENT = 26
    temps_fusion=[T_AMBIENT]
    for i in range(0, len(ids)-1):
        delta_t = temps_fusion[-1] - T_AMBIENT
        current = ids[i]*ids[i]+iqs[i]*iqs[i]
        temp_derivate = (current * K1) - (delta_t * K2)
        DT = times[i+1] - times[i]
        temps_fusion.append(temps_fusion[-1] + ((temp_derivate) * DT))

        e = temps_fusion[-1] - temps_lstq[i+1]
        # trust = 1.0 - .004*1* (.01*(min(current, 100.0)))
        if abs(iqs[i])  < 3:
            trust = 0.001
        else:
            trust = 1
        temps_fusion[-1] = (temps_fusion[-1]-trust*.01*e)

    return temps_fusion

# calculate termique model
def thermal_model(times_fit, iqs, ids):
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

def complementaryFilter(arr_hp, arr_lp, tau_hp, tau_lp):
    arr_hp = HPF_FILTER(tau_hp, arr_hp)
    arr_lp = LPF_FILTER(tau_lp, arr_lp)
    
    arr_filtered = []
    for i in range(len(arr_hp)):
        arr_filtered.append(arr_hp[i] + arr_lp[i])

    return arr_filtered

def get_matching_txt_files():
    folder_path = "./data/"  # Substitua pelo caminho da sua pasta
    prefix = "rolling_data"
    matching_files = []
    for filename in os.listdir(folder_path):
        if filename.startswith(prefix) and filename.endswith(".txt"):
            matching_files.append(filename)
    return matching_files
