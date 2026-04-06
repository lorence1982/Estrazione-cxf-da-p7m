# Estrazione cxf da p7m
Estrazione automatica dai file p7m dei cxf catastali sia in ambiente Windows che ambiente QGIS

# Utilizzare lo script in ambiente Windows (*estrai_catasto.py*)
- Attraverso il Prompt dei comandi (o PowerShell), installare la libreria che gestisce la crittografia, digitando *pip install asn1crypto*
- Scaricare il file **estrai_catasto.py**
- Avviare il file **estrai_catasto.py** utilizzando un *IDE*, oppure tramite prompt dei comandi, digitando *python estrai_catasto.py*

Si aprirà una finestra classica di Windows che chiederà di selezionare prima la cartella dove sono salvati tutti i file .p7m scaricati da Sister, e subito dopo, si aprirà un'altra finestra in cui indicare dove salvare i .cxf

# Utilizzare lo script in ambiente QGIS (*estrai_catasto_qgis.py*)
- In **OSGeo4W Shell** digitare *pip install asn1crypto*
- Scaricare il file **estrai_catasto_qgis.py**
- Aprire il file **estrai_catasto_qgis.py** tramite la console Python di QGIS
- Eseguire lo script

Anche in questo caso si aprirà una finestra classica di Windows che chiederà di selezionare prima la cartella dove sono salvati tutti i file .p7m scaricati da Sister, e subito dopo, si aprirà un'altra finestra in cui indicare dove salvare i .cxf
