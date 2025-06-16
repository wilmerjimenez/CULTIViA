def generar_alerta(severidad, tipo, mensaje):
    if severidad == 'crítica':
        print(f"[ALERTA CRÍTICA] {tipo.upper()}: {mensaje}")
    elif severidad == 'moderada':
        print(f"[ALERTA MODERADA] {tipo.upper()}: {mensaje}")
    else:
        print(f"[ALERTA] {tipo.upper()}: {mensaje}")
