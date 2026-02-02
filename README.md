# HW6ID - Entity Resolution Project

## 📋 Descrizione
Progetto di Entity Resolution per matching di record di veicoli tra due dataset (Craigslist e Used Cars) senza VIN.

---

## 🗂️ Struttura del Progetto

```
HW6ID/
├── dataset/                          # Dataset originali
│   ├── craigslist.csv               # Dataset Craigslist
│   └── used_cars.csv                # Dataset Used Cars
│
├── ground_truth/                     # Ground truth generato da VIN matching
│   ├── dataset_A_no_vin.csv        # Dataset A senza VIN
│   ├── dataset_B_no_vin.csv        # Dataset B senza VIN
│   ├── ground_truth_complete.csv   # Tutti i match trovati (15,412)
│   ├── train.csv                   # Training set (10,790 coppie)
│   ├── validation.csv              # Validation set (2,311 coppie)
│   ├── test.csv                    # Test set (2,315 coppie)
│   └── metadata.json               # Metadati split
│
├── blocking_results/                # Risultati blocking strategies
│   ├── candidates_B1.csv           # B1: Manufacturer+Model (964,002 coppie)
│   ├── candidates_B2.csv           # B2: Manufacturer+Model+Year (77,087 coppie)
│   └── blocking_metrics.json       # Metriche blocking (Pairs Quality, Completeness)
│
├── record_linkage_results/          # Risultati Python recordlinkage
│   ├── predictions_B1.csv
│   ├── predictions_B2.csv
│   └── metrics.json
│
├── dedupe_results/                  # Risultati Python dedupe library
│   ├── dedupe_predictions_B1.csv
│   ├── dedupe_predictions_B2.csv
│   ├── dedupe_settings             # Modello salvato
│   ├── dedupe_training.json        # Training data
│   └── dedupe_metrics.json
│
├── ditto_results/                   # Risultati Ditto (Deep Learning)
│   ├── ditto_predictions_B1.csv
│   ├── ditto_predictions_B2.csv
│   ├── ditto_metrics.json
│   └── Cars_ER/                    # Modello addestrato (escluso da Git)
│       └── model.pt                # Modello PyTorch (~260MB)
│
├── FAIR-DA4ER/                      # Framework Ditto (submodule)
│   └── ditto/
│       ├── train_ditto.py
│       ├── ditto_light/
│       └── data/cars/              # Dati training Ditto
│
└── Notebooks:
    ├── analisi_dati.ipynb          # 1. Analisi esplorativa dataset
    ├── schema_mediato.ipynb        # 2. Allineamento schema
    ├── ground_truth_vin.ipynb      # 3. Creazione ground truth con VIN
    ├── blocking_strategies.ipynb   # 4. Blocking B1 e B2
    ├── record_linkage.ipynb        # 5. RecordLinkage (rule-based)
    ├── dedupe_library.ipynb        # 6. Dedupe (ML probabilistico)
    └── ditto_model.ipynb           # 7. Ditto (Deep Learning)
```

---

## 🚀 Ordine di Esecuzione (Procedura Completa)

### **FASE 1: Preparazione Dati**

#### 1.1 Analisi Esplorativa
📓 **Notebook**: `analisi_dati.ipynb`
- Caricamento dataset originali
- Statistiche descrittive
- Analisi valori mancanti
- Distribuzione attributi (manufacturer, year, price, mileage)

#### 1.2 Allineamento Schema
📓 **Notebook**: `schema_mediato.ipynb`
- Normalizzazione nomi colonne
- Mapping manufacturer (es: "chevy" → "Chevrolet")
- Standardizzazione fuel_type, transmission
- Salvataggio schema allineato

#### 1.3 Ground Truth con VIN
📓 **Notebook**: `ground_truth_vin.ipynb`
- **INPUT**: `craigslist.csv`, `used_cars.csv` (con VIN)
- **OUTPUT**: 
  - `ground_truth_complete.csv` (15,412 match)
  - `dataset_A_no_vin.csv`, `dataset_B_no_vin.csv` (VIN rimosso)
  - `train.csv` (10,790), `validation.csv` (2,311), `test.csv` (2,315)
- **Split**: 70% train, 15% validation, 15% test
- ⚠️ **IMPORTANTE**: Train/Test separati per evitare data leakage

---

### **FASE 2: Blocking Strategies**

#### 2.1 Generazione Coppie Candidate
📓 **Notebook**: `blocking_strategies.ipynb`
- **B1 (Manufacturer + Model)**:
  - Coppie candidate: 964,002
  - Pairs Quality: 0.24%
  - Pairs Completeness: 99.57%
  
- **B2 (Manufacturer + Model + Year)**:
  - Coppie candidate: 77,087
  - Pairs Quality: 3.00%
  - Pairs Completeness: 98.50%

- **OUTPUT**: `candidates_B1.csv`, `candidates_B2.csv`

---

### **FASE 3: Entity Resolution - Metodi**

#### 3.1 RecordLinkage (Rule-Based)
📓 **Notebook**: `record_linkage.ipynb`

**Approccio**:
- Libreria: `recordlinkage`
- Comparatori: Jaro-Winkler (manufacturer, model), Linear (year), Gaussian (price, mileage)
- Classificazione: Score-based (sum of features >= threshold)

**CONFIG**:
```python
CONFIG = {
    'jw_threshold': 0.85,      # Threshold Jaro-Winkler
    'year_offset': 1.0,        # Offset year (±1 anno)
    'year_scale': 2.0,         # Scale linear
    'score_threshold': 5.5     # Threshold classificazione
}
```

**Risultati Migliori**:
- **B1** @ threshold=5.5: Precision 1.21%, Recall 35.12%, **F1 2.33%**
- **B2** @ threshold=5.5: Precision 5.21%, Recall 32.44%, **F1 5.19%**

**Limitazioni**: Precision bassa a causa di Blocking Quality (0.24% B1)

---

#### 3.2 Dedupe Library (ML Probabilistico)
📓 **Notebook**: `dedupe_library.ipynb`

**Approccio**:
- Libreria: `dedupe` (RecordLink)
- Active Learning (usato ground-truth invece)
- Campi: String (manufacturer, model), Price (year, price, mileage), Exact (fuel, transmission)

**Training**:
- Match pairs: ~2,724 (tutte le coppie positive nel train set)
- Distinct pairs: ~8,064 (tutte le coppie negative)
- Training time: ~5-10s

**Risultati**:
- **B1** @ threshold=0.5: Precision ~1-2%, Recall ~85-90%, F1 ~2-4%
- **B2** @ threshold=0.5: Precision ~5-7%, Recall ~85-90%, F1 ~10-13%

**Miglioramenti**: Recall molto alto, ma precision ancora limitata dal blocking

---

#### 3.3 Ditto (Deep Learning)
📓 **Notebook**: `ditto_model.ipynb`

**Approccio**:
- Framework: FAIR-DA4ER/Ditto
- Modello: DistilBERT (trasformers)
- Formato: COL attr VAL value (serializzazione)
- Epochs: 10, Batch size: 32, LR: 3e-5

**FIX Importante**: 
- Problema risolto: correlazione spuria (righe con "year" = match)
- Soluzione: ricostruito train/valid/test con year da dataset originali

**Training**:
- Training set: 10,788 coppie (100% con year)
- Training time: ~84s (GPU RTX 5080)

**Risultati**:
- **B1** @ threshold=0.5: Precision 1.27%, Recall 90.75%, **F1 2.50%**
- **B1** @ threshold=0.7: Precision 1.58%, Recall 88.38%, **F1 3.11%**
- **B2** @ threshold=0.5: Precision 6.76%, Recall 92.38%, **F1 12.59%**
- **B2** @ threshold=0.7: Precision 8.04%, Recall 90.09%, **F1 14.76%**

**Performance**: Miglior metodo, ma ancora limitato dal blocking

---

## 📊 Confronto Metodi (Best Results)

| Metodo          | Strategia | Precision | Recall  | **F1**   | Tempo Inference |
|-----------------|-----------|-----------|---------|----------|-----------------|
| RecordLinkage   | B1        | 1.21%     | 35.12%  | 2.33%    | ~5s            |
| RecordLinkage   | B2        | 5.21%     | 32.44%  | **5.19%**| ~1s            |
| Dedupe          | B1        | ~1.5%     | ~88%    | ~3%      | ~120s          |
| Dedupe          | B2        | ~6%       | ~90%    | ~11%     | ~15s           |
| **Ditto**       | B1        | 1.58%     | 88.38%  | 3.11%    | ~406s          |
| **Ditto**       | **B2**    | **8.04%** | **90.09%**| **14.76%**| ~34s        |

**🏆 VINCITORE**: Ditto B2 @ threshold=0.7 (F1: 14.76%)

---

## ⚠️ Limitazioni e Osservazioni

### Blocking Bottleneck
- **B1 Pairs Quality**: 0.24% → precision massima teorica ~0.24%
- **B2 Pairs Quality**: 3.00% → precision massima teorica ~3.00%
- Senza VIN, manufacturer+model crea blocchi enormi (es: Ford F-150: 318,660 coppie, 129 match = 0.04%)

### Recall vs Precision Trade-off
- **RecordLinkage**: Bassa recall (30-35%), precision media (1-5%)
- **Dedupe/Ditto**: Alta recall (88-92%), bassa precision (1-8%)
- Tutti i metodi limitati dal blocking

### Data Leakage Prevention
✅ **Corretto**:
- Training su `train.csv` (10,790 coppie)
- Valutazione su `test.csv` (2,315 coppie)
- Nessun overlap tra train e test

❌ **Da evitare**:
- Non filtrare dataset solo su ground-truth IDs
- Non usare test set per training

---

## 🔧 Setup Ambiente

### Requisiti
```bash
# Python 3.11
pip install pandas numpy scikit-learn matplotlib seaborn

# RecordLinkage
pip install recordlinkage

# Dedupe
pip install dedupe

# Ditto (PyTorch + Transformers)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
pip install transformers tqdm jsonlines nltk tensorboardX
```

### GPU (Opzionale per Ditto)
- CUDA 12.8
- GPU: NVIDIA RTX 5080 (16GB VRAM)
- Mixed Precision (FP16): Abilitato

---

## 📁 File NON Inclusi nel Repository Git

**Esclusi dal `.gitignore`**:
- ✅ `.venv/` - Virtual environment Python
- ✅ `__pycache__/` - Cache Python
- ✅ `*.pyc` - Bytecode compilato
- ✅ `.ipynb_checkpoints/` - Checkpoint Jupyter
- ✅ `ditto_results/Cars_ER/model.pt` - Modello PyTorch (~260MB)
- ✅ `ditto_results/events.out.*` - TensorBoard logs

**Inclusi nel repository**:
- ✅ Tutti i notebook `.ipynb`
- ✅ Tutti i CSV (dataset, ground_truth, risultati)
- ✅ JSON metriche
- ✅ File settings/training di Dedupe
- ✅ README.md, .gitignore

---

## 🎯 Prossimi Passi (Opzionali)

1. **Blocking Avanzato**:
   - Multi-pass blocking (più strategie combinate)
   - LSH (Locality Sensitive Hashing)
   - Canopy clustering

2. **Feature Engineering**:
   - N-gram similarity per model
   - Phonetic encoding (Soundex) per manufacturer
   - Feature geografiche (se disponibili)

3. **Ensemble Methods**:
   - Combinare RecordLinkage + Dedupe + Ditto
   - Voting o stacking

4. **Hyperparameter Tuning**:
   - Grid search su thresholds
   - Ottimizzazione learning rate Ditto
   - Cross-validation

---

## 📝 Note Importanti

### Tempi di Esecuzione Tipici
- Ground Truth VIN: ~5-10 min
- Blocking B1/B2: ~2-5 min
- RecordLinkage: ~5-10 min totale
- Dedupe Training: ~5-10s, Inference: ~2-3 min (B1+B2)
- Ditto Training: ~1.5 min, Inference: ~7 min (B1+B2)

### Memoria Richiesta
- Dataset: ~500MB (CSV)
- Blocking B1 candidates: ~50MB
- Ditto Model: ~260MB (model.pt)
- GPU VRAM: ~4-6GB durante training Ditto

### Riproducibilità
- Random seed: 42 (impostato in tutti i notebook)
- Versioni librerie: vedere requirements.txt (da creare)

---

## 👤 Autore
**migli** - HW6ID Entity Resolution Project - Febbraio 2026

---

## 📄 Licenza
Progetto educativo - Non specificata
