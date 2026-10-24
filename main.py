from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Syringe - سرنجة")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# بيانات المدير ورقم الهاتف الخاص بك
# ==========================================
ADMIN_USER = "ahmed"
ADMIN_PASS = "syringe2026"
ADMIN_PHONE = "01111727081"

# 1. الصفحة الرئيسية الترويجية
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>سرنجة - منصة الخدمات التمريضية المنزلية</title>
        <style>
            body { 
                font-family: Tahoma, sans-serif; background-color: #1e2229; margin: 0; padding: 0; 
                direction: rtl; text-align: right; color: #fff; min-height: 100vh; display: flex; 
                flex-direction: column; justify-content: space-between; position: relative;
            }
            body::before {
                content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(rgba(26, 30, 36, 0.8), rgba(26, 30, 36, 0.85)), 
                            url('https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=1920&q=80') no-repeat center center fixed;
                background-size: cover; z-index: -1;
            }
            header { padding: 25px 50px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); }
            
            /* تكبير ووضوح اسم المنصة (الشعار) ليصبح بارزاً جداً وجذاباً */
            .logo { font-size: 38px; font-weight: bold; color: #4dabf7; text-shadow: 0 3px 6px rgba(0,0,0,0.7); letter-spacing: 1px; }
            
            .hero { max-width: 900px; margin: auto; text-align: center; padding: 60px 20px; }
            .hero h1 { font-size: 46px; color: #74c0fc; margin-bottom: 20px; line-height: 1.3; font-weight: bold; }
            .hero p { font-size: 20px; color: #ced4da; margin-bottom: 45px; line-height: 1.6; }
            .cta-buttons { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 20px; }
            .btn-primary { background-color: #2b8a3e; color: white; padding: 18px 35px; text-decoration: none; border-radius: 40px; font-weight: bold; font-size: 18px; border: 2px solid #40c057; transition: 0.3s; }
            .btn-primary:hover { background-color: #2f9e44; transform: scale(1.05); }
            .btn-secondary { background-color: #1c7ed6; color: white; padding: 18px 35px; text-decoration: none; border-radius: 40px; font-weight: bold; font-size: 18px; border: 2px solid #339af0; transition: 0.3s; }
            .btn-secondary:hover { background-color: #1971c2; transform: scale(1.05); }
            .btn-accent { background-color: #f59f00; color: white; padding: 18px 35px; text-decoration: none; border-radius: 40px; font-weight: bold; font-size: 18px; border: 2px solid #fcc419; transition: 0.3s; }
            .btn-accent:hover { background-color: #f08c00; transform: scale(1.05); }
            .features { display: flex; justify-content: center; gap: 30px; padding: 40px 20px; max-width: 1000px; margin: auto; flex-wrap: wrap; }
            .feature-card { background: rgba(30, 35, 45, 0.85); border: 1px solid rgba(255,255,255,0.15); padding: 25px; border-radius: 15px; width: 260px; text-align: center; }
            .feature-card h3 { color: #4dabf7; margin-bottom: 10px; font-size: 20px; }
            .feature-card p { color: #adb5bd; font-size: 15px; line-height: 1.5; }
            footer { text-align: center; padding: 20px; color: #6c757d; border-top: 1px solid rgba(255,255,255,0.05); font-size: 14px; }
        </style>
    </head>
    <body>
        <header>
            <div class="logo">سرنجة 🩺</div>
            <div>
                <a href="/nurse_portal" style="color: #4dabf7; text-decoration: none; margin-left: 20px; font-weight: bold; font-size: 16px;">بوابة الممرضين 📋</a>
                <a href="/login" style="color: #adb5bd; text-decoration: none; margin-left: 20px; font-weight: bold; font-size: 16px;">لوحة التحكم 🔒</a>
            </div>
        </header>
        <div class="hero">
            <h1>رعاية صحية منزلية احترافية، بين إيديك في أي وقت 🏥</h1>
            <p>منصة "سرنجة" تربط المرضى بأقوى طاقم تمريض معتمد ومحترف للخدمات الطبية المنزلية بسرعة وأمان تام.</p>
            <div class="cta-buttons">
                <a href="/create_request_page" class="btn-primary">اطلب خدمة منزلية الآن 📋</a>
                <a href="/register_nurse_page" class="btn-secondary">انضم كـ ممرض معتمد 🩺</a>
                <a href="/nurse_portal" class="btn-accent">تصفح الطلبات المتاحة للممرضين 🚀</a>
            </div>
        </div>
        <div class="features">
            <div class="feature-card"><h3>سرعة استجابة ⚡</h3><p>توصيل سريع للحالات الطارئة والخدمات المنزلية.</p></div>
            <div class="feature-card"><h3>طاقم معتمد 👨‍⚕️</h3><p>ممرضون محترفون ومقيدون بنقابة التمريض.</p></div>
            <div class="feature-card"><h3>تقييم ومتابعة ⭐</h3><p>نظام تقييم دقيق لضمان جودة الخدمة.</p></div>
        </div>
        <footer>جميع الحقوق محفوظة لمنصة سرنجة الطبية © 2026</footer>
    </body>
    </html>
    """

# 2. صفحة تسجيل دخول المدير
@app.get("/login", response_class=HTMLResponse)
def login_page(error: str = ""):
    err_msg = "<p style='color: #ff6b6b; font-size: 13px; margin-bottom: 10px;'>اسم المستخدم أو كلمة المرور غير صحيحة!</p>" if error else ""
    return f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>تسجيل دخول المدير</title>
        <style>
            body {{ font-family: Tahoma; background-color: #1e2229; color: #fff; padding: 40px; direction: rtl; text-align: right; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .container {{ width: 100%; max-width: 400px; background: rgba(30, 35, 45, 0.9); padding: 35px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.15); text-align: center; }}
            h2 {{ color: #74c0fc; margin-bottom: 20px; }}
            input {{ width: 100%; padding: 12px; margin: 10px 0; background: rgba(44, 49, 58, 0.9); border: 1px solid #495057; color: #fff; border-radius: 8px; box-sizing: border-box; }}
            button {{ background-color: #2b8a3e; color: white; padding: 12px; border: none; border-radius: 8px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; margin-top: 10px; }}
            .links {{ display: flex; justify-content: space-between; margin-top: 15px; font-size: 13px; }}
            .links a {{ color: #4dabf7; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>لوحة تحكم المدير 🔒</h2>
            {err_msg}
            <form action="/login" method="post">
                <input type="text" name="username" placeholder="اسم المستخدم" required>
                <input type="password" name="password" placeholder="كلمة المرور" required>
                <button type="submit">دخول للوحة التحكم</button>
            </form>
            <div class="links">
                <a href="/forgot_password">نسيت كلمة السر؟</a>
                <a href="/">← الرئيسية</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    global ADMIN_USER, ADMIN_PASS
    if username == ADMIN_USER and password == ADMIN_PASS:
        response = RedirectResponse(url="/requests", status_code=303)
        response.set_cookie(key="is_admin", value="true")
        return response
    return RedirectResponse(url="/login?error=1", status_code=303)

# 3. استعادة كلمة المرور
@app.get("/forgot_password", response_class=HTMLResponse)
def forgot_password_page(msg: str = "", sent: str = ""):
    feedback = f"<p style='color: #51cf66; font-size: 13px; margin-bottom: 10px;'>{msg}</p>" if msg else ""
    notice = "<div style='background: rgba(24, 100, 50, 0.4); border: 1px solid #40c057; padding: 10px; border-radius: 8px; margin-bottom: 15px; font-size: 13px; color: #51cf66;'>تم التحقق وتحديث كلمة المرور بنجاح!</div>" if sent == "1" else ""
    return f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>تغيير كلمة المرور</title>
        <style>
            body {{ font-family: Tahoma; background-color: #1e2229; color: #fff; padding: 40px; direction: rtl; text-align: right; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .container {{ width: 100%; max-width: 420px; background: rgba(30, 35, 45, 0.9); padding: 35px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.15); text-align: center; }}
            h2 {{ color: #74c0fc; margin-bottom: 15px; }}
            p.desc {{ font-size: 13px; color: #adb5bd; margin-bottom: 20px; }}
            .input-group {{ position: relative; margin: 10px 0; }}
            .input-group input {{ width: 100%; padding: 12px; background: rgba(44, 49, 58, 0.9); border: 1px solid #495057; color: #fff; border-radius: 8px; box-sizing: border-box; }}
            .eye-btn {{ position: absolute; left: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; color: #adb5bd; cursor: pointer; font-size: 14px; }}
            button.submit-btn {{ background-color: #1c7ed6; color: white; padding: 12px; border: none; border-radius: 8px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; margin-top: 10px; }}
            .back-btn {{ display: inline-block; margin-top: 15px; color: #adb5bd; text-decoration: none; font-size: 14px; }}
        </style>
        <script>
            function togglePassword() {{
                var passInput = document.getElementById("new_password");
                var eyeBtn = document.getElementById("eyeBtn");
                if (passInput.type === "password") {{ passInput.type = "text"; eyeBtn.textContent = "🙈 إخفاء"; }}
                else {{ passInput.type = "password"; eyeBtn.textContent = "👁️ عرض"; }}
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <h2>إعادة تعيين كلمة المرور 📱</h2>
            <p class="desc">أدخل رقم هاتفك المسجل وكلمة المرور الجديدة لتحديثها.</p>
            {feedback} {notice}
            <form action="/send_confirmation" method="post">
                <div class="input-group"><input type="password" name="phone" placeholder="أدخل رقم الهاتف المسجل" required></div>
                <div class="input-group">
                    <input type="password" id="new_password" name="new_password" placeholder="كلمة المرور الجديدة" required>
                    <button type="button" id="eyeBtn" class="eye-btn" onclick="togglePassword()">👁️ عرض</button>
                </div>
                <button type="submit" class="submit-btn">تحديث كلمة المرور</button>
            </form>
            <a href="/login" class="back-btn">← العودة لتسجيل الدخول</a>
        </div>
    </body>
    </html>
    """

@app.post("/send_confirmation")
def send_confirmation(phone: str = Form(...), new_password: str = Form(...)):
    global ADMIN_PASS, ADMIN_PHONE
    if phone.strip() == ADMIN_PHONE:
        ADMIN_PASS = new_password
        return RedirectResponse(url="/forgot_password?sent=1&msg=تم تغيير كلمة المرور بنجاح!", status_code=303)
    return RedirectResponse(url="/forgot_password?msg=رقم الهاتف غير صحيح!", status_code=303)

# 4. لوحة التحكم الإدارية
@app.get("/requests", response_class=HTMLResponse)
def view_requests(request: Request, search: str = "", db: Session = Depends(get_db)):
    is_admin = request.cookies.get("is_admin")
    if not is_admin:
        return RedirectResponse(url="/login", status_code=303)
    query = db.query(models.NursingRequest)
    if search:
        query = query.filter((models.NursingRequest.patient_name.contains(search)) | (models.NursingRequest.service_type.contains(search)) | (models.NursingRequest.address.contains(search)))
    requests_list = query.all()
    nurses = db.query(models.Nurse).all()
    
    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>طلبات المرضى</title>
        <style>
            body {{ font-family: Tahoma; background-color: #1e2229; color: #fff; padding: 40px; direction: rtl; text-align: right; }}
            .container {{ max-width: 1000px; margin: auto; background: rgba(30, 35, 45, 0.85); padding: 35px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.15); }}
            h2 {{ color: #74c0fc; text-align: center; }}
            .search-box {{ margin: 20px 0; display: flex; gap: 10px; }}
            .search-box input {{ flex: 1; padding: 10px; background: rgba(44, 49, 58, 0.9); border: 1px solid #495057; color: #fff; border-radius: 8px; }}
            .search-box button {{ padding: 10px 20px; background: #2b8a3e; color: white; border: none; border-radius: 8px; cursor: pointer; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th, td {{ border: 1px solid #495057; padding: 10px; text-align: center; color: #fff; font-size: 13px; }}
            th {{ background-color: #1c7ed6; color: white; }}
            select, input[type="text"] {{ padding: 5px; background: #2c313a; color: #fff; border: 1px solid #495057; border-radius: 4px; }}
            .action-btn {{ background-color: #2b8a3e; color: white; padding: 5px 10px; border: none; border-radius: 4px; font-size: 12px; font-weight: bold; cursor: pointer; }}
            .nav-buttons {{ display: flex; justify-content: space-between; margin-bottom: 20px; }}
            .back-btn, .logout-btn {{ padding: 8px 15px; color: white; text-decoration: none; border-radius: 8px; }}
            .back-btn {{ background: #495057; }} .logout-btn {{ background: #c92a2a; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav-buttons">
                <a href="/" class="back-btn">← العودة للرئيسية</a>
                <a href="/login" class="logout-btn" onclick="document.cookie='is_admin=; Max-Age=0';">تسجيل خروج 🔓</a>
            </div>
            <h2>لوحة تحكم المدير - طلبات الخدمة 📋</h2>
            <form method="get" action="/requests" class="search-box">
                <input type="text" name="search" value="{search}" placeholder="ابحث باسم المريض، الخدمة، أو العنوان...">
                <button type="submit">بحث</button>
            </form>
            <table>
                <tr><th>اسم المريض</th><th>نوع الخدمة</th><th>العنوان</th><th>رقم التواصل</th><th>الممرض المسؤول</th><th>التقييم ⭐</th><th>الحالة</th><th>إجراء</th></tr>
    """
    for r in requests_list:
        if r.status == "Completed":
            nurse_display = f"<span style='color: #74c0fc; font-weight: bold;'>{r.assigned_nurse or 'غير محدد'}</span>"
            rating_display = f"<span style='color: #fcc419; font-weight: bold;'>{r.rating or '⭐ ممتاز'}</span>"
            action_btn = "<span style='color: #adb5bd;'>منتهي ✓</span>"
        else:
            nurse_options = "".join([f"<option value='{n.name}'>{n.name}</option>" for n in nurses])
            action_btn = f"""
            <form action="/complete_request/{r.id}" method="post" style="display:flex; gap:4px; justify-content:center; align-items:center; flex-wrap:wrap;">
                <select name="assigned_nurse" required style="font-size:11px;"><option value="">اختر الممرض</option>{nurse_options}</select>
                <select name="rating" style="font-size:11px;"><option value="⭐⭐⭐⭐⭐ ممتاز">⭐⭐⭐⭐⭐ ممتاز</option><option value="⭐⭐⭐⭐ جيد جداً">⭐⭐⭐⭐ جيد جداً</option></select>
                <button type="submit" class="action-btn">إنهاء</button>
            </form>
            """
            nurse_display = f"<span style='color: #ffa94d;'>{r.assigned_nurse or 'قيد الانتظار'}</span>"
            rating_display = "<span style='color: #adb5bd;'>قيد الانتظار</span>"
        html += f"<tr><td>{r.patient_name}</td><td>{r.service_type}</td><td>{r.address}</td><td>{r.phone}</td><td>{nurse_display}</td><td>{rating_display}</td><td>{'<span style=\"color: #51cf66; font-weight: bold;\">تم التنفيذ</span>' if r.status == 'Completed' else '<span style=\"color: #ffa94d;\">قيد الانتظار</span>'}</td><td>{action_btn}</td></tr>"
    html += "</table></div></body></html>"
    return html

# 5. بوابة الممرضين التفاعلية
@app.get("/nurse_portal", response_class=HTMLResponse)
def nurse_portal(db: Session = Depends(get_db)):
    requests_list = db.query(models.NursingRequest).all()
    nurses = db.query(models.Nurse).all()
    
    nurses_options_html = "".join([f"<option value='{n.name}'>{n.name} ({n.area})</option>" for n in nurses])
    
    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>بوابة الممرضين - طلبات الحالات</title>
        <style>
            body {{ font-family: Tahoma; background-color: #1e2229; color: #fff; padding: 40px; direction: rtl; text-align: right; }}
            .container {{ max-width: 1000px; margin: auto; background: rgba(30, 35, 45, 0.9); padding: 35px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            h2 {{ color: #74c0fc; text-align: center; margin-bottom: 10px; }}
            p.sub {{ text-align: center; color: #adb5bd; margin-bottom: 25px; font-size: 15px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th, td {{ border: 1px solid #495057; padding: 12px; text-align: center; color: #fff; font-size: 14px; }}
            th {{ background-color: #2b8a3e; color: white; }}
            select {{ padding: 8px; background: #2c313a; color: #fff; border: 1px solid #495057; border-radius: 6px; font-size: 13px; }}
            .accept-btn {{ background-color: #2b8a3e; color: white; padding: 8px 16px; border: none; border-radius: 6px; font-size: 13px; font-weight: bold; cursor: pointer; transition: 0.3s; }}
            .accept-btn:hover {{ background-color: #2f9e44; transform: scale(1.05); }}
            .back-btn {{ display: inline-block; margin-bottom: 20px; padding: 8px 15px; background: #495057; color: white; text-decoration: none; border-radius: 8px; }}
            .taken-badge {{ color: #74c0fc; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← العودة للرئيسية</a>
            <h2>بوابة الممرضين - طلبات الحالات المتاحة 🩺📋</h2>
            <p class="sub">اختر اسمك من القائمة واضغط على "قبول الطلب" لتأكيد استلاستلام الحالة ومباشرتها فوراً.</p>
            <table>
                <tr><th>اسم المريض</th><th>نوع الخدمة المطلوبة</th><th>العنوان بالتفصيل</th><th>رقم التواصل</th><th>الممرض المسؤول</th><th>إجراء (قبول الطلب)</th></tr>
    """
    
    for r in requests_list:
        if r.assigned_nurse:
            action_cell = f"<span class='taken-badge'>تم قبولها بواسطة ({r.assigned_nurse}) ✓</span>"
            nurse_cell = f"<span style='color: #51cf66; font-weight: bold;'>{r.assigned_nurse}</span>"
        else:
            if nurses:
                action_cell = f"""
                <form action="/accept_request/{r.id}" method="post" style="display:flex; gap:6px; justify-content:center; align-items:center;">
                    <select name="nurse_name" required>
                        <option value="">اختر اسمك (الممرض)</option>
                        {nurses_options_html}
                    </select>
                    <button type="submit" class="accept-btn">قبول الطلب 🤝</button>
                </form>
                """
            else:
                action_cell = "<span style='color: #ff6b6b;'>لا يوجد ممرضين مسجلين بعد</span>"
            nurse_cell = "<span style='color: #ffa94d;'>قيد الانتظار</span>"

        html += f"<tr><td>{r.patient_name}</td><td>{r.service_type}</td><td>{r.address}</td><td>{r.phone}</td><td>{nurse_cell}</td><td>{action_cell}</td></tr>"
        
    html += "</table></div></body></html>"
    return html

# 6. مسار قبول الطلب بواسطة الممرض
@app.post("/accept_request/{request_id}")
def accept_request(request_id: int, nurse_name: str = Form(...), db: Session = Depends(get_db)):
    req = db.query(models.NursingRequest).filter(models.NursingRequest.id == request_id).first()
    if req:
        req.assigned_nurse = nurse_name
        db.commit()
    return RedirectResponse(url="/nurse_portal", status_code=303)

# 7. صفحة طلب الخدمة للمريض
@app.get("/create_request_page", response_class=HTMLResponse)
def create_request_page():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>طلب خدمة</title>
        <style>
            body { font-family: Tahoma; background-color: #1e2229; color: #fff; padding: 40px; direction: rtl; text-align: right; }
            .container { max-width: 600px; margin: auto; background: rgba(30, 35, 45, 0.85); padding: 35px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.15); }
            h2 { color: #74c0fc; text-align: center; }
            input { width: 100%; padding: 12px; margin: 10px 0; background: rgba(44, 49, 58, 0.9); border: 1px solid #495057; color: #fff; border-radius: 8px; box-sizing: border-box; }
            button { background-color: #2b8a3e; color: white; padding: 12px; border: none; border-radius: 8px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
            .back-btn { display: inline-block; margin-bottom: 20px; padding: 8px 15px; background: #495057; color: white; text-decoration: none; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← العودة للرئيسية</a>
            <h2>طلب خدمة تمريضية للمريض 📋</h2>
            <form action="/create_request" method="post">
                <input type="text" name="patient_name" placeholder="اسم المريض" required>
                <input type="text" name="service_type" placeholder="نوع الخدمة (حقنة، تركيب كانيولا...)" required>
                <input type="text" name="address" placeholder="العنوان بالتفصيل" required>
                <input type="text" name="phone" placeholder="رقم التواصل" required>
                <button type="submit">إرسال الطلب</button>
            </form>
        </div>
    </body>
    </html>
    """

# 8. حفظ طلب الخدمة
@app.post("/create_request")
def create_request(patient_name: str = Form(...), service_type: str = Form(...), address: str = Form(...), phone: str = Form(...), db: Session = Depends(get_db)):
    db_request = models.NursingRequest(
        patient_name=patient_name,
        service_type=service_type,
        address=address,
        phone=phone,
        status="Pending",
        assigned_nurse="",
        rating=""
    )
    db.add(db_request)
    db.commit()
    return RedirectResponse(url="/nurse_portal", status_code=303)

# 9. تسجيل ممرض جديد
@app.get("/register_nurse_page", response_class=HTMLResponse)
def register_nurse_page():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>تسجيل ممرض</title>
        <style>
            body { font-family: Tahoma; background-color: #1e2229; color: #fff; padding: 40px; direction: rtl; text-align: right; }
            .container { max-width: 600px; margin: auto; background: rgba(30, 35, 45, 0.85); padding: 35px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.15); }
            h2 { color: #74c0fc; text-align: center; }
            input { width: 100%; padding: 12px; margin: 10px 0; background: rgba(44, 49, 58, 0.9); border: 1px solid #495057; color: #fff; border-radius: 8px; box-sizing: border-box; }
            button { background-color: #1c7ed6; color: white; padding: 12px; border: none; border-radius: 8px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
            .back-btn { display: inline-block; margin-bottom: 20px; padding: 8px 15px; background: #495057; color: white; text-decoration: none; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← العودة للرئيسية</a>
            <h2>تسجيل ممرض جديد 🩺</h2>
            <form action="/register_nurse" method="post">
                <input type="text" name="name" placeholder="اسم الممرض" required>
                <input type="text" name="syndicate_id" placeholder="رقم كارنيه النقابة" required>
                <input type="text" name="phone" placeholder="رقم الهاتف" required>
                <input type="text" name="area" placeholder="المنطقة / الإدارة التابع لها" required>
                <button type="submit">إتمام التسجيل</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/register_nurse")
def register_nurse(name: str = Form(...), syndicate_id: str = Form(...), phone: str = Form(...), area: str = Form(...), db: Session = Depends(get_db)):
    db_nurse = models.Nurse(name=name, syndicate_id=syndicate_id, phone=phone, area=area, is_verified=True)
    db.add(db_nurse)
    db.commit()
    return RedirectResponse(url="/nurses", status_code=303)

@app.get("/nurses", response_class=HTMLResponse)
def view_nurses(search: str = "", db: Session = Depends(get_db)):
    query = db.query(models.Nurse)
    if search:
        query = query.filter((models.Nurse.name.contains(search)) | (models.Nurse.area.contains(search)))
    nurses = query.all()
    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>الممرضون المسجلون</title>
        <style>
            body {{ font-family: Tahoma; background-color: #1e2229; color: #fff; padding: 40px; direction: rtl; text-align: right; }}
            .container {{ max-width: 800px; margin: auto; background: rgba(30, 35, 45, 0.85); padding: 35px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.15); }}
            h2 {{ color: #74c0fc; text-align: center; }}
            .search-box {{ margin: 20px 0; display: flex; gap: 10px; }}
            .search-box input {{ flex: 1; padding: 10px; background: rgba(44, 49, 58, 0.9); border: 1px solid #495057; color: #fff; border-radius: 8px; }}
            .search-box button {{ padding: 10px 20px; background: #1c7ed6; color: white; border: none; border-radius: 8px; cursor: pointer; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th, td {{ border: 1px solid #495057; padding: 12px; text-align: center; color: #fff; }}
            th {{ background-color: #1c7ed6; color: white; }}
            .back-btn {{ display: inline-block; margin-bottom: 20px; padding: 8px 15px; background: #495057; color: white; text-decoration: none; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← العودة للرئيسية</a>
            <h2>قائمة الممرضون المسجلون 🩺</h2>
            <form method="get" action="/nurses" class="search-box">
                <input type="text" name="search" value="{search}" placeholder="ابحث بالاسم أو المنطقة...">
                <button type="submit">بحث</button>
            </form>
            <table>
                <tr><th>الاسم</th><th>رقم النقابة</th><th>الهاتف</th><th>المنطقة</th></tr>
    """
    for n in nurses:
        html += f"<tr><td>{n.name}</td><td>{n.syndicate_id}</td><td>{n.phone}</td><td>{n.area}</td></tr>"
    html += "</table></div></body></html>"
    return html

@app.post("/complete_request/{request_id}")
def complete_request(request_id: int, assigned_nurse: str = Form(...), rating: str = Form(...), db: Session = Depends(get_db)):
    req = db.query(models.NursingRequest).filter(models.NursingRequest.id == request_id).first()
    if req:
        req.status = "Completed"
        req.assigned_nurse = assigned_nurse
        req.rating = rating
        db.commit()
    return RedirectResponse(url="/requests", status_code=303)