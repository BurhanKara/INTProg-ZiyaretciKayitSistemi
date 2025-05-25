🏨 Otel Rezervasyon Yönetim Paneli


🧾 Proje Tanıtımı:
Bu web tabanlı uygulama, bir otelin rezervasyon sürecini ve müşteri yorumlarını yönetmek amacıyla geliştirilmiş bir yönetim panelidir. Flask framework’ü ile geliştirilmiş olup, kullanıcı girişi, yorum yapma, yorumları düzenleme/silme ve genel panel üzerinden sistemin kontrolü gibi işlevler sunar. Yönetici paneli üzerinden kullanıcı işlemleri ve yor


🚀 Proje Özellikleri

🔐 Kullanıcı kayıt ve giriş işlemleri

💬 Kullanıcıların yorum ekleyebilmesi

🛠️ Yorumları düzenleme ve silme

🧑‍💼 Yönetici paneli üzerinden kullanıcıları ve yorumları görüntüleme/silme

📦 SQLite veritabanı ile kalıcı veri saklama

🎨 Bootstrap ile responsive ve sade arayüz tasarımı

⚙️ Kurulum ve Çalıştırma


✅ Gereksinimler
Bu projeyi çalıştırmak için bilgisayarınızda aşağıdaki yazılımlar kurulu olmalıdır:
Python 3.x
Ayrıca aşağıdaki Python kütüphaneleri kullanılmaktadır:
Flask
Flask-Login
Flask-SQLAlchemy
Werkzeug

├── app.py                  # Ana Python uygulama dosyası
├── templates/              # HTML şablonları
│   ├── base.html           # Ortak sayfa şablonu (header/footer)
│   ├── index.html          # Anasayfa
│   ├── login.html          # Giriş formu
│   ├── register.html       # Kayıt formu
│   ├── dashboard.html      # Kullanıcı kontrol paneli
│   ├── yorum_paneli.html   # Yorum yapma ve görüntüleme sayfası
│   ├── destek.html         # Destek sayfası
│   ├── iletisim.html       # İletişim sayfası
│   ├── restoran.html       # Restoran bilgilendirme sayfası
│   ├── siparis.html        # Sipariş sayfası
│   ├── yorumlar.html       # Yorum sayfası
│   └── admin_panel.html    # Yönetici paneli (kullanıcı ve yorum yönetimi)
├── static/
│   └── styles.css          # CSS stil dosyası
├── requirements.txt        # Kullanılan kütüphaneler
└── README.md               # Proje açıklama dosyası
