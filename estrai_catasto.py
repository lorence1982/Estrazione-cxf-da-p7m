import os
import io
import zipfile
import tkinter as tk
from tkinter import filedialog
from asn1crypto import cms

def extract_cxf_from_p7m():
    # Nascondi la finestra principale di tkinter (serve solo per i dialoghi)
    root = tk.Tk()
    root.withdraw()

    print("=== ESTRATTORE FOGLI CATASTALI (Sister) ===")
    
    # 1. Scelta cartella di INPUT
    print("\nIn attesa della selezione della cartella di INPUT...")
    input_dir = filedialog.askdirectory(title="1. Seleziona la cartella contenente i .p7m")
    if not input_dir:
        print("Operazione annullata. Nessuna cartella di input selezionata.")
        return

    # 2. Scelta cartella di OUTPUT
    print("In attesa della selezione della cartella di OUTPUT...")
    output_dir = filedialog.askdirectory(title="2. Seleziona la cartella dove salvare i .cxf")
    if not output_dir:
        print("Operazione annullata. Nessuna cartella di output selezionata.")
        return

    # Trova tutti i file p7m
    p7m_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.p7m')]
    
    if not p7m_files:
        print("\nNessun file .p7m trovato nella cartella selezionata.")
        return

    print(f"\nTrovati {len(p7m_files)} file .p7m. Inizio l'estrazione...\n")

    # Elaborazione batch
    for filename in p7m_files:
        filepath = os.path.join(input_dir, filename)
        print(f"Elaborazione: {filename}")
        
        try:
            # Leggi il file p7m in formato binario
            with open(filepath, 'rb') as f:
                der_bytes = f.read()
            
            # Analizza la struttura crittografica (Decodifica ASN.1)
            content_info = cms.ContentInfo.load(der_bytes)
            
            # Verifica che sia un file firmato
            if content_info['content_type'].native != 'signed_data':
                print(f"  [!] Il file {filename} non sembra un p7m valido.")
                continue
                
            # Estrai il payload (il file ZIP) dalla busta p7m
            signed_data = content_info['content']
            payload_bytes = signed_data['encap_content_info']['content'].native
            
            # Carica il file ZIP direttamente nella RAM
            zip_buffer = io.BytesIO(payload_bytes)
            
            # Apri lo ZIP ed estrai i file .cxf
            with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
                cxf_files = [f for f in zip_ref.namelist() if f.lower().endswith('.cxf')]
                
                if not cxf_files:
                    print("  [!] Nessun file .cxf trovato all'interno di questo archivio.")
                
                for cxf_file in cxf_files:
                    zip_ref.extract(cxf_file, output_dir)
                    print(f"  -> Estratto: {cxf_file}")
                    
        except Exception as e:
            print(f"  [X] Errore durante l'estrazione di {filename}: {e}")

    print("\n=== ESTRAZIONE COMPLETATA CON SUCCESSO! ===")

if __name__ == "__main__":
    extract_cxf_from_p7m()