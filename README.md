# TikTok Image Telegram Bot

بوت Telegram يستقبل رابط TikTok ويحاول استخراج الصور فقط وإرسالها للمستخدم.

## التشغيل محليًا

1. ثبّت Python 3.10 أو أحدث.
2. نفّذ:
   `pip install -r requirements.txt`
3. انسخ `.env.example` إلى `.env` وضع توكن البوت في `BOT_TOKEN`.
4. عيّن متغير البيئة `BOT_TOKEN` ثم شغّل:
   `python bot.py`

على Windows PowerShell:
`$env:BOT_TOKEN="توكن_البوت"`
`python bot.py`

## التشغيل على Render

المشروع مهيأ كـ Worker عبر `render.yaml`.

- ارفع المشروع إلى GitHub.
- في Render اختر New > Blueprint ثم اختر المستودع.
- أضف قيمة `BOT_TOKEN` من BotFather.
- Deploy.

## ملاحظات

استخدم البوت فقط مع المحتوى الذي تملك حق تنزيله أو إعادة استخدامه، والتزم بشروط TikTok وحقوق أصحاب المحتوى.
