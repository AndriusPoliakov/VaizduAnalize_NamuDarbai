# Vaizdų analizės sistema - namų darbai

## 1ND – Nuotraukų analizė ir orientyrų atpažinimas

**Naudoti metodai ir bibliotekos:**
- **OpenAI CLIP** – naudojamas orientyrų atpažinimui nuotraukose.
- **PyTorch** – leidžia įkelti ir naudoti CLIP modelį.
- **OpenCV** – vaizdų apdorojimui ir anotacijoms.
- **Pillow** – nuotraukų skaitymui ir konvertavimui.

**Veikimo procesas:**
1. Vartotojo įkelta nuotrauka apdorojama CLIP modeliu.
2. Modelis atlieka palyginimą su žinomais orientyrais.
3. Aptiktas orientyras pažymimas ant nuotraukos ir išsaugomas.

## 2ND – Drono sekimas vaizdo įrašuose

**Naudoti metodai ir bibliotekos:**
- **OpenCV Tracker (CSRT)** – naudojamas objekto sekimui vaizdo įraše.
- **OpenCV VideoCapture** – vaizdo įrašų nuskaitymui.
- **NumPy** – duomenų apdorojimui.

**Veikimo procesas:**
1. Naudojamas CSRT algoritmas drono sekimui vaizdo įraše.
2. Vartotojas pažymi droną pirmame kadre.
3. Algoritmas seką droną per visus kadrus ir išsaugo pažymėtą vaizdo įrašą.

## 3ND – Sistemos veikimas
Ši sistema leidžia vartotojams įkelti nuotraukas ir vaizdo įrašus, kurie yra apdorojami naudojant Flask API ir pateikiami per React vartotojo sąsają. Sistema atpažįsta orientyrus iš nuotraukų bei seka dronus vaizdo įrašuose.

**Pilnas veikimo procesas:**
1. Vartotojas įkelia nuotrauką → sistema atpažįsta orientyrą ir grąžina pažymėtą vaizdą.
2. Vartotojas įkelia vaizdo įrašą → sistema suseka droną ir grąžina pažymėtą vaizdo įrašą. ## Per web sąsają ir google collab'e neveikia dėl pirmo kadro žymėjimo (vartotojas pažymi kur yra dronas, 2ND kodą reikia pasileisti lokaliai)
3. Flask API apdoroja užklausas ir siunčia atsakymus į React frontendą.

## Sistemos paleidimo instrukcijos

### Flask API paleidimas
```bash
cd "kelias iki katalogo"
python flask_api_3nd.py
```
API veiks adresu: **http://localhost:5000**

### React frontend paleidimas
```bash
cd "kelias iki katalogo"
npm install
npm start
```
React aplikacija bus pasiekiama adresu: **http://localhost:3000**

## 🛠 Iškilusios problemos ir jų sprendimai

**1. Web sąsajoj neveikia 2ND užduoties sprendimas
Drono sekimo programinį kodą reikia pasileisti lokaliai, nes web sąsaja ir google collab crashina, nes prieš modeliui pradedant sekti droną, vartotojas turi pažymėti pradinę drono vietą.


**2. `ModuleNotFoundError` klaidos dėl bibliotekų**  
**Įdiegtos trūkstamos bibliotekos:**
```bash
pip install flask flask-cors torch torchvision clip-by-openai numpy pillow opencv-python matplotlib
```

**3. `Large file detected` klaida GitHub**

**4. Netikslus 1ND modelio veikimas
Buvo išbandyti 3 modeliai:
1) YOLOv3, YOLOv5, YOLOv8 modeliai - atpažino paprastus objektus, tokius kaip laivai, žmonės ir pan., bet ne žymius objektus.
2) Google Landmarks API - Nerado nei vieno objekto iš pateiktų nuotraukų
3) CLIP - pirmoji versija atpažino 1 iš 3, praplėtus orientyrų sąrašą - visi objektai buvo atpažinti.


## Rezultatų pavyzdžiai
Input nuotraukos yra Input kataloge, tiek pirmojo ir antrojo ND kataloguose.
Rezultatai yra Output kataloge, tiek pirmojo ir antrojo ND kataloguose.

---
📌 **Autorius**: Andrius Poliakov
📅 **Data**: 2025-03-01
