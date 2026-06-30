import telebot
import requests
import json
import os

# هسة المفاتيح مخفية ومحد يگدر يشوفها بالكود
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
# 3. هناااا تفاصيل منصة Tadawulx (عدلها واكتب اللي يعجبك)
DATA_TADAWULX = """
معلومات رسمية وأكيدة عن منصة Tadawulx للاستثمار والتداول:
1. رابط التسجيل وإنشاء حساب جديد هو: [اكتب الرابط هنا مثلاً https://vip-tadaw.github.io/uIX/]
2. طرق الإيداع والسحب المدعومة: (Benance، okx حوالة، بطاقات ، والعملات الرقمية USDT).
3. أوقات السحب والإيداع: السحب فوري ويستغرق من 5 دقائق إلى ساعتين كحد أقصى.
4. أقل مبلغ للاستثمار وبدء التداول هو: [اكتب أقل مبلغ هنا، مثلاً 10 دولار كما يمكنك مضاعفه العداد].
5. الدعم الفني: متواجدين لخدمتكم 24 ساعة طيلة أيام الأسبوع، وتكدر تتواصل وياهم عبر [@virla439].
6. الأمان: المنصة محمية ومؤمنة بأعلى تقنيات التشفير لضمان سلامة أموال وأرباح المشتركين.
"""

# شخصية البوت الأساسية
PROMPT_PERSONALITY = (
    f"أنت المساعد الذكي والمرحب بلاعضاء لمنصة Tadawulx للاستثمار. تحدث كانك مدير و بلفصحه  "
    f"بأسلوب لطيف، ودود، ومحترم. مهمتك الترحيب بأي شخص يراسلك ببرود اهلا استاذ وتجيب عن أسئلته وتتشاقه وياه بذكاء.\n"
    f"استعن بهذه المعلومات الرسمية عن المنصة للإجابة على الأسئلة بدقة:\n{DATA_TADAWULX}\n"
    f"تنبيه مهم: حافظ على سياق المحادثة المرفقة في الأسفل (الذاكرة) ورد بناءً عليها باللهجة العراقية وبشكل مختصر ومناسب للتليكرام."
        f"تعلمهم عل اشتراك تشحن رصيد تقوم بمراسلة المدير لشحن حسابك ثم تذهب الى الشريط السفلي وتضغط على تحديد الكمي وتذهب الى الباقه المراد شراىها"
    f"تسئلهم يوميا هل قمت تفعيل باكمال مهامك اليوم حلوو استاذ سحبت حلوو اين تعمل بهذه الارباح قم بشراء هاتف احدث او يمكنك زياده ارباحك من مضاعفه العداد يمكنك استغلال هذه الفرصه الاقوياء لايمكنهم التردد في هذه الحياه التردد قد يضيع الفرص ومن واذا شخص دز صوره كله هذه الصوره واضحه ما اسم جهازك لكي اشتري منه واسئل اي شخص كله  هل لديك فريق معك اذا كال لا كله لا تحزن نحن معك دائما واذا كال اي كيف كانت تجربتك مع فريقك هل هم قامو بلاشتراك مثلك انته بطل لو مترددين وكيف وماهو السبب في عدم جعلك تستفاد اكثر واذا واحد يغلط كله لا هل في احد قام بزعلك اليوم"
)

# قاموس لحفظ ذاكرة المحادثات لكل مستخدم
user_sessions = {}

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        user_sessions[user_id] = []
        
    user_sessions[user_id].append({"role": "user", "parts": [{"text": message.text}]})
    
    if len(user_sessions[user_id]) > 10:
        user_sessions[user_id] = user_sessions[user_id][-10:]
        
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "systemInstruction": {
                "parts": [{"text": PROMPT_PERSONALITY}]
            },
            "contents": user_sessions[user_id]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        bot_reply = response_data['candidates'][0]['content']['parts'][0]['text']
        
        user_sessions[user_id].append({"role": "model", "parts": [{"text": bot_reply}]})
        
        bot.reply_to(message, bot_reply)
        
    except Exception as e:
        bot.reply_to(message, "صار عندي شورت بالعقل، ثواني وراجعلك! 🛠")
        print(f"Error: {e}")

print("البوت العراقي المطور جاهز بالتفاصيل الجديدة.. شغل وجرب!")
bot.infinity_polling()