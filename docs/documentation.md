# Dokumentacja Systemu: CT Logs Phishing Detection

Niniejsza dokumentacja wyjaśnia zasady działania systemu, wykorzystywane przez niego narzędzia, biblioteki oraz to, jak wszystkie te elementy łączą się w spójną całość chroniącą przed atakami typu phishing.

---

## 1. Skąd bierzemy dane? (Certificate Transparency)
System opiera się na analizie publicznych rejestrów tzw. **Certificate Transparency (CT)**. Kiedy jakakolwiek strona internetowa na świecie kupuje lub generuje darmowy certyfikat SSL/TLS (kłódka w przeglądarce, protokół `https://`), urząd certyfikacji (np. Let's Encrypt) ma obowiązek zapisać ten fakt w publicznym rejestrze CT. 

Większość fałszywych stron phishingowych stara się wyglądać wiarygodnie, dlatego przestępcy masowo generują darmowe certyfikaty SSL dla swoich złośliwych domen. Nasz system "podsłuchuje" te publiczne logi i wyłapuje nowo zarejestrowane domeny.

### Biblioteka: `certstream`
Dzięki użyciu tej biblioteki łączymy się w czasie rzeczywistym z siecią strumieniową `wss://certstream.calidog.io/` za pomocą WebSocketów. Pozwala nam to na bieżąco (nawet kilkadziesiąt domen na sekundę) nasłuchiwać i przekazywać nowe adresy internetowe bezpośrednio do analizy.

---

## 2. Jak rozpoznajemy potencjalne zagrożenie? (Heurystyki)
Zanim zaangażujemy zaawansowane modele matematyczne, najpierw filtrujemy ogromny strumień danych przy użyciu szybkich, wstępnych reguł (heurystyk). Szukamy w nich bezpośrednich odniesień do chronionych marek (np. `paypal`, `google`).

### Biblioteka: `dnstwist`
Atakujący rzadko rejestrują dokładną nazwę `paypal.com` (ponieważ jest zajęta). Zamiast tego rejestrują tzw. warianty **typosquattingowe** – domeny, które wyglądają łudząco podobnie, bazujące na:
*   Błędach klawiaturowych (np. uderzenie obok na klawiaturze: `paupal.com`)
*   Podmianach znaków (tzw. homografy, litery z innych alfabetów wyglądające jak łacińskie)
*   Podwójnych literach (np. `payppal.com`)
*   Ominięciach liter (np. `paypl.com`)

Gdy system startuje, moduł `dnstwist` przetwarza listę Twoich chronionych marek i w ułamku sekundy automatycznie generuje i zapamiętuje w pamięci RAM **dziesiątki tysięcy** matematycznie prawdopodobnych pomyłek dla tych marek (stąd log "Generated 43339 typosquatting variants in total"). Każda nowa strona jest z nimi błyskawicznie porównywana w złożoności czasowej $O(1)$.

---

## 3. Uczenie Maszynowe (Machine Learning)
Kiedy domena zostanie oznaczona przez heurystyki jako "podejrzana", wkracza moduł Sztucznej Inteligencji oparty na metodzie Random Forest (Lasów Losowych).

### Biblioteka: `scikit-learn` i `Levenshtein`
Moduł ML nie analizuje samego faktu wystąpienia literówki, ale oblicza tzw. "cechy" (features) matematyczne z nazwy domeny:
1.  **Entropia Shannona:** Mierzy "chaos" w ciągu znaków. Legalne adresy, takie jak `facebook.com`, mają naturalną entropię językową. Adresy generowane losowo (np. `fb-login-xh29dfks.com`) mają nienaturalnie wysoką entropię.
2.  **Dystans Levenshteina:** Mierzy "odległość edycyjną" pomiędzy dwiema nazwami, czyli informuje nas, ile operacji wstawienia, usunięcia lub zamiany pojedynczego znaku dzieli podejrzaną domenę od oryginału (im mniej, tym większe ryzyko phishingu). Wykorzystujemy do tego moduł `Levenshtein`.
3.  **Długość i znaki specjalne:** Liczymy nagromadzenie myślników i cyfr, co jest typowe dla linków podszywających się pod komunikaty wsparcia technicznego.

Algorytm klasyfikatora podejmuje ostateczną decyzję na podstawie wagi tych cech, zmniejszając ryzyko tzw. "False Positives" (fałszywych alarmów).

---

## 4. Wyrocznia zewnętrzna (Threat Intelligence)
Nawet jeśli model ML wskaże domenę jako phishing, dla 100% pewności wysyłamy ciche, asynchroniczne zapytania w tle do dwóch światowych baz złośliwego oprogramowania, aby uzyskać potwierdzenie.

### API: `VirusTotal` oraz `Google Safe Browsing`
Moduł używa systemowej biblioteki `requests`, aby wysłać zapytania sieciowe. Posiadając klucze API pobierane bezpiecznie z pliku `.env` (przy pomocy biblioteki `python-dotenv`), nasz system łączy się z bazami Google oraz VirusTotal w chmurze i weryfikuje ich ostateczną reputację (czy znalazły się już na oficjalnej czarnej liście u producentów przeglądarek/antywirusów).

---

## Architektura Połączeń (Przepływ Danych)

Cały system działa opierając się o zasady programowania wielowątkowego (Multi-threading).

1.  Wystartowanie `main.py` inicjuje instancje wszystkich modułów i trenuje wstępnie model `scikit-learn`.
2.  Wydzielany jest tzw. "Wątek w tle" (Background Thread), w którym działa klient `certstream`. Jego jedynym zadaniem jest łapanie domen i wpychanie ich do `queue.Queue` (bufora).
3.  W tym samym czasie, Twój główny wątek (Główna pętla `while True`) "wyciąga" na bieżąco domeny z bufora kolejki:
    *   Jeśli kolejka jest pełna – wątek główny ma co robić na najwyższych obrotach.
    *   Jeśli jest pusta – zasypia bez niepotrzebnego zużywania procesora, czekając na nowe zdarzenia od CertStream.
4.  Dane swobodnie spływają "w dół wodospadu" (Pipeline): **Log -> Kolejka -> Heurystyki -> Ekstrakcja Cech matematycznych -> Model ML -> (Opcjonalnie) External API -> Konsola Ostrzeżeń.**

Dzięki tak zbudowanej architekturze obiektowej jesteś w stanie w przyszłości łatwo dodawać nową logikę (np. sprawdzanie rekordów DNS każdej wyłapanej domeny), tworząc nową klasę i wpinając ją pomiędzy powyższe kroki w `main.py`.
