import sqlite3
from pathlib import Path

db_path = Path(r'C:\Users\Romalyn Amante\Desktop\RESEARCH\pupqc_plant_db.sqlite')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

plants = [
    {
        'common_name': 'Bignay',
        'scientific_name': 'Antidesma bunius',
        'family': 'Phyllanthaceae',
        'category_id': 1,
        'local_name': 'Bignay / Bugnay',
        'conservation_status': 'Least Concern',
        'location_in_campus': 'Campus Buildings and Grounds',
        'description': (
            'A versatile plant native to Southeast Asia including the Philippines, Northern Australia, and parts of South Asia, '
            'belonging to the family Phyllanthaceae. It can grow as a variable shrub or a small-to-tall erect tree, occasionally '
            'reaching heights of 15 to 30 meters with a dense, shady, dark-green canopy. Leaves are alternate, simple, large, '
            'oval-to-oblong, leathery, and dark green, growing up to 20 cm long and 7 cm wide. The tree is dioecious, meaning '
            'male and female flowers are borne on separate trees. Flowers have a distinct somewhat pungent or heavy scent, with '
            'female flowers growing on long racemes that develop into prominent fruit strands. Fruits are small, spherical-to-oval '
            'berries roughly 6 to 8 mm wide, growing in dense dangling clusters. They ripen unevenly, starting bright green when '
            'immature and tasting sharply sour, then turning vibrant red, and finally maturing into a deep dark purple or black. '
            'The thin skin encloses pulp with a single seed. The fruits are exceptionally rich in total phenolic compounds, '
            'flavonoids, and anthocyanins, providing powerful antioxidant activity. Due to its attractive dense dark-green foliage '
            'and striking multi-colored fruit clusters showing green, red, and black simultaneously, it is frequently planted as '
            'an ornamental landscape tree in backyard agroforestry systems.'
        ),
        'medicinal_uses': (
            'Bignay fruits especially the flesh and seeds of fully ripe berries are exceptionally rich in total phenolic compounds, '
            'flavonoids, and anthocyanins that provide powerful antioxidant activity scavenging free radicals and helping mitigate '
            'oxidative stress linked to chronic illnesses. Extracts and fruit wine made from bignay have been traditionally used to '
            'help regulate blood pressure and support heart health with cardioprotective effects. Infusions or decoctions of the '
            'leaves are traditionally used to treat stomach complaints, flatulence, and intestinal colic, while modern pharmacological '
            'studies note its potential anti-diabetic properties including alpha-glucosidase inhibition. Leaf and bark extracts have '
            'historically been applied to treat localized infections and snakebites. In the Philippines, the fruit is heavily processed '
            'into jams, jellies, teas, and local bignay wine consumed both as delicacies and functional health foods.'
        ),
        'ecological_role': (
            'Because bignay produces abundant fruit crops that ripen successively over several weeks, it serves as an important food '
            'source for frugivorous birds, bats, and small mammals on campus, which in turn aid in natural seed dispersal and '
            'biodiversity support. As a hardy native tree it adapts well to secondary forests and contributes to forest regeneration, '
            'canopy coverage, and soil stabilization. Due to its attractive dense dark-green foliage and striking multi-colored fruit '
            'clusters, it functions as an ornamental and biodiversity hotspot within the campus landscape. The tree is well-suited for '
            'agroforestry and campus greening programs as a productive, low-maintenance native fruit tree.'
        ),
        'image_url': '/static/images/plants/default_plant.jpg'
    },
    {
        'common_name': 'Binayuyu',
        'scientific_name': 'Antidesma ghaesembilla',
        'family': 'Phyllanthaceae',
        'category_id': 1,
        'local_name': 'Binayuyu / Binayuyo / Arosep',
        'conservation_status': 'Least Concern',
        'location_in_campus': 'Campus Buildings and Grounds',
        'description': (
            'A fascinating indigenous plant species belonging to the family Phyllanthaceae, widely known by local vernacular names '
            'such as Binayuyu or Binayuyo in Tagalog and Arosep in Ilokano, and sometimes called Black Currant Tree or Wild Currant '
            'internationally. It is a small to medium-sized deciduous tree or shrub, typically growing 3 to 12 meters tall with a '
            'trunk diameter of about 10 to 20 cm. Leaves are alternate, simple, shortly petioled, and broadly elliptic to oblong-ovate '
            'with rounded or obtuse tips. The plant produces small yellowish-green flowers arranged in axillary or terminal spikes or '
            'racemes. It is typically dioecious with separate male and female trees. Fruits are small round-to-ovoid drupes growing '
            'in clusters resembling miniature grapes, changing color as they ripen from green to red and finally maturing into dark '
            'purple or black. The fruits bear a striking resemblance to blackcurrants in both appearance and taste. It is closely '
            'related to Antidesma bunius (Bignay) and both serve similar ecological and cultural roles in Philippine forests. '
            'The plant is regionally distributed across tropical Asia from India and Southern China through Southeast Asia to '
            'Northern Australia.'
        ),
        'medicinal_uses': (
            'Various parts of the plant, particularly the leaves and bark, are utilized in Philippine traditional herbal medicine and '
            'across other parts of tropical Asia. Decoctions or poultices made from the leaves are traditionally applied or consumed '
            'to help reduce fevers and headaches. Bark and leaf extracts have a long history of folk use in treating rheumatic pains '
            'and respiratory discomforts such as coughs. The ripe fruits are edible and rich in micronutrients and phenolic compounds, '
            'consumed fresh as a wild-harvested snack or processed into jams and preserves. Young shoots are also sometimes consumed '
            'locally as vegetables or flavorings. Modern scientific studies have isolated several bioactive secondary metabolites from '
            'the plant, including triterpenes such as lupeol and beta-friedelinol, sterols like beta-sitosterol, squalene, and '
            'polyprenols from its leaves, confirming its value as a source of natural therapeutics and functional foods.'
        ),
        'ecological_role': (
            'Antidesma ghaesembilla is commonly found in open thickets, secondary forests, mountainous areas, and low-altitude forest '
            'edges in the Philippines. As an indigenous fruit tree, its sweet-to-tart ripe fruits serve as a valuable food source for '
            'frugivorous birds and various insects on campus, supporting local biodiversity through natural seed dispersal. Being a '
            'resilient component of secondary growth and open woodland systems, it assists in soil stabilization and acts as part of '
            'the natural pioneer vegetation that helps restore disturbed landscapes. Its adaptability to a wide range of soil types '
            'makes it a robust and low-maintenance addition to the campus green space. The plant represents an important element of '
            'Philippine indigenous forest biodiversity and contributes to campus ecological diversity.'
        ),
        'image_url': '/static/images/plants/default_plant.jpg'
    },
    {
        'common_name': 'Kamansi',
        'scientific_name': 'Artocarpus camansi',
        'family': 'Moraceae',
        'category_id': 1,
        'local_name': 'Kamansi / Kuluot',
        'conservation_status': 'Least Concern',
        'location_in_campus': 'Campus Buildings and Grounds',
        'description': (
            'A notable tropical tree belonging to the mulberry and fig family Moraceae, commonly known as Breadnut, and locally '
            'referred to as Kamansi or Kuluot in the Philippines. Widely recognized as the wild ancestral precursor to the seedless '
            'breadfruit Artocarpus altilis, it is an essential component of traditional agroforestry systems in the Philippines and '
            'greater Southeast Asia. It is a medium to large evergreen tree typically growing between 10 to 15 meters tall, with some '
            'specimens reaching up to 35 meters, featuring a straight buttressed trunk with bole diameter that can exceed 100 cm. '
            'Leaves are very large, about 40 to 60 cm long and 25 to 45 cm wide, dark green, leathery, and deeply pinnately lobed. '
            'The plant is monoecious with separate male and female flowers on the same tree. Male flowers form large club-shaped or '
            'cylindrical inflorescences up to 35 cm long. The fruit is heavily seeded, roughly globular to oval measuring about 16 to '
            '20 cm long and 8 to 15 cm wide, weighing around 800 grams to over a kilogram. The outer skin is yellow-green and covered '
            'in soft fleshy spiny tips. Inside are numerous large light-brown seeds, often 30 to 50 or more per fruit, which are rich '
            'in starch and high-quality vegetable proteins. It is native to New Guinea, the Moluccas, and parts of Oceania and '
            'Southeast Asia.'
        ),
        'medicinal_uses': (
            'Kamansi is best known in Filipino cuisine where the tender immature fruits are sliced and cooked in coconut milk as '
            'ginataan, and the starchy seeds are boiled in soups, but it also holds a prominent place in traditional herbal medicine. '
            'Decoctions made from the leaves are widely consumed in traditional folk medicine to help manage blood sugar levels in '
            'individuals with diabetes mellitus, with antidiabetic properties well-documented in ethnobotanical literature. Modern '
            'phytochemical and pharmacological studies validate many traditional claims, as extracts from the leaves, bark, and seeds '
            'are rich in secondary metabolites particularly phenolics, flavonoids, and triterpenoids. Laboratory evaluations show '
            'these compounds possess strong antioxidant properties and significant antibacterial activity against pathogens like '
            'Staphylococcus aureus and Escherichia coli. Plant sap and crushed bark or leaves have historically been utilized topically '
            'in various indigenous practices to soothe skin infections, boils, and rheumatic conditions.'
        ),
        'ecological_role': (
            'Artocarpus camansi plays a vital ecological role in the PUPQC campus environment. The massive canopy provides '
            'exceptionally dense shade, significantly cooling the microclimate around campus structures and walkways. Its fleshy '
            'fruits and nutrient-dense seeds play an essential ecological role in seed dispersal, as bats, birds, and forest rodents '
            'consume the ripe fruits, naturally propagating biodiversity across the campus. The tree is frequently integrated into '
            'agroforestry plots and riparian zones where its extensive root systems and buttressed trunks help stabilize soil and '
            'reduce erosion during heavy tropical downpours and typhoons. It is frequently one of the pioneer species colonizing '
            'disturbed areas, making it resilient and self-sustaining in the campus landscape. As the ancestral wild relative of the '
            'economically important breadfruit, it also holds significant genetic conservation value for Philippine food security '
            'and agricultural heritage.'
        ),
        'image_url': '/static/images/plants/default_plant.jpg'
    }
]

inserted = []
for p in plants:
    cursor.execute('''
        INSERT INTO plants (common_name, scientific_name, family, category_id, local_name,
        conservation_status, location_in_campus, description, medicinal_uses, ecological_role, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (p['common_name'], p['scientific_name'], p['family'], p['category_id'], p['local_name'],
          p['conservation_status'], p['location_in_campus'], p['description'],
          p['medicinal_uses'], p['ecological_role'], p['image_url']))
    new_id = cursor.lastrowid
    inserted.append((new_id, p['common_name'], p['scientific_name']))
    print(f"Inserted: {p['common_name']} (ID: {new_id})")

conn.commit()

cursor.execute('SELECT COUNT(*) FROM plants')
total = cursor.fetchone()[0]
print(f'\nTotal plants in DB: {total}')
print('\nAll inserted:')
for i in inserted:
    print(f'  ID#{i[0]}: {i[1]} - {i[2]}')

conn.close()
print('Done!')
