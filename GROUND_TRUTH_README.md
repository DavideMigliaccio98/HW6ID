# Ground-Truth Generation - Documentazione

## 📋 Panoramica

Il notebook `ground_truth_vin.ipynb` implementa un processo robusto di creazione di ground-truth per Entity Resolution basato su VIN (Vehicle Identification Number).

## 🔄 Processo Implementato

### 1. Pre-Processing e Deduplicazione
**Problema**: Stesso veicolo (VIN) può apparire più volte → prodotto cartesiano di match

**Soluzione**: Deduplicazione su VIN mantenendo solo prima occorrenza

```
Craigslist: 427k → X record unici con VIN valido
Used Cars: 3M → Y record unici con VIN valido
```

### 2. Positive Matches (Label = 1)
**Metodo**: Join su VIN con **Anti-Noise Filter**

**Anti-Noise Filter**: 
- ✅ VIN coincide + Manufacturer coerente → ACCEPT
- ❌ VIN coincide MA Manufacturer incompatibile → REJECT (VIN errato/riciclato)

**Validazione aggiuntiva**:
- Anno identico (OBBLIGATORIO)
- Model simile (WARNING se diverso)
- Prezzo nel range ±$5000 o ±50%
- Mileage coerente ±10000 miglia o ±20%

### 3. Negative Matches (Label = 0)
**Strategia**: Campionamento casuale sintetico

**Parametri**:
- Ratio: 5 negativi per ogni 1 positivo
- Verifica: Coppia NON presente nei positivi
- Evita: Duplicati nel dataset negativo

**Risultato atteso**:
```
Positivi: ~N coppie (label=1)
Negativi: ~5N coppie (label=0)
Totale: ~6N coppie
```

### 4. Train/Validation/Test Split
**Proporzioni**:
- Train: 60% (~3.6N coppie)
- Validation: 20% (~1.2N coppie)
- Test: 20% (~1.2N coppie)

**Garanzie**:
- ✅ Shuffle con random_state=42
- ✅ No Data Leakage (0 overlap tra split)
- ✅ Distribuzione bilanciata label in ogni split

### 5. Dataset ML (No-VIN)
**Output**:
- `dataset_A_no_vin.csv`: Record Craigslist coinvolti SENZA VIN
- `dataset_B_no_vin.csv`: Record Used Cars coinvolti SENZA VIN

**Obiettivo**: Forzare il modello ML a imparare su attributi fuzzy:
- year, manufacturer/make_name, model/model_name
- price, odometer/mileage
- fuel, transmission, drive/wheel_system
- latitude, longitude, region/city

## 📦 File Generati

```
ground_truth/
├── train.csv                        # Training set (60%, ~3.6N coppie)
├── validation.csv                   # Validation set (20%, ~1.2N coppie)
├── test.csv                         # Test set (20%, ~1.2N coppie)
├── ground_truth_complete.csv        # Dataset completo con label (100%, ~6N coppie)
├── dataset_A_no_vin.csv            # Craigslist record senza VIN
├── dataset_B_no_vin.csv            # Used Cars record senza VIN
├── positive_matches_mapping.csv     # Mapping VIN → ID solo per positivi
└── metadata.json                    # Metadati completi del processo
```

## 📊 Struttura Dataset

### Ground-Truth Files (train/val/test/complete)
| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| `vin` | string | VIN comune (solo positivi) |
| `craigslist_id` | int | ID record Craigslist |
| `used_cars_id` | int | ID record Used Cars |
| `label` | int | 1=match, 0=non-match |
| `year` | int | Anno veicolo |
| `manufacturer_cr` | string | Produttore Craigslist |
| `manufacturer_uc` | string | Produttore Used Cars |
| `model_cr` | string | Modello Craigslist |
| `model_uc` | string | Modello Used Cars |
| `price_cr` | float | Prezzo Craigslist |
| `price_uc` | float | Prezzo Used Cars |
| `mileage_cr` | float | Chilometraggio Craigslist |
| `mileage_uc` | float | Chilometraggio Used Cars |
| `warnings` | int | Numero warnings validazione (solo positivi) |
| `warning_details` | string | Dettagli warnings (solo positivi) |

### Dataset No-VIN Files
Contengono **tutti** gli attributi originali ECCETTO:
- ❌ VIN / vin
- ❌ vin_clean

## 🎯 Utilizzi

### 1. Training Modelli ML Supervisionati
```python
import pandas as pd

# Carica split
df_train = pd.read_csv('ground_truth/train.csv')
df_val = pd.read_csv('ground_truth/validation.csv')
df_test = pd.read_csv('ground_truth/test.csv')

# Carica dataset no-VIN
df_A = pd.read_csv('ground_truth/dataset_A_no_vin.csv')
df_B = pd.read_csv('ground_truth/dataset_B_no_vin.csv')

# Feature engineering
# ... calcola similarity scores tra attributi
# ... train modello su df_train
# ... valida su df_val
# ... test finale su df_test
```

### 2. Valutazione Entity Resolution
```python
from sklearn.metrics import precision_score, recall_score, f1_score

# Applica algoritmo di matching
predictions = your_matching_algorithm(df_test)

# Valuta
precision = precision_score(df_test['label'], predictions)
recall = recall_score(df_test['label'], predictions)
f1 = f1_score(df_test['label'], predictions)

print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1-Score: {f1:.3f}")
```

### 3. Active Learning
```python
# Identifica coppie con bassa confidence
uncertain_pairs = identify_uncertain_matches(df_unlabeled)

# Labeling manuale
for pair in uncertain_pairs:
    label = human_annotator(pair)
    add_to_ground_truth(pair, label)

# Ritraining
model.retrain(expanded_ground_truth)
```

## ⚠️ Limitazioni

### Coverage
- Solo veicoli con **VIN validi** in entrambi i dataset
- Possibile % bassa di overlap (~0.1-1% tipico)

### Bias
- Bias verso dealership professionali (più VIN validi)
- Bias verso veicoli recenti (VIN standardizzato dal 1981)

### Negativi Sintetici
- Non sono "hard negatives" (coppie simili ma diverse)
- Potrebbero essere troppo facili da distinguere
- Considera generazione targeted di hard negatives

## 🔍 Metriche di Qualità

**Balance**:
```
Ratio negativi/positivi = 5:1 ✅
```

**Diversity**:
```
✅ Manufacturer unici: >10
✅ Anni coperti: 1980-2026
✅ Fasce prezzo: $500-$200,000
✅ Fasce mileage: 0-500,000 miglia
```

**Consistency** (solo positivi):
```
✅ Anno identico: 100%
✅ Manufacturer compatibile: 100%
⚠️ Warnings (price/mileage diff): <30%
```

**Size**:
```
✅ Train: >1000 esempi
✅ Validation: >300 esempi
✅ Test: >300 esempi
```

## 🚀 Prossimi Passi

### Se Ground-Truth Generato con Successo
1. **Feature Engineering**:
   - Similarity scores (Levenshtein, Jaro-Winkler)
   - Difference features (price_diff, mileage_diff)
   - Categorical matches (same_year, same_manufacturer)

2. **Model Training**:
   - Random Forest / XGBoost per interpretabilità
   - Neural Networks per performance
   - Ensemble per robustezza

3. **Evaluation**:
   - Cross-validation su train
   - Hyperparameter tuning su validation
   - Final metrics su test (SOLO UNA VOLTA)

### Se Pochi/Nessun VIN Comune
1. **Matching Probabilistico**:
   - Blocking su (year, manufacturer)
   - Similarity su (model, price, mileage)
   - Threshold tuning

2. **Clustering + Validation**:
   - Cluster veicoli simili
   - Validazione manuale campione rappresentativo
   - Propagazione label

3. **Record Linkage Libraries**:
   - Dedupe (Python)
   - Splink (Python)
   - RecordLinkage (Python)

4. **Crowdsourcing**:
   - Amazon Mechanical Turk
   - Label Studio
   - Prodigy

## 📚 Riferimenti

- **VIN Standard**: ISO 3779, ISO 4030
- **Entity Resolution**: Christen, P. (2012). "Data Matching"
- **Active Learning**: Settles, B. (2012). "Active Learning Literature Survey"
- **Imbalanced Learning**: He & Garcia (2009). "Learning from Imbalanced Data"

## ❓ FAQ

**Q: Perché ratio 5:1 negativi/positivi?**  
A: Balance tra realismo (matching è task raro) e learnability (non troppo imbalanced).

**Q: Posso modificare il ratio?**  
A: Sì, cambia `NEGATIVE_RATIO = 5` nel codice. Valori comuni: 1:1, 3:1, 5:1, 10:1.

**Q: Cosa fare se nessun VIN comune?**  
A: Implementa matching probabilistico o crowdsourcing (vedi "Prossimi Passi").

**Q: Come gestire hard negatives?**  
A: Genera negativi con blocking su (year, manufacturer) → più simili ma diversi.

**Q: Posso usare per altri domini?**  
A: Sì! Sostituisci VIN con qualsiasi unique key (ISBN, Product Code, SSN, etc.).
