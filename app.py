from flask import Flask, render_template_string, jsonify
from threading import Lock

app = Flask(__name__)
LOCK = Lock()
PROTECTION = {"huyen": False, "hang": False, "tien": False, "hung": False}
EVENTS = []
MEMBERS = {"huyen": "Huyền", "hang": "Hằng", "tien": "Tiên", "hung": "Hưng"}

PAGE = r"""
<!doctype html>
<html lang="vi"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ShopMart | Quản lý tài khoản</title>
<style>
:root{--orange:#f97316;--red:#e5483f;--ink:#202637;--muted:#778095;--line:#e8eaf0;--bg:#f4f6fa;--green:#159765;--shadow:0 10px 30px rgba(27,39,67,.07)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif}
.topbar{height:70px;padding:0 34px;display:flex;align-items:center;justify-content:space-between;color:#fff;background:linear-gradient(105deg,#f97316,#e5483f);box-shadow:0 5px 18px #e5483f33}
.brand{display:flex;align-items:center;gap:12px;font-weight:800;font-size:22px}.mark{width:36px;height:36px;border-radius:11px;background:#fff;color:#ef5b28;display:grid;place-items:center;font-weight:900}.topmeta{font-size:13px}
.wrap{max-width:1440px;margin:24px auto;padding:0 24px 40px}.panel,.sidebar,.card,.activity{background:#fff;border:1px solid var(--line);border-radius:17px;box-shadow:var(--shadow)}
.panel{padding:17px 20px;margin-bottom:22px;border-color:#f1d7cc}.panelhead{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:14px}
h1{font-size:20px;margin:0}.sub{color:var(--muted);font-size:13px;margin-top:4px}.demo{color:#b45309;background:#fff4e8;border-radius:999px;padding:6px 10px;font-size:11px;font-weight:800;white-space:nowrap}
.switches{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.switchcard{border:1px solid var(--line);border-radius:12px;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;gap:10px}.switchtitle{font-weight:700;font-size:14px}.switchdesc{color:var(--muted);font-size:11px;margin-top:3px}
.toggle{border:0;border-radius:999px;padding:8px 13px;color:white;font-size:11px;font-weight:800;cursor:pointer;min-width:62px}.off{background:#dc4545}.on{background:#159765}
.layout{display:grid;grid-template-columns:265px minmax(0,1fr);gap:22px;align-items:start}.sidebar{padding:22px 18px}.avatar{width:58px;height:58px;display:grid;place-items:center;border-radius:18px;color:white;font-size:21px;font-weight:800;background:linear-gradient(135deg,#fb923c,#e5483f)}
.username{font-weight:800;margin-top:13px;font-size:16px}.rank{display:inline-block;margin-top:7px;background:#fff4d8;color:#a66b08;border-radius:999px;padding:5px 9px;font-size:11px;font-weight:800}
.balance{margin-top:20px;padding:16px;border-radius:13px;background:linear-gradient(135deg,#fff3e8,#fff8f3)}.balance small{color:#9a6b51;font-size:11px}.balance strong{display:block;font-size:23px;margin-top:5px;color:#d84b2c}
.nav{margin-top:22px;display:grid;gap:7px}.nav a{text-decoration:none;color:#596174;font-size:13px;padding:10px 11px;border-radius:9px}.nav a.active,.nav a:hover{color:#e65a2d;background:#fff2eb;font-weight:700}
.mainhead{display:flex;align-items:end;justify-content:space-between;margin:2px 2px 17px;gap:12px}.mainhead h2{margin:0;font-size:22px}.mainhead p{margin:5px 0 0;color:var(--muted);font-size:13px}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:17px}.card{min-height:258px;padding:20px;position:relative}.cardtop{display:flex;justify-content:space-between;align-items:center;gap:10px}.ico{width:43px;height:43px;border-radius:13px;display:grid;place-items:center;background:#fff0e7;color:#e65b2e;font-size:20px}.status{font-size:10px;font-weight:800;color:#778095;background:#f3f4f7;padding:6px 9px;border-radius:999px}
.card h3{font-size:17px;margin:17px 0 7px}.card p{color:var(--muted);font-size:12px;line-height:1.55;min-height:38px;margin:0 0 15px}
.action{border:0;background:linear-gradient(100deg,#f97316,#e6533c);color:white;border-radius:10px;padding:11px 14px;font-weight:750;cursor:pointer;font-size:12px}.secondary{background:#263449}.action:disabled{background:#b8bec9;cursor:not-allowed}
.note{color:#9299a8;font-size:10px;margin-top:11px}.step{margin:9px 0 12px;padding:10px 11px;background:#f8f9fb;border:1px solid #edf0f4;border-radius:10px;font-size:11px;color:#5f6879}.step strong{color:#273247}
.activity{margin-top:18px;padding:17px 20px}.activity h3{margin:0 0 10px;font-size:15px}.event{padding:9px 0;border-top:1px solid #f0f1f4;color:#667085;font-size:12px}.event:first-of-type{border-top:0}
.footer{margin-top:18px;color:#8991a2;font-size:11px;text-align:center}.toast{position:fixed;right:22px;bottom:22px;z-index:5;max-width:360px;background:#202b3d;color:#fff;padding:13px 16px;border-radius:12px;box-shadow:0 12px 35px #0003;font-size:13px;display:none}.toast.show{display:block}
@media(max-width:900px){.switches{grid-template-columns:repeat(2,1fr)}.layout{grid-template-columns:1fr}.sidebar{display:grid;grid-template-columns:1fr 1fr;align-items:center}.nav{grid-column:1/-1;grid-template-columns:repeat(3,1fr)}}
@media(max-width:620px){.topbar{padding:0 17px}.topmeta{display:none}.wrap{padding:0 13px 28px;margin-top:14px}.switches,.grid{grid-template-columns:1fr}.panelhead,.mainhead{align-items:flex-start;flex-direction:column}.sidebar{display:block}.nav{grid-template-columns:1fr 1fr}}
</style></head><body>
<header class="topbar"><div class="brand"><div class="mark">S</div>ShopMart</div><div class="topmeta">TRUNG TÂM QUẢN LÝ TÀI KHOẢN &amp; VÍ ĐIỆN TỬ</div></header>
<div class="wrap">
<section class="panel"><div class="panelhead"><div><h1>Control Panel · Demo phòng thủ</h1><div class="sub">Bật/tắt bảo vệ minh họa riêng cho từng khu vực; thay đổi có hiệu lực ngay trên trang.</div></div><span class="demo">CHẾ ĐỘ THỰC NGHIỆM · DỮ LIỆU GIẢ</span></div>
<div class="switches">
{% for key,name in members.items() %}<div class="switchcard"><div><div class="switchtitle">{{name}}</div><div class="switchdesc" id="desc-{{key}}">{{"Đang bật bảo vệ" if protections[key] else "Đang tắt bảo vệ"}}</div></div><button class="toggle {{'on' if protections[key] else 'off'}}" id="toggle-{{key}}" onclick="toggleProtection('{{key}}')">{{"BẬT" if protections[key] else "TẮT"}}</button></div>{% endfor %}
</div></section>
<div class="layout"><aside class="sidebar"><div><div class="avatar">A</div><div class="username">Nguyễn Văn A</div><span class="rank">✦ HẠNG KIM CƯƠNG</span></div>
<div class="balance"><small>SỐ DƯ VÍ SHOPMART</small><strong>50.000 Xu</strong><small>Dữ liệu tài khoản mô phỏng</small></div>
<nav class="nav"><a class="active" href="/">Tổng quan</a><a href="#cards">Dịch vụ của tôi</a><a href="#activity">Lịch sử demo</a></nav></aside>
<main><div class="mainhead"><div><h2>Trung tâm dịch vụ</h2><p>Quản lý các tiện ích và thiết lập tài khoản ShopMart của bạn.</p></div><span class="demo">TÀI KHOẢN THỬ NGHIỆM</span></div>
<section class="grid" id="cards">
<article class="card"><div class="cardtop"><div class="ico">✦</div><span class="status" id="status-huyen">{{"ĐÃ BẢO VỆ" if protections.huyen else "DEMO"}}</span></div><h3>Ví Điểm Thưởng ShopMart</h3><p>Mô phỏng thao tác với điểm thưởng trong ví. Không có giao dịch hoặc chuyển Xu thật.</p><button class="action" id="action-huyen" onclick="simulate('huyen')" {{'disabled' if protections.huyen else ''}}>Mô phỏng tặng 50.000 Xu</button><div class="note">Tài khoản nhận minh họa: <b>demo_receiver</b> · Không phát sinh giao dịch.</div></article>
<article class="card"><div class="cardtop"><div class="ico">◎</div><span class="status" id="status-hang">{{"ĐÃ BẢO VỆ" if protections.hang else "DEMO"}}</span></div><h3>Liên kết đăng nhập nhanh</h3><p>Mô phỏng quy trình xác nhận liên kết hai bước bằng tài khoản mẫu, không kết nối Google hoặc OAuth thật.</p><div class="step"><strong>Bước 1.</strong> Tài khoản minh họa: demo@example.test</div><button class="action" id="action-hang" onclick="showStepTwo()" {{'disabled' if protections.hang else ''}}>Mô phỏng bước 1 · Liên kết</button><div class="step" id="step-two" hidden><strong>Bước 2.</strong> Đây chỉ là xác nhận giả lập.<div style="margin-top:9px"><button class="action secondary" onclick="simulate('hang')">Xác nhận demo</button></div></div><div class="note">Không cấp quyền đăng nhập cho dịch vụ bên ngoài.</div></article>
<article class="card"><div class="cardtop"><div class="ico">⌖</div><span class="status" id="status-tien">{{"ĐÃ BẢO VỆ" if protections.tien else "DEMO"}}</span></div><h3>Quyền riêng tư &amp; giao hàng</h3><p>Minh họa màn hình tùy chọn chia sẻ thông tin giao hàng bằng dữ liệu đã được làm giả.</p><div class="step">Địa chỉ mẫu: 123 Đường Demo, Quận Mẫu · SĐT: 09xx xxx 000</div><button class="action" id="action-tien" onclick="simulate('tien')" {{'disabled' if protections.tien else ''}}>Mô phỏng chia sẻ dữ liệu mẫu</button><div class="note">Không truy cập, gửi hoặc lưu địa chỉ/số điện thoại thật.</div></article>
<article class="card"><div class="cardtop"><div class="ico">⌑</div><span class="status" id="status-hung">{{"ĐÃ BẢO VỆ" if protections.hung else "DEMO"}}</span></div><h3>Bảo mật số điện thoại OTP</h3><p>Mô phỏng khu vực quản lý số điện thoại nhận mã xác minh. Không gửi OTP và không thay đổi số thật.</p><div class="step">Số điện thoại hiển thị: <strong>09xx xxx 123</strong></div><button class="action" id="action-hung" onclick="simulate('hung')" {{'disabled' if protections.hung else ''}}>Mô phỏng yêu cầu đổi số</button><div class="note">Có thể dùng trang này để kiểm tra chính sách nhúng; không có mã OTP thật.</div></article>
</section>
<section class="activity" id="activity"><h3>Nhật ký thao tác mô phỏng</h3><div id="events">{% if events %}{% for event in events %}<div class="event">{{event}}</div>{% endfor %}{% else %}<div class="event" id="empty-event">Chưa có thao tác demo nào.</div>{% endif %}</div></section>
<div class="footer">ShopMart Demo Lab · Chỉ sử dụng dữ liệu giả trong môi trường học tập được cho phép.</div>
</main></div></div><div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
const names={huyen:"Huyền",hang:"Hằng",tien:"Tiên",hung:"Hưng"};
let protections={{protections|tojson}};
function toast(message){const box=document.getElementById("toast");box.textContent=message;box.classList.add("show");clearTimeout(window.__toastTimer);window.__toastTimer=setTimeout(()=>box.classList.remove("show"),3200)}
async function toggleProtection(key){const r=await fetch("/api/protection/"+key,{method:"POST"});const d=await r.json();protections[key]=d.enabled;
const b=document.getElementById("toggle-"+key);b.textContent=d.enabled?"BẬT":"TẮT";b.className="toggle "+(d.enabled?"on":"off");
document.getElementById("desc-"+key).textContent=d.enabled?"Đang bật bảo vệ":"Đang tắt bảo vệ";
document.getElementById("status-"+key).textContent=d.enabled?"ĐÃ BẢO VỆ":"DEMO";
document.getElementById("action-"+key).disabled=d.enabled;
if(key==="hang"&&d.enabled)document.getElementById("step-two").hidden=true;
toast(names[key]+": "+(d.enabled?"đã bật bảo vệ mô phỏng.":"đã tắt bảo vệ mô phỏng."))}
function showStepTwo(){if(protections.hang)return toast("Khu vực này đang bật bảo vệ mô phỏng.");document.getElementById("step-two").hidden=false;toast("Đã mở bước xác nhận demo; không kết nối dịch vụ bên ngoài.")}
async function simulate(key){if(protections[key])return toast("Khu vực này đang bật bảo vệ mô phỏng.");const r=await fetch("/api/simulate/"+key,{method:"POST"});const d=await r.json();toast(d.message);const box=document.getElementById("events");const empty=document.getElementById("empty-event");if(empty)empty.remove();const row=document.createElement("div");row.className="event";row.textContent=d.event;box.prepend(row)}
</script></body></html>
"""

@app.get("/")
def home():
    with LOCK:
        protections = dict(PROTECTION)
        events = list(EVENTS)
    return render_template_string(PAGE, members=MEMBERS, protections=protections, events=events)

@app.post("/api/protection/<member>")
def toggle_protection(member):
    if member not in PROTECTION:
        return jsonify(error="Thành viên không hợp lệ"), 404
    with LOCK:
        PROTECTION[member] = not PROTECTION[member]
        enabled = PROTECTION[member]
    return jsonify(member=member, enabled=enabled)

@app.post("/api/simulate/<member>")
def simulate(member):
    if member not in MEMBERS:
        return jsonify(error="Kịch bản không hợp lệ"), 404
    with LOCK:
        if PROTECTION[member]:
            return jsonify(message="Khu vực đang bật bảo vệ mô phỏng."), 403
        event = f"Đã chạy thao tác mô phỏng của {MEMBERS[member]} — không có giao dịch hoặc dữ liệu thật được thay đổi."
        EVENTS.insert(0, event)
        del EVENTS[12:]
    return jsonify(message="Hoàn tất thao tác giả lập. Không có giao dịch hoặc dữ liệu thật.",
                   event=event)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
