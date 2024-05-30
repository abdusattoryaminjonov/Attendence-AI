Talablarni ishlab chiqish
-Tizimning funksional talablari
Funksionalligi.
# Texnik Qismlar
- PYTHON va DGANGOdan foydalanamiz
- SQLITE ma'lumotlar bazasi saqlash uchun ishlatiladi.
- Back-end uchun DGANGO,
# Funksiyalar
1.Insonni tanish moduli
2.Face ni aniqlash moduli
3. Statistik ma’lumotlarni tahlil qilish  moduli
# Ogohlantirishlar va Cheklovlar
- Xato holatlari uchun mos ogohlantirishlar chiqarish.
- Aftarizatsiya

Tizim uchun umumiy va funksional talablarni ishlab chiqish 
 
Har bir tizimni va dasturiy ta’minotni ishlab chiqishda unga qo’yiladigan umumiy va funksional talablarni ishlab chiqish zarur hisoblanadi va talablar yordamida ishlab chiqiladigan tizimni to’liq tasnifi keltiriladi. Asosan dasturiy injiniring sohasi shuni ko’rsatadiki, ko’pchilik hollarda talablarni aniqlash uchun funksional va no-funksional yondashuv amalga oshiriladi. Tizimning funksional talablariga asosan tizim yoki dasturning asosiy bajariladigan funksiyalari kiradi. Boshqacha qilib aytganda, tizimning funksional talablari dasturning nima qilishini ko’rsatib bersa, no-funksional talablar esa shu funksiyalarning qanday amalga oshirilishini ko’rsatib beradi. Undan tashqari dastur interfeysiga qo’yiladigan talablarni ishlab chiqish ham maqsadga muvofiq bo’ladi. Quyidagi jadvallar  asosida “Attendance” tizimi uchun funksional, no-funksional va tizim interfeysi talablari ko’rsatib o’tilgan. 

Tizimning funksional talablari va tasnifi. 
*Prioritet: 1-yuqori, 2-o’rta, 3-past
Jadval. Tizimning finksional talablari 
Talab identifikatori 	Talab 
*prioriteti 	Talab tasnifi 
REQ-01 	1 	Foydalanuvchilar tizimdan foydalanish uchun ro’yhatdan o’tadi 
REQ-02 	1 	Tizimda userlarga  model yarata olishligi.
REQ-03 	2 	Tizimda odamlarning yuzlarini aniqlaydigan  funksiyalar mavjudligi
REQ-04 	2 	Tizimda foydalanuvchilarning ma’lumotlarni boshqaradi 
(qo’shish, o’zgartirish yoki ochirib tashlaydi) 
REQ-05 	1 	Dasturni kodlash va asosiy funksiyalarini ishlab chiqish
REQ-06	2 	Dasturning asosiy maqsadi - turli muassasalardagi xavfsizlikni ta'minlash va odamlarning qayerda, qachon, qay payta va usha biz qidirgan odamligini topish.
REQ-07 	1 	Tizim aniq yaratilgan modellar bilan ishlashi.
REQ-08 	3 	Dastur malumotlar API orqali o’qib olishi.
REQ-09 	3 	Foydalanuvchi ga qulay interface bo’lishi.
REQ-10 	1 	Foydalanuvchilarni Modeldan kelgan malumotlarini jadvalga saqlash(sana , vaqt)
REQ-11	3 	Yuzni aniqlash modelini yaratish va o'qitish.
REQ-12 	2 	Model ishlashini tekshirish 
REQ-13 	2 	Foydalanuvchini o’chirish uchun adminga murojat qilishligi

REQ-14 	          1	Barcha tekshirilgan suratlar bazada yeg’ib borilishi . Modelni aniqroq tanishiga imkon berishi.
*Prioritet: 1-yuqori, 2-o’rta, 3-past 
![image](https://github.com/abdusattoryaminjonov/Attendence-AI/assets/118427554/43c75449-33f2-4776-9ca5-b16c21c3c94f)


Usecase.
Dastur ishlatish jarayoni. 
![image](https://github.com/abdusattoryaminjonov/Attendence-AI/assets/118427554/fd83bf50-dc7a-43ab-8350-3ce605f7a148)


Ilovadan foydalanish bo’limi:
Foydalanuvchilar tizimdan to’liq foydalanish uchun ro’yhatdan o’tkaziladi.
Userlar qismi:
Bu qisimda barcha foydalanuvchilar zo’yhati bo’ladi. Shu yerdan link orqali foydalanuvchilarning profiliga kiriladi . Harqanday o’zgaratirishlar kiritiladi(o’zgartirish, bo’sh qatorni to’ldirish).
Yangi foydalanuvchilarni shu yerdan qo’shiladi . Aftarizatsiya qismi shu yerda .

Model qismi:
Userlar qismida har bir userga tegishli tugma orqali yangi model yaratish.
Model vidyo camera orqali yaratiladi. Keyinchalik Suratlar yuklash imkoniyati boladi.

EDA qismi:
Modeldagi eda taxlili . Modelda neshta class borligi va clarsalrda neshta rasim borligini aniqlaydi. Barcha sonli taxlillar shu qisimda ko’rsatilgan . Natija ko’rsatkichlari.

Live… qismi:
Bu qisimda doyimiy kamera ishlab turadi foydalanuvchilarni tekshirib modelga malumot jo’natib turadi va qaytgan malumotni Attandanse qismiga jo’natadi .

Asosiy(Attentanse) qismi:
Bu qisimda Modeldan qaytgan javobni user ma’lumoti, vaqti va sanasi bo’yicha 
davomat jadvaliga yozib qo’yadi. Attandanse qismida jadvaldagi barcha ma’lumotlarni chiqaradi va ularni boshqaradi. 

Xato holatlari uchun mos ogohlantirishlar chiqarish.
Malumotlarni to’ldirish jarayonida hato malumotlar kiritilsa, ya’niy 8tadan kam harf ishlatsa, qator bo’sh qolsa, muhm qatorga malumot kiritilmasa hatolik bor degan to’g’irlang degan habarlar chiqadi.
Aftarizatsiya:
Aftarizatsiya faqat admin uchun ishlaydi. Dastur faqat Admin tomonidan boshqariladi.

Django foydalanuvchi autentifikatsiya tizimi bilan birga keladi. U foydalanuvchi hisoblari, guruhlar, ruxsatlar va cookie-fayllarga asoslangan foydalanuvchi seanslarini boshqaradi. Hujjatlarning ushbu bo'limi standart dastur qanday ishlashini, shuningdek uni loyihangiz ehtiyojlariga moslashtirish uchun qanday kengaytirish va sozlashni tushuntiradi.

Django autentifikatsiya tizimi autentifikatsiya va avtorizatsiya bilan shug'ullanadi. Qisqacha aytganda, autentifikatsiya foydalanuvchining o'zini kimligini tasdiqlaydi va avtorizatsiya autentifikatsiya qilingan foydalanuvchiga nima qilishiga ruxsat berilganligini aniqlaydi. Bu erda autentifikatsiya atamasi ikkala vazifaga nisbatan qo'llaniladi.
