import pandas as pd
import numpy as np

# Funktion zur Bereinigung der Prozentwerte und Umwandlung in float
def clean_percentage(value):
    try:
        return float(value.strip('%'))  # Entfernen von "%" und Umwandeln in Float
    except ValueError:
        return None

# Funktion zur Umwandlung von Float in Prozent-String
def format_percentage(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:.1f}%"

# Datei laden
file_path = 'upos_percentages.csv'  # Originaldatei
output_path = 'upos_percentage_differences.csv'  # Ausgabe

data = pd.read_csv(file_path)

# Bereinigen der Daten
for col in ['gpt4o', 'gpt35t', 'perplexity', 'claude', 'human']:
    data[col] = data[col].apply(clean_percentage)

# Berechnung der prozentualen Unterschiede
language_models = ['gpt4o', 'gpt35t', 'perplexity', 'claude']
results = []

for _, row in data.iterrows():
    result_row = {'UPOS': row['UPOS']}
    for model in language_models:
        if row['human'] == 0:  # Überprüfung auf Division durch Null
            diff = np.nan
        else:
            diff = ((row[model] - row['human']) / row['human']) * 100  # Prozentuale Differenz
        result_row[model] = format_percentage(diff)
    results.append(result_row)

# Erstellen eines DataFrames für die Ergebnisse
results_df = pd.DataFrame(results)

# Speichern der Ergebnisse in einer neuen CSV-Datei
results_df.to_csv(output_path, index=False)

print(f"Ergebnisse wurden in der Datei '{output_path}' gespeichert.")
