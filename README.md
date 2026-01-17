## PL

# Symulacja Zagadki "Stań za plecami"

Prosta wizualizacja zagadki logicznej:

> **"W pomieszczeniu jest tłum ludzi. Każda z osób zostaje poproszona o wybranie jakiejś innej osoby  w tym pomieszczeniu (nie mówiąc nikomu). Na dany znak każda osoba próbuje dotrzeć do osoby, którą wybrała i stanąć za jej plecami. "**

Program pokazuje, jak z chaosu wyłania się uporządkowany graf i automatycznie wykrywa powstające pętle (cykle).

### Jak uruchomić

Wymagany jest Python oraz biblioteka `pygame`.

1. Zainstaluj bibliotekę:
```bash
pip install pygame

```


2. Uruchom plik:
```bash
python main.py

```



### Sterowanie

* **Panel Górny:**
* **Input:** Wpisz liczbę kulek (zatwierdź Enter).
* **RESET:** Nowe losowanie.
* **STOP/WZNÓW:** Zatrzymuje lub wznawia symulację.
* **Slider:** Zmienia siłę przyciągania do środka ekranu.


* **Myszka:** Możesz łapać i przesuwać kulki.
* **Spacja:** Szybki reset.

---

## ENG

# "Stand Behind" Riddle Simulation

A visualization of a simple riddle:

> **"There's a crowd of people in the room. Each person is asked to choose someone else in the room (without telling anyone). On a given signal, each person tries to reach the person they've chosen and stand behind them.?"**

The simulation shows how chaos turns into a structured graph and automatically highlights any resulting loops (cycles).

### How to run

You need Python and `pygame`.

1. Install the library:
```bash
pip install pygame

```


2. Run the script:
```bash
python main.py

```



### Controls

* **Top Panel:**
* **Input:** Type the number of nodes (press Enter).
* **RESET:** Restart with new random positions.
* **STOP/RESUME:** Pause or unpause the physics.
* **Slider:** Adjust center gravity force.


* **Mouse:** Drag and drop nodes.
* **Spacebar:** Quick reset.
