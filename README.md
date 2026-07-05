# پروژه تحلیل و یادگیری ماشین آگهی‌های املاک دیوار

پروژه گروهی بوت‌کمپ هوش مصنوعی کوئرا برای تحلیل آماری، آزمون فرض، خوشه‌بندی و مدل‌سازی روی دیتاست آگهی‌های املاک دیوار.

## اعضای تیم

* علی
* بنیامین
* لیلا
* تینا

## ساختار پروژه

```text
divar-ml-project/
├── README.md
├── .gitignore
├── requirements.txt
├── utils.py
└── notebooks/
    ├── 01_preprocessing.ipynb
    ├── 02_descriptive_stats.ipynb
    ├── 03_hypothesis_tests.ipynb
    ├── 04_clustering.ipynb
    ├── 05_prediction.ipynb
    └── work/
```

توضیح فایل‌ها:

* `README.md`: نقشه کلی پروژه، مسیر فایل‌ها، قوانین تیمی و وضعیت خروجی‌ها
* `.gitignore`: جلوگیری از آپلود فایل‌های دیتا و فایل‌های موقت
* `requirements.txt`: کتابخانه‌های موردنیاز پروژه
* `utils.py`: توابع مشترک پروژه مانند تبدیل تاریخ، تبدیل UTM و توابع کمکی قیمت
* `01_preprocessing.ipynb`: نوت‌بوک اصلی preprocessing و ادغام کارهای اعضای تیم
* `02_descriptive_stats.ipynb`: آمار توصیفی
* `03_hypothesis_tests.ipynb`: آزمون فرض
* `04_clustering.ipynb`: خوشه‌بندی و توصیه‌گر
* `05_prediction.ipynb`: پیش‌بینی قیمت
* `notebooks/work/`: نوت‌بوک‌های کاری هر نفر قبل از ادغام

## دسترسی به داده‌ها

داده‌ها روی Google Drive نگه‌داری می‌شوند و نباید داخل GitHub آپلود شوند.

### پوشه دیتای خام

```text
/content/drive/MyDrive/Divar Dataset/
```

فایل‌های اصلی:

```text
Divar.csv
iran_city_classification.csv
```

### پوشه خروجی‌های تیم

```text
/content/drive/MyDrive/divar_project/
```

فایل‌های خروجی preprocessing:

```text
cleaned_step1.parquet
cleaned_step2_benyamin_v2.parquet
cleaned_step3_geo.parquet
```

برای لود دیتای خام:

```python
df = pd.read_csv("/content/drive/MyDrive/Divar Dataset/Divar.csv")
```

برای لود آخرین نسخه تمیزشده:

```python
df = pd.read_parquet("/content/drive/MyDrive/divar_project/cleaned_step3_geo.parquet")
```

برای لود خروجی‌های میانی preprocessing:

```python
df_step1 = pd.read_parquet("/content/drive/MyDrive/divar_project/cleaned_step1.parquet")
df_step2 = pd.read_parquet("/content/drive/MyDrive/divar_project/cleaned_step2_benyamin_v2.parquet")
df_step3 = pd.read_parquet("/content/drive/MyDrive/divar_project/cleaned_step3_geo.parquet")
```

نکته: خروجی‌های تمیزشده با فرمت `parquet` ذخیره شده‌اند تا نوع داده‌ها مثل `category`، `boolean`، `datetime` و `Int64` بهتر حفظ شوند.

## محیط اجرا

* اجرای کدها: Google Colab
* نگه‌داری کدها: GitHub
* نگه‌داری داده‌ها: Google Drive

برای نصب کتابخانه‌های موردنیاز:

```python
!pip install -r requirements.txt
```

در صورتی که نوت‌بوک مستقیم در Colab اجرا شود و فایل `requirements.txt` در همان مسیر در دسترس نباشد، کتابخانه‌های اصلی می‌توانند جداگانه نصب شوند:

```python
!pip install -q jdatetime utm pyarrow
```

## نکات مهم درباره داده

* ستون‌های `transformable_price` و `rent_credit_transform` با وجود نامشان، مقدار عددی قیمت نیستند و به‌عنوان flagهای `True/False` استفاده می‌شوند.
* قیمت فروش در ستون `price_value` قرار دارد.
* مقدار رهن در ستون `credit_value` قرار دارد.
* مقدار اجاره در ستون `rent_value` قرار دارد.
* بعضی از مقدارهای گم‌شده ساختاری هستند و نباید با مقدار کلی پر شوند.
* ستون‌هایی مثل `land_size`، `floor`، `total_floors_count`، `unit_per_floor`، `regular_person_capacity` و ستون‌های `transformed_*` در بسیاری از ردیف‌ها عمداً خالی باقی مانده‌اند، چون معنی آن‌ها به نوع آگهی وابسته است.
* برای تحلیل قیمت، ردیف‌ها حذف نشده‌اند؛ به‌جای حذف، flagهای اعتبارسنجی ساخته شده‌اند.
* برای تحلیل جغرافیایی نیز ردیف‌ها حذف نشده‌اند؛ فقط ردیف‌های قابل استفاده با flag مشخص شده‌اند.

## خروجی مرحله اول preprocessing

در مرحله اول، دیتای خام خوانده شد و عملیات پایه preprocessing انجام شد.

کارهای اصلی این مرحله:

* حذف ستون اضافی `Unnamed: 0`
* اصلاح نوع داده ستون‌های عددی
* تبدیل ستون‌های بولین به نوع مناسب
* تبدیل مقدار `unselect` به `NaN`
* تبدیل تاریخ میلادی `created_at_month` به تاریخ شمسی
* ساخت ستون‌های `created_at_shamsi` و `created_at_shamsi_readable`
* حذف چند ستون غیرضروری مربوط به اجاره روزانه
* پر کردن مقدارهای گم‌شده `construction_year` با میانه کل
* پر کردن مقدارهای گم‌شده `rooms_count` و `building_size` با میانه هر `cat3_slug`
* حذف ردیف‌هایی که ستون‌های کلیدی `title`، `cat3_slug` یا `city_slug` را ندارند

خروجی این مرحله:

```text
cleaned_step1.parquet
```

خلاصه خروجی:

```text
total_rows: 999,943
output_columns_count: 53
dropped_rows: 57
```

## خروجی مرحله دوم preprocessing

در مرحله دوم، کدهای بنیامین روی خروجی مرحله اول اجرا شد.

در این مرحله ستون‌های مربوط به قیمت، متراژ، قیمت هدف و flagهای اعتبارسنجی ساخته شدند. هیچ ردیفی در این مرحله حذف نشده است.

ستون‌های مهم ساخته‌شده:

* `transaction_type`: نوع معامله شامل فروش، اجاره، اجاره موقت یا سایر موارد
* `price_value_pos`: نسخه مثبت قیمت فروش
* `rent_value_pos`: نسخه مثبت اجاره
* `credit_value_pos`: نسخه مثبت رهن
* `building_size_pos`: نسخه مثبت متراژ بنا
* `land_size_pos`: نسخه مثبت متراژ زمین
* `area_for_unit_price`: متراژ مبنا برای محاسبه قیمت واحد
* `monthly_rent_equivalent`: معادل اجاره ماهانه برای آگهی‌های اجاره
* `credit_equivalent`: معادل رهن برای آگهی‌های اجاره
* `sale_price_per_m2`: قیمت فروش به ازای هر متر مربع
* `monthly_rent_equivalent_per_m2`: اجاره ماهانه معادل به ازای هر متر مربع
* `credit_equivalent_per_m2`: رهن معادل به ازای هر متر مربع
* `target_price`: قیمت هدف برای تحلیل و مدل‌سازی
* `target_price_type`: نوع قیمت هدف
* `target_price_per_m2`: قیمت هدف به ازای هر متر مربع
* `is_valid_for_price_analysis`: flag نهایی برای انتخاب ردیف‌های مناسب تحلیل قیمت
* `has_geo`: مشخص می‌کند ردیف مختصات جغرافیایی دارد یا نه
* `is_valid_geo_basic`: اعتبارسنجی اولیه مختصات جغرافیایی

خروجی این مرحله:

```text
cleaned_step2_benyamin_v2.parquet
```

خلاصه خروجی:

```text
total_rows: 999,943
rows_with_target_price: 917,334
valid_for_price_analysis: 877,587
invalid_for_price_analysis: 122,356
rows_with_geo: 655,594
invalid_geo_rows: 18
output_columns_count: 78
```

## خروجی مرحله سوم preprocessing

در مرحله سوم، پردازش جغرافیایی داده‌ها توسط علی انجام شد.

در این مرحله ردیف‌ها حذف نشدند. ابتدا مختصات جغرافیایی بررسی شد، سپس برای ردیف‌هایی که مختصات معتبر داشتند، تبدیل latitude و longitude به UTM انجام شد.

ستون‌های مهم ساخته‌شده:

* `is_valid_geo_for_analysis`: flag نهایی برای مشخص کردن ردیف‌های قابل استفاده در تحلیل جغرافیایی
* `utm_easting`: مختصات UTM در محور شرقی-غربی
* `utm_northing`: مختصات UTM در محور شمالی-جنوبی
* `utm_zone_number`: شماره zone در سیستم UTM
* `utm_zone_letter`: حرف zone در سیستم UTM

منطق ستون `is_valid_geo_for_analysis`:

* مقدار `True`: ردیف مختصات معتبر دارد و برای تحلیل جغرافیایی قابل استفاده است.
* مقدار `False`: ردیف مختصات ندارد یا مختصات آن نامعتبر است.

خروجی این مرحله:

```text
cleaned_step3_geo.parquet
```

خلاصه خروجی:

```text
total_rows: 999,943
valid_geo_for_analysis: 655,576
invalid_or_missing_geo_for_analysis: 344,367
invalid_geo_rows: 18
output_columns_count: 83
```

بررسی zoneهای UTM نشان داد داده‌ها در چند zone مختلف قرار دارند. بیشترین حجم داده در zone زیر است:

```text
UTM zone 39S: 452,153 rows ≈ 68.97%
```

نکته: چون داده‌ها در چند zone مختلف UTM قرار دارند، در مراحل بعدی، مخصوصاً clustering سراسری، نباید `utm_easting` و `utm_northing` بدون توجه به `utm_zone_number` و `utm_zone_letter` مستقیم با هم مقایسه شوند.

## خروجی نهایی preprocessing

آخرین فایل آماده برای استفاده در مراحل بعدی پروژه:

```text
cleaned_step3_geo.parquet
```

مشخصات فایل نهایی:

```text
rows: 999,943
columns: 83
rows_with_target_price: 917,334
valid_for_price_analysis: 877,587
valid_geo_for_analysis: 655,576
```

## قوانین کار تیمی

* هر نفر فقط روی نوت‌بوک مربوط به فاز خودش کار می‌کند.
* همزمان دو نفر روی یک فایل مشترک کار نمی‌کنند.
* قبل از شروع کار، آخرین نسخه فایل‌ها از GitHub گرفته می‌شود.
* بعد از اتمام هر بخش، commit با پیام واضح ثبت می‌شود.
* commitهای کوچک و مکرر بهتر از یک commit بزرگ و مبهم هستند.
* فایل‌های دیتا نباید داخل GitHub آپلود شوند.
* نام فایل‌ها و مسیرها نباید فاصله داشته باشند.
* خروجی‌های سنگین فقط در Google Drive نگه‌داری می‌شوند.

## تقسیم وظایف

### آماده‌سازی داده

* مدیریت مقادیر گم‌شده: علی ✅
* اصلاح نوع داده‌ها: علی ✅
* تبدیل تاریخ شمسی: علی ✅
* ساخت خروجی مرحله اول preprocessing: علی ✅
* ساخت ستون قیمت واحد: بنیامین ✅
* ساخت قیمت هدف و معادل‌سازی رهن/اجاره: بنیامین ✅
* مدیریت داده‌های پرت قیمت و متراژ با flag: بنیامین ✅
* ساخت خروجی مرحله دوم preprocessing: بنیامین ✅
* بررسی و آماده‌سازی داده‌های جغرافیایی: علی ✅
* تبدیل مختصات latitude/longitude به UTM: علی ✅
* ساخت خروجی مرحله سوم preprocessing: علی ✅
* ادغام نهایی در نوت‌بوک اصلی `01_preprocessing.ipynb`: علی ✅
* جمع‌بندی و مستندسازی دیتا: تینا

### آمار توصیفی

* سؤال ۱، ۲، ۳: لیلا
* سؤال ۴، ۵: بنیامین
* سؤال ۶، ۷: علی
* سؤال ۸، ۹: تینا

### آزمون فرض

* فرضیه ۱: علی
* فرضیه ۲: بنیامین
* فرضیه ۳: لیلا
* فرضیه ۴: تینا

### یادگیری ماشین

تقسیم وظایف بخش خوشه‌بندی و پیش‌بینی قیمت بعداً نهایی و به README اضافه می‌شود.
