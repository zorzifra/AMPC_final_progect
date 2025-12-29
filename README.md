# AMPC_final_progect
Final project of the course of Adaptive and Model Predictive Control

AMPC_Final_Project/
│
├── README.md              # Descrizione del progetto e istruzioni per l'esecuzione
├── .gitignore             # File essenziale per ignorare i file generati da acados
├── requirements.txt       # Librerie Python necessarie (numpy, matplotlib, casadi, etc.)
│
├── src/                   # Codice sorgente principale
│   ├── __init__.py
│   ├── model.py           # Definizione del modello del pendolo (Eq. 1a-1d) e modello esteso (Task 1)
│   ├── parameters.py      # Costanti fisiche (M, m, l, g) e parametri NMPC (Ts, N)
│   ├── utils.py           # Funzioni di supporto (es. plot dei risultati, animazioni)
│   │
│   ├── task1/     # Codice per il Task 1
│   │   ├── nmpc_standard.py    # NMPC base
│   │   ├── nmpc_input_rate.py  # NMPC con input rate penalization (modello esteso)
│   │   └── simulation.py       # Script per eseguire la simulazione e confrontare
│   │
│   ├── task2/ # Codice per il Task 2
│   │   └── model_mismatch.py   # task 3 del punto 2
│   │
│   └── task3/      # Codice per il Task 3 (Linear MPC)
│       └── linear_mpc.py
│
├── docs/                  # Documentazione e presentazione
│   └── presentation.pdf   # Le slide richieste nel Task 4 [cite: 3986]
│
└── results/               # Cartella dove salvare i grafici generati dagli 