import os
import io
import zipfile
import subprocess
import sys
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.core import Qgis
from qgis.utils import iface

# 1. Gestione dinamica della libreria asn1crypto nell'ambiente QGIS
try:
    from asn1crypto import cms
except ImportError:
    iface.messageBar().pushMessage("Installazione", "Sto installando la libreria necessaria (asn1crypto)...", level=Qgis.Info, duration=5)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "asn1crypto"])
        from asn1crypto import cms
        iface.messageBar().pushMessage("Successo", "Libreria installata!", level=Qgis.Success, duration=3)
    except Exception as e:
        iface.messageBar().pushMessage("Errore", "Impossibile installare asn1crypto. Installa manualmente da OSGeo4W Shell.", level=Qgis.Critical, duration=10)
        raise

def estrai_cxf_qgis():
    # 2. Finestre di dialogo native di QGIS
    input_dir = QFileDialog.getExistingDirectory(None, "1. Seleziona la cartella contenente i .p7m")
    if not input_dir:
        return

    output_dir = QFileDialog.getExistingDirectory(None, "2. Seleziona la cartella dove salvare i .cxf")
    if not output_dir:
        return

    p7m_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.p7m')]
    
    if not p7m_files:
        iface.messageBar().pushMessage("Attenzione", "Nessun .p7m trovato nella cartella selezionata.", level=Qgis.Warning, duration=5)
        return

    estratti = 0
    errori = []

    iface.messageBar().pushMessage("Elaborazione", f"Estrazione di {len(p7m_files)} file p7m in corso...", level=Qgis.Info, duration=5)

    # 3. Estrazione dei .cxf senza caricamento in mappa
    for filename in p7m_files:
        filepath = os.path.join(input_dir, filename)
        try:
            # Lettura e decodifica della busta crittografica
            with open(filepath, 'rb') as f:
                der_bytes = f.read()
            
            content_info = cms.ContentInfo.load(der_bytes)
            
            if content_info['content_type'].native != 'signed_data':
                errori.append(f"{filename} non sembra un file p7m valido.")
                continue
                
            signed_data = content_info['content']
            payload_bytes = signed_data['encap_content_info']['content'].native
            
            # Lettura dello ZIP in memoria
            zip_buffer = io.BytesIO(payload_bytes)
            
            # Estrazione fisica dei file
            with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
                cxf_files = [f for f in zip_ref.namelist() if f.lower().endswith('.cxf')]
                for cxf_file in cxf_files:
                    zip_ref.extract(cxf_file, output_dir)
                    estratti += 1
                    
        except Exception as e:
            errori.append(f"Errore su {filename}: {e}")

    # 4. Report Finale
    if estratti > 0:
        iface.messageBar().pushMessage("Completato", f"Operazione conclusa: estratti fisicamente {estratti} file .cxf!", level=Qgis.Success, duration=5)
    
    if errori:
        iface.messageBar().pushMessage("Attenzione", "Ci sono stati alcuni errori. Controlla la console Python.", level=Qgis.Warning, duration=5)
        print("\n--- REPORT ERRORI ---")
        for err in errori:
            print(err)

# Avvia lo script
estrai_cxf_qgis()