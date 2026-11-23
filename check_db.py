import sqlite3
conn = sqlite3.connect('pupqc_plant_db.sqlite')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:", [r[0] for r in c.fetchall()])
c.execute("SELECT id, common_name, image_url FROM plants ORDER BY id")
print("\nPlants:")
for r in c.fetchall():
    print(r)
c.execute("SELECT * FROM plant_images ORDER BY plant_id")
print("\nPlant Images:")
for r in c.fetchall():
    print(r)
conn.close()
