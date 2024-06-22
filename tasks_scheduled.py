import shutil
import os
import sqlite3
import random
from datetime import datetime
import schedule
import time

# Database and direction of backups
db_path = 'user/users.db'
backup_dir = 'backup'


# Create backup
def create_backup():
    try:
        print(f'Creating the backup at {datetime.now()}')

        if not os.path.exists(backup_dir):
            print(f'The save directory does not exist. Creation of {backup_dir}')
            os.makedirs(backup_dir)

        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'users_{now}.db'
        backup_path = os.path.join(backup_dir, backup_filename)
        shutil.copy2(db_path, backup_path)
        print(f'Sauvegarde créée : {backup_path}')

        # Clean old backups if more than 10 present
        backups = sorted(os.listdir(backup_dir), key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)))
        if len(backups) > 10:
            for old_backup in backups[:-10]:
                os.remove(os.path.join(backup_dir, old_backup))
                print(f'Save deleted: {old_backup}')

    except Exception as e:
        print(f'Error creating backup: {e}')


# Daily reward
def daily_reward():
    try:
        print(f'Adding money to all users {datetime.now()}')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        additional_money = random.randint(75, 125)
        c.execute('UPDATE users SET money = money + ?', (additional_money,))
        conn.commit()
        print(f'Add {additional_money}$ to all users')
        conn.close()
    except Exception as e:
        print(f'Error adding money: {e}')


# Backup every 15min
schedule.every(15).minutes.do(create_backup)
# Daily reward at 2:00 A.M
schedule.every().day.at("02:00").do(daily_reward)

# Run scheduler
print("Starting the Backup and Add Money Scheduler...")
create_backup()
daily_reward()

while True:
    schedule.run_pending()
    time.sleep(1)
