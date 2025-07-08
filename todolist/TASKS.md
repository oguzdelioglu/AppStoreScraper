### Proje: App Store Fırsat Analiz Aracı

**Ana Hedef:** App Store'un Top Listelerini anlık olarak analiz ederek, yeni çıkan veya trend olan uygulamaları tespit etmek, bu uygulamaların potansiyel anahtar kelimelerini ve bu kelimelerin rekabet yoğunluğunu belirleyerek, kullanıcıya yeni uygulama fikirleri sunan bir raporu CSV formatında oluşturmak.

---

### **Aşama 1: Proje Temelleri ve Kurulum**

Bu aşama, projenin çalışması için gerekli olan dosya ve klasör yapısını oluşturmayı ve bağımlılıkları belirlemeyi içerir.

*   **Task 1.1: Dizin Yapısını Oluşturma**
    *   `todolist/` adında bir klasör oluşturulacak. (Onayınız sonrası görev listesi buraya kaydedilecek).
    *   `src/` adında bir ana kaynak kodu klasörü oluşturulacak. Bu, kodun düzenli kalmasını sağlar.

*   **Task 1.2: Bağımlılıkları Belirleme**
    *   Proje ana dizininde `requirements.txt` adında bir dosya oluşturulacak.
    *   İçerisine aşağıdaki kütüphaneler eklenecek:
        *   `requests`  # API istekleri yapmak için.
        *   `pandas`    # Verileri kolayca işlemek ve CSV olarak kaydetmek için.

*   **Task 1.3: Boş Python Dosyalarını Oluşturma**
    *   Proje ana dizininde `main.py` dosyası oluşturulacak. Bu, programın başlangıç noktası olacak.
    *   `src/` klasörü içinde `itunes_api.py` dosyası oluşturulacak. Tüm iTunes API iletişimi bu dosyada toplanacak.
    *   `src/` klasörü içinde `analysis.py` dosyası oluşturulacak. Verilerin analiz ve işleme mantığı burada yer alacak.
    *   `src/` klasörü içinde `__init__.py` adında boş bir dosya oluşturulacak. Bu, `src` klasörünün bir Python paketi olarak tanınmasını sağlar.

### **Aşama 2: iTunes API İstemcisi (`src/itunes_api.py`)**

Bu modül, Apple'ın sunucularıyla tüm iletişimi yönetecek. Dış dünyaya açılan kapımız olacak.

*   **Task 2.1: Temel API Fonksiyonu**
    *   `_make_request(endpoint, params)` adında özel bir yardımcı fonksiyon yazılacak. Bu fonksiyon, tüm API isteklerinde tekrar eden kısımları (hata kontrolü, JSON'a çevirme) yönetecek. `requests.get()` çağrısını yapacak ve `try-except` blokları ile ağ hatalarını yakalayacak.

*   **Task 2.2: Top Listeleri Çekme Fonksiyonu**
    *   `get_top_app_ids(country, category, limit=100)` adında bir fonksiyon tanımlanacak.
    *   **Girdiler:** `country` (örn: 'us'), `category` (örn: 'top-free'), `limit` (kaç uygulama çekileceği).
    *   **İşlev:** Apple'ın RSS beslemesi API'sine istek atarak belirtilen ülkenin ve kategorinin en popüler uygulamalarının ID listesini çekecek.
    *   **Çıktı:** Uygulama ID'lerini içeren bir Python listesi (örn: `['id123', 'id456', ...]`).

*   **Task 2.3: Uygulama Detaylarını Çekme Fonksiyonu**
    *   `get_app_details(app_id, country)` adında bir fonksiyon tanımlanacak.
    *   **Girdiler:** `app_id` (tek bir uygulama ID'si), `country`.
    *   **İşlev:** iTunes Search API'nin `lookup` özelliğini kullanarak tek bir uygulamanın tüm detaylarını (isim, geliştirici, açıklama, yayınlanma tarihi, puan, kategori vb.) çekecek.
    *   **Çıktı:** Uygulama detaylarını içeren bir Python sözlüğü (`dict`).

*   **Task 2.4: Anahtar Kelime Arama Sonucu Sayısını Alma Fonksiyonu**
    *   `get_search_result_count(term, country)` adında bir fonksiyon tanımlanacak.
    *   **Girdiler:** `term` (aranacak anahtar kelime), `country`.
    *   **İşlev:** iTunes Search API'yi kullanarak bir anahtar kelime için arama yapacak ve sadece arama sonucu sayısını (`resultCount`) alacak. Bu, bizim "Tahmini Rekabet Yoğunluğu" metriğimiz olacak.
    *   **Çıktı:** Bir tamsayı (`int`) (örn: `2451`).

### **Aşama 3: Analiz Motoru (`src/analysis.py`)**

Bu modül, API'den gelen ham veriyi işleyip anlamlı bilgilere dönüştürecek olan projenin beynidir.

*   **Task 3.1: Anahtar Kelime Çıkarıcı**
    *   `extract_keywords_from_text(text, num_keywords=5)` adında bir fonksiyon yazılacak.
    *   **İşlev:** Verilen metni (uygulama adı + açıklama) alacak, genelgeçer kelimeleri ("ve", "bir", "için" gibi - "stop words") temizleyecek, kelimelerin frekansını sayacak ve en sık geçen `num_keywords` adedini döndürecek.
    *   **Çıktı:** Anahtar kelimeleri içeren bir liste (örn: `['photo', 'editor', 'filters', 'effects', 'collage']`).

*   **Task 3.2: "Yeni Uygulama" Tespiti**
    *   `is_app_considered_new(release_date_str, days_threshold=60)` adında bir fonksiyon yazılacak.
    *   **İşlev:** API'den gelen yayınlanma tarihi metnini alıp Python'un `datetime` objesine çevirecek. Bugünün tarihi ile arasındaki farkı hesaplayacak. Fark `days_threshold`'dan küçükse `True` döndürecek.
    *   **Çıktı:** `True` veya `False`.

### **Aşama 4: Ana Betik ve Kullanıcı Arayüzü (`main.py`)**

Bu dosya, tüm parçaları bir araya getirip orkestrayı yönetecek ve kullanıcı ile etkileşime girecek.

*   **Task 4.1: Kullanıcı Girdilerini Alma**
    *   Program başladığında kullanıcıya hangi ülke için analiz yapmak istediğini soracak (`input()`).
    *   Kullanıcıya analiz edilecek Top Chart kategorisini bir menü şeklinde sunacak ve seçim yapmasını isteyecek (örn: 1: En Popüler Ücretsiz, 2: En Popüler Ücretli).

*   **Task 4.2: Ana İş Akışını Yönetme**
    *   Bir `main()` fonksiyonu içinde tüm süreci yönetecek.
    *   `itunes_api.get_top_app_ids()` fonksiyonunu çağırarak en popüler uygulama ID'lerini alacak.
    *   Konsola "Liste çekildi, X uygulama bulundu. Analiz başlıyor..." gibi bir bilgi basacak.

*   **Task 4.3: Uygulama Analiz Döngüsü**
    *   Alınan her bir uygulama ID'si için bir `for` döngüsü başlatacak.
    *   **Her döngü adımında:**
        1.  Konsola `[X/Y] 'Uygulama Adı' analiz ediliyor...` yazacak.
        2.  `itunes_api.get_app_details()` ile uygulamanın detaylarını çekecek.
        3.  `analysis.is_app_considered_new()` ile uygulamanın yeni olup olmadığını kontrol edecek.
        4.  `analysis.extract_keywords_from_text()` ile anahtar kelimeleri bulacak.
        5.  Bulunan her anahtar kelime için `itunes_api.get_search_result_count()` ile rekabet yoğunluğunu ölçecek.
        6.  Tüm bu bilgileri tek bir sözlükte toplayıp genel bir sonuç listesine ekleyecek.

*   **Task 4.4: Raporlama ve CSV Oluşturma**
    *   Döngü bittiğinde, konsola "Analiz tamamlandı. Rapor oluşturuluyor..." yazacak.
    *   Toplanan sonuçlar listesini `pandas.DataFrame` objesine dönüştürecek.
    *   DataFrame'i, dinamik bir isme sahip (örn: `AppStore_Top_Free_US_2025-07-09.csv`) bir CSV dosyasına `to_csv()` metodu ile kaydedecek.
    *   Kullanıcıya "Rapor başarıyla 'dosya_adı.csv' olarak kaydedildi." mesajını gösterecek.

### **Aşama 5: Dokümantasyon ve Son Dokunuşlar**

*   **Task 5.1: README Dosyasını Güncelleme**
    *   `README.md` dosyasını projenin ne işe yaradığını, nasıl kurulacağını (`pip install -r requirements.txt`) ve nasıl çalıştırılacağını (`python main.py`) detaylı bir şekilde açıklayacak şekilde düzenleyecek.
