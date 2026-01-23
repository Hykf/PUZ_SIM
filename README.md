## PL

# Symulacja Zagadki "Stań za plecami"

Prosta wizualizacja zagadki logicznej:

> **"W pomieszczeniu jest tłum ludzi. Każda z osób zostaje poproszona o wybranie jakiejś innej osoby  w tym pomieszczeniu (nie mówiąc nikomu). Na dany znak każda osoba próbuje dotrzeć do osoby, którą wybrała i stanąć za jej plecami. "**

Program pokazuje, jak z chaosu wyłania się uporządkowany graf i automatycznie wykrywa powstające pętle (cykle).

### Jak uruchomić

**Opcja A: Plik wykonywalny (Windows)**
Uruchom plik `puz_emu.exe`. Instalacja Pythona nie jest wymagana.

**Opcja B: Kod źródłowy (Python)**
Wymagany jest Python oraz biblioteka `pygame`.

1. Zainstaluj bibliotekę:
```bash
pip install pygame

```

2. Uruchom plik:
```bash
python puz_emu.py

```


### Sterowanie

* **Panel Górny:**
* **Input:** Wpisz liczbę kulek (zatwierdź Enter).
* **RESET:** Nowe losowanie.
* **STOP/WZNÓW:** Zatrzymuje lub wznawia symulację.
* **Slider:** Zmienia siłę przyciągania do środka ekranu.


* **Myszka:** Możesz łapać i przesuwać kulki.
* **Spacja:** Szybki reset.

<img width="998" height="874" alt="image" src="https://github.com/user-attachments/assets/98b84751-6772-48b4-ba76-5173ef58105b" />

---

## ENG

# "Stand Behind" Riddle Simulation

A simple visualization of a logic riddle:

> **"There's a crowd of people in the room. Each person is asked to choose someone else in the room (without telling anyone). On a given signal, each person tries to reach the person they've chosen and stand behind them.?"**

The simulation shows how chaos turns into a structured graph and automatically highlights any resulting loops (cycles).

### How to run

Option A: Executable (Windows) Run the puz_emu.exe file. Python installation is not required.

Option B: Source Code (Python) You need Python and pygame installed.

1. Install the library:
```bash
pip install pygame

```


2. Run the script:
```bash
python puz_emu.py

```



### Controls

* **Top Panel:**
* **Input:** Type the number of nodes (press Enter).
* **RESET:** Restart with new random positions.
* **STOP/RESUME:** Pause or unpause the physics.
* **Slider:** Adjust center gravity force.


* **Mouse:** Drag and drop nodes.
* **Spacebar:** Quick reset.

<img width="998" height="874" alt="image" src="https://github.com/user-attachments/assets/98b84751-6772-48b4-ba76-5173ef58105b" />


Zgoda / Consent
PL: Wyrażam zgodę na wykorzystanie i publikację tego programu w materiałach dydaktycznych kursu.
ENG: I hereby grant permission for this software to be used and published in the course materials.

Wróbel Mateusz s24298
