
from flask import Flask, render_template_string, jsonify
from threading import Lock
from datetime import datetime

app = Flask(__name__)

# =====================================================
# 1. DU LIEU MO PHONG
# =====================================================

MEMBERS = {
    "huyen": {
        "name": "Huyền",
        "technique": "Classic Clickjacking",
        "description": "Mô phỏng thao tác nhận và tặng xu",
        "color": "orange"
    },
    "hang": {
        "name": "Hằng",
        "technique": "Multi-step Clickjacking",
        "description": "Mô phỏng quy trình đăng nhập hai bước",
        "color": "blue"
    },
    "tien": {
        "name": "Tiên",
        "technique": "Cursor-based Clickjacking",
        "description": "Mô phỏng thao tác chia sẻ thông tin",
        "color": "purple"
    },
    "hung": {
        "name": "Hưng",
        "technique": "Clickjacking Bypass Demo",
        "description": "Mô phỏng yêu cầu thay đổi số điện thoại",
        "color": "green"
    }
}

# Trạng thái bảo vệ dùng trong giao diện mô phỏng.
PROTECTION = {
    member: False for member in MEMBERS
}

EVENTS = [
    {
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": "Hệ thống ShopMart đã khởi động.",
        "type": "system"
    }
]

lock = Lock()


# =====================================================
# 2. GIAO DIEN SHOPMART
# =====================================================


PAGE = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ShopMart - Online Shopping</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --bg: #10131b;
    --panel: #191e29;
    --panel2: #202735;
    --orange: #ff7139;
    --text: #f5f5f6;
    --muted: #929baa;
    --border: rgba(255,255,255,0.08);
}

body {
    background: var(--bg);
    color: var(--text);
    font-family: Arial, Helvetica, sans-serif;
}

/* SIDEBAR */

.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 245px;
    height: 100vh;
    background: #171c27;
    border-right: 1px solid var(--border);
    padding: 28px 20px;
    display: flex;
    flex-direction: column;
    z-index: 10;
}

.logo {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 0 8px;
    margin-bottom: 42px;
}

.logo-symbol {
    width: 39px;
    height: 39px;
    background: var(--orange);
    color: white;
    border-radius: 12px;
    display: grid;
    place-items: center;
    font-size: 23px;
    font-weight: bold;
}

.logo-name {
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -1px;
}

.logo-name span {
    color: var(--orange);
}

.menu-title {
    color: #687386;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 2px;
    padding: 0 12px;
    margin-bottom: 15px;
}

.menu-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 13px;
    margin-bottom: 6px;
    border-radius: 9px;
    color: #a7b0bf;
    font-size: 13px;
}

.menu-item.active {
    background: rgba(255,113,57,0.13);
    color: #ff8759;
}

.menu-icon {
    width: 20px;
    text-align: center;
    font-size: 17px;
}

.sidebar-bottom {
    margin-top: auto;
}

.user-card {
    background: #222a38;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 10px;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #f2c39e;
    color: #68432c;
    display: grid;
    place-items: center;
    font-weight: bold;
}

.user-name {
    font-size: 12px;
    font-weight: bold;
}

.user-rank {
    color: #f2bd62;
    font-size: 10px;
    margin-top: 5px;
}

.wallet-card {
    padding: 16px;
    border-radius: 12px;
    background: linear-gradient(135deg, #f36b36, #f99a4e);
}

.wallet-label {
    font-size: 10px;
    color: rgba(255,255,255,.85);
    letter-spacing: 1px;
}

.wallet-value {
    font-size: 22px;
    font-weight: bold;
    margin-top: 8px;
}

/* MAIN */

.main {
    margin-left: 245px;
    padding: 25px 35px 45px;
    max-width: 1600px;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 22px;
    border-bottom: 1px solid var(--border);
}

.nav-links {
    display: flex;
    gap: 28px;
    color: #aab3c1;
    font-size: 12px;
}

.nav-links span:first-child {
    color: white;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 17px;
    color: #b3bdca;
    font-size: 12px;
}

.search-icon {
    width: 35px;
    height: 35px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 50%;
    display: grid;
    place-items: center;
}

/* HERO */

.hero {
    margin-top: 27px;
    min-height: 245px;
    border-radius: 17px;
    padding: 38px 42px;
    background:
        radial-gradient(circle at 85% 25%, rgba(255,130,70,.25), transparent 30%),
        linear-gradient(110deg, #292f3d, #202735 70%, #352a2a);
    border: 1px solid rgba(255,255,255,.07);
    display: flex;
    align-items: center;
    justify-content: space-between;
    overflow: hidden;
}

.hero-content {
    max-width: 530px;
}

.hero-tag {
    color: #ff956b;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 2px;
    margin-bottom: 15px;
}

.hero h1 {
    font-size: 31px;
    line-height: 1.3;
    margin-bottom: 12px;
}

.hero h1 span {
    color: var(--orange);
}

.hero p {
    color: #aeb7c5;
    font-size: 12px;
    line-height: 1.8;
    max-width: 440px;
}

.hero-decoration {
    width: 170px;
    height: 170px;
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 50%;
    display: grid;
    place-items: center;
    font-size: 75px;
    color: rgba(255,255,255,.8);
    box-shadow: 0 0 0 20px rgba(255,255,255,.025),
                0 0 0 42px rgba(255,255,255,.02);
    margin-right: 40px;
}

/* GENERAL SECTION */

.section {
    margin-top: 34px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: end;
    margin-bottom: 17px;
}

.section-header h2 {
    font-size: 19px;
    letter-spacing: -.3px;
}

.section-header p {
    color: var(--muted);
    font-size: 11px;
    margin-top: 6px;
}

.view-label {
    color: var(--orange);
    font-size: 11px;
}

/* HIGHLIGHTS */

.highlights {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
}

.highlight {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 17px 19px;
    display: flex;
    align-items: center;
    gap: 14px;
}

.highlight-icon {
    width: 43px;
    height: 43px;
    background: #292f3c;
    border-radius: 11px;
    display: grid;
    place-items: center;
    font-size: 20px;
}

.highlight-number {
    font-size: 19px;
    font-weight: bold;
}

.highlight-text {
    color: var(--muted);
    font-size: 10px;
    margin-top: 5px;
}

/* PROTECTION SETTINGS */

.protection-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 20px;
}

.protection-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 17px;
}

.protection-top h3 {
    font-size: 14px;
}

.demo-tag {
    background: rgba(255,113,57,.13);
    color: #ff946b;
    padding: 6px 10px;
    border-radius: 5px;
    font-size: 9px;
    font-weight: bold;
}

.protection-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 11px;
}

.protection-item {
    background: #202735;
    border: 1px solid var(--border);
    padding: 13px;
    border-radius: 9px;
}

.protection-name {
    font-size: 12px;
    font-weight: bold;
}

.protection-tech {
    color: var(--muted);
    font-size: 9px;
    margin-top: 5px;
    min-height: 22px;
}

.switch-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 11px;
}

.status-text {
    font-size: 9px;
    font-weight: bold;
}

.status-text.on {
    color: #55d69b;
}

.status-text.off {
    color: #f17a75;
}

.switch {
    width: 36px;
    height: 20px;
    border: none;
    border-radius: 20px;
    background: #525d6d;
    position: relative;
    cursor: pointer;
}

.switch::after {
    content: "";
    width: 14px;
    height: 14px;
    position: absolute;
    top: 3px;
    left: 3px;
    background: white;
    border-radius: 50%;
    transition: .2s;
}

.switch.on {
    background: #27a975;
}

.switch.on::after {
    left: 19px;
}

/* FUNCTION CARDS */

.function-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
}

.function-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;
    transition: .2s;
}

.function-card:hover {
    border-color: rgba(255,113,57,.45);
    transform: translateY(-2px);
}

.function-cover {
    height: 92px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 23px;
}

.cover-orange {
    background: linear-gradient(110deg, #493126, #29232a);
}

.cover-blue {
    background: linear-gradient(110deg, #253a55, #252b3c);
}

.cover-purple {
    background: linear-gradient(110deg, #3b3052, #292638);
}

.cover-green {
    background: linear-gradient(110deg, #24473e, #242e36);
}

.function-icon {
    font-size: 31px;
}

.function-index {
    color: rgba(255,255,255,.45);
    font-size: 11px;
    letter-spacing: 2px;
}

.function-body {
    padding: 19px 21px 21px;
}

.function-title {
    font-size: 15px;
    font-weight: bold;
}

.function-tech {
    font-size: 10px;
    color: var(--orange);
    margin-top: 6px;
}

.function-description {
    font-size: 11px;
    line-height: 1.7;
    color: #a0aaba;
    margin-top: 13px;
    min-height: 37px;
}

.demo-info {
    margin-top: 14px;
    padding: 12px;
    background: #202735;
    border-radius: 8px;
    color: #aeb8c6;
    font-size: 10px;
    line-height: 1.9;
}

.demo-info strong {
    color: #f3f4f6;
}

.action-button {
    margin-top: 14px;
    width: 100%;
    border: none;
    padding: 12px;
    border-radius: 7px;
    color: white;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: .5px;
    cursor: pointer;
    transition: .2s;
}

.action-button:hover {
    filter: brightness(1.12);
}

.action-orange { background: #e96e3b; }
.action-blue { background: #477bc3; }
.action-purple { background: #8060c3; }
.action-green { background: #299b70; }

.action-button:disabled {
    background: #515c6b;
    cursor: not-allowed;
    filter: none;
}

.note {
    color: #788597;
    font-size: 9px;
    text-align: center;
    margin-top: 9px;
}

/* ACTIVITY */

.activity-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 17px 20px;
}

.activity-item {
    display: flex;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
}

.activity-item:last-child {
    border-bottom: none;
}

.activity-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--orange);
    margin-top: 5px;
    flex-shrink: 0;
}

.activity-message {
    color: #dce1e9;
    font-size: 11px;
    line-height: 1.6;
}

.activity-time {
    color: #778397;
    font-size: 9px;
    margin-top: 4px;
}

.empty-message {
    color: var(--muted);
    font-size: 11px;
}

.footer {
    text-align: center;
    color: #657083;
    font-size: 10px;
    padding: 30px 0 5px;
}

/* RESPONSIVE */

@media(max-width: 1050px) {
    .protection-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .hero-decoration {
        margin-right: 10px;
    }
}

@media(max-width: 800px) {
    .sidebar {
        width: 70px;
        padding: 20px 9px;
    }

    .logo {
        justify-content: center;
        padding: 0;
        margin-bottom: 35px;
    }

    .logo-name,
    .menu-title,
    .menu-item span:not(.menu-icon),
    .sidebar-bottom {
        display: none;
    }

    .menu-item {
        justify-content: center;
        padding: 14px 5px;
    }

    .main {
        margin-left: 70px;
        padding: 20px;
    }

    .nav-links {
        gap: 12px;
    }
}

@media(max-width: 600px) {
    .function-grid,
    .highlights {
        grid-template-columns: 1fr;
    }

    .hero {
        padding: 25px;
    }

    .hero h1 {
        font-size: 24px;
    }

    .hero-decoration {
        display: none;
    }

    .protection-grid {
        grid-template-columns: 1fr 1fr;
    }

    .nav-links span:nth-child(n+3) {
        display: none;
    }
}
</style>
</head>

<body>

<!-- SIDEBAR -->

<aside class="sidebar">

    <div class="logo">
        <div class="logo-symbol">S</div>
        <div class="logo-name">Shop<span>Mart</span></div>
    </div>

    <div class="menu-title">KHÁM PHÁ</div>

    <div class="menu-item active">
        <span class="menu-icon">⌂</span>
        <span>Trang chủ</span>
    </div>

    <div class="menu-item">
        <span class="menu-icon">▣</span>
        <span>Ví của tôi</span>
    </div>

    <div class="menu-item">
        <span class="menu-icon">♙</span>
        <span>Tài khoản</span>
    </div>

    <div class="menu-item">
        <span class="menu-icon">♡</span>
        <span>Yêu thích</span>
    </div>

    <div class="menu-item">
        <span class="menu-icon">◷</span>
        <span>Lịch sử</span>
    </div>

    <div class="sidebar-bottom">

        <div class="user-card">
            <div class="user-info">
                <div class="avatar">A</div>
                <div>
                    <div class="user-name">Nguyễn Văn A</div>
                    <div class="user-rank">★ Hạng Kim Cương</div>
                </div>
            </div>
        </div>

        <div class="wallet-card">
            <div class="wallet-label">SHOPMART WALLET</div>
            <div class="wallet-value">50.000 Xu</div>
        </div>

    </div>

</aside>


<!-- MAIN WEBSITE -->

<main class="main">

    <nav class="navbar">

        <div class="nav-links">
            <span>Trang chủ</span>
            <span>Sản phẩm</span>
            <span>Ưu đãi</span>
            <span>Hỗ trợ</span>
        </div>

        <div class="nav-right">
            <div class="search-icon">⌕</div>
            <span>♙ Tài khoản của tôi</span>
        </div>

    </nav>


    <!-- HERO -->

    <section class="hero">

        <div class="hero-content">

            <div class="hero-tag">SHOPMART MEMBER EXCLUSIVE</div>

            <h1>
                Mua sắm thông minh.<br>
                Tận hưởng <span>ưu đãi</span> mỗi ngày.
            </h1>

            <p>
                Chào mừng bạn đến với ShopMart.
                Quản lý tài khoản, ví điện tử và trải nghiệm
                các tiện ích dành riêng cho thành viên.
            </p>

        </div>

        <div class="hero-decoration">S</div>

    </section>


    <!-- HIGHLIGHTS -->

    <section class="section">

        <div class="highlights">

            <div class="highlight">
                <div class="highlight-icon">◈</div>
                <div>
                    <div class="highlight-number">50.000 Xu</div>
                    <div class="highlight-text">Số dư ví hiện tại</div>
                </div>
            </div>

            <div class="highlight">
                <div class="highlight-icon">✦</div>
                <div>
                    <div class="highlight-number">Kim Cương</div>
                    <div class="highlight-text">Hạng thành viên</div>
                </div>
            </div>

            <div class="highlight">
                <div class="highlight-icon">✓</div>
                <div>
                    <div class="highlight-number" id="protectedCount">0/4</div>
                    <div class="highlight-text">Bảo vệ demo đang bật</div>
                </div>
            </div>

        </div>

    </section>


    <!-- PROTECTION -->

    <section class="section">

        <div class="section-header">
            <div>
                <h2>Trung tâm bảo mật</h2>
                <p>Quản lý trạng thái bảo vệ trong môi trường mô phỏng.</p>
            </div>
            <span class="view-label">SECURITY CENTER</span>
        </div>

        <div class="protection-panel">

            <div class="protection-top">
                <h3>Cài đặt bảo vệ</h3>
                <span class="demo-tag">DEMO CONTROL</span>
            </div>

            <div class="protection-grid">

                {% for member, info in members.items() %}

                <div class="protection-item">

                    <div class="protection-name">{{ info.name }}</div>

                    <div class="protection-tech">
                        {{ info.technique }}
                    </div>

                    <div class="switch-row">

                        <span
                            class="status-text {{ 'on' if protection[member] else 'off' }}"
                            id="status-{{ member }}">
                            {{ 'ĐANG BẬT' if protection[member] else 'ĐANG TẮT' }}
                        </span>

                        <button
                            class="switch {{ 'on' if protection[member] else '' }}"
                            id="switch-{{ member }}"
                            onclick="toggleProtection('{{ member }}')">
                        </button>

                    </div>

                </div>

                {% endfor %}

            </div>

        </div>

    </section>


    <!-- FUNCTIONS -->

    <section class="section">

        <div class="section-header">
            <div>
                <h2>Tiện ích dành cho thành viên</h2>
                <p>Khám phá các chức năng tài khoản trên ShopMart.</p>
            </div>
            <span class="view-label">EXPLORE FEATURES →</span>
        </div>


        <div class="function-grid">


            <!-- HUYEN -->

            <article class="function-card">

                <div class="function-cover cover-orange">
                    <div class="function-icon">◈</div>
                    <div class="function-index">FEATURE 01</div>
                </div>

                <div class="function-body">

                    <div class="function-title">Ví điện tử ShopMart</div>

                    <div class="function-tech">
                        Classic Clickjacking
                    </div>

                    <p class="function-description">
                        Quản lý số dư ví và trải nghiệm tiện ích tặng xu
                        dành cho các thành viên ShopMart.
                    </p>

                    <div class="demo-info">
                        Số dư: <strong>50.000 Xu</strong><br>
                        Tài khoản demo: <strong>hacker_nhom8</strong>
                    </div>

                    <button
                        class="action-button action-orange"
                        id="button-huyen"
                        onclick="simulate('huyen')">
                        MÔ PHỎNG TẶNG 50.000 XU
                    </button>

                    <div class="note">
                        Thao tác chỉ được ghi nhận trong nhật ký demo
                    </div>

                </div>

            </article>


            <!-- HANG -->

            <article class="function-card">

                <div class="function-cover cover-blue">
                    <div class="function-icon">◎</div>
                    <div class="function-index">FEATURE 02</div>
                </div>

                <div class="function-body">

                    <div class="function-title">Đăng nhập tài khoản</div>

                    <div class="function-tech">
                        Multi-step Clickjacking
                    </div>

                    <p class="function-description">
                        Mô phỏng quy trình đăng nhập và xác nhận
                        tài khoản qua hai bước.
                    </p>

                    <div class="demo-info">
                        Dịch vụ: <strong>Google Login Demo</strong><br>
                        Email demo: <strong>hacker@gmail.com</strong>
                    </div>

                    <button
                        class="action-button action-blue"
                        id="button-hang"
                        onclick="simulate('hang')">
                        MÔ PHỎNG XÁC NHẬN ĐĂNG NHẬP
                    </button>

                    <div class="note">
                        Không kết nối Google OAuth thật
                    </div>

                </div>

            </article>


            <!-- TIEN -->

            <article class="function-card">

                <div class="function-cover cover-purple">
                    <div class="function-icon">♧</div>
                    <div class="function-index">FEATURE 03</div>
                </div>

                <div class="function-body">

                    <div class="function-title">Thông tin cá nhân</div>

                    <div class="function-tech">
                        Cursor-based Clickjacking
                    </div>

                    <p class="function-description">
                        Quản lý thông tin liên hệ và các thiết lập
                        chia sẻ thông tin tài khoản.
                    </p>

                    <div class="demo-info">
                        Địa chỉ: <strong>123 Đường ABC, Hà Nội</strong><br>
                        Điện thoại: <strong>09xx xxx xxx</strong>
                    </div>

                    <button
                        class="action-button action-purple"
                        id="button-tien"
                        onclick="simulate('tien')">
                        MÔ PHỎNG CHIA SẺ THÔNG TIN
                    </button>

                    <div class="note">
                        Dữ liệu giả lập, không gửi ra bên ngoài
                    </div>

                </div>

            </article>


            <!-- HUNG -->

            <article class="function-card">

                <div class="function-cover cover-green">
                    <div class="function-icon">▣</div>
                    <div class="function-index">FEATURE 04</div>
                </div>

                <div class="function-body">

                    <div class="function-title">Bảo mật tài khoản</div>

                    <div class="function-tech">
                        Clickjacking Defense Demo
                    </div>

                    <p class="function-description">
                        Quản lý thông tin xác minh và yêu cầu
                        thay đổi số điện thoại liên kết.
                    </p>

                    <div class="demo-info">
                        Số hiện tại: <strong>09xx xxx xxx</strong><br>
                        Số mới: <strong>08xx xxx xxx</strong>
                    </div>

                    <button
                        class="action-button action-green"
                        id="button-hung"
                        onclick="simulate('hung')">
                        MÔ PHỎNG YÊU CẦU THAY ĐỔI
                    </button>

                    <div class="note">
                        Không gửi hoặc xác thực OTP thật
                    </div>

                </div>

            </article>

        </div>

    </section>


    <!-- ACTIVITY -->

    <section class="section">

        <div class="section-header">
            <div>
                <h2>Lịch sử hoạt động</h2>
                <p>Các hoạt động gần đây trong phiên mô phỏng.</p>
            </div>
        </div>

        <div class="activity-panel" id="activityPanel">

            {% for event in events %}

            <div class="activity-item">
                <div class="activity-dot"></div>

                <div>
                    <div class="activity-message">
                        {{ event.message }}
                    </div>

                    <div class="activity-time">
                        {{ event.time }}
                    </div>
                </div>
            </div>

            {% endfor %}

        </div>

    </section>


    <footer class="footer">
        © 2026 ShopMart. Educational Demonstration Website.
    </footer>

</main>


<script>

// CAP NHAT GIAO DIEN BAO VE

function updateProtectionUI(member, enabled) {

    const switchButton =
        document.getElementById("switch-" + member);

    const statusText =
        document.getElementById("status-" + member);

    const actionButton =
        document.getElementById("button-" + member);

    switchButton.classList.toggle("on", enabled);

    statusText.textContent =
        enabled ? "ĐANG BẬT" : "ĐANG TẮT";

    statusText.className =
        enabled ? "status-text on" : "status-text off";

    actionButton.disabled = enabled;

    updateProtectedCount();
}


// BAT / TAT BAO VE

async function toggleProtection(member) {

    try {

        const response = await fetch(
            "/api/protection/" + member,
            { method: "POST" }
        );

        const data = await response.json();

        if (!response.ok) {
            alert(data.message);
            return;
        }

        updateProtectionUI(member, data.enabled);
        loadEvents();

    } catch (error) {

        alert("Không thể kết nối đến ShopMart.");

    }
}


// MO PHONG CHUC NANG

async function simulate(member) {

    const button =
        document.getElementById("button-" + member);

    button.disabled = true;

    try {

        const response = await fetch(
            "/api/simulate/" + member,
            { method: "POST" }
        );

        const data = await response.json();

        if (!response.ok) {
            alert(data.message);
            return;
        }

        alert(data.message);
        loadEvents();

    } catch (error) {

        alert("Không thể kết nối đến ShopMart.");

    } finally {

        const switchButton =
            document.getElementById("switch-" + member);

        if (!switchButton.classList.contains("on")) {
            button.disabled = false;
        }

    }
}


// TAI NHAT KY

async function loadEvents() {

    try {

        const response = await fetch("/api/events");
        const data = await response.json();

        const panel =
            document.getElementById("activityPanel");

        panel.innerHTML = "";

        if (data.events.length === 0) {

            panel.innerHTML =
                '<div class="empty-message">Chưa có hoạt động nào.</div>';

            return;
        }

        data.events.forEach(event => {

            const item = document.createElement("div");
            item.className = "activity-item";

            const dot = document.createElement("div");
            dot.className = "activity-dot";

            const content = document.createElement("div");

            const message = document.createElement("div");
            message.className = "activity-message";
            message.textContent = event.message;

            const time = document.createElement("div");
            time.className = "activity-time";
            time.textContent = event.time;

            content.appendChild(message);
            content.appendChild(time);

            item.appendChild(dot);
            item.appendChild(content);

            panel.appendChild(item);

        });

    } catch (error) {

        console.log("Không thể tải nhật ký.");

    }
}


// DEM SO KICH BAN DANG BAT

async function updateProtectedCount() {

    try {

        const response = await fetch("/api/protection");
        const data = await response.json();

        const count = Object.values(data.protection)
            .filter(value => value === true).length;

        document.getElementById("protectedCount").textContent =
            count + "/4";

    } catch (error) {

        console.log("Không thể cập nhật trạng thái.");

    }
}


// KHOI TAO

document.addEventListener("DOMContentLoaded", function() {

    {% for member in members %}

    updateProtectionUI(
        "{{ member }}",
        {{ 'true' if protection[member] else 'false' }}
    );

    {% endfor %}

    updateProtectedCount();

});

</script>

</body>
</html>
"""



# =====================================================
# 8. CAC ROUTE CUA FLASK
# =====================================================

@app.route("/")
def home():

    return render_template_string(
        PAGE,
        members=MEMBERS,
        protection=PROTECTION,
        events=EVENTS
    )


# -----------------------------------------------------
# Lay trang thai bao ve
# -----------------------------------------------------

@app.route("/api/protection", methods=["GET"])
def get_all_protection():

    with lock:
        return jsonify({
            "protection": PROTECTION
        })


# -----------------------------------------------------
# Bat / tat trang thai bao ve
# -----------------------------------------------------

@app.route("/api/protection/<member>", methods=["POST"])
def toggle_protection(member):

    if member not in MEMBERS:
        return jsonify({
            "message": "Không tìm thấy kịch bản."
        }), 404

    with lock:

        PROTECTION[member] = not PROTECTION[member]

        enabled = PROTECTION[member]

        status = "bật" if enabled else "tắt"

        EVENTS.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "message": (
                f"Đã {status} trạng thái bảo vệ mô phỏng "
                f"cho thành viên {MEMBERS[member]['name']}."
            ),
            "type": "protection"
        })

        del EVENTS[12:]

    return jsonify({
        "success": True,
        "member": member,
        "enabled": enabled
    })


# -----------------------------------------------------
# Mo phong thao tac cua tung kich ban
# -----------------------------------------------------

@app.route("/api/simulate/<member>", methods=["POST"])
def simulate(member):

    if member not in MEMBERS:
        return jsonify({
            "message": "Không tìm thấy kịch bản."
        }), 404

    with lock:

        if PROTECTION[member]:

            return jsonify({
                "success": False,
                "message": (
                    "Trạng thái bảo vệ mô phỏng đang được bật. "
                    "Thao tác demo đã bị chặn."
                )
            }), 403

        name = MEMBERS[member]["name"]

        messages = {
            "huyen": (
                "Đã ghi nhận thao tác mô phỏng tặng 50.000 Xu "
                "cho tài khoản hacker_nhom8. "
                "Số dư thật không bị thay đổi."
            ),

            "hang": (
                "Đã ghi nhận thao tác mô phỏng xác nhận "
                "đăng nhập Google hai bước. "
                "Không có tài khoản Google nào được kết nối."
            ),

            "tien": (
                "Đã ghi nhận thao tác mô phỏng chia sẻ "
                "thông tin liên hệ. "
                "Không có dữ liệu nào được gửi ra ngoài."
            ),

            "hung": (
                "Đã ghi nhận thao tác mô phỏng yêu cầu "
                "thay đổi số điện thoại. "
                "Không có số điện thoại hoặc OTP thật nào được xử lý."
            )
        }

        message = messages[member]

        EVENTS.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "message": f"{name}: {message}",
            "type": "simulation"
        })

        del EVENTS[12:]

    return jsonify({
        "success": True,
        "message": message
    })


# -----------------------------------------------------
# Lay nhat ky hoat dong
# -----------------------------------------------------

@app.route("/api/events", methods=["GET"])
def get_events():

    with lock:

        return jsonify({
            "events": EVENTS
        })


# =====================================================
# 9. CHAY UNG DUNG
# =====================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
