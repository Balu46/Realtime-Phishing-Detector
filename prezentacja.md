---
marp: true
theme: default
class: lead
paginate: true
backgroundColor: #fff
---

# System Wykrywania Phishingu w Czasie Rzeczywistym
**Detekcja na podstawie Certificate Transparency Logs**

---
## Cel Projektu
* Wykrywanie złośliwych domen internetowych w momencie ich rejestracji.
* Aktywna ochrona popularnych marek przed atakami typu **typosquatting**.
* Automatyzacja procesu klasyfikacji domen i błyskawiczne ostrzeganie przed zagrożeniem.

---
## Architektura Systemu
* **Nasłuchiwanie:** Pobieranie danych w czasie rzeczywistym z sieci CertStream.
* **Analiza Heurystyczna:** Wykrywanie podobieństwa za pomocą ukrytych słów i generatora dnstwist.
* **Model ML:** Analiza wyodrębnionych cech domeny za pomocą klasyfikatora Random Forest.
* **Weryfikacja (Threat Intel):** Asynchroniczne odpytywanie baz VirusTotal oraz Google Safe Browsing.

---
## Model Uczenia Maszynowego (Machine Learning)
* Algorytm: **Random Forest Classifier** (scikit-learn)
* Analizowane Cechy (Features): 
  * Długość domeny
  * Entropia informacyjna znaków
  * Odległość Levenshteina od celu
  * Występowanie nietypowych znaków specjalnych
* Zbiory danych uczących:
  * **OpenPhish** (dane phishingowe)
  * **Tranco Top 1M** (dane bezpieczne)

---
## Jak odtworzyć projekt (Kroki Replikacji)
1. **Konfiguracja środowiska:** Utworzenie `virtualenv`, instalacja pakietów z `requirements.txt` oraz konfiguracja kluczy API.
2. **Trening Modelu:** Uruchomienie skryptu `train.py --dataset public`, by system pobrał OpenPhish/Tranco i wygenerował plik `.pkl`.
3. **Nasłuch w Czasie Rzeczywistym:** Start programu `main.py` – pipeline przetwarza asynchronicznie dziesiątki domen na sekundę.
4. **Ewaluacja:** Automatyczne raportowanie przez skrypt `evaluate.py`.

---
## Wnioski i Przyszły Rozwój
* **Skuteczność:** Połączenie heurystyki z AI pozwala na detekcję nowych wektorów ataku w fazie "zero-day".
* **Wydajność:** Kolejki asynchroniczne zapobiegają blokowaniu systemu przy zapytaniach do API.
* **Rozwój:** Planowane eksperymenty z głębokimi sieciami neuronowymi (PyTorch) oraz poszerzenie wektorów ekstrakcji cech z serwerów DNS (np. weryfikacja rekordów MX czy TXT).

---
# Dziękujemy za uwagę!
Czy są jakieś pytania?
