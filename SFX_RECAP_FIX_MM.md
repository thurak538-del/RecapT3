# Recap Mode — SFX ပြန်ထည့်ခြင်း

Recap mode မှာ SFX မပါသွားစေခဲ့တဲ့ routing အမှားကို ပြင်ထားသည်။ Orchestrator သည် Recap/Dubbing အတွက် Demucs `no_vocals.wav` background stem ကို အခုထုတ်ယူပြီး Story mode သာ မူရင်းအသံကို မထည့်တော့ပါ။ ထို့အပြင် Recap ၏ Smart Sync final render ကလည်း TTS track တစ်ခုတည်းကိုသာ map လုပ်နေခဲ့သည့်အတွက် background stem ကို final video ထဲမထည့်နိုင်ခဲ့ပါ။ ယခု stem ကို source video segment တစ်ခုချင်းစီအလိုက် trim လုပ်၊ Smart Sync narration slot နှင့် အချိန်ကိုက် retime လုပ်ပြီး TTS နှင့် mix လုပ်သည်။

Background stem gain ကို လက်ရှိ mixer နှင့်ကိုက်ညီစေရန် `0.7` ထားသည်။ `no_vocals` stem ထဲတွင် music နှင့် SFX နှစ်မျိုးလုံးပါဝင်သောကြောင့် နှစ်မျိုးစလုံး ပြန်ကြားရမည်။ Demucs က SFX ကို music မှ သီးခြားမခွဲပေးသလို၊ source mix ထဲတွင် SFX/dialogue အလွန်ရောနေပါက artifact သို့မဟုတ် ကျန်စကားသံ အနည်းငယ် ရှိနိုင်သည်။

Synthetic video နှင့် sine-wave background audio ဖြင့် Smart Sync SFX integration test ထည့်ထားသည်။ Test သည် final MP4 မှ audio ကို ပြန်ဖတ်ပြီး background signal ကြားနိုင်ကြောင်း RMS အဆင့်ဖြင့် စစ်ဆေးသည်။ Real user video/Demucs quality ကိုတော့ ဒီ offline test က မစစ်ဆေးပါ။
