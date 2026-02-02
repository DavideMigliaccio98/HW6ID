import kagglehub

# Download dataset 1: Craigslist Cars & Trucks Data
print("Downloading Craigslist Cars & Trucks dataset...")
path1 = kagglehub.dataset_download("austinreese/craigslist-carstrucks-data")
print("Path to dataset 1 files:", path1)

# Download dataset 2: US Used Cars Dataset
print("\nDownloading US Used Cars dataset...")
path2 = kagglehub.dataset_download("ananaymital/us-used-cars-dataset")
print("Path to dataset 2 files:", path2)

print("\n✓ Both datasets downloaded successfully!")
