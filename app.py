from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from db_config import get_db, get_mysql_connection

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    """Render main homepage."""
    return render_template("index.html")

@app.route("/admin")
def admin():
    """Render admin management page."""
    return render_template("admin.html")

# ==========================================
# REST API ENDPOINTS
# ==========================================

@app.route("/api/status", methods=["GET"])
def api_status():
    """Return status of database connection mode (MySQL or SQLite fallback)."""
    mysql_conn = get_mysql_connection()
    if mysql_conn:
        mysql_conn.close()
        return jsonify({
            "status": "online",
            "database_engine": "MySQL",
            "message": "Connected to MySQL database (pupqc_plant_db)."
        })
    else:
        return jsonify({
            "status": "online",
            "database_engine": "SQLite (Fallback)",
            "message": "MySQL connection unavailable; running on auto-seeded SQLite database."
        })

@app.route("/api/categories", methods=["GET"])
def get_categories():
    """Fetch all plant categories."""
    db = get_db()
    query = "SELECT * FROM categories ORDER BY id ASC"
    categories = db.execute_query(query)
    return jsonify({"status": "success", "categories": categories})

@app.route("/api/plants", methods=["GET"])
def get_plants():
    """Fetch plants with optional search and category filters."""
    search_query = request.args.get("q", "").strip()
    category_id = request.args.get("category_id", "").strip()
    
    db = get_db()
    sql = """
        SELECT p.*, c.name as category_name 
        FROM plants p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE 1=1
    """
    params = []

    if search_query:
        sql += " AND (p.common_name LIKE %s OR p.scientific_name LIKE %s OR p.local_name LIKE %s OR p.family LIKE %s OR p.location_in_campus LIKE %s)"
        pattern = f"%{search_query}%"
        params.extend([pattern, pattern, pattern, pattern, pattern])

    if category_id and category_id.isdigit():
        sql += " AND p.category_id = %s"
        params.append(int(category_id))

    sql += " ORDER BY p.id DESC"
    
    plants = db.execute_query(sql, tuple(params))
    return jsonify({"status": "success", "count": len(plants), "plants": plants})

@app.route("/api/plants/<int:plant_id>", methods=["GET"])
def get_plant_by_id(plant_id):
    """Fetch details of a specific plant."""
    db = get_db()
    sql = """
        SELECT p.*, c.name as category_name 
        FROM plants p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE p.id = %s
    """
    plants = db.execute_query(sql, (plant_id,))
    if plants:
        return jsonify({"status": "success", "plant": plants[0]})
    return jsonify({"status": "error", "message": "Plant record not found"}), 404

@app.route("/api/plants", methods=["POST"])
def add_plant():
    """Add a new plant to the database."""
    data = request.json or request.form
    
    common_name = data.get("common_name", "").strip()
    scientific_name = data.get("scientific_name", "").strip()
    family = data.get("family", "").strip()
    category_id = data.get("category_id")
    local_name = data.get("local_name", "").strip()
    conservation_status = data.get("conservation_status", "Least Concern").strip()
    location_in_campus = data.get("location_in_campus", "").strip()
    description = data.get("description", "").strip()
    medicinal_uses = data.get("medicinal_uses", "").strip()
    ecological_role = data.get("ecological_role", "").strip()
    image_url = data.get("image_url", "").strip() or "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?auto=format&fit=crop&w=600&q=80"

    if not common_name or not scientific_name or not location_in_campus:
        return jsonify({"status": "error", "message": "Common Name, Scientific Name, and Location in Campus are required."}), 400

    db = get_db()
    sql = """
        INSERT INTO plants 
        (common_name, scientific_name, family, category_id, local_name, conservation_status, location_in_campus, description, medicinal_uses, ecological_role, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (common_name, scientific_name, family, category_id, local_name, conservation_status, location_in_campus, description, medicinal_uses, ecological_role, image_url)
    
    try:
        new_id = db.execute_insert(sql, params)
        return jsonify({"status": "success", "message": "Plant added successfully!", "plant_id": new_id}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/plants/<int:plant_id>", methods=["PUT"])
def update_plant(plant_id):
    """Update an existing plant record."""
    data = request.json or request.form
    
    common_name = data.get("common_name", "").strip()
    scientific_name = data.get("scientific_name", "").strip()
    family = data.get("family", "").strip()
    category_id = data.get("category_id")
    local_name = data.get("local_name", "").strip()
    conservation_status = data.get("conservation_status", "Least Concern").strip()
    location_in_campus = data.get("location_in_campus", "").strip()
    description = data.get("description", "").strip()
    medicinal_uses = data.get("medicinal_uses", "").strip()
    ecological_role = data.get("ecological_role", "").strip()
    image_url = data.get("image_url", "").strip()

    db = get_db()
    sql = """
        UPDATE plants 
        SET common_name = %s, scientific_name = %s, family = %s, category_id = %s, 
            local_name = %s, conservation_status = %s, location_in_campus = %s, 
            description = %s, medicinal_uses = %s, ecological_role = %s, image_url = %s
        WHERE id = %s
    """
    params = (common_name, scientific_name, family, category_id, local_name, conservation_status, location_in_campus, description, medicinal_uses, ecological_role, image_url, plant_id)
    
    try:
        db.execute_update(sql, params)
        return jsonify({"status": "success", "message": "Plant record updated successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/plants/<int:plant_id>", methods=["DELETE"])
def delete_plant(plant_id):
    """Delete a plant record."""
    db = get_db()
    sql = "DELETE FROM plants WHERE id = %s"
    try:
        db.execute_update(sql, (plant_id,))
        return jsonify({"status": "success", "message": "Plant record deleted successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("Starting PUPQC Campus Plant Database Server...")
    print("Access application at: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
