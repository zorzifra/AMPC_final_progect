import numpy as np

# System parameters (Inverted Pendulum on Cart)
p = {
    'M': 1.0,       # Massa del carrello [kg] [cite: 90]
    'm': 0.1,       # Massa del pendolo [kg]
    'l': 0.8,       # Lunghezza del pendolo [m] [cite: 96]
    'g': 9.81,      # Accelerazione di gravità [m/s^2]
    'F_max': 20.0,  # Forza massima [N] [cite: 11]
}
M = 1.0             # mass of the cart [kg] 
m = 0.1             # pendulum mass [kg]
l = 0.8             # pendulum length [m]
g = 9.81            # gravity acceleration [m/s^2]
F_max = 20.0        # maximum force [N]

# Symulation parameters
T_horizon = 2.0    # Orizzonte temporale (esempio)
N_horizon = 40     # Numero di passi di discretizzazione
dt = 0.001         # Passo di simulazione [cite: 13]
