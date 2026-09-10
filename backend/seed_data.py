"""
Janaseva Seed Data Script
Pre-populates the PostgreSQL/SQLite database with verified Malayalam and English records
for all 17 mandatory government services.
"""

import sys
import os

# Ensure backend root is on sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.models.service import Service, ServiceDocument, ServiceGuide, ServiceFAQ

def seed_database(db_session: Session = None):
    Base.metadata.create_all(bind=engine)
    db: Session = db_session if db_session else SessionLocal()

    if db.query(Service).count() > 0:
        print("Database already contains services. Skipping seed.")
        if not db_session:
            db.close()
        return

    services_data = [
        # 1. Driving Licence Renewal
        {
            "slug": "renew-driving-licence",
            "category": "Transport / Motor Vehicles Department",
            "name_en": "Driving Licence Renewal",
            "name_ml": "ഡ്രൈവിംഗ് ലൈസൻസ് പുതുക്കൽ",
            "description_en": "Renewal of expired Driving Licence issued by Kerala MVD.",
            "description_ml": "കേരള മോട്ടോർ വാഹന വകുപ്പ് നൽകിയ ഡ്രൈവിംഗ് ലൈസൻസ് പുതുക്കൽ സേവനം.",
            "eligibility_en": "Existing DL holder in Kerala whose licence is near or past expiry.",
            "eligibility_ml": "കേരളത്തിൽ നിലവിലുള്ള ഡ്രൈവിംഗ് ലൈസൻസ് കാലാവധി കഴിയാറായവരോ കഴിഞ്ഞവരോ ആയ വ്യക്തികൾ.",
            "application_fee": "₹450 + Portal charges",
            "processing_time_days": 7,
            "official_website": "https://parivahan.gov.in",
            "office_type": "Sub RTO / Akshaya Center",
            "aliases_manglish": "license puthukkanam, driving license puthukkanam, dl renewal, laisenso puthukkanam",
            "documents": [
                {"doc_name_en": "Existing Original Driving Licence", "doc_name_ml": "നിലവിലെ ഡ്രൈവിംഗ് ലൈസൻസ്", "is_mandatory": True},
                {"doc_name_en": "Form 1A Medical Certificate (if age > 40)", "doc_name_ml": "ഫോറം 1A മെഡിക്കൽ സർട്ടിഫിക്കറ്റ് (40 വയസ്സിന് മുകളിൽ)", "is_mandatory": True},
                {"doc_name_en": "Passport Size Photograph", "doc_name_ml": "പാസ്‌പോർട്ട് സൈസ് ഫോട്ടോ", "is_mandatory": True},
                {"doc_name_en": "Aadhaar Card", "doc_name_ml": "ആധാർ കാർഡ്", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Visit Parivahan Portal", "title_ml": "പരിവാഹൻ പോർട്ടൽ സന്ദർശിക്കുക", "description_en": "Go to parivahan.gov.in and select Drivers/ Learners License.", "description_ml": "parivahan.gov.in സന്ദർശിച്ച് Drivers/ Learners License തിരഞ്ഞെടുക്കുക."},
                {"step_number": 2, "title_en": "Select State", "title_ml": "സംസ്ഥാനം തിരഞ്ഞെടുക്കുക", "description_en": "Select Kerala state from dropdown list.", "description_ml": "ഡ്രോപ്പ്ഡൗൺ ലിസ്റ്റിൽ നിന്ന് കേരളം തിരഞ്ഞെടുക്കുക."},
                {"step_number": 3, "title_en": "Apply for DL Renewal", "title_ml": "DL Renewal സേവനം നൽകുക", "description_en": "Enter DL number and date of birth to load details.", "description_ml": "DL നമ്പറും ജനനത്തീയതിയും നൽകി വിവരങ്ങൾ ലോഡ് ചെയ്യുക."},
                {"step_number": 4, "title_en": "Upload Documents & Pay Fee", "title_ml": "രേഖകൾ അപ്‌ലോഡ് ചെയ്തു ഫീസ് അടയ്ക്കുക", "description_en": "Upload medical certificate, photo and complete online payment.", "description_ml": "മെഡിക്കൽ സർട്ടിഫിക്കറ്റ്, ഫോട്ടോ അപ്‌ലോഡ് ചെയ്ത് ഫീസ് അടയ്ക്കുക."}
            ],
            "faqs": [
                {"question_en": "What is the grace period for DL renewal?", "question_ml": "ഡ്രൈവിംഗ് ലൈസൻസ് പുതുക്കാൻ എത്ര ദിവസത്തെ ഗ്രേസ് പിരീഡ് ഉണ്ട്?", "answer_en": "You can renew 1 year before expiry or up to 1 year after expiry without re-test.", "answer_ml": "കാലാവധി തീരുന്നതിന് 1 വർഷം മുമ്പോ അല്ലെങ്കിൽ 1 വർഷം വരെ വൈകിയോ റീ-ടെസ്റ്റ് ഇല്ലാതെ പുതുക്കാം."}
            ]
        },
        # 2. Driving Licence (New)
        {
            "slug": "new-driving-licence",
            "category": "Transport / Motor Vehicles Department",
            "name_en": "New Driving Licence",
            "name_ml": "പുതിയ ഡ്രൈവിംഗ് ലൈസൻസ്",
            "description_en": "Application for fresh Driving Licence after passing driving test.",
            "description_ml": "ഡ്രൈവിംഗ് ടെസ്റ്റ് പാസ്സായതിന് ശേഷമുള്ള പുതിയ ഡ്രൈവിംഗ് ലൈസൻസിനായുള്ള അപേക്ഷ.",
            "eligibility_en": "Held Learner's License for minimum 30 days and passed driving test.",
            "eligibility_ml": "കുറഞ്ഞത് 30 ദിവസം ലേണേഴ്‌സ് ലൈസൻസ് പൂർത്തിയാക്കി ടെസ്റ്റ് പാസ്സായവർ.",
            "application_fee": "₹800",
            "processing_time_days": 14,
            "official_website": "https://parivahan.gov.in",
            "office_type": "RTO / Sub RTO",
            "aliases_manglish": "license edukkanam, puthiya license, new dl",
            "documents": [
                {"doc_name_en": "Valid Learner's Licence Number", "doc_name_ml": "സാധുവായ ലേണേഴ്‌സ് ലൈസൻസ് നമ്പർ", "is_mandatory": True},
                {"doc_name_en": "Driving School Certificate (Form 5)", "doc_name_ml": "ഡ്രൈവിംഗ് സ്കൂൾ സർട്ടിഫിക്കറ്റ് (ഫോറം 5)", "is_mandatory": True},
                {"doc_name_en": "Aadhaar Card / ID Proof", "doc_name_ml": "ആധാർ കാർഡ് / തിരിച്ചറിയൽ രേഖ", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Apply Online on Parivahan", "title_ml": "പരിവാഹനിൽ അപേക്ഷിക്കുക", "description_en": "Select 'Apply for Driving Licence' on Sarathi portal.", "description_ml": "സാരഥി പോർട്ടലിൽ 'Apply for Driving Licence' തിരഞ്ഞെടുക്കുക."},
                {"step_number": 2, "title_en": "Book Test Slot", "title_ml": "ടെസ്റ്റ് സ്ലോട്ട് ബുക്ക് ചെയ്യുക", "description_en": "Schedule your driving test date at local RTO.", "description_ml": "സമീപത്തെ RTO-യിൽ ഡ്രൈവിംഗ് ടെസ്റ്റ് തിയ്യതി ബുക്ക് ചെയ്യുക."}
            ],
            "faqs": [
                {"question_en": "How long is the DL valid?", "question_ml": "ഡ്രൈവിംഗ് ലൈസൻസ് കാലാവധി എത്രയാണ്?", "answer_en": "Valid for 20 years or until age 40.", "answer_ml": "20 വർഷം അല്ലെങ്കിൽ 40 വയസ്സ് തികയുന്നത് വരെ കാലാവധിയുണ്ട്."}
            ]
        },
        # 3. Learner's Licence
        {
            "slug": "learners-licence",
            "category": "Transport / Motor Vehicles Department",
            "name_en": "Learner's Licence",
            "name_ml": "ലേണേഴ്‌സ് ലൈസൻസ്",
            "description_en": "Provisional permit for learning to drive motor vehicles in Kerala.",
            "description_ml": "വാഹനം ഓടിക്കാൻ പഠിക്കുന്നതിനായുള്ള താത്കാലിക അനുമതി പത്രം.",
            "eligibility_en": "Age 18+ for gear vehicles (16+ for gearless 50cc).",
            "eligibility_ml": "ഗിയറുള്ള വാഹനങ്ങൾക്ക് 18 വയസ്സും ഗിയറില്ലാത്തവയ്ക്ക് 16 വയസ്സും പൂർത്തിയായവർ.",
            "application_fee": "₹350",
            "processing_time_days": 3,
            "official_website": "https://parivahan.gov.in",
            "office_type": "Online / Akshaya",
            "aliases_manglish": "learners license, learners test, learner puthukkanam",
            "documents": [
                {"doc_name_en": "Aadhaar Card (E-KYC)", "doc_name_ml": "ആധാർ കാർഡ് (ഇ-കെവൈസി)", "is_mandatory": True},
                {"doc_name_en": "SSLC Certificate / Age Proof", "doc_name_ml": "എസ്.എസ്.എൽ.സി സർട്ടിഫിക്കറ്റ് / വയസ്സ് തെളിയിക്കുന്ന രേഖ", "is_mandatory": True},
                {"doc_name_en": "Blood Group Report", "doc_name_ml": "രക്തഗ്രൂപ്പ് സർട്ടിഫിക്കറ്റ്", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Aadhaar E-KYC Authentication", "title_ml": "ആധാർ ഓതന്റിക്കേഷൻ", "description_en": "Login using Aadhaar linked phone to skip RTO visit.", "description_ml": "ആധാർ ലിങ്ക് ചെയ്ത ഫോൺ നമ്പർ ഉപയോഗിച്ച് ലോഗിൻ ചെയ്യുക."},
                {"step_number": 2, "title_en": "Online Learners Test", "title_ml": "ഓൺലൈൻ ലേണേഴ്‌സ് പരീക്ഷ", "description_en": "Pass 15 minute online road safety test from home.", "description_ml": "വീട്ടിലിരുന്ന് 15 മിനിറ്റ് ഓൺലൈൻ റോഡ് സേഫ്റ്റി പരീക്ഷ പാസ്സാകുക."}
            ],
            "faqs": [
                {"question_en": "What is the pass mark for online test?", "question_ml": "ലേണേഴ്‌സ് പരീക്ഷയ്ക്ക് എത്ര മാർക്ക് വേണം?", "answer_en": "Must score 12 out of 20 questions.", "answer_ml": "20 ചോദ്യങ്ങളിൽ 12 എണ്ണത്തിന് കൃത്യമായി ഉത്തരം നൽകണം."}
            ]
        },
        # 4. Aadhaar Update
        {
            "slug": "aadhaar-update",
            "category": "UIDAI / Identity",
            "name_en": "Aadhaar Card Update",
            "name_ml": "ആധാർ കാർഡ് തിരുത്തൽ",
            "description_en": "Update address, phone number, name, DOB, or biometrics in Aadhaar.",
            "description_ml": "ആധാറിലെ വിലാസം, ഫോൺ നമ്പർ, പേര്, ജനനത്തീയതി എന്നിവ തിരുത്തൽ സേവനം.",
            "eligibility_en": "All Indian Aadhaar holders.",
            "eligibility_ml": "ആധാർ കാർഡുള്ള എല്ലാ ഇന്ത്യൻ പൗരന്മാർക്കും.",
            "application_fee": "₹50 (Demographic) / ₹100 (Biometric)",
            "processing_time_days": 15,
            "official_website": "https://myaadhaar.uidai.gov.in",
            "office_type": "Aadhaar Seva Kendra / Akshaya",
            "aliases_manglish": "aadhaar update, aadhaar card change, aadhaar thiruthal",
            "documents": [
                {"doc_name_en": "Existing Aadhaar Card", "doc_name_ml": "നിലവിലുള്ള ആധാർ കാർഡ്", "is_mandatory": True},
                {"doc_name_en": "Proof of Address (Ration Card/Voter ID)", "doc_name_ml": "വിലാസം തെളിയിക്കുന്ന രേഖ", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Visit MyAadhaar Portal", "title_ml": "MyAadhaar പോർട്ടൽ തുറക്കുക", "description_en": "Login using Aadhaar & OTP.", "description_ml": "ആധാറും OTP യും ഉപയോഗിച്ച് ലോഗിൻ ചെയ്യുക."},
                {"step_number": 2, "title_en": "Update Address Online", "title_ml": "വിലാസം ഓൺലൈനായി നൽകുക", "description_en": "Upload Proof of Address document and submit.", "description_ml": "വിലാസം തെളിയിക്കുന്ന രേഖ അപ്‌ലോഡ് ചെയ്യുക."}
            ],
            "faqs": [
                {"question_en": "Can I update phone number online?", "question_ml": "ഫോൺ നമ്പർ ഓൺലൈനായി മാറ്റാമോ?", "answer_en": "Mobile update requires biometric visit at Aadhaar Kendra.", "answer_ml": "ഫോൺ നമ്പർ മാറ്റാൻ ആധാർ കേന്ദ്രത്തിൽ നേരിട്ട് എത്തണം."}
            ]
        },
        # 5. PAN Card
        {
            "slug": "pan-card",
            "category": "Income Tax / NSDL",
            "name_en": "PAN Card Application",
            "name_ml": "പാൻ കാർഡ് അപേക്ഷ",
            "description_en": "Apply for new Permanent Account Number (PAN) or correction.",
            "description_ml": "പുതിയ ഇൻകം ടാക്സ് പാൻ കാർഡിനായുള്ള അപേക്ഷ അല്ലെങ്കിൽ തിരുത്തൽ.",
            "eligibility_en": "All Indian citizens.",
            "eligibility_ml": "എല്ലാ ഇന്ത്യൻ പൗരന്മാർക്കും.",
            "application_fee": "₹107",
            "processing_time_days": 10,
            "official_website": "https://www.onlineservices.nsdl.com",
            "office_type": "Online / Akshaya",
            "aliases_manglish": "pan card, pan edukkanam, pan card application",
            "documents": [
                {"doc_name_en": "Aadhaar Card", "doc_name_ml": "ആധാർ കാർഡ്", "is_mandatory": True},
                {"doc_name_en": "Passport Size Photo", "doc_name_ml": "ഫോട്ടോ", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "e-KYC Instant PAN", "title_ml": "ഇൻസ്റ്റന്റ് പാൻ കാർഡ്", "description_en": "Use Income Tax portal for instant free e-PAN via Aadhaar OTP.", "description_ml": "ആധാർ OTP ഉപയോഗിച്ച് സൗജന്യമായി e-PAN ഉടൻ നേടാം."}
            ],
            "faqs": [
                {"question_en": "Is PAN compulsory for bank accounts?", "question_ml": "ബാങ്ക് അക്കൗണ്ടിന് പാൻ നിർബന്ധമാണോ?", "answer_en": "Yes, required for major financial transactions.", "answer_ml": "അതെ, വലിയ തുകകളുടെ ഇടപാടുകൾക്ക് പാൻ കാർഡ് നിർബന്ധമാണ്."}
            ]
        },
        # 6. Passport
        {
            "slug": "passport",
            "category": "External Affairs / Passport Seva",
            "name_en": "Passport Application",
            "name_ml": "പാസ്‌പോർട്ട് അപേക്ഷ",
            "description_en": "Application for Fresh or Re-issue of Indian Passport.",
            "description_ml": "ഇന്ത്യൻ പാസ്‌പോർട്ടിനായുള്ള പുതിയ അപേക്ഷ അല്ലെങ്കിൽ പുതുക്കൽ.",
            "eligibility_en": "Indian Citizens.",
            "eligibility_ml": "ഇന്ത്യൻ പൗരന്മാർ.",
            "application_fee": "₹1,500 (Normal 36 pages) / ₹2,000 (60 pages)",
            "processing_time_days": 15,
            "official_website": "https://www.passportindia.gov.in",
            "office_type": "Passport Seva Kendra (PSK)",
            "aliases_manglish": "passport, pass port, passport edukkanam",
            "documents": [
                {"doc_name_en": "Aadhaar Card", "doc_name_ml": "ആധാർ കാർഡ്", "is_mandatory": True},
                {"doc_name_en": "Proof of Birth (SSLC / Birth Cert)", "doc_name_ml": "ജനനത്തീയതി തെളിയിക്കുന്ന രേഖ", "is_mandatory": True},
                {"doc_name_en": "Non-ECR Proof (SSLC Book / Degree)", "doc_name_ml": "Non-ECR രേഖ (SSLC / ഡിഗ്രി സർട്ടിഫിക്കറ്റ്)", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Register on Passport Seva", "title_ml": "പാസ്‌പോർട്ട് സേവയിൽ രജിസ്റ്റർ ചെയ്യുക", "description_en": "Create user login on passportindia.gov.in.", "description_ml": "passportindia.gov.in ൽ ലോഗിൻ സൃഷ്ടിക്കുക."},
                {"step_number": 2, "title_en": "Pay Fee & Schedule PSK Appointment", "title_ml": "ഫീസ് അടച്ച് PSK അപ്പോയിന്റ്മെന്റ് എടുക്കുക", "description_en": "Pay ₹1500 online and choose date for PSK document verification.", "description_ml": "ഫീസ് അടച്ച് സമീപത്തെ പാസ്‌പോർട്ട് സേവാ കേന്ദ്രത്തിലേക്ക് അപ്പോയിന്റ്മെന്റ് ബുക്ക് ചെയ്യുക."}
            ],
            "faqs": [
                {"question_en": "How long is passport valid?", "question_ml": "പാസ്‌പോർട്ട് കാലാവധി എത്രയാണ്?", "answer_en": "Valid for 10 years for adults.", "answer_ml": "മുതിർന്നവർക്ക് 10 വർഷം കാലാവധിയുണ്ട്."}
            ]
        },
        # 7. Birth Certificate
        {
            "slug": "birth-certificate",
            "category": "Local Self Government / Civil Registration",
            "name_en": "Birth Certificate",
            "name_ml": "ജനന സർട്ടിഫിക്കറ്റ്",
            "description_en": "Registration and certificate issuance for births in Kerala.",
            "description_ml": "കേരളത്തിൽ നടക്കുന്ന ജനനങ്ങളുടെ രജിസ്ട്രേഷനും സർട്ടിഫിക്കറ്റും.",
            "eligibility_en": "Birth occurred in Kerala Panchayat/Municipality/Corporation.",
            "eligibility_ml": "കേരളത്തിലെ പഞ്ചായത്ത്/മുൻസിപ്പാലിറ്റി/കോർപ്പറേഷൻ പരിധിയിൽ ജനനം നടന്നവർ.",
            "application_fee": "₹20 - ₹100",
            "processing_time_days": 5,
            "official_website": "https://cr.lsgkerala.gov.in",
            "office_type": "Panchayat / Municipality Office / Sevana",
            "aliases_manglish": "birth certificate, janana certificate, birth cert",
            "documents": [
                {"doc_name_en": "Hospital Birth Report Form", "doc_name_ml": "ആശുപത്രിയിൽ നിന്നുള്ള ജനന റിപ്പോർട്ട് ഫോറം", "is_mandatory": True},
                {"doc_name_en": "Parents Aadhaar Cards", "doc_name_ml": "മാതാപിതാക്കളുടെ ആധാർ കാർഡുകൾ", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Check Sevana Portal", "title_ml": "സേവന പോർട്ടൽ പരിശോധിക്കുക", "description_en": "Search record on cr.lsgkerala.gov.in using hospital details.", "description_ml": "cr.lsgkerala.gov.in ൽ ആശുപത്രി വിവരങ്ങൾ നൽകി സെർച്ച് ചെയ്യുക."}
            ],
            "faqs": [
                {"question_en": "Is child name mandatory at registration?", "question_ml": "രജിസ്ട്രേഷൻ സമയത്ത് കുട്ടിയുടെ പേര് നിർബന്ധമാണോ?", "answer_en": "No, child name can be added within 1 year.", "answer_ml": "അല്ല, ജനനം രജിസ്റ്റർ ചെയ്ത ശേഷം 1 വർഷത്തിനുള്ളിൽ പേര് ചേർക്കാം."}
            ]
        },
        # 8. Death Certificate
        {
            "slug": "death-certificate",
            "category": "Local Self Government / Sevana",
            "name_en": "Death Certificate",
            "name_ml": "മരണ സർട്ടിഫിക്കറ്റ്",
            "description_en": "Registration and issuance of Death Certificate in Kerala.",
            "description_ml": "കേരളത്തിൽ നടക്കുന്ന മരണങ്ങൾ രജിസ്റ്റർ ചെയ്യുന്നതിനുള്ള സേവനം.",
            "eligibility_en": "Legal heir / relative of deceased person.",
            "eligibility_ml": "മരിച്ച വ്യക്തിയുടെ നിയമപരമായ അവകാശികൾ.",
            "application_fee": "₹20",
            "processing_time_days": 5,
            "official_website": "https://cr.lsgkerala.gov.in",
            "office_type": "Panchayat / Municipality",
            "aliases_manglish": "death certificate, marana certificate",
            "documents": [
                {"doc_name_en": "Hospital Death Intimation Form", "doc_name_ml": "ആശുപത്രിയിൽ നിന്നുള്ള മരണം സ്ഥിരീകരിക്കുന്ന ഫോറം", "is_mandatory": True},
                {"doc_name_en": "Aadhaar Card of Deceased", "doc_name_ml": "മരിച്ച വ്യക്തിയുടെ ആധാർ കാർഡ്", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Submit Report to LSG Secretary", "title_ml": "പഞ്ചായത്ത് സെക്രട്ടറിക്കും റിപ്പോർട്ട് നൽകുക", "description_en": "Hospital submits Form 2 directly to Panchayat.", "description_ml": "ആശുപത്രി ഫോറം 2 നേരിട്ട് തദ്ദേശ സ്ഥാപനത്തിലേക്ക് അയക്കും."}
            ],
            "faqs": [
                {"question_en": "Within how many days should death be reported?", "question_ml": "മരണം എത്ര ദിവസത്തിനുള്ളിൽ റിപ്പോർട്ട് ചെയ്യണം?", "answer_en": "Within 21 days for free registration.", "answer_ml": "21 ദിവസത്തിനുള്ളിൽ റിപ്പോർട്ട് ചെയ്താൽ സൗജന്യമാണ്."}
            ]
        },
        # 9. Income Certificate
        {
            "slug": "income-certificate",
            "category": "Revenue Department / e-District",
            "name_en": "Income Certificate",
            "name_ml": "വരുമാന സർട്ടിഫിക്കറ്റ്",
            "description_en": "Official certificate confirming annual family income in Kerala.",
            "description_ml": "കുടുംബത്തിന്റെ വാർഷിക വരുമാനം തെളിയിക്കുന്ന വില്ലേജ് ഓഫീസർ നൽകുന്ന സർട്ടിഫിക്കറ്റ്.",
            "eligibility_en": "Kerala residents for educational, welfare, or loan purposes.",
            "eligibility_ml": "കേരളത്തിലെ സ്ഥിരതാമസക്കാരായ പൗരന്മാർ.",
            "application_fee": "₹28",
            "processing_time_days": 7,
            "official_website": "https://edistrict.kerala.gov.in",
            "office_type": "Village Office / Akshaya",
            "aliases_manglish": "income certificate, varamana certificate, income cert",
            "documents": [
                {"doc_name_en": "Ration Card", "doc_name_ml": "റേഷൻ കാർഡ്", "is_mandatory": True},
                {"doc_name_en": "Aadhaar Card", "doc_name_ml": "ആധാർ കാർഡ്", "is_mandatory": True},
                {"doc_name_en": "Salary Slip / Land Tax Receipt", "doc_name_ml": "ശമ്പള സർട്ടിഫിക്കറ്റ് / കരം ഒടുക്കിയ രസീത്", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "e-District Portal Application", "title_ml": "ഇ-ഡിസ്ട്രിക്ട് അപേക്ഷ", "description_en": "Apply via Akshaya or direct e-District citizen login.", "description_ml": "അക്ഷയ കേന്ദ്രം വഴിയോ e-District ലോഗിൻ വഴിയോ അപേക്ഷിക്കുക."}
            ],
            "faqs": [
                {"question_en": "What is the validity of Income Certificate?", "question_ml": "വരുമാന സർട്ടിഫിക്കറ്റിന്റെ കാലാവധി എത്രയാണ്?", "answer_en": "Valid for 1 year from issuance date.", "answer_ml": "നൽകുന്ന തിയ്യതി മുതൽ 1 വർഷമാണ് കാലാവധി."}
            ]
        },
        # 10. Community Certificate
        {
            "slug": "community-certificate",
            "category": "Revenue Department / e-District",
            "name_en": "Community Certificate",
            "name_ml": "ജാതി സർട്ടിഫിക്കറ്റ്",
            "description_en": "Caste / Community certification for reservations and scholarships.",
            "description_ml": "സംവരണത്തിനും സ്കോളർഷിപ്പിനുമുള്ള ജാതി സർട്ടിഫിക്കറ്റ്.",
            "eligibility_en": "Members of SC/ST/OBC/OEC communities in Kerala.",
            "eligibility_ml": "കേരളത്തിലെ SC/ST/OBC/OEC വിഭാഗങ്ങളിൽപെട്ടവർ.",
            "application_fee": "₹28",
            "processing_time_days": 7,
            "official_website": "https://edistrict.kerala.gov.in",
            "office_type": "Village Office / Akshaya",
            "aliases_manglish": "community certificate, jaathi certificate, caste cert",
            "documents": [
                {"doc_name_en": "SSLC Book showing Caste", "doc_name_ml": "ജാതി രേഖപ്പെടുത്തിയ SSLC ബുക്ക്", "is_mandatory": True},
                {"doc_name_en": "Aadhaar Card", "doc_name_ml": "ആധാർ കാർഡ്", "is_mandatory": True},
                {"doc_name_en": "Ration Card", "doc_name_ml": "റേഷൻ കാർഡ്", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Submit Application at Village Office", "title_ml": "വില്ലേജ് ഓഫീസിൽ അപേക്ഷ സമർപ്പിക്കുക", "description_en": "Apply through e-District portal or Akshaya.", "description_ml": "ഇ-ഡിസ്ട്രിക്ട് പോർട്ടൽ വഴി ഓൺലൈനായി അപേക്ഷിക്കുക."}
            ],
            "faqs": [
                {"question_en": "Is Community Certificate valid for life?", "question_ml": "ജാതി സർട്ടിഫിക്കറ്റിന് ആജീവനാന്ത കാലാവധിയുണ്ടോ?", "answer_en": "Valid for 3 years for OBC/OEC (Lifetime for SC/ST in most cases).", "answer_ml": "OBC വിഭാഗങ്ങൾക്ക് 3 വർഷം കാലാവധിയുണ്ട്."}
            ]
        },
        # 11. Residence Certificate
        {
            "slug": "residence-certificate",
            "category": "Revenue Department / e-District",
            "name_en": "Residence Certificate",
            "name_ml": "താമസ സർട്ടിഫിക്കറ്റ്",
            "description_en": "Proof of residential address issued by local Village Office or LSG.",
            "description_ml": "സ്ഥിരതാമസം തെളിയിക്കുന്നതിനായി തദ്ദേശ സ്ഥാപനമോ വില്ലേജ് ഓഫീസോ നൽകുന്ന സർട്ടിഫിക്കറ്റ്.",
            "eligibility_en": "Resident of Kerala.",
            "eligibility_ml": "കേരളത്തിൽ താമസിക്കുന്ന പൗരന്മാർ.",
            "application_fee": "₹28",
            "processing_time_days": 5,
            "official_website": "https://edistrict.kerala.gov.in",
            "office_type": "Village Office / Panchayat",
            "aliases_manglish": "residence certificate, thalamasam certificate, natukaran cert",
            "documents": [
                {"doc_name_en": "Aadhaar Card / Voter ID", "doc_name_ml": "ആധാർ / വോട്ടർ ഐഡി", "is_mandatory": True},
                {"doc_name_en": "Land Tax Receipt / Electricity Bill", "doc_name_ml": "നികുതി രസീത് / കറന്റ് ബിൽ", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Apply via e-District", "title_ml": "ഇ-ഡിസ്ട്രിക്ട് വഴി അപേക്ഷിക്കുക", "description_en": "Upload electricity bill or tax receipt.", "description_ml": "ഇലക്ട്രിസിറ്റി ബില്ലോ നികുതി രസീതോ അപ്‌ലോഡ് ചെയ്യുക."}
            ],
            "faqs": [
                {"question_en": "How long is Natukaran certificate valid?", "question_ml": "താമസ സർട്ടിഫിക്കറ്റിന്റെ കാലാവധി എത്രയാണ്?", "answer_en": "Valid for 1 year.", "answer_ml": "1 വർഷം കാലാവധിയുണ്ട്."}
            ]
        },
        # 12. Ration Card
        {
            "slug": "ration-card",
            "category": "Civil Supplies Department",
            "name_en": "Ration Card Application / Correction",
            "name_ml": "റേഷൻ കാർഡ് അപേക്ഷ / തിരുത്തൽ",
            "description_en": "New Ration Card issuance, member addition/deletion, or card category change.",
            "description_ml": "പുതിയ റേഷൻ കാർഡ്, അംഗങ്ങളെ ചേർക്കൽ/ഒഴിവാക്കൽ, തിരുത്തലുകൾ.",
            "eligibility_en": "Kerala families without duplicate ration card.",
            "eligibility_ml": "കേരളത്തിലെ കുടുംബങ്ങൾ.",
            "application_fee": "₹50",
            "processing_time_days": 15,
            "official_website": "https://ecitizen.civilsupplieskerala.gov.in",
            "office_type": "Taluk Supply Office (TSO) / Akshaya",
            "aliases_manglish": "ration card, ration card maattanum, member serkkanam",
            "documents": [
                {"doc_name_en": "Aadhaar Cards of All Family Members", "doc_name_ml": "എല്ലാ കുടുംബാംഗങ്ങളുടെയും ആധാർ കാർഡുകൾ", "is_mandatory": True},
                {"doc_name_en": "Electricity Bill / House Tax Receipt", "doc_name_ml": "കറന്റ് ബിൽ / കെട്ടിട നികുതി രസീത്", "is_mandatory": True},
                {"doc_name_en": "Surrender Certificate (if moving from another card)", "doc_name_ml": "റദ്ദാക്കൽ സർട്ടിഫിക്കറ്റ് (മറ്റൊരു കാർഡിൽ ഉണ്ടെങ്കിൽ)", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Visit Civil Supplies Portal", "title_ml": "സിവിൽ സപ്ലൈസ് പോർട്ടൽ സന്ദർശിക്കുക", "description_en": "Create citizen account on ecitizen portal.", "description_ml": "ecitizen പോർട്ടലിൽ അക്കൗണ്ട് തുടങ്ങി അപേക്ഷിക്കുക."}
            ],
            "faqs": [
                {"question_en": "How to add a newborn child to Ration Card?", "question_ml": "നവജാത ശിശുവിനെ റേഷൻ കാർഡിൽ എങ്ങനെ ചേർക്കാം?", "answer_en": "Apply online with Birth Certificate and child Aadhaar.", "answer_ml": "ജനന സർട്ടിഫിക്കറ്റും ആധാറും ഉപയോഗിച്ച് ഓൺലൈനായി അപേക്ഷിക്കാം."}
            ]
        },
        # 13. Voter ID
        {
            "slug": "voter-id",
            "category": "Election Commission of India",
            "name_en": "Voter ID Card Registration",
            "name_ml": "വോട്ടർ ഐഡി രജിസ്ട്രേഷൻ",
            "description_en": "Enrolment of new voter (Form 6) or correction (Form 8).",
            "description_ml": "പുതിയ വോട്ടർമാർക്കുള്ള രജിസ്ട്രേഷൻ (ഫോറം 6) അല്ലെങ്കിൽ തിരുത്തൽ.",
            "eligibility_en": "Indian Citizens completing age 18.",
            "eligibility_ml": "18 വയസ്സ് പൂർത്തിയായ ഇന്ത്യൻ പൗരന്മാർ.",
            "application_fee": "Free",
            "processing_time_days": 30,
            "official_website": "https://voters.eci.gov.in",
            "office_type": "Online / BLO / Akshaya",
            "aliases_manglish": "voter id, vote card, voter id application",
            "documents": [
                {"doc_name_en": "Passport Size Photograph", "doc_name_ml": "പാസ്‌പോർട്ട് സൈസ് ഫോട്ടോ", "is_mandatory": True},
                {"doc_name_en": "Age Proof (Aadhaar / SSLC)", "doc_name_ml": "വയസ്സ് തെളിയിക്കുന്ന രേഖ", "is_mandatory": True},
                {"doc_name_en": "Address Proof", "doc_name_ml": "മേൽവിലാസം തെളിയിക്കുന്ന രേഖ", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Fill Form 6 Online", "title_ml": "ഫോറം 6 ഓൺലൈനായി പൂരിപ്പിക്കുക", "description_en": "Visit voters.eci.gov.in and fill Form 6.", "description_ml": "voters.eci.gov.in ൽ ഫോറം 6 പൂരിപ്പിക്കുക."}
            ],
            "faqs": [
                {"question_en": "Is Voter ID required for voting?", "question_ml": "വോട്ട് ചെയ്യാൻ വോട്ടർ ഐഡി കാർഡ് വേണമെന്നുണ്ടോ?", "answer_en": "Name must be in electoral roll; any approved photo ID works on polling day.", "answer_ml": "വോട്ടർ പട്ടികയിൽ പേരുണ്ടായാൽ മതിയാകും."}
            ]
        },
        # 14. Pension Schemes
        {
            "slug": "pension-schemes",
            "category": "Social Justice / Sevana Pension",
            "name_en": "Social Security Pension Schemes",
            "name_ml": "സാമൂഹ്യ സുരക്ഷാ പെൻഷനുകൾ",
            "description_en": "Indira Gandhi Old Age Pension, Disability Pension, Agricultural Worker Pension.",
            "description_ml": "വാർദ്ധക്യകാല പെൻഷൻ, ഭിന്നശേഷി പെൻഷൻ, കർഷകത്തൊഴിലാളി പെൻഷനുകൾ.",
            "eligibility_en": "Kerala residents below poverty line (BPL) meeting age criteria.",
            "eligibility_ml": "കേരളത്തിലെ ബി.പി.എൽ (BPL) വിഭാഗത്തിൽപ്പെട്ട പൗരന്മാർ.",
            "application_fee": "Free",
            "processing_time_days": 30,
            "official_website": "https://welfarepension.lsgkerala.gov.in",
            "office_type": "Grama Panchayat / Municipality Office",
            "aliases_manglish": "pension, vayo pension, pension schemes, old age pension",
            "documents": [
                {"doc_name_en": "Aadhaar Card", "doc_name_ml": "ആധാർ കാർഡ്", "is_mandatory": True},
                {"doc_name_en": "BPL Ration Card Copy", "doc_name_ml": "BPL റേഷൻ കാർഡ് കോപ്പി", "is_mandatory": True},
                {"doc_name_en": "Bank Passbook linked to Aadhaar", "doc_name_ml": "ബാങ്ക് പാസ്ബുക്ക് കോപ്പി", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Submit Application at Panchayat", "title_ml": "പഞ്ചായത്തിൽ അപേക്ഷ നൽകുക", "description_en": "Fill prescribed form and submit to local body office.", "description_ml": "നിശ്ചിത ഫോറത്തിൽ ഗ്രാമപഞ്ചായത്തിൽ അപേക്ഷ സമർപ്പിക്കുക."}
            ],
            "faqs": [
                {"question_en": "What is the monthly pension amount?", "question_ml": "പ്രതിമാസ പെൻഷൻ തുക എത്രയാണ്?", "answer_en": "Currently ₹1,600 per month transferred directly to bank account.", "answer_ml": "നിലവിൽ മാസം 1,600 രൂപ ബാങ്ക് അക്കൗണ്ടിലേക്ക് നേരിട്ടെത്തും."}
            ]
        },
        # 15. Welfare Schemes
        {
            "slug": "welfare-schemes",
            "category": "Welfare / Health Department",
            "name_en": "Kerala Welfare & Health Schemes (Karunya / KSRTC Concession)",
            "name_ml": "ക്ഷേമ പദ്ധതികൾ (കാരുണ്യ / KSRTC കൺസെഷൻ)",
            "description_en": "Karunya Benevolent Fund, MEDISEP, and KSRTC Student Concession.",
            "description_ml": "കാരുണ്യ ബെനവലന്റ് ഫണ്ട്, വിദ്യാർത്ഥികൾക്കുള്ള KSRTC യാത്രാ ആനുകൂല്യം.",
            "eligibility_en": "Kerala citizens, BPL patients, and eligible students.",
            "eligibility_ml": "കേരളത്തിലെ നിർദ്ധനരായ രോഗികളും വിദ്യാർത്ഥികളും.",
            "application_fee": "Free",
            "processing_time_days": 15,
            "official_website": "https://sha.kerala.gov.in",
            "office_type": "Government Hospital / KSRTC Depot",
            "aliases_manglish": "ksrtc concession, karunya scheme, medisep, welfare schemes",
            "documents": [
                {"doc_name_en": "Doctor's Medical Certificate & Treatment Estimate", "doc_name_ml": "ഡോക്ടറുടെ സർട്ടിഫിക്കറ്റും ചികിത്സാ എസ്റ്റിമേറ്റും", "is_mandatory": True},
                {"doc_name_en": "Ration Card Copy", "doc_name_ml": "റേഷൻ കാർഡ് കോപ്പി", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Apply at Government Hospital Kiosk", "title_ml": "സർക്കാർ ആശുപത്രി കിയോസ്കിൽ അപേക്ഷിക്കുക", "description_en": "Submit medical estimate to Karunya desk.", "description_ml": "ആശുപത്രിയിലെ കാരുണ്യ ഡെസ്കിൽ രേഖകൾ സമർപ്പിക്കുക."}
            ],
            "faqs": [
                {"question_en": "What is maximum financial assistance in Karunya?", "question_ml": "കാരുണ്യ പദ്ധതിയിലൂടെ പരമാവധി എത്ര തുക ലഭിക്കും?", "answer_en": "Up to ₹2 Lakhs for major critical illnesses.", "answer_ml": "മാരക രോഗങ്ങൾക്ക് പരമാവധി 2 ലക്ഷം രൂപ വരെ ധനസഹായം ലഭിക്കും."}
            ]
        },
        # 16. Vehicle Registration
        {
            "slug": "vehicle-registration",
            "category": "Transport / Motor Vehicles Department",
            "name_en": "New Vehicle Registration",
            "name_ml": "പുതിയ വാഹനം രജിസ്ട്രേഷൻ",
            "description_en": "Registration of newly purchased motor vehicles in Kerala.",
            "description_ml": "പുതായി വാങ്ങിയ വാഹനങ്ങളുടെ മോട്ടോർ വാഹന വകുപ്പ് വഴിയുള്ള രജിസ്ട്രേഷൻ.",
            "eligibility_en": "Owner of new motor vehicle in Kerala.",
            "eligibility_ml": "കേരളത്തിൽ പുതിയ വാഹനം വാങ്ങിയ ഉടമകൾ.",
            "application_fee": "Varies by vehicle class & road tax",
            "processing_time_days": 7,
            "official_website": "https://vahan.parivahan.gov.in",
            "office_type": "Auto Dealer / RTO Office",
            "aliases_manglish": "vehicle registration, vandi registration, new vehicle reg",
            "documents": [
                {"doc_name_en": "Form 20 Application Form", "doc_name_ml": "ഫോറം 20 അപേക്ഷാ ഫോറം", "is_mandatory": True},
                {"doc_name_en": "Sale Certificate (Form 21) & Road Worthiness (Form 22)", "doc_name_ml": "സെയിൽ സർട്ടിഫിക്കറ്റും (Form 21) റോഡ് വർത്തിനസ്സ് ഫോറവും", "is_mandatory": True},
                {"doc_name_en": "Valid Vehicle Insurance Policy", "doc_name_ml": "വാഹന ഇൻഷുറൻസ് പോളിസി", "is_mandatory": True},
                {"doc_name_en": "Address Proof (Aadhaar Card)", "doc_name_ml": "വിലാസം തെളിയിക്കുന്ന രേഖ", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Dealer Point Registration", "title_ml": "ഡീലർ പോയിന്റ് രജിസ്ട്രേഷൻ", "description_en": "Most new vehicle registrations are handled directly at the vehicle dealership via Vahan portal.", "description_ml": "പുതിയ വാഹനങ്ങളുടെ രജിസ്ട്രേഷൻ വഗൻ പോർട്ടൽ വഴി വാഹന ഷോറൂമുകളിൽ തന്ന നിർവ്വഹിക്കാം."}
            ],
            "faqs": [
                {"question_en": "Is physical RTO inspection required?", "question_ml": "വാഹനം RTO ഓഫീസിൽ കൊണ്ടുപോകണമെന്നുണ്ടോ?", "answer_en": "Fully digital dealer registration requires no RTO visit for non-commercial cars/bikes.", "answer_ml": "ഡീലർ രജിസ്ട്രേഷൻ സങ്കേതം ഉള്ളതിനാൽ സാധാരണ വാഹനങ്ങൾ ഓഫീസിൽ എത്തിക്കേണ്ടതില്ല."}
            ]
        },
        # 17. Vehicle Transfer
        {
            "slug": "vehicle-transfer",
            "category": "Transport / Motor Vehicles Department",
            "name_en": "Vehicle Ownership Transfer (RC Transfer)",
            "name_ml": "വാഹന ഉടമസ്ഥാവകാശ മാറ്റം (RC ട്രാൻസ്ഫർ)",
            "description_en": "Transfer of vehicle ownership upon sale or succession.",
            "description_ml": "വാഹനം വിൽപ്പന നടത്തുമ്പോഴുള്ള ഉടമസ്ഥാവകാശ മാറ്റം (RC ട്രാൻസ്ഫർ).",
            "eligibility_en": "Seller and Buyer of registered motor vehicle in Kerala.",
            "eligibility_ml": "വാഹനം വിൽക്കുന്നയാളും വാങ്ങുന്നയാളും.",
            "application_fee": "₹300 - ₹500",
            "processing_time_days": 14,
            "official_website": "https://parivahan.gov.in",
            "office_type": "RTO / Sub RTO",
            "aliases_manglish": "vehicle transfer, vandi maattal, rc transfer, ownership change",
            "documents": [
                {"doc_name_en": "Original Registration Certificate (RC)", "doc_name_ml": "അസ്സൽ ആർ.സി ബുക്ക് (RC)", "is_mandatory": True},
                {"doc_name_en": "Form 29 & Form 30 Notice of Transfer", "doc_name_ml": "ഫോറം 29, ഫോറം 30", "is_mandatory": True},
                {"doc_name_en": "Valid Pollution Under Control (PUC) Certificate", "doc_name_ml": "പുക പരിശോധനാ സർട്ടിഫിക്കറ്റ് (PUC)", "is_mandatory": True},
                {"doc_name_en": "Valid Insurance Policy & Aadhaar of Buyer", "doc_name_ml": "ഇൻഷുറൻസും വാങ്ങുന്നയാളുടെ ആധാറും", "is_mandatory": True}
            ],
            "guides": [
                {"step_number": 1, "title_en": "Apply on Parivahan Vahan Portal", "title_ml": "പരിവാഹനിൽ അപേക്ഷിക്കുക", "description_en": "Select Transfer of Ownership and submit Form 29/30.", "description_ml": "പരിവാഹൻ പോർട്ടലിൽ 'Transfer of Ownership' തിരഞ്ഞെടുത്ത് ഫീസ് അടയ്ക്കുക."}
            ],
            "faqs": [
                {"question_en": "Within how many days should RC transfer be reported?", "question_ml": "വിൽപ്പന കഴിഞ്ഞ് എത്ര ദിവസത്തിനകം ആർ.സി മാറ്റണം?", "answer_en": "Within 14 days if within same RTO, 45 days if outside state.", "answer_ml": "അതേ RTO പരിധിയിലാണെങ്കിൽ 14 ദിവസത്തിനകം അപേക്ഷിക്കണം."}
            ]
        }
    ]

    for data in services_data:
        docs = data.pop("documents", [])
        guides = data.pop("guides", [])
        faqs = data.pop("faqs", [])

        service = Service(**data)
        db.add(service)
        db.flush()

        for d in docs:
            db.add(ServiceDocument(service_id=service.id, **d))
        for g in guides:
            db.add(ServiceGuide(service_id=service.id, **g))
        for f in faqs:
            db.add(ServiceFAQ(service_id=service.id, **f))

    db.commit()
    print(f"Successfully seeded database with {len(services_data)} government services!")
    db.close()

if __name__ == "__main__":
    seed_database()
