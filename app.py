
"""
MediMate Voice Assistant - Main Application
A medical voice assistant that uses the Heygen Streaming API.
"""
import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
HEYGEN_API_KEY = os.getenv('HEYGEN_API_KEY')
HEYGEN_API_BASE_URL = os.getenv('HEYGEN_API_BASE_URL', 'https://api.heygen.com')
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')
PORT = int(os.getenv('PORT', 5000))

# Available avatars (these should match what Heygen provides)
AVAILABLE_AVATARS = [
    {'id': 'Wayne_20240711', 'name': 'Male Doctor', 'icon': 'fas fa-user-md'},
    {'id': 'Onat_1731911456', 'name': 'Female Doctor', 'icon': 'fas fa-user-nurse'},
    {'id': '1732832799', 'name': 'Cardiologist', 'icon': 'fas fa-heartbeat'},
    {'id': '84a12ccb99774fd29bcb27727a9d38ed', 'name': 'Pediatrician', 'icon': 'fas fa-child'},
    {'id': 'Michael_20240415', 'name': 'Neurologist', 'icon': 'fas fa-brain'},
    {'id': 'Emily_20240320', 'name': 'Pharmacist', 'icon': 'fas fa-pills'}
]

# Medical domain keywords to identify medical queries
MEDICAL_KEYWORDS = [
    # General medical terms
    'health', 'medical', 'doctor', 'hospital', 'symptom', 'pain', 'treatment', 
    'medicine', 'disease', 'diagnosis', 'prescription', 'dose', 'therapy',
    'allergy', 'vaccination', 'surgery', 'emergency', 'vaccine', 'drug',
    'specialist', 'clinic', 'ache', 'discomfort', 'condition', 'illness',
    'remedy', 'cure', 'healing', 'wellness', 'complication',
    
    # Body parts
    'blood', 'heart', 'lung', 'kidney', 'liver', 'brain', 'stomach', 'intestine',
    'colon', 'skin', 'bone', 'joint', 'muscle', 'nerve', 'artery', 'vein',
    'throat', 'ear', 'eye', 'nose', 'mouth', 'head', 'neck', 'chest', 'back',
    'arm', 'leg', 'foot', 'hand', 'finger', 'toe', 'shoulder', 'knee', 'hip',
    'ankle', 'wrist', 'spine', 'abdomen', 'lymph', 'thyroid', 'pancreas',
    
    # Common symptoms
    'headache', 'fever', 'cough', 'cold', 'flu', 'covid', 'virus', 'dizziness',
    'nausea', 'vomiting', 'diarrhea', 'constipation', 'fatigue', 'tired',
    'rash', 'itch', 'swelling', 'inflammation', 'infection', 'bleeding', 'bruise',
    'sneeze', 'congestion', 'sore', 'stiff', 'weak', 'cramp', 'spasm',
    'insomnia', 'snore', 'breathe', 'breath', 'dizzy', 'faint', 'unconscious',
    'numbness', 'tingle', 'burn', 'chills', 'sweat', 'weight',
    
    # Conditions and diseases
    'diabetes', 'hypertension', 'pressure', 'cancer', 'stroke', 'arthritis',
    'asthma', 'allergy', 'alzheimer', 'dementia', 'parkinson', 'epilepsy',
    'seizure', 'depression', 'anxiety', 'adhd', 'autism', 'bipolar', 'schizophrenia',
    'pneumonia', 'bronchitis', 'emphysema', 'copd', 'influenza', 'hepatitis',
    'cirrhosis', 'ulcer', 'irritable', 'ibs', 'crohn', 'colitis', 'celiac',
    'anemia', 'hemophilia', 'leukemia', 'lymphoma', 'melanoma', 'carcinoma',
    'tumor', 'cyst', 'polyp', 'hernia', 'appendicitis', 'gallstone', 'kidney stone',
    'osteoporosis', 'scoliosis', 'fibromyalgia', 'migraine', 'concussion',
    'fracture', 'sprain', 'strain', 'tear', 'rupture', 'tendonitis', 'bursitis',
    'gout', 'lupus', 'ms', 'sclerosis', 'als', 'hiv', 'aids', 'std', 'sti',
    'herpes', 'hpv', 'gonorrhea', 'chlamydia', 'syphilis', 'ebola', 'malaria',
    'tuberculosis', 'lyme', 'meningitis', 'thyroid', 'goiter', 'grave', 'hashimoto',
    'addison', 'cushing', 'diabetes', 'gerd', 'reflux', 'psoriasis', 'eczema',
    'acne', 'rosacea', 'vertigo', 'tinnitus', 'glaucoma', 'cataract', 'macular',
    
    # Medical specialties
    'cardiology', 'neurology', 'gastroenterology', 'dermatology', 'orthopedic',
    'pediatric', 'gynecology', 'obstetrics', 'urology', 'endocrinology',
    'psychiatry', 'psychology', 'oncology', 'radiology', 'immunology',
    'pulmonology', 'rheumatology', 'nephrology', 'hematology',
    
    # Health topics
    'nutrition', 'diet', 'exercise', 'fitness', 'sleep', 'stress', 'mental',
    'pregnancy', 'prenatal', 'postnatal', 'breastfeeding', 'vaccine', 'immunization',
    'vitamin', 'mineral', 'supplement', 'probiotic', 'antibiotic', 'antiseptic',
    'hygiene', 'sanitation', 'prevention', 'screening', 'checkup', 'mortality',
    'longevity', 'disability', 'therapy', 'rehabilitation', 'prescription',
    'medication', 'pharmacy', 'generic', 'side effect', 'overdose', 'addiction',
    'withdrawal', 'deficiency', 'insulin', 'testosterone', 'estrogen', 'hormone',
    'contraceptive', 'fertility', 'infertility', 'ivf', 'menopause', 'menstruation',
    'childbirth', 'neonatal', 'pediatric', 'geriatric', 'elderly', 'chronic',
    'acute', 'terminal', 'palliative', 'hospice', 'recovery', 'remission',
    'biopsy', 'scan', 'mri', 'ct', 'x-ray', 'ultrasound', 'ekg', 'ecg', 'eeg'
]

# Initialize Flask app
app = Flask(__name__)

def is_medical_query(text):
    """
    Determines if a query is medical-related using simple keyword matching.
    """
    text_lower = text.lower()
    for keyword in MEDICAL_KEYWORDS:
        if keyword in text_lower:
            return True
    return False

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html', avatars=AVAILABLE_AVATARS)

@app.route('/api/create_token', methods=['POST'])
def create_token():
    """Create a session token for Heygen Streaming API."""
    try:
        response = requests.post(
            f"{HEYGEN_API_BASE_URL}/v1/streaming.create_token",
            headers={
                "Content-Type": "application/json",
                "X-Api-Key": HEYGEN_API_KEY
            }
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/check_query', methods=['POST'])
def check_query():
    """Check if a query is medical-related and generate a response."""
    data = request.json
    query_text = data.get('text', '')
    
    is_medical = is_medical_query(query_text)
    
    if is_medical:
        # Generate a medical response
        response = generate_medical_response(query_text)
        return jsonify({"is_medical": True, "response": response})
    else:
        return jsonify({
            "is_medical": False, 
            "response": "I'm sorry, I can only provide assistance with medical-related questions. Please ask me something related to healthcare or medical information."
        })

@app.route('/api/config', methods=['GET'])
def get_config():
    """Return application configuration for the frontend."""
    return jsonify({
        "api_base_url": HEYGEN_API_BASE_URL,
        "avatars": AVAILABLE_AVATARS
    })

def generate_medical_response(query):
    """Generate a response to a medical query.
    In a production environment, this would use a medical knowledge base or API.
    """
    query_lower = query.lower()
    
    # COMMON SYMPTOMS
    # Headaches and migraines
    if any(word in query_lower for word in ['headache', 'head pain', 'migraine']):
        return "Headaches can have many causes, including stress, dehydration, lack of sleep, or eye strain. For occasional headaches, rest, hydration, and over-the-counter pain relievers may help. If you experience severe, persistent, or unusual headaches, please consult a healthcare provider for proper diagnosis and treatment. Migraines specifically can cause throbbing pain, sensitivity to light and sound, and sometimes nausea. They might benefit from specific migraine medications."
    
    # Fever
    elif any(word in query_lower for word in ['fever', 'temperature', 'hot']):
        return "A fever is usually a sign that your body is fighting an infection. Adults with a temperature above 100.4°F (38°C) have a fever. Rest, hydration, and over-the-counter fever reducers can help manage mild fevers. If the fever is high (above 103°F or 39.4°C), lasts more than 3 days, or is accompanied by severe symptoms, please seek medical attention. Fevers in infants and young children should be evaluated by a healthcare provider promptly."
    
    # Respiratory issues
    elif any(word in query_lower for word in ['cold', 'flu', 'cough', 'sneeze', 'congestion', 'stuffy nose']):
        return "Common cold and flu symptoms include coughing, sneezing, congestion, and sometimes fever. Rest, hydration, and over-the-counter medications can help manage symptoms. Most colds resolve within 7-10 days. Flu may last longer and can cause more severe symptoms. For persistent cough, difficulty breathing, or symptoms that worsen after initially improving, please consult a healthcare provider. Annual flu vaccines are recommended to reduce the risk of influenza."
    
    # Digestive issues
    elif any(word in query_lower for word in ['stomach', 'nausea', 'vomiting', 'diarrhea', 'constipation', 'ibs', 'indigestion', 'heartburn', 'gerd', 'reflux']):
        return "Digestive issues can range from mild discomfort to more serious conditions. For occasional nausea, vomiting, or diarrhea, staying hydrated is important. Clear liquids and bland foods can help when returning to eating. For heartburn or reflux, avoiding spicy foods, large meals, and eating close to bedtime may help. If symptoms are severe, persistent, or accompanied by weight loss, blood in stool, or difficulty swallowing, please seek medical attention promptly. Chronic digestive issues like IBS benefit from medical management."
    
    # Skin conditions
    elif any(word in query_lower for word in ['rash', 'itch', 'acne', 'eczema', 'psoriasis', 'hives', 'skin', 'dermatitis']):
        return "Skin conditions can be caused by allergies, infections, immune system disorders, or environmental factors. For mild itching or rashes, over-the-counter antihistamines or hydrocortisone cream may provide relief. Keeping the skin moisturized and avoiding harsh soaps can help with eczema and dry skin. For severe, widespread, or painful skin conditions, or those that don't improve with home care, please consult a dermatologist. Conditions like psoriasis and chronic eczema typically require medical management."
    
    # Pain
    elif any(word in query_lower for word in ['pain', 'ache', 'sore', 'hurt']):
        if any(word in query_lower for word in ['back', 'spine', 'neck']):
            return "Back and neck pain are common and often related to muscle strain, poor posture, or overuse. Rest, gentle stretching, proper posture, and over-the-counter pain relievers may help. Heat or ice can also provide relief. For pain that is severe, persistent, or accompanied by numbness, tingling, or weakness in the limbs, please seek medical attention. Physical therapy can be beneficial for chronic back or neck issues."
        elif any(word in query_lower for word in ['joint', 'arthritis', 'knee', 'hip', 'shoulder', 'elbow']):
            return "Joint pain can be caused by injury, overuse, or conditions like arthritis. Rest, over-the-counter pain relievers, and ice or heat may help manage symptoms. Maintaining a healthy weight reduces stress on joints, particularly knees and hips. For severe, persistent, or worsening joint pain, especially if accompanied by swelling, redness, or reduced mobility, please consult a healthcare provider. Conditions like rheumatoid arthritis benefit from early medical intervention."
        elif any(word in query_lower for word in ['chest', 'heart']):
            return "Chest pain can be caused by various conditions, from muscle strain to serious heart problems. If you're experiencing severe chest pain, especially if it's accompanied by shortness of breath, sweating, nausea, or pain radiating to the arm, jaw, or back, please seek emergency medical attention immediately. These could be signs of a heart attack. Even if chest pain seems mild, it's important to have it evaluated by a healthcare provider to rule out serious conditions."
        elif any(word in query_lower for word in ['abdominal', 'stomach', 'belly']):
            return "Abdominal pain can have many causes, from gas and indigestion to more serious conditions like appendicitis or gallstones. Mild, temporary pain may be managed with rest and over-the-counter medications. For severe, persistent, or worsening abdominal pain, especially if accompanied by fever, vomiting, or signs of dehydration, please seek medical attention. Sudden, severe abdominal pain could indicate a medical emergency requiring immediate care."
        else:
            return "Pain can be a symptom of many different conditions and may require different approaches to management. For mild pain, rest, ice or heat, and over-the-counter pain relievers may help. For severe, persistent, or worsening pain, especially if it limits your daily activities or is accompanied by other concerning symptoms, please consult a healthcare provider. Chronic pain often benefits from a comprehensive treatment approach that may include medication, physical therapy, and lifestyle modifications."
    
    # Fatigue
    elif any(word in query_lower for word in ['fatigue', 'tired', 'exhausted', 'energy', 'lethargy']):
        return "Fatigue can result from various factors including poor sleep, stress, overexertion, or medical conditions. Ensuring adequate sleep, regular physical activity, a balanced diet, and stress management can help improve energy levels. If fatigue is severe, persistent, or not improved with rest, it could indicate an underlying health issue such as anemia, thyroid disorders, or depression. If fatigue significantly impacts your daily life or is accompanied by other symptoms, please consult a healthcare provider for evaluation."
    
    # Sleep issues
    elif any(word in query_lower for word in ['sleep', 'insomnia', 'apnea', 'snore', 'snoring']):
        return "Quality sleep is crucial for overall health. Adults typically need 7-9 hours of sleep per night. Poor sleep can affect mood, cognitive function, and physical health. Establishing a regular sleep schedule, creating a restful environment, and avoiding caffeine and screens before bedtime can help improve sleep quality. Sleep apnea, characterized by interrupted breathing during sleep and often accompanied by snoring, may require medical intervention. If you're experiencing persistent sleep problems, consider consulting a healthcare provider for proper evaluation and treatment options."
    
    # CHRONIC CONDITIONS
    # Cardiovascular
    elif any(word in query_lower for word in ['blood pressure', 'hypertension', 'hypotension']):
        return "Normal blood pressure is typically around 120/80 mmHg. Hypertension (high blood pressure) is generally considered to be 130/80 mmHg or higher. Lifestyle changes like reducing sodium intake, regular exercise, maintaining a healthy weight, and limiting alcohol can help manage blood pressure. Hypotension (low blood pressure) can cause dizziness and fainting. If you have concerns about your blood pressure or experience symptoms like severe headaches, chest pain, or dizziness, please consult a healthcare provider for proper evaluation and treatment recommendations."
    
    # Heart disease
    elif any(word in query_lower for word in ['heart disease', 'cardiac', 'heart attack', 'angina', 'coronary']):
        return "Heart disease encompasses various conditions affecting the heart, including coronary artery disease, heart rhythm problems, and heart valve issues. Symptoms may include chest pain or discomfort (angina), shortness of breath, and fatigue. Risk factors include high blood pressure, high cholesterol, smoking, diabetes, obesity, and family history. A heart-healthy lifestyle includes regular exercise, a balanced diet low in saturated fats and sodium, not smoking, and managing stress. If you experience chest pain, shortness of breath, or other concerning symptoms, please seek immediate medical attention."
    
    # Stroke
    elif any(word in query_lower for word in ['stroke', 'tia', 'transient ischemic']):
        return "A stroke occurs when blood flow to part of the brain is interrupted, causing brain cells to die. Symptoms include sudden numbness or weakness (especially on one side of the body), confusion, trouble speaking or understanding speech, vision problems, dizziness, or severe headache. Remember the acronym FAST for stroke symptoms: Face drooping, Arm weakness, Speech difficulty, Time to call emergency services. Prompt treatment is crucial to minimize brain damage. Risk factors include high blood pressure, smoking, diabetes, and high cholesterol. If you suspect someone is having a stroke, seek emergency medical attention immediately."
    
    # Diabetes
    elif any(word in query_lower for word in ['diabetes', 'blood sugar', 'glucose', 'insulin']):
        return "Diabetes is a condition that affects how your body processes blood sugar (glucose). There are several types, with Type 1, Type 2, and gestational diabetes being the most common. Symptoms may include increased thirst, frequent urination, hunger, fatigue, and blurred vision. Managing diabetes typically involves monitoring blood sugar, medication (including insulin for some), healthy eating, regular physical activity, and maintaining a healthy weight. Complications can affect the heart, kidneys, eyes, and nerves, making regular medical check-ups important. If you have concerns about diabetes or experience symptoms, please consult a healthcare provider for proper evaluation."
    
    # Cancer
    elif any(word in query_lower for word in ['cancer', 'tumor', 'oncology', 'chemotherapy', 'radiation', 'malignant']):
        return "Cancer occurs when abnormal cells divide uncontrollably and can invade nearby tissues. There are many types of cancer, affecting different parts of the body. Symptoms vary widely depending on the type and stage but may include unexplained weight loss, fatigue, pain, changes in skin, unusual bleeding, or persistent cough. Risk factors include genetic predisposition, certain infections, radiation exposure, and lifestyle factors like tobacco use. Treatment options may include surgery, chemotherapy, radiation therapy, immunotherapy, and targeted therapy. Early detection through regular screenings and prompt medical attention for concerning symptoms is important. If you notice unusual changes in your body, please consult a healthcare provider."
    
    # Respiratory diseases
    elif any(word in query_lower for word in ['asthma', 'copd', 'emphysema', 'bronchitis', 'pneumonia', 'lung disease']):
        return "Respiratory diseases affect the lungs and breathing. Asthma causes airway inflammation and breathing difficulty, often triggered by allergens or exercise. COPD (including emphysema and chronic bronchitis) typically results from long-term exposure to irritants like tobacco smoke. Pneumonia is an infection that inflames air sacs in the lungs. Symptoms of respiratory conditions may include shortness of breath, coughing, wheezing, and chest tightness. Management depends on the specific condition but may include medications, inhalers, oxygen therapy, pulmonary rehabilitation, and avoiding triggers. If you experience breathing difficulties, persistent cough, or other respiratory symptoms, please seek medical evaluation."
    
    # Autoimmune disorders
    elif any(word in query_lower for word in ['autoimmune', 'lupus', 'rheumatoid arthritis', 'multiple sclerosis', 'ms', 'psoriasis', 'crohn', 'celiac']):
        return "Autoimmune disorders occur when the immune system mistakenly attacks the body's own tissues. There are over 80 types, including rheumatoid arthritis, lupus, multiple sclerosis, psoriasis, Crohn's disease, and celiac disease. Symptoms vary widely but may include fatigue, joint pain, skin problems, digestive issues, and recurrent fever. Many autoimmune conditions have genetic components and may be triggered by environmental factors or infections. Treatment typically aims to reduce inflammation, manage symptoms, and modulate the immune system. If you experience persistent, unusual symptoms that affect multiple body systems, please consult a healthcare provider for evaluation."
    
    # Neurological disorders
    elif any(word in query_lower for word in ['alzheimer', 'dementia', 'parkinson', 'epilepsy', 'seizure', 'neuropathy', 'multiple sclerosis', 'ms']):
        return "Neurological disorders affect the brain, spinal cord, and nerves. Alzheimer's disease and other dementias cause progressive memory loss and cognitive decline. Parkinson's disease affects movement, causing tremors, stiffness, and balance problems. Epilepsy involves recurrent seizures. Multiple sclerosis damages the protective covering of nerves. Symptoms vary widely based on the condition but may include memory problems, tremors, muscle weakness, pain, seizures, or difficulty with coordination. Treatment depends on the specific disorder and may include medications, physical therapy, lifestyle modifications, and in some cases, surgery. If you experience concerning neurological symptoms, please consult a healthcare provider for proper evaluation."
    
    # MENTAL HEALTH
    elif any(word in query_lower for word in ['stress', 'anxiety', 'depression', 'mental health', 'panic', 'bipolar', 'schizophrenia', 'ocd', 'ptsd']):
        return "Mental health is as important as physical health. Conditions like depression, anxiety, bipolar disorder, schizophrenia, OCD, and PTSD are medical conditions that affect mood, thinking, and behavior. Symptoms vary but may include persistent sadness, excessive worry, mood swings, abnormal thought patterns, or flashbacks to traumatic events. Effective treatments include therapy, medication, lifestyle changes, and support groups. The combination of treatments depends on the individual and the specific condition. If you're struggling with mental health concerns, please reach out to a healthcare provider or mental health professional. Remember that seeking help is a sign of strength, and many mental health conditions respond well to treatment."
    
    # LIFESTYLE & PREVENTION
    # Diet and nutrition
    elif any(word in query_lower for word in ['diet', 'nutrition', 'food', 'eat', 'weight', 'obesity', 'underweight']):
        return "A balanced diet is essential for good health. This includes a variety of fruits, vegetables, whole grains, lean proteins, and healthy fats. Limiting processed foods, added sugars, and excessive salt is recommended. Nutritional needs can vary based on age, sex, activity level, and health conditions. Maintaining a healthy weight reduces the risk of many chronic diseases including diabetes, heart disease, and certain cancers. If you're concerned about your weight or nutritional status, consider consulting a healthcare provider or registered dietitian for personalized advice. Remember that sustainable dietary changes, rather than extreme diets, tend to be most effective for long-term health."
    
    # Exercise and fitness
    elif any(word in query_lower for word in ['exercise', 'workout', 'fitness', 'physical activity', 'sedentary']):
        return "Regular physical activity offers numerous health benefits, including weight management, stronger bones and muscles, and reduced risk of various diseases like heart disease, stroke, type 2 diabetes, and some cancers. Adults should aim for at least 150 minutes of moderate-intensity exercise per week, along with muscle-strengthening activities twice weekly. Activities can include walking, swimming, cycling, strength training, or sports. Starting slowly and gradually increasing intensity and duration is recommended, especially if you've been inactive. Always consult a healthcare provider before beginning a new exercise program, especially if you have existing health conditions."
    
    # Preventive care
    elif any(word in query_lower for word in ['prevention', 'screening', 'checkup', 'vaccine', 'immunization']):
        return "Preventive healthcare helps identify and address health issues before they become serious. This includes regular check-ups, screening tests (like mammograms, colonoscopies, and blood pressure checks), and vaccinations. The recommended screenings and their frequency depend on factors like age, sex, family history, and personal risk factors. Vaccines are important tools for preventing infectious diseases and are recommended throughout life, not just in childhood. Staying up-to-date with preventive care helps maintain good health and can detect conditions early when they're most treatable. Your healthcare provider can help determine which preventive measures are appropriate for you."
    
    # SPECIAL POPULATIONS
    # Women's health
    elif any(word in query_lower for word in ['menstruation', 'period', 'menopause', 'pregnancy', 'breast', 'cervical', 'ovarian', 'uterine', 'gynecological']):
        return "Women's health encompasses various aspects including reproductive health, pregnancy, menopause, and conditions that primarily affect women. Regular gynecological check-ups and screenings like Pap tests and mammograms are important for preventive care. Menstrual irregularities, pelvic pain, or unusual vaginal discharge should be evaluated by a healthcare provider. During pregnancy, prenatal care is essential for the health of both mother and baby. Menopause, typically occurring in the late 40s to early 50s, involves hormonal changes that can cause symptoms like hot flashes and sleep disturbances. For specific concerns about women's health issues, please consult with a healthcare provider for personalized guidance."
    
    # Men's health
    elif any(word in query_lower for word in ['prostate', 'testicular', 'erectile', 'male pattern baldness', 'men\'s health']):
        return "Men's health includes issues related to the prostate, testicles, and conditions that primarily affect men. Regular check-ups can help detect conditions like prostate cancer early. The prostate-specific antigen (PSA) test and digital rectal exam are screening tools for prostate health. Testicular self-exams can help detect abnormalities. Erectile dysfunction may result from various physical or psychological factors and often has effective treatments available. Male pattern baldness is influenced by genetics and hormones, with various treatment options. For specific concerns about men's health issues, please consult with a healthcare provider for personalized evaluation and advice."
    
    # Children's health
    elif any(word in query_lower for word in ['child', 'pediatric', 'infant', 'baby', 'toddler', 'adolescent', 'teen']):
        return "Children's health requires special consideration of their developing bodies and immune systems. Regular well-child visits help monitor growth, development, and overall health. Vaccinations are crucial for preventing serious childhood diseases. Common childhood illnesses include colds, ear infections, and strep throat. For infants, proper nutrition (through breastfeeding or formula) and safe sleep practices are important. Adolescence brings physical, emotional, and social changes that may affect health. If you have concerns about a child's health, growth, or development, please consult a pediatrician or family doctor for appropriate evaluation and guidance."
    
    # Elderly health
    elif any(word in query_lower for word in ['elderly', 'aging', 'geriatric', 'senior']):
        return "Aging brings physiological changes that can affect health and well-being. Older adults may face challenges including multiple chronic conditions, medication management, increased fall risk, and changes in memory or cognitive function. Regular health check-ups, appropriate screenings, staying physically and mentally active, maintaining social connections, and proper nutrition are important aspects of healthy aging. Some medications may affect older adults differently, making medication reviews important. Memory changes that interfere with daily activities should be evaluated by a healthcare provider. For specific concerns about aging-related health issues, please consult with a healthcare provider for personalized guidance."
    
    # MEDICATIONS AND TREATMENTS
    elif any(word in query_lower for word in ['medication', 'drug', 'medicine', 'prescription', 'over-the-counter', 'side effect']):
        return "Medications play an important role in treating many health conditions. Prescription medications require a healthcare provider's order, while over-the-counter medications are available without a prescription. All medications can have potential side effects and may interact with other medications, supplements, or foods. It's important to take medications as prescribed, inform your healthcare providers of all medications you're taking (including over-the-counter and supplements), and report any concerning side effects. Never stop taking a prescribed medication without consulting your healthcare provider. If you have questions about a specific medication, its use, or potential side effects, please consult with a healthcare provider or pharmacist."
    
    # Surgery and procedures
    elif any(word in query_lower for word in ['surgery', 'operation', 'procedure', 'transplant']):
        return "Surgical procedures range from minor outpatient procedures to complex operations requiring hospital stays. Before surgery, your healthcare team will explain the procedure, potential risks and benefits, and what to expect during recovery. Following pre-surgical instructions (like fasting or medication adjustments) is important for safety. After surgery, proper wound care, activity restrictions, and follow-up appointments help ensure good outcomes. Pain management and watching for signs of complications (like infection) are also important during recovery. If you have questions about a specific surgical procedure or are experiencing issues after surgery, please consult with your healthcare provider for personalized guidance."
    
    # MISCELLANEOUS HEALTH TOPICS
    # Allergies
    elif any(word in query_lower for word in ['allergy', 'allergic', 'allergen', 'hay fever']):
        return "Allergies occur when the immune system reacts to substances (allergens) that are typically harmless. Common allergens include pollen, dust mites, pet dander, certain foods, insect stings, and medications. Symptoms can range from mild (sneezing, runny nose, itchy eyes) to severe (difficulty breathing, anaphylaxis). Management strategies include avoiding triggers, over-the-counter or prescription medications, and in some cases, immunotherapy (allergy shots). For food allergies, careful label reading and carrying emergency medication for severe reactions is important. If you experience concerning allergy symptoms or suspect a new allergy, please consult a healthcare provider for proper evaluation and treatment recommendations."
    
    # Infectious diseases
    elif any(word in query_lower for word in ['infection', 'infectious', 'virus', 'bacteria', 'fungal', 'parasite', 'covid', 'flu', 'pneumonia', 'tuberculosis', 'hiv', 'hepatitis']):
        return "Infectious diseases are caused by organisms like viruses, bacteria, fungi, or parasites. They can spread through various routes including person-to-person contact, insect bites, contaminated food or water, or environmental exposure. Common infectious diseases include colds, flu, COVID-19, urinary tract infections, and foodborne illnesses. Prevention strategies include good hygiene practices, vaccinations, safe food handling, and avoiding contact with individuals who are ill. Treatment depends on the specific pathogen but may include antibiotics (for bacterial infections), antivirals, or supportive care. If you experience symptoms of infection like fever, unusual fatigue, or localized symptoms, please consult a healthcare provider for proper evaluation and treatment."
    
    # First aid
    elif any(word in query_lower for word in ['first aid', 'emergency', 'cpr', 'bleeding', 'burn', 'fracture', 'sprain', 'wound', 'injury']):
        return "First aid knowledge is valuable for handling emergencies until professional help arrives. For bleeding, apply direct pressure with clean material. For burns, cool with room temperature water and cover with clean, dry bandage. For suspected fractures, immobilize the area without attempting to realign bones. For choking, perform abdominal thrusts (Heimlich maneuver). For cardiac arrest, perform CPR if trained. Always call emergency services for serious injuries or medical emergencies. Taking a certified first aid and CPR course is recommended. This general information is not a substitute for emergency medical care. For any serious injury or medical emergency, please seek professional medical help immediately."


if __name__ == '__main__':
    print(f"Starting MediMate application on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)