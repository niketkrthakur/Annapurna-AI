from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import random, os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint, google
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")
import pandas as pd
# Load dataset (once, globally)
# crop_df = pd.read_csv("data/crop_dataset.csv") 
 # update path as needed

# ⚠️ ONLY FOR LOCAL DEVELOPMENT
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# ======================================
# 🔧 App Config
# ======================================
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# ======================================
# 👤 User Model
# ======================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    phone = db.Column(db.String(20), unique=True)
    plot_size = db.Column(db.String(50))
    role = db.Column(db.String(20))  # farmer/admin
    email = db.Column(db.String(120), unique=True)

# ======================================
# 🔑 Google OAuth
# ======================================
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ],
    redirect_to="google_login"
)
app.register_blueprint(google_bp, url_prefix="/login")



# ======================================
# 🌾 Load AI Disease Model
# ======================================
MODEL_PATH = "models/plant_disease_model.h5"
model, CLASS_LABELS = None, []

if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
    CLASS_LABELS = [
        "Apple Scab", "Apple Black Rot", "Apple Cedar Rust", "Apple Healthy",
        "Corn Cercospora", "Corn Common Rust", "Corn Northern Leaf Blight", "Corn Healthy",
        "Grape Black Rot", "Grape Esca", "Grape Leaf Blight", "Grape Healthy",
        "Potato Early Blight", "Potato Late Blight", "Potato Healthy",
        "Tomato Bacterial Spot", "Tomato Early Blight", "Tomato Late Blight",
        "Tomato Leaf Mold", "Tomato Septoria Leaf Spot", "Tomato Spider Mites",
        "Tomato Target Spot", "Tomato Mosaic Virus", "Tomato Healthy"
    ]
    print("✅ Plant disease model loaded!")
else:
    print("⚠️ No model found, using dummy predictions.")

# ======================================
# 🌐 Routes
# ======================================
@app.route("/") 
def home():
    return render_template("index.html")

@app.route("/index") 
def index_page(): 
    return render_template("index.html")

@app.route("/crop")  
def crop_page():
    return render_template("crop.html")

@app.route("/disease")
def disease_page():
    return render_template("disease.html")

@app.route("/smart")
def smart_page():
    return render_template("smart.html")

@app.route("/str")
def str_page():
    return render_template("str.html")

# Tomato
@app.route("/tom")
def tom_page():
    return render_template("tom.html")

# Tea
@app.route("/tea")
def tea_page():
    return render_template("tea.html")

# Sugarcane
@app.route("/sugercane")
def sugercane_page():
    return render_template("sugercane.html")

# Spinach
@app.route("/spinach")
def spinach_page():
    return render_template("spinach.html")

# Soyabean
@app.route("/soyabean")
def soyabean_page():
    return render_template("soyabean.html")

# Sesam
@app.route("/sesam")
def sesam_page():
    return render_template("sesam.html")

# Sapota
@app.route("/sapota")
def sapota_page():
    return render_template("sapota.html")

# Potato (short as pot)
@app.route("/pot")
def pot_page():
    return render_template("pot.html")

# Orange
@app.route("/orange")
def orange_page():
    return render_template("orange.html")

# Mango
@app.route("/mango")
def mango_page():
    return render_template("mango.html")

# Cauliflower (?) – cauki
@app.route("/cauli")
def cauli_page():
    return render_template("cauli.html")

# Carrot
@app.route("/carrot")
def carrot_page():
    return render_template("carrot.html")

# Apple
@app.route("/apple")
def apple_page():
    return render_template("apple.html")

# watermelon
@app.route("/watermelon")
def watermelon_page():
    return render_template("watermelon.html")

# # modern
# @app.route("/modern")
# def modern_page():
#     return render_template("modern.html")

# # micro_irrigation
# @app.route("/micro_irrigation")
# def micro_irrigation_page():
#     return render_template("micro_irrigation.html")

# Mulching
@app.route("/mulching")
def mulching_page():
    return render_template("mulching.html")

# Vermicomposting
@app.route("/vermi")
def vermi_page():
    return render_template("vermi.html")

# Rain Water Harvesting
@app.route("/rain_water")
def rain_water_page():
    return render_template("rain_water.html")


# modern
@app.route("/modern")
def modern_page():
    return render_template("modern.html")

# Micro Irrigation
@app.route("/micro_irrigation")
def micro_irrigation_page():
    return render_template("micro_irrigation.html")

# Agroforestry
@app.route("/agroforestry")
def agroforestry_page(): 
    return render_template("agroforestry.html")



# ======================================
# 👤 Auth Routes  
# ======================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            name=request.form['name'],
            location=request.form['location'],
            phone=request.form['phone'],
            plot_size=request.form['plot_size'],
            role=request.form['role'],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form['phone']
        user = User.query.filter_by(phone=phone).first()
        if user:
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/google_login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    
    resp = google.get("/oauth2/v2/userinfo")
    info = resp.json()
    
    email = info.get("email")
    name = info.get("name", "No Name")
    
    if not email:
        return "❌ Google login failed: email not available", 400

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email, role="farmer")
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    session["role"] = user.role
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    role = session["role"]
    if role == "farmer":
        return render_template("farmer_dashboard.html")
    elif role == "admin":
        return render_template("admin_dashboard.html")
    return "Unknown role"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ======================================
# 🌱 Crop Recommendation
# ======================================
soil_crop_map = {
    "sandy": {"yes": ["Groundnut", "Watermelon", "Sugarcane"], "no": ["Bajra", "Millets"]},
    "loamy": {"yes": ["Wheat", "Sugarcane", "Tomato"], "no": ["Pulses", "Maize"]},
    "clay": {"yes": ["Paddy", "Mustard", "Potato"], "no": ["Rice", "Jute"]}
}

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    soil, irrigation = data.get("soil"), data.get("irrigation")
    crops = soil_crop_map.get(soil, {}).get(irrigation, ["Maize", "Wheat", "Rice"])
    prediction = random.choice(crops)
    return jsonify({"recommendation": prediction})

# ======================================
# ❓ FAQ API
# ======================================
@app.route("/faq")
def faq():
    return jsonify([
        {"q": "How does Annapurna AI help farmers?", "a": "It provides crop, weather, and market insights."},
        {"q": "Do I need to know NPK values?", "a": "No, just soil type & irrigation are enough."}
    ])

# ======================================
# 🌾 Disease Detection
# ======================================
@app.route("/detect_disease", methods=["POST"])
def detect_disease():
    if "crop_image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["crop_image"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    if model is None:
        return jsonify({"disease": "Dummy Prediction", "confidence": "N/A", "image_url": filepath})

    img = image.load_img(filepath, target_size=(224, 224))  
    img_array = np.expand_dims(image.img_to_array(img), axis=0) / 255.0
    predictions = model.predict(img_array)
    predicted_class = CLASS_LABELS[np.argmax(predictions[0])]
    confidence = round(100 * np.max(predictions[0]), 2)

    return jsonify({"disease": predicted_class, "confidence": f"{confidence}%", "image_url": filepath})

# ======================================
# 🚀 Run App
# ======================================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
