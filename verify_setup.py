import pandas as pd
import os

print("=" * 60)
print("VERIFICA SETUP DATASET - HW6ID")
print("=" * 60)

# Lista file da verificare con dimensioni attese
files_to_check = [
    ('dataset/craigslist.csv', 'Craigslist Original', 1300, 1400),
    ('dataset/used_cars.csv', 'Used Cars Original', 1300, 1400),
    ('ground_truth/dataset_A_no_vin.csv', 'Dataset A (no VIN)', 50, 55),
    ('ground_truth/dataset_B_no_vin.csv', 'Dataset B (no VIN)', 45, 55),
    ('schema/craigslist_aligned.csv', 'Craigslist Aligned', 1300, 1400),
    ('schema/used_cars_aligned.csv', 'Used Cars Aligned', 300, 350),
]

# File già presenti nel repository
files_already_present = [
    ('ground_truth/train.csv', 'Train Set'),
    ('ground_truth/validation.csv', 'Validation Set'),
    ('ground_truth/test.csv', 'Test Set'),
    ('ground_truth/ground_truth_complete.csv', 'Ground Truth Complete'),
]

all_ok = True
missing_files = []
present_files = []

print("\n📥 FILE DA SCARICARE/RIGENERARE:")
print("-" * 60)

for filepath, name, min_mb, max_mb in files_to_check:
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath, nrows=5)  # Quick check
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            
            if min_mb <= size_mb <= max_mb:
                status = "✅ OK"
            else:
                status = f"⚠️  WARN (expected {min_mb}-{max_mb}MB)"
            
            print(f"{status} {name}: {size_mb:.2f} MB")
            present_files.append(name)
        except Exception as e:
            print(f"❌ ERRORE {name}: {str(e)}")
            all_ok = False
            missing_files.append(name)
    else:
        print(f"❌ MANCANTE: {name}")
        all_ok = False
        missing_files.append(name)

print("\n" + "-" * 60)
print("✅ FILE GIÀ PRESENTI NEL REPOSITORY:")
print("-" * 60)

for filepath, name in files_already_present:
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath, nrows=5)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            rows = len(pd.read_csv(filepath))
            print(f"✅ {name}: {rows:,} righe, {size_mb:.2f} MB")
        except Exception as e:
            print(f"⚠️  {name}: Error reading - {str(e)}")
    else:
        print(f"❌ {name}: MANCANTE (dovrebbe essere nel repo!)")

print("\n" + "=" * 60)
print("RIEPILOGO")
print("=" * 60)

if all_ok:
    print("✅ SETUP COMPLETO!")
    print("   Tutti i file necessari sono presenti e validi.")
    print("   Puoi procedere con l'esecuzione dei notebook.")
else:
    print("❌ SETUP INCOMPLETO")
    print(f"   File presenti: {len(present_files)}/{len(files_to_check)}")
    print(f"   File mancanti: {len(missing_files)}")
    print("\n📋 Azioni richieste:")
    
    if any('Original' in f for f in missing_files):
        print("   1. Scarica i dataset originali:")
        print("      cd dataset && python download_datasets.py")
    
    if any('no VIN' in f for f in missing_files):
        print("   2. Esegui ground_truth_vin.ipynb per generare:")
        print("      - dataset_A_no_vin.csv")
        print("      - dataset_B_no_vin.csv")
    
    if any('Aligned' in f for f in missing_files):
        print("   3. Esegui schema_mediato.ipynb per generare:")
        print("      - craigslist_aligned.csv")
        print("      - used_cars_aligned.csv")
    
    print("\n   Consulta DATASET_SETUP.md per istruzioni dettagliate.")

print("=" * 60)
