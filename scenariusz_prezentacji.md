# Scenariusz i Wskazówki do Prezentacji

Twój projekt: **System Wykrywania Phishingu w Czasie Rzeczywistym oparty na logach Certificate Transparency (CT)**.
Poniżej znajdziesz propozycję tego, co mówić na każdym slajdzie, oraz ogólne porady jak zaciekawić widownię.

---

## 🎤 Krok po kroku: Co mówić na każdym slajdzie

### Slajd 1: Tytuł (System Wykrywania Phishingu w Czasie Rzeczywistym)
*   **Jak to zagrać:** Zacznij od mocnego wejścia. Nie czytaj tylko tytułu.
*   **Co powiedzieć:** *"Dzień dobry. Wyobraźcie sobie, że w tej sekundzie, gdy my tu rozmawiamy, ktoś rejestruje domenę do oszukania klientów banku, z którego korzystacie. Mój projekt powstał po to, aby wyłapać takich oszustów dokładnie w momencie, w którym wystawiają certyfikat SSL dla fałszywej strony. Opowiem Wam dzisiaj o systemie detekcji na podstawie Certificate Transparency Logs."*

### Slajd 2: Cel Projektu
*   **Jak to zagrać:** Skup się na wartości biznesowej i bezpieczeństwie.
*   **Co powiedzieć:** *"Głównym problemem, z którym się mierzymy, jest typosquatting – czyli rejestrowanie domen łudząco podobnych do znanych marek (np. `paypa1.com`). Naszym celem jest aktywna ochrona tych marek poprzez automatyczną i błyskawiczną klasyfikację rejestrowanych domen, zanim jeszcze oszust zdąży rozesłać maile phishingowe."*

### Slajd 3: Architektura Systemu
*   **Jak to zagrać:** To kluczowy slajd. Pokaż drogę (pipeline), jaką pokonuje podejrzana domena od momentu rejestracji do oflagowania.
*   **Co powiedzieć:** *"Jak to działa pod maską? System to potok przetwarzania (pipeline) składający się z 4 etapów. 
    1. Najpierw nasłuchujemy w czasie rzeczywistym na logach z sieci **CertStream**. 
    2. Każda domena przechodzi przez **analizę heurystyczną** (odrzucamy bezpieczne domeny, wyłapujemy słowa kluczowe i korzystamy z generatora `dnstwist`).
    3. Podejrzane domeny trafiają do naszego **modelu sztucznej inteligencji (Machine Learning)**.
    4. Na koniec, by uniknąć fałszywych alarmów (False Positives), system asynchronicznie odpytuje zewnętrzne bazy: **VirusTotal** i **Google Safe Browsing**."*

### Slajd 4: Model Uczenia Maszynowego (Machine Learning)
*   **Jak to zagrać:** Jeśli audytorium jest techniczne, możesz wspomnieć o tym, dlaczego wybrałeś akurat ten model.
*   **Co powiedzieć:** *"Sercem detekcji jest algorytm **Random Forest Classifier**. Do wytrenowania modelu pobrałem zbiór domen złośliwych z OpenPhish oraz czystych domen z listy Tranco. System nie ocenia samej nazwy jako tekstu, ale wyciąga tzw. cechy matematyczne: mierzy entropię Shannona (co świetnie wykrywa losowe ciągi znaków, np. algorytmy DGA), dystans Levenshteina od atakowanej marki oraz obecność nietypowych znaków czy całkowitą długość nazwy. Zestawienie tych cech daje modelowi wysoką skuteczność."*

### Slajd 5: Jak odtworzyć projekt (Kroki Replikacji) / 🔥 MIEJSCE NA LIVE DEMO!
*   **Jak to zagrać:** Czytanie komend ze slajdu jest nudne. **Zrób tutaj Live Demo!** 
*   **Co powiedzieć:** *"System został napisany bardzo modułowo. Składa się z prostej konfiguracji i procesu trenowania. Ale zamiast tylko o tym mówić... chciałbym wam to po prostu pokazać w działaniu."*
*   **Akcja:** Zminimalizuj prezentację, otwórz terminal i uruchom: `python main.py --mock`. Pokaż ludziom terminal, w którym migają wykryte zagrożenia w czasie rzeczywistym. Pokaż również plik `phishing_results.csv`, do którego są logowane.

### Slajd 6: Wnioski i Przyszły Rozwój
*   **Jak to zagrać:** Zakończ z wizją tego, co dalej. Pokaż, że myślisz przyszłościowo.
*   **Co powiedzieć:** *"Projekt dowiódł, że połączenie szybkich reguł heurystycznych ze sztuczną inteligencją daje świetne rezultaty przeciwko atakom zero-day. Użycie asynchroniczności w Pythonie sprawiło, że odpytywanie API działa płynnie i nie blokuje systemu. W przyszłości planuję wdrożyć głębokie sieci neuronowe w PyTorchu i sprawdzać konfiguracje DNS (np. rekordy MX), co sugerowałoby gotowość domeny do masowej wysyłki phishingu."*

### Slajd 7: Q&A
*   Podziękuj za uwagę i bądź gotowy na pytania z widowni. 
*   *Przewidywane pytania:* Jaka jest skuteczność modelu (True Positives / False Positives)? Co w przypadku awarii CertStream (możesz wspomnieć o module zapasowym `UrlScanListener`)?

---

## 💡 Główne wskazówki:

1. **Skup się na problemie, a nie tylko na kodzie:** Ludzie zapamiętują historie. Zacznij od problemu cyberprzestępczości, by nadać sens Twojemu rozwiązaniu.
2. **"Pokaż, nie opowiadaj" (Live Demo):** Uruchomienie trybu `--mock` lub odpalenie nasłuchu na `--urlscan` czy czystym CertStreamie zrobi największe wrażenie. Nic nie sprzedaje projektów IT tak dobrze jak działająca, dynamiczna konsola.
3. **Bądź asynchroniczny w opowieści:** Masz system, w którym dużo dzieje się pod spodem – nie tłumacz poszczególnych linijek kodu, skup się na przepływie danych (Data Pipeline).
4. **Złap pewność siebie:** Twój projekt jest kompletny, ma fallbacki na wypadek awarii sieci, integruje kilka API i korzysta z uczenia maszynowego. Bądź dumny z tej architektury!
