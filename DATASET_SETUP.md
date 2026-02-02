# 📥 Setup Dataset - File CSV Mancanti

## ⚠️ Importante
I file CSV dei dataset originali **non sono inclusi** nel repository Git perché superano il limite di 100MB di GitHub.

**File mancanti**:
- `dataset/craigslist.csv` (1.38 GB)
- `dataset/used_cars.csv` (1.33 GB)
- `ground_truth/dataset_A_no_vin.csv` (52 MB)
- `ground_truth/dataset_B_no_vin.csv` (48 MB)
- `schema/craigslist_aligned.csv` (1.33 GB)
- `schema/used_cars_aligned.csv` (310 MB)
- `schema/schema_finale.csv`

---

## 🔄 Opzione 1: Download Automatico (Consigliato)

### 1.1 Script Automatico

Usa lo script Python incluso per scaricare i dataset originali:

```bash
cd dataset
python download_datasets.py
```

Lo script scaricherà:
- ✅ `craigslist.csv` (Craigslist Vehicles)
- ✅ `used_cars.csv` (Used Cars Dataset)

**Fonte Dataset**:
- **Craigslist Vehicles**: [Kaggle - Craigslist Vehicles Dataset](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data)
- **Used Cars**: [Kaggle - Used Cars Dataset](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data) o simili

### 1.2 Download Manuale da Kaggle

Se lo script non funziona:

1. **Vai su Kaggle**: https://www.kaggle.com
2. **Crea un account** (se non ce l'hai)
3. **Cerca i dataset**:
   - "Craigslist Vehicles" 
   - "Used Cars Dataset"
4. **Scarica i CSV**
5. **Rinomina e posiziona**:
   ```
   dataset/
   ├── craigslist.csv     # Rinomina il file scaricato
   └── used_cars.csv      # Rinomina il file scaricato
   ```

---

## 🔧 Opzione 2: Rigenera da Zero (Se hai già i dataset originali)

Se hai già `craigslist.csv` e `used_cars.csv` nella cartella `dataset/`, esegui i notebook in ordine:

### Step 1: Allineamento Schema
📓 **Notebook**: `schema_mediato.ipynb`

Esegui tutte le celle per generare:
- ✅ `schema/craigslist_aligned.csv`
- ✅ `schema/used_cars_aligned.csv`
- ✅ `schema/schema_finale.csv`

### Step 2: Ground Truth con VIN
📓 **Notebook**: `ground_truth_vin.ipynb`

**IMPORTANTE**: Questo notebook richiede i dataset **CON VIN** originali.

Esegui tutte le celle per generare:
- ✅ `ground_truth/dataset_A_no_vin.csv`
- ✅ `ground_truth/dataset_B_no_vin.csv`
- ✅ `ground_truth/ground_truth_complete.csv` (già presente)
- ✅ `ground_truth/train.csv` (già presente)
- ✅ `ground_truth/validation.csv` (già presente)
- ✅ `ground_truth/test.csv` (già presente)

**Nota**: I file `train.csv`, `test.csv`, `validation.csv` sono già nel repository, ma puoi rigenerarli se necessario.

---

## 📋 Checklist Setup Completo

Dopo aver scaricato/rigenerato, verifica di avere:

### Dataset Originali
```
dataset/
├── craigslist.csv          ✅ (1.38 GB)
├── used_cars.csv           ✅ (1.33 GB)
└── download_datasets.py    ✅ (già presente)
```

### Schema Allineato
```
schema/
├── craigslist_aligned.csv      ✅ (1.33 GB)
├── used_cars_aligned.csv       ✅ (310 MB)
├── schema_finale.csv           ✅
├── metadata_allineamento.json  ✅ (già presente)
└── report_allineamento_*.txt   ✅ (già presente)
```

### Ground Truth
```
ground_truth/
├── dataset_A_no_vin.csv           ✅ (52 MB)
├── dataset_B_no_vin.csv           ✅ (48 MB)
├── ground_truth_complete.csv      ✅ (già presente)
├── train.csv                      ✅ (già presente)
├── validation.csv                 ✅ (già presente)
├── test.csv                       ✅ (già presente)
├── positive_matches_mapping.csv   ✅ (già presente)
└── metadata.json                  ✅ (già presente)
```

---

## 🚀 Verifica Setup

Dopo il download/rigenerazione, testa con questo script Python:

```python
import pandas as pd
import os

# Verifica dataset originali
print("=" * 60)
print("VERIFICA DATASET ORIGINALI")
print("=" * 60)

files_to_check = [
    ('dataset/craigslist.csv', 'Craigslist'),
    ('dataset/used_cars.csv', 'Used Cars'),
    ('ground_truth/dataset_A_no_vin.csv', 'Dataset A (no VIN)'),
    ('ground_truth/dataset_B_no_vin.csv', 'Dataset B (no VIN)'),
]

all_ok = True
for filepath, name in files_to_check:
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"✅ {name}: {len(df):,} righe, {size_mb:.2f} MB")
    else:
        print(f"❌ {name}: FILE MANCANTE")
        all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("✅ SETUP COMPLETO - Tutti i file necessari sono presenti!")
else:
    print("❌ SETUP INCOMPLETO - Alcuni file mancano")
print("=" * 60)
```

Salva come `verify_setup.py` ed esegui:
```bash
python verify_setup.py
```

---

## 🔗 Link Utili

### Dataset Kaggle
- **Craigslist Vehicles**: https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data
- **Alternative**: Cerca "used cars dataset" su Kaggle

### Kaggle API (Download Programmatico)
Se hai configurato Kaggle API:

```bash
# Installa Kaggle CLI
pip install kaggle

# Configura credenziali (~/.kaggle/kaggle.json)
# Scarica dataset
kaggle datasets download -d austinreese/craigslist-carstrucks-data
unzip craigslist-carstrucks-data.zip -d dataset/
```

---

## ⚠️ Troubleshooting

### Problema: "File not found" nei notebook
**Soluzione**: Verifica che i file CSV siano nelle cartelle corrette:
- `dataset/craigslist.csv`
- `dataset/used_cars.csv`

### Problema: "Out of memory" durante caricamento
**Soluzione**: I dataset sono grandi (~2.7GB totali). Serve almeno:
- 8GB RAM per caricare i CSV
- 16GB RAM consigliati per elaborazione

Usa chunk loading:
```python
# Invece di pd.read_csv(file)
chunks = pd.read_csv(file, chunksize=50000)
df = pd.concat(chunks, ignore_index=True)
```

### Problema: Download lento da Kaggle
**Soluzione**: 
- Usa Kaggle API (più veloce)
- Scarica durante la notte
- Usa connessione stabile (no mobile)

---

## 📞 Supporto

Se hai problemi:
1. Verifica di aver scaricato i dataset corretti (Craigslist Vehicles con VIN)
2. Controlla dimensioni file (~1.3-1.4GB ciascuno)
3. Esegui `verify_setup.py` per diagnostica
4. Controlla i log nei notebook per errori specifici

---

## 📝 Note Importanti

1. **VIN è essenziale**: Il dataset Craigslist deve contenere la colonna `VIN` per generare il ground truth
2. **Non committare i CSV grandi**: Sono esclusi dal `.gitignore` per evitare problemi con GitHub
3. **Backup locale**: Conserva una copia locale dei dataset originali dopo il download
4. **Privacy**: I dataset Kaggle sono pubblici, ma verifica le licenze prima di redistribuire

---

## ✅ Setup Rapido (TL;DR)

```bash
# 1. Download dataset
cd dataset
python download_datasets.py

# 2. Verifica
cd ..
python verify_setup.py

# 3. Se OK, rigenera file derivati
# Esegui in ordine:
# - schema_mediato.ipynb
# - ground_truth_vin.ipynb

# 4. Procedi con il resto del workflow
```

---

**Ultimo aggiornamento**: Febbraio 2026
