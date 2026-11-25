# =============================================================================
# NHOM 8 - DO AN CLICKJACKING - VICTIM SERVER (ShopMart)
# File: victim_server/app.py
# Chay: python3 app.py  (mac dinh port 5000)
# Yeu cau: pip3 install flask
# =============================================================================
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# -----------------------------------------------------------------------
# TRANG THAI PHONG THU TOAN CUC (chi phuc vu DEMO, luu trong RAM server)
# Key tuong ung voi tung thanh vien / tung ky thuat phong chong
# -----------------------------------------------------------------------
defense_state = {
    "huyen": False,   # X-Frame-Options: DENY
    "hang":  False,   # Content-Security-Policy: frame-ancestors 'none'
    "tien":  False,   # Content-Security-Policy: frame-ancestors 'self'
    "hung":  False,   # CSP frame-ancestors 'none' + SameSite=Strict
}

# -----------------------------------------------------------------------
# The second Hang step is a modal; all other action buttons stay in the
# shared ShopMart dashboard layout.
# -----------------------------------------------------------------------
HANG_STEP2 = {"top": 449, "left": 830, "w": 260, "h": 42}

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ShopMart - Trung Tam Quan Ly Tai Khoan &amp; Vi Dien Tu</title>
<style>
  :root {{
    --cam: #ff6a3d;
    --do: #e8392b;
    --xanh: #1fae5e;
    --nen: #f4f6f9;
    --vien: #e3e7ee;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, Arial, sans-serif; }}
  body {{ background: var(--nen); color: #222; }}

  /* ---------- HEADER ---------- */
  header {{
    height: 70px;
    background: linear-gradient(90deg, var(--cam), var(--do));
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 28px;
    color: white;
    box-shadow: 0 2px 10px rgba(0,0,0,.15);
    position: relative; z-index: 5;
  }}
  header .logo {{ font-size: 24px; font-weight: 800; letter-spacing: .5px; }}
  header .logo span {{ font-weight: 400; opacity: .85; font-size: 14px; display:block; }}
  header .user-pill {{
    background: rgba(255,255,255,.18); padding: 8px 16px; border-radius: 30px;
    font-size: 14px; font-weight: 600;
  }}

  /* ---------- SIDEBAR ---------- */
  .sidebar {{
    position: absolute; top: 70px; left: 0; width: 260px; bottom: 0;
    background: #1b2430; color: #cfd8e3; padding: 24px 18px;
  }}
  .sidebar .avatar {{
    width: 72px; height: 72px; border-radius: 50%;
    background: linear-gradient(135deg, var(--cam), var(--do));
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; font-weight: 800; color: white; margin: 0 auto 12px;
  }}
  .sidebar .name {{ text-align: center; font-weight: 700; font-size: 16px; color: #fff; }}
  .sidebar .rank {{ text-align: center; font-size: 12px; color: #ffcf8f; margin-top: 2px; }}
  .sidebar .wallet {{
    margin-top: 22px; background: #263345; border-radius: 12px; padding: 14px; text-align: center;
  }}
  .sidebar .wallet .amount {{ font-size: 22px; font-weight: 800; color: #ffd166; }}
  .sidebar .wallet .label {{ font-size: 12px; opacity: .75; margin-top: 2px; }}
  .sidebar nav {{ margin-top: 26px; }}
  .sidebar nav div {{
    padding: 10px 12px; border-radius: 8px; font-size: 14px; margin-bottom: 6px; opacity: .8;
  }}
  .sidebar nav div.active {{ background: #30405a; opacity: 1; font-weight: 600; color: #fff; }}

  /* ---------- MAIN ---------- */
  main {{
    position: absolute; top: 70px; left: 260px; right: 0; bottom: 0;
    padding: 30px 40px 29px; overflow: auto;
  }}
  h1.page-title {{ font-size: 22px; margin-bottom: 4px; }}
  p.sub {{ color: #777; font-size: 13px; margin-bottom: 20px; }}

  /* ---------- CONTROL PANEL DEMO ---------- */
  .demo-panel {{
    background: #101826; border-radius: 14px; padding: 16px 20px; margin-bottom: 26px;
    display: flex; align-items: center; gap: 18px; flex-wrap: wrap;
    box-shadow: 0 4px 16px rgba(0,0,0,.25);
  }}
  .demo-panel .title {{ color: #9fd3ff; font-weight: 700; font-size: 13px; letter-spacing: .5px; }}
  .toggle-item {{ display: flex; align-items: center; gap: 8px; }}
  .toggle-item .nm {{ color: #e8edf5; font-size: 13px; font-weight: 600; }}
  .toggle-btn {{
    border: none; cursor: pointer; font-weight: 700; font-size: 12px;
    padding: 7px 14px; border-radius: 20px; color: #fff; transition: .15s;
  }}
  .toggle-btn.off {{ background: var(--do); }}
  .toggle-btn.on  {{ background: var(--xanh); }}

  /* ---------- CARDS ---------- */
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; max-width: 980px; }}
  .card {{
    position: relative;
    background: #fff; border: 1px solid var(--vien); border-radius: 16px;
    padding: 22px; box-shadow: 0 3px 14px rgba(0,0,0,.05);
    height: 150px;
  }}
  .card .icon {{ font-size: 26px; }}
  .card h3 {{ font-size: 16px; margin: 6px 0 4px; }}
  .card p {{ font-size: 12.5px; color: #888; margin-bottom: 10px; }}
  .badge {{
    position: absolute; top: 14px; right: 14px; font-size: 11px; font-weight: 700;
    padding: 4px 10px; border-radius: 20px;
  }}
  .badge.safe {{ background: #e3f8ec; color: var(--xanh); }}
  .badge.danger {{ background: #ffeaea; color: var(--do); }}

  .action-btn {{
    position: absolute;
    border: none; border-radius: 10px; font-weight: 700; font-size: 13.5px;
    color: #fff; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,.15);
  }}
  .btn-huyen {{ background: linear-gradient(90deg,#ff9a3d,#ff5c3d); }}
  .btn-hang  {{ background: linear-gradient(90deg,#4f8cff,#2a5bd7); }}
  .btn-tien  {{ background: linear-gradient(90deg,#9b5cff,#6a2bd7); }}
  .btn-huyen, .btn-hang, .btn-tien {{
    left:22px; bottom:18px; width:calc(100% - 44px); height:42px;
  }}
  .btn-hung  {{
    background: linear-gradient(90deg,#18c37e,#0e9c63);
    left:22px; bottom:18px; width:calc(100% - 44px); height:42px;
  }}
  .action-btn:disabled {{ background: #b9c2cf !important; cursor: not-allowed; }}

  #hangModal {{
    display:none; position: fixed; top: 310px; left: 660px; width: 260px; height: 50px;
    z-index: 50;
  }}

  .flash {{
    position: fixed; bottom: 24px; right: 24px; background: #202a3a; color: #fff;
    padding: 14px 20px; border-radius: 10px; font-size: 13px; display: none; z-index: 99;
    box-shadow: 0 6px 20px rgba(0,0,0,.3);
  }}
</style>
</head>
<body>

<header>
  <div class="logo">ShopMart <span>Trung tam quan ly tai khoan &amp; vi dien tu</span></div>
  <div class="user-pill">👤 Nguyen Van A &nbsp;|&nbsp; Hang Kim Cuong</div>
</header>

<div class="sidebar">
  <div class="avatar">A</div>
  <div class="name">Nguyen Van A</div>
  <div class="rank">💎 Hang Kim Cuong</div>
  <div class="wallet">
    <div class="amount">50.000</div>
    <div class="label">Xu trong vi</div>
  </div>
  <nav>
    <div class="active">🏠 Tong quan</div>
    <div>💳 Vi dien tu</div>
    <div>🔐 Bao mat</div>
    <div>📦 Don hang</div>
    <div>⚙️ Cai dat</div>
  </nav>
</div>

<main>
  <h1 class="page-title">Bang dieu khien tai khoan</h1>
  <p class="sub">Day la mang luoi demo phuc vu do an "Clickjacking" - Nhom 8. Khong dung du lieu that.</p>

  <div class="demo-panel">
    <div class="title">🎛 CONTROL PANEL (CHI DANH CHO NGUOI THUYET TRINH)</div>
    {toggles_html}
  </div>

  <div class="grid">

    <!-- CARD 1 - HUYEN -->
    <div class="card">
      <span class="badge {huyen_badge_class}">{huyen_badge_text}</span>
      <div class="icon">🪙</div>
      <h3>Vi Diem Thuong ShopMart</h3>
      <p>Tang toan bo so xu hien co trong vi cho mot tai khoan khac.</p>
      <button id="btnHuyen" class="action-btn btn-huyen" {huyen_disabled}
        onclick="doAction('huyen')">Tang toan bo 50.000 Xu cho hacker_nhom8</button>
    </div>

    <!-- CARD 2 - HANG (2 buoc) -->
    <div class="card card-hang">
      <span class="badge {hang_badge_class}">{hang_badge_text}</span>
      <div class="icon">🔗</div>
      <h3>Lien ket Dang nhap Nhanh (OAuth)</h3>
      <p>Lien ket tai khoan Google de dang nhap nhanh lan sau.</p>
      <button id="btnHangStep1" class="action-btn btn-hang" {hang_disabled}
        onclick="hangStep1()">Lien ket voi Google (hacker@gmail.com)</button>
    </div>

    <!-- CARD 3 - TIEN -->
    <div class="card">
      <span class="badge {tien_badge_class}">{tien_badge_text}</span>
      <div class="icon">📍</div>
      <h3>Quyen Rieng Tu &amp; Giao Hang</h3>
      <p>Cho phep doi tac ben thu ba truy cap dia chi giao hang cua ban.</p>
      <button id="btnTien" class="action-btn btn-tien" {tien_disabled}
        onclick="doAction('tien')">Chia se Dia chi nha &amp; SDT voi doi tac</button>
    </div>

    <!-- CARD 4 - HUNG -->
    <div class="card">
      <span class="badge {hung_badge_class}">{hung_badge_text}</span>
      <div class="icon">📱</div>
      <h3>Bao Mat So Dien Thoai OTP</h3>
      <p>Thay doi so dien thoai nhan ma OTP xac thuc giao dich.</p>
      <form method="post" action="/log_action">
        <input type="hidden" name="action" value="hung">
        <button id="btnHung" type="submit" class="action-btn btn-hung" {hung_disabled}>
          Doi SDT nhan OTP sang so cua Hacker
        </button>
      </form>
    </div>

  </div>
</main>

<!-- Hop thoai buoc 2 cua Hang -->
<button id="hangModal" class="action-btn btn-hang" {hang_modal_disabled}
  style="top:{h2t}px; left:{h2l}px; width:{h2w}px; height:{h2h}px;"
  onclick="doAction('hang')">Xac nhan cap quyen dang nhap</button>

<div class="flash" id="flash"></div>

<script>
function showFlash(msg) {{
  var f = document.getElementById('flash');
  f.innerText = msg;
  f.style.display = 'block';
  setTimeout(function() {{ f.style.display = 'none'; }}, 2600);
}}

function doAction(who) {{
  var msgs = {{
    huyen: '⚠️ [GIA LAP] Da tang 50.000 Xu cho hacker_nhom8 !',
    tien: '⚠️ [GIA LAP] Da chia se dia chi nha & SDT cho ben thu 3 !',
    hung: '⚠️ [GIA LAP] Da doi so nhan OTP sang so cua Hacker !',
    hang: '⚠️ [GIA LAP] Da cap quyen dang nhap OAuth cho hacker@gmail.com !'
  }};
  fetch('/log_action', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify({{action: who}})}})
    .then(function(response) {{
      if (!response.ok) throw new Error('HTTP ' + response.status);
      showFlash(msgs[who] || 'Da thuc hien hanh dong');
      if (window.parent !== window) {{
        window.parent.postMessage({{
          type:'shopmart-action-result', action:who, ok:true
        }}, '*');
      }}
    }})
    .catch(function() {{
      showFlash('Khong gui duoc hanh dong demo. Hay kiem tra server Flask.');
      if (window.parent !== window) {{
        window.parent.postMessage({{
          type:'shopmart-action-result', action:who, ok:false
        }}, '*');
      }}
    }});
}}

function hangStep1() {{
  document.getElementById('hangModal').style.display = 'block';
  showFlash('Buoc 1: Da chon lien ket Google. Dang cho xac nhan Buoc 2...');
  if (window.parent !== window) {{
    window.parent.postMessage({{type:'shopmart-hang-step1'}}, '*');
  }}
}}

/* ----- FRAME-BUSTING JS (muc tieu cua Hung) -----
   Doan nay chi hoat dong khi trinh duyet THUC THI JavaScript trong iframe.
   Neu attacker dung <iframe sandbox="allow-forms" ...> (KHONG co allow-scripts)
   thi script nay se KHONG BAO GIO chay => ky thuat bypass frame-busting thanh cong. */
if ({hung_bust_active} && top !== self) {{
  try {{ top.location = self.location; }} catch (e) {{
    document.body.innerHTML =
      '<div style="padding:60px;text-align:center;font-size:20px;color:#e8392b;font-weight:700;">'
      + '🛡️ ShopMart phat hien trang dang bi nhung (iframe) va da chan truy cap!</div>';
  }}
}}
</script>
</body>
</html>
"""

TOGGLE_LABEL = {
    "huyen": "Huyen · X-Frame-Options",
    "hang":  "Hang · CSP frame-ancestors 'none'",
    "tien":  "Tien · CSP frame-ancestors 'self'",
    "hung":  "Hung · CSP + SameSite=Strict",
}


def render_toggles():
    html = ""
    for key, label in TOGGLE_LABEL.items():
        state = defense_state[key]
        cls = "on" if state else "off"
        text = "BAT" if state else "TAT"
        html += (
            '<div class="toggle-item"><span class="nm">{label}</span>'
            '<button class="toggle-btn {cls}" onclick="toggleDefense(\'{key}\')">{text}</button></div>'
        ).format(label=label, cls=cls, text=text, key=key)
    html += """
    <script>
    function toggleDefense(key){
      fetch('/toggle/' + key, {method:'POST'}).then(function(){ location.reload(); });
    }
    </script>
    """
    return html


@app.route("/")
def index():
    scenario = request.args.get("scenario")
    if scenario not in defense_state:
        scenario = None

    active_defenses = (
        {scenario: defense_state[scenario]}
        if scenario
        else defense_state
    )

    hb = defense_state["huyen"]
    hg = defense_state["hang"]
    ti = defense_state["tien"]
    hu = defense_state["hung"]

    html = PAGE_TEMPLATE.format(
        toggles_html=render_toggles(),
        huyen_badge_class="safe" if hb else "danger",
        huyen_badge_text="🛡 Da bao ve" if hb else "⚠ Chua bao ve",
        huyen_disabled="disabled" if hb else "",
        hang_badge_class="safe" if hg else "danger",
        hang_badge_text="🛡 Da bao ve" if hg else "⚠ Chua bao ve",
        hang_disabled="disabled" if hg else "",
        h2t=HANG_STEP2["top"], h2l=HANG_STEP2["left"],
        h2w=HANG_STEP2["w"], h2h=HANG_STEP2["h"],

        tien_badge_class="safe" if ti else "danger",
        tien_badge_text="🛡 Da bao ve" if ti else "⚠ Chua bao ve",
        tien_disabled="disabled" if ti else "",

        hung_badge_class="safe" if hu else "danger",
        hung_badge_text="🛡 Da bao ve" if hu else "⚠ Chua bao ve",
        hung_disabled="disabled" if hu else "",
        hung_bust_active=(
            "true"
            if not hu and (scenario == "hung" or request.args.get("framebust") == "1")
            else "false"
        ),
        hang_modal_disabled="",
    )

    resp = make_response(html)

    # ---------------- HEADER PHONG THU (dong theo trang thai toggle) ----------------
    # 1) Huyen - X-Frame-Options
    if active_defenses.get("huyen", False):
        resp.headers["X-Frame-Options"] = "DENY"

    # 2) Hang, Hung & Tien - CSP frame-ancestors ('none' takes precedence).
    frame_ancestors = None
    if active_defenses.get("hang", False) or active_defenses.get("hung", False):
        frame_ancestors = "'none'"
    elif active_defenses.get("tien", False):
        frame_ancestors = "'self'"
    if frame_ancestors:
        resp.headers["Content-Security-Policy"] = "frame-ancestors {};".format(frame_ancestors)

    # SameSite is defense in depth; CSP is what prevents framing.
    cookie_member = scenario or "default"
    samesite = "Strict" if active_defenses.get("hung", False) else "Lax"
    resp.set_cookie(
        "shopmart_session_" + cookie_member,
        "demo-session-token",
        samesite=samesite,
        httponly=True,
    )

    return resp


@app.route("/toggle/<member>", methods=["POST"])
def toggle(member):
    if member in defense_state:
        defense_state[member] = not defense_state[member]
        return jsonify({"ok": True, "state": defense_state[member]})
    return jsonify({"ok": False}), 404


@app.route("/api/defense/hung")
def hung_defense_status():
    enabled = defense_state["hung"]
    response = make_response(jsonify({
        "enabled": enabled,
        "content_security_policy": "frame-ancestors 'none';" if enabled else None,
        "cookie_same_site": "Strict" if enabled else "Lax",
    }))
    if request.headers.get("Origin") == "http://127.0.0.1:8000":
        response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:8000"
        response.headers["Vary"] = "Origin"
    return response


@app.route("/log_action", methods=["POST"])
def log_action():
    data = request.get_json(silent=True) or request.form
    action = data.get("action")
    if action not in defense_state:
        return jsonify({"ok": False, "error": "invalid_action"}), 400
    print("[SHOPMART DEMO] SUCCESS action={}".format(action), flush=True)
    if action == "hung" and not request.is_json:
        return make_response(
            "<!doctype html><html lang='vi'><meta charset='utf-8'>"
            "<title>Kết quả mô phỏng Hưng</title>"
            "<body style='margin:0;padding:24px;font:700 16px Segoe UI,Arial;"
            "color:#176b37;background:#e9fff0'>"
            "✓ SUCCESS — Flask đã ghi nhận form mô phỏng của Hưng."
            "<br><span style='font-size:13px;font-weight:400'>"
            "Không có số điện thoại hay OTP thật được thay đổi.</span></body></html>"
        )
    return jsonify({"ok": True})


@app.route("/reset", methods=["POST"])
def reset():
    for k in defense_state:
        defense_state[k] = False
    return jsonify({"ok": True})


if __name__ == "__main__":
    print("=" * 70)
    print(" SHOPMART VICTIM SERVER - NHOM 8 - DANG CHAY TAI http://127.0.0.1:5000")
    print(" Dung Ctrl+C de dung server.")
    print("=" * 70)
    app.run(host="127.0.0.1", port=5000, debug=False)
