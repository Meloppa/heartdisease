from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# -------------------------------
#       DIAGNOSIS ENGINE
# -------------------------------
def diagnose(
    age_group, gender, chest_pain, short_breath, fatigue,
    dizziness, cold_sweat, smoker, diabetes, blood_pressure,
    family_history, inactive
):
    # =========================================================
    # HIGH RISK CATEGORY (Rules 1 - 40)
    # Focus: Severe symptoms, Elderly comorbidities, & Silent MI
    # =========================================================
    
    # --- Group A: Classic Severe Presentations ---
    if chest_pain == "Severe" and short_breath == "Yes" and blood_pressure == "High": return "High Risk" # R1
    if chest_pain == "Severe" and cold_sweat == "Yes" and dizziness == "Yes": return "High Risk" # R2
    if chest_pain == "Severe" and age_group == "Elderly": return "High Risk" # R3
    if chest_pain == "Severe" and diabetes == "Yes" and smoker == "Smoker": return "High Risk" # R4
    if chest_pain == "Moderate" and age_group == "Elderly" and diabetes == "Yes": return "High Risk" # R5
    if chest_pain == "Moderate" and short_breath == "Yes" and smoker == "Smoker" and blood_pressure == "High": return "High Risk" # R6

    # --- Group B: Comorbidity Stacks ("The Deadly Quartet") ---
    if diabetes == "Yes" and blood_pressure == "High" and smoker == "Smoker" and family_history == "Yes": return "High Risk" # R7
    if age_group == "Elderly" and diabetes == "Yes" and blood_pressure == "High": return "High Risk" # R8
    if smoker == "Smoker" and inactive == "Physically Inactive" and blood_pressure == "High" and age_group != "Young Adult": return "High Risk" # R9
    if family_history == "Yes" and diabetes == "Yes" and inactive == "Physically Inactive" and age_group == "Elderly": return "High Risk" # R10

    # --- Group C: Atypical & Silent Presentations (Complex Logic) ---
    # Women often present with fatigue/dizziness rather than chest pain
    if gender == "Female" and fatigue == "Yes" and dizziness == "Yes" and cold_sweat == "Yes" and age_group != "Young Adult": return "High Risk" # R11
    # Diabetics can have "Silent" heart attacks (no pain, just breathlessness)
    if diabetes == "Yes" and chest_pain == "None" and short_breath == "Yes" and cold_sweat == "Yes": return "High Risk" # R12
    if age_group == "Elderly" and fatigue == "Yes" and dizziness == "Yes" and blood_pressure == "High": return "High Risk" # R13
    
    # --- Group D: Additional High Risk Iterations (R14 - R40) ---
    if chest_pain == "Severe" and inactive == "Physically Inactive" and family_history == "Yes": return "High Risk"
    if age_group == "Middle-Aged Adult" and chest_pain == "Severe" and smoker == "Smoker": return "High Risk"
    if blood_pressure == "High" and short_breath == "Yes" and dizziness == "Yes": return "High Risk"
    if chest_pain == "Moderate" and age_group == "Elderly" and cold_sweat == "Yes": return "High Risk"
    if gender == "Male" and age_group == "Middle-Aged Adult" and chest_pain == "Severe" and smoker == "Smoker": return "High Risk"
    if diabetes == "Yes" and smoker == "Smoker" and blood_pressure == "High": return "High Risk"
    if age_group == "Elderly" and short_breath == "Yes" and family_history == "Yes": return "High Risk"
    if chest_pain == "Moderate" and diabetes == "Yes" and inactive == "Physically Inactive": return "High Risk"
    if cold_sweat == "Yes" and short_breath == "Yes" and family_history == "Yes": return "High Risk"
    if age_group == "Elderly" and chest_pain == "Moderate" and blood_pressure == "High": return "High Risk"
    if smoker == "Smoker" and blood_pressure == "High" and dizziness == "Yes": return "High Risk"
    if inactive == "Physically Inactive" and diabetes == "Yes" and age_group == "Elderly": return "High Risk"
    if chest_pain == "Severe" and fatigue == "Yes" and blood_pressure != "Normal": return "High Risk"
    if gender == "Female" and age_group == "Elderly" and chest_pain == "Moderate": return "High Risk"
    if blood_pressure == "High" and age_group == "Elderly" and family_history == "Yes": return "High Risk"
    if smoker == "Smoker" and diabetes == "Yes" and age_group == "Middle-Aged Adult": return "High Risk"
    if chest_pain == "Severe" and gender == "Male" and smoker == "Smoker": return "High Risk"
    if short_breath == "Yes" and fatigue == "Yes" and blood_pressure == "High": return "High Risk"
    if age_group == "Elderly" and cold_sweat == "Yes" and diabetes == "Yes": return "High Risk"
    if chest_pain == "Moderate" and dizziness == "Yes" and blood_pressure == "High": return "High Risk"
    if family_history == "Yes" and smoker == "Smoker" and age_group == "Elderly": return "High Risk"
    if chest_pain == "Severe" and age_group == "Elderly" and dizziness == "Yes": return "High Risk"
    if gender == "Female" and chest_pain == "Severe" and diabetes == "Yes": return "High Risk"
    if smoker == "Smoker" and short_breath == "Yes" and chest_pain == "Moderate": return "High Risk"
    if diabetes == "Yes" and family_history == "Yes" and chest_pain == "Severe": return "High Risk"
    if blood_pressure == "High" and inactive == "Physically Inactive" and chest_pain == "Moderate": return "High Risk"
    if age_group == "Middle-Aged Adult" and diabetes == "Yes" and short_breath == "Yes": return "High Risk"

    # =========================================================
    # MODERATE RISK CATEGORY (Rules 41 - 75)
    # Focus: Middle-aged lifestyle risks & Young Adult symptoms
    # =========================================================
    
    if age_group == "Middle-Aged Adult" and chest_pain in ["Mild","Moderate"] and short_breath == "Yes": return "Moderate Risk" # R41
    if smoker == "Smoker" and chest_pain in ["Mild","Moderate"]: return "Moderate Risk" # R42
    if fatigue == "Yes" and cold_sweat == "Yes" and chest_pain == "Moderate": return "Moderate Risk" # R43
    if blood_pressure == "Elevated" and family_history == "Yes": return "Moderate Risk" # R44
    if inactive == "Physically Inactive" and chest_pain == "Moderate" and short_breath == "No": return "Moderate Risk" # R45
    
    # --- Group E: Lifestyle & Age Interactions ---
    if age_group == "Middle-Aged Adult" and smoker == "Smoker" and blood_pressure == "Elevated": return "Moderate Risk" # R46
    if age_group == "Young Adult" and chest_pain == "Moderate" and diabetes == "No": return "Moderate Risk" # R47
    if gender == "Female" and fatigue == "Yes" and blood_pressure == "Elevated": return "Moderate Risk" # R48
    if chest_pain == "Mild" and short_breath == "Yes" and age_group != "Young Adult": return "Moderate Risk" # R49
    if smoker == "Smoker" and age_group == "Young Adult" and chest_pain != "None": return "Moderate Risk" # R50
    
    # --- Iterative Moderate Rules (R51 - R75) ---
    if blood_pressure == "Elevated" and diabetes == "Yes": return "Moderate Risk"
    if family_history == "Yes" and chest_pain == "Mild": return "Moderate Risk"
    if age_group == "Elderly" and chest_pain == "None" and inactive == "Physically Inactive": return "Moderate Risk"
    if dizziness == "Yes" and fatigue == "Yes" and age_group == "Middle-Aged Adult": return "Moderate Risk"
    if gender == "Male" and age_group == "Young Adult" and smoker == "Smoker": return "Moderate Risk"
    if blood_pressure == "Elevated" and family_history == "Yes": return "Moderate Risk"
    if chest_pain == "Moderate" and age_group == "Young Adult" and inactive == "Active": return "Moderate Risk"
    if diabetes == "Yes" and smoker == "Non-Smoker" and age_group == "Middle-Aged Adult": return "Moderate Risk"
    if age_group == "Elderly" and fatigue == "Yes" and blood_pressure == "Normal": return "Moderate Risk"
    if cold_sweat == "Yes" and chest_pain == "Mild": return "Moderate Risk"
    if short_breath == "Yes" and age_group == "Young Adult" and family_history == "Yes": return "Moderate Risk"
    if blood_pressure == "High" and age_group == "Young Adult" and chest_pain == "None": return "Moderate Risk"
    if chest_pain == "Mild" and diabetes == "Yes": return "Moderate Risk"
    if inactive == "Physically Inactive" and age_group == "Middle-Aged Adult" and blood_pressure == "Elevated": return "Moderate Risk"
    if smoker == "Smoker" and fatigue == "Yes" and age_group != "Elderly": return "Moderate Risk"
    if gender == "Female" and chest_pain == "Moderate" and age_group == "Young Adult": return "Moderate Risk"
    if family_history == "Yes" and diabetes == "Yes" and age_group == "Young Adult": return "Moderate Risk"
    if chest_pain == "Mild" and dizziness == "Yes": return "Moderate Risk"
    if age_group == "Middle-Aged Adult" and inactive == "Physically Inactive" and family_history == "No": return "Moderate Risk"
    if blood_pressure == "Elevated" and smoker == "Smoker": return "Moderate Risk"
    if fatigue == "Yes" and age_group == "Elderly" and chest_pain == "None": return "Moderate Risk"
    if short_breath == "Yes" and blood_pressure == "Normal" and age_group == "Middle-Aged Adult": return "Moderate Risk"
    if chest_pain == "Moderate" and smoker == "Non-Smoker" and diabetes == "No": return "Moderate Risk"
    if dizziness == "Yes" and family_history == "Yes": return "Moderate Risk"
    if age_group == "Young Adult" and diabetes == "Yes": return "Moderate Risk"

    # =========================================================
    # LOW RISK CATEGORY (Rules 76 - 105+)
    # Focus: Young, Healthy Habits, No Symptoms
    # =========================================================
    
    # --- Group F: Healthy Baselines ---
    if age_group == "Young Adult" and chest_pain == "None" and short_breath == "No" and fatigue == "No": return "Low Risk" # R76
    if smoker == "Non-Smoker" and blood_pressure == "Normal" and diabetes == "No": return "Low Risk" # R77
    if inactive == "Active" and chest_pain in ["None","Mild"] and cold_sweat == "No": return "Low Risk" # R78
    if family_history == "No" and dizziness == "No" and short_breath == "No": return "Low Risk" # R79
    if age_group == "Young Adult" and family_history == "No" and inactive == "Active": return "Low Risk" # R80
    
    # --- Iterative Low Risk Rules (R81 - R105+) ---
    if gender == "Male" and age_group == "Young Adult" and blood_pressure == "Normal" and smoker == "Non-Smoker": return "Low Risk"
    if age_group == "Middle-Aged Adult" and inactive == "Active" and blood_pressure == "Normal" and chest_pain == "None": return "Low Risk"
    if diabetes == "No" and family_history == "No" and smoker == "Non-Smoker" and age_group != "Elderly": return "Low Risk"
    if chest_pain == "None" and short_breath == "No" and dizziness == "No" and fatigue == "No": return "Low Risk"
    if age_group == "Young Adult" and blood_pressure in ["Normal", "Elevated"] and smoker == "Non-Smoker": return "Low Risk"
    if inactive == "Active" and age_group == "Young Adult" and chest_pain == "Mild": return "Low Risk"
    if blood_pressure == "Normal" and family_history == "No" and age_group == "Middle-Aged Adult": return "Low Risk"
    if gender == "Female" and age_group == "Young Adult" and smoker == "Non-Smoker" and inactive == "Active": return "Low Risk"
    if fatigue == "No" and cold_sweat == "No" and diabetes == "No" and age_group == "Young Adult": return "Low Risk"
    if blood_pressure == "Normal" and smoker == "Non-Smoker" and inactive == "Active" and family_history == "No": return "Low Risk"
    if age_group == "Young Adult" and dizziness == "No" and short_breath == "No" and cold_sweat == "No": return "Low Risk"
    if age_group == "Middle-Aged Adult" and smoker == "Non-Smoker" and diabetes == "No" and family_history == "No" and chest_pain == "None": return "Low Risk"
    if chest_pain == "None" and blood_pressure == "Normal" and inactive == "Active" and gender == "Female": return "Low Risk"
    if age_group == "Young Adult" and fatigue == "No" and family_history == "No": return "Low Risk"
    if blood_pressure == "Normal" and short_breath == "No" and diabetes == "No" and smoker == "Non-Smoker": return "Low Risk"
    if inactive == "Active" and age_group != "Elderly" and chest_pain == "None" and dizziness == "No": return "Low Risk"
    if gender == "Female" and chest_pain == "None" and family_history == "No" and blood_pressure == "Normal": return "Low Risk"
    if smoker == "Non-Smoker" and diabetes == "No" and inactive == "Active": return "Low Risk"
    if age_group == "Young Adult" and chest_pain == "None" and blood_pressure == "Normal": return "Low Risk"
    if family_history == "No" and age_group == "Young Adult" and short_breath == "No": return "Low Risk"
    if blood_pressure == "Normal" and dizziness == "No" and age_group == "Young Adult": return "Low Risk"
    if chest_pain == "None" and inactive == "Active" and age_group == "Middle-Aged Adult": return "Low Risk"
    if age_group == "Young Adult" and cold_sweat == "No" and diabetes == "No": return "Low Risk"
    if smoker == "Non-Smoker" and family_history == "No" and blood_pressure == "Normal": return "Low Risk"
    if age_group == "Young Adult" and gender == "Male" and chest_pain == "None" and inactive == "Active": return "Low Risk"

    # Default fallback
    return "Moderate Risk"

# -------------------------------
#       ROUTES
# -------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/page2", response_class=HTMLResponse)
async def page2(
    request: Request,
    age_group: str = Form(...),
    gender: str = Form(...),
    chest_pain: str = Form(...),
    short_breath: str = Form(...),
    fatigue: str = Form(...),
    dizziness: str = Form(...),
    cold_sweat: str = Form(...),
):
    return templates.TemplateResponse("page2.html", {
        "request": request,
        "age_group": age_group,
        "gender": gender,
        "chest_pain": chest_pain,
        "short_breath": short_breath,
        "fatigue": fatigue,
        "dizziness": dizziness,
        "cold_sweat": cold_sweat
    })

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    age_group: str = Form(...),
    gender: str = Form(...),
    chest_pain: str = Form(...),
    short_breath: str = Form(...),
    fatigue: str = Form(...),
    dizziness: str = Form(...),
    cold_sweat: str = Form(...),
    smoker: str = Form(...),
    diabetes: str = Form(...),
    blood_pressure: str = Form(...),
    family_history: str = Form(...),
    inactive: str = Form(...),
):
    diagnosis_result = diagnose(
        age_group, gender, chest_pain, short_breath, fatigue,
        dizziness, cold_sweat, smoker, diabetes, blood_pressure,
        family_history, inactive
    )

    rec = {
        "High Risk": "Consult a cardiologist immediately. Follow a strict heart-healthy lifestyle.",
        "Moderate Risk": "Schedule a medical checkup and improve lifestyle habits.",
        "Low Risk": "Maintain healthy habits and regular checkups."
    }
    advice = rec.get(diagnosis_result)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "diagnosis": diagnosis_result,
        "recommendation": advice,
        "inputs": {
            "Age Group": age_group,
            "Gender": gender,
            "Chest Pain": chest_pain,
            "Shortness of Breath": short_breath,
            "Fatigue": fatigue,
            "Dizziness/Nausea": dizziness,
            "Cold Sweating": cold_sweat,
            "Smoking": smoker,
            "Diabetes": diabetes,
            "Blood Pressure": blood_pressure,
            "Family History": family_history,
            "Physical Activity": inactive
        }
    })

#uvicorn app:app --reload