import shutil
import os
from datetime import datetime
import schedule
import time

# Chemins des répertoires et fichier de la base de données
db_path = 'user/users.db'
backup_dir = 'backup'

# Fonction pour créer une sauvegarde de la base de données
def create_backup():
    try:
        print(f'Création de la sauvegarde à {datetime.now()}')

        if not os.path.exists(backup_dir):
            print(f'Le répertoire de sauvegarde n\'existe pas. Création de {backup_dir}')
            os.makedirs(backup_dir)

        # Générer le nom de fichier de la sauvegarde avec la date et l'heure
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'users_{now}.db'
        backup_path = os.path.join(backup_dir, backup_filename)

        # Copier le fichier de la base de données
        shutil.copy2(db_path, backup_path)
        print(f'Sauvegarde créée : {backup_path}')

        # Nettoyer les anciennes sauvegardes si plus de 10 présentes
        backups = sorted(os.listdir(backup_dir), key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)))
        if len(backups) > 10:
            for old_backup in backups[:-10]:
                os.remove(os.path.join(backup_dir, old_backup))
                print(f'Sauvegarde supprimée : {old_backup}')
    except Exception as e:
        print(f'Erreur lors de la création de la sauvegarde : {e}')

# Planifier la sauvegarde toutes les 15 minutes
schedule.every(0.5).minutes.do(create_backup)

# Exécuter le planificateur
print("Démarrage du planificateur de sauvegarde...")

# Créer une première sauvegarde immédiatement
create_backup()

while True:
    schedule.run_pending()
    time.sleep(1)
