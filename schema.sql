-- ==========================================================
-- PUPQC Campus Plant Database - MySQL Schema & Seed Data
-- Database Name: pupqc_plant_db
-- ==========================================================

CREATE DATABASE IF NOT EXISTS `pupqc_plant_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `pupqc_plant_db`;

-- ----------------------------------------------------------
-- Table structure for `categories`
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `plants`;
DROP TABLE IF EXISTS `categories`;

CREATE TABLE `categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL UNIQUE,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------
-- Table structure for `plants`
-- ----------------------------------------------------------
CREATE TABLE `plants` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `common_name` VARCHAR(100) NOT NULL,
    `scientific_name` VARCHAR(150) NOT NULL,
    `family` VARCHAR(100) NOT NULL,
    `category_id` INT,
    `local_name` VARCHAR(100),
    `conservation_status` VARCHAR(50) DEFAULT 'Least Concern',
    `location_in_campus` VARCHAR(150) NOT NULL,
    `description` TEXT,
    `medicinal_uses` TEXT,
    `ecological_role` TEXT,
    `image_url` VARCHAR(255) DEFAULT '/static/images/plants/default_plant.jpg',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`category_id`) REFERENCES `categories`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------
-- Seed Data for `categories`
-- ----------------------------------------------------------
INSERT INTO `categories` (`id`, `name`, `description`) VALUES
(1, 'Native & Endemic Trees', 'Trees native or indigenous to the Philippines'),
(2, 'Medicinal Plants', 'Plants known for therapeutic, herbal, and traditional health uses'),
(3, 'Ornamental Plants', 'Decorative plants grown for aesthetic appeal around campus buildings'),
(4, 'Shade & Canopy Trees', 'Large spread trees providing canopy shade in quadrangle and walkways');

-- ----------------------------------------------------------
-- Seed Data for `plants`
-- ----------------------------------------------------------
INSERT INTO `plants` (`common_name`, `scientific_name`, `family`, `category_id`, `local_name`, `conservation_status`, `location_in_campus`, `description`, `medicinal_uses`, `ecological_role`, `image_url`) VALUES
('Narra', 'Pterocarpus indicus', 'Fabaceae', 1, 'Narra', 'Vulnerable', 'Main Quadrangle & East Lawn', 'The National Tree of the Philippines. A large timber tree producing bright yellow flowers and valuable reddish wood.', 'Bark decoction used traditionally for astringent properties.', 'Provides dense shade, nitrogen fixation in soil, and habitat for local birds.', 'https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?auto=format&fit=crop&w=600&q=80'),

('Banaba', 'Lagerstroemia speciosa', 'Lythraceae', 2, 'Banaba', 'Least Concern', 'PUPQC Front Garden & Entrance Path', 'A deciduous tropical tree known for its striking pink to purple crinkled blossoms and distinctive smooth bark.', 'Leaves are widely boiled into herbal tea for blood sugar control and kidney health.', 'Attracts pollinators like bees and butterflies during bloom season.', 'https://images.unsplash.com/photo-1509100194014-d49809396daa?auto=format&fit=crop&w=600&q=80'),

('Sampaguita', 'Jasminum sambac', 'Oleaceae', 3, 'Sampaguita', 'Least Concern', 'Administration Building Courtyard', 'The National Flower of the Philippines. A sweet-scented evergreen shrub with small star-shaped white flowers.', 'Infusion of flowers used to soothe headaches and eye inflammation.', 'Aromatic attraction for beneficial pollinators and urban floral beauty.', 'https://images.unsplash.com/photo-1596073413225-300dd1d21616?auto=format&fit=crop&w=600&q=80'),

('Acacia / Rain Tree', 'Samanea saman', 'Fabaceae', 4, 'Akasya', 'Least Concern', 'Campus Perimeter & Open Grounds', 'A massive canopy tree with a wide umbrella crown that folds its leaves during rainfall and at night.', 'Bark and seeds contain mild traditional antimicrobial compounds.', 'Crucial canopy shade reducer for ground temperature and atmospheric carbon capture.', 'https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=600&q=80'),

('Katmon', 'Dillenia philippinensis', 'Dilleniaceae', 1, 'Katmon', 'Vulnerable', 'Eco-Park & Botanical Corner', 'An endemic Philippine fruit tree with large white fragrant flowers and edible fleshy green sour fruit.', 'Juice from fresh fruit used for cough relief and natural hair cleanser.', 'Endemic food source for fruit bats and indigenous avian species.', 'https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?auto=format&fit=crop&w=600&q=80'),

('Bougainvillea', 'Bougainvillea spectabilis', 'Nyctaginaceae', 3, 'Bogambilya', 'Least Concern', 'Student Center Fencing & Terraces', 'A thorny ornamental vine/shrub with vibrant magenta, purple, and orange flower-like bracts.', 'Bark and leaves used in folk remedies for cough and fever.', 'Urban greenery aesthetic, soil erosion control on sloped garden margins.', 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=600&q=80'),

('Neem Tree', 'Azadirachta indica', 'Meliaceae', 2, 'Neem', 'Least Concern', 'Library Rear Pathway', 'A fast-growing evergreen tree known for its natural insect-repellent properties and dense foliage.', 'Leaves used for natural antiseptic wash, organic pest repellent, and skin remedies.', 'Natural mosquito repellent and air purifier along campus walkways.', 'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=600&q=80'),

('Snake Plant', 'Sansevieria trifasciata', 'Asparagaceae', 3, 'Espada', 'Least Concern', 'Academic Building Corridors', 'An evergreen perennial plant with vertical sword-like leaves with yellow-green variegated borders.', 'Leaves traditionally crushed for topical poultice on minor skin cuts.', 'Air purifying plant absorbing toxins like benzene and formaldehyde.', 'https://images.unsplash.com/photo-1509423350716-97f9360b4e09?auto=format&fit=crop&w=600&q=80');
