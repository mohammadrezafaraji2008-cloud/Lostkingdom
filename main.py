import json, os, random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

SAVE = 'lost_kingdom_save.json'
ENEMIES = [('Wild Wolf',35,(6,12),5,12,20),('Bandit',45,(8,14),10,20,30),('Skeleton Warrior',55,(10,17),12,25,40),('Orc',75,(12,21),20,35,60)]
WEAPONS = [('Wooden Sword',10,10),('Iron Sword',35,17),('Steel Sword',80,25),('Legendary Sword',160,35)]
ARMORS = [('Simple Clothes',0,0),('Leather Armor',40,4),('Iron Armor',90,8),('Guardian Armor',170,13)]
SHIELDS = [('No Shield',0,0),('Wooden Shield',25,10),('Iron Shield',60,20),('Steel Shield',120,30),('Guardian Shield',200,40)]
LOC = {'Village':['Forest','Plains','Market'],'Forest':['Village','Cave','Plains'],'Plains':['Village','Forest','Castle'],'Market':['Village'],'Cave':['Forest','Castle'],'Castle':['Plains','Cave']}

T = {
    'en': {
        'title':'THE LOST KINGDOM','start':'START NEW GAME','continue':'CONTINUE GAME','exit':'EXIT',
        'language':'LANGUAGE','english':'ENGLISH','persian':'PERSIAN','guide':'GUIDE','back':'BACK',
        'choose_language':'CHOOSE YOUR DEFAULT LANGUAGE','language_saved':'Language selected: English',
        'hero_name':'Hero Name','enter_name':'Enter hero name','start_btn':'START',
        'move':'MOVE','explore':'EXPLORE','fight':'RANDOM FIGHT','shop':'SHOP','inventory':'INVENTORY','stats':'STATS','rest':'REST','boss':'CASTLE / BOSS','save':'SAVE GAME','title_btn':'EXIT TO TITLE',
        'where':'WHERE DO YOU WANT TO GO?','not_energy':'Not enough energy.','combat':'COMBAT','your_hp':'Your HP','enemy_hp':'Enemy HP',
        'attack':'ATTACK','power':'POWER ATTACK (15 ENERGY)','defense':'DEFENSE (+10 ENERGY)','potion':'USE POTION','run':'RUN AWAY',
        'saved':'Game saved.','no_save':'No save file found.','defeated':'You were defeated.','not_potion':'Cannot use a potion now.','rested':'Rested. Health and energy restored.','reach_castle':'Reach the Castle first.','boss_done':'You already defeated the Dark King.',
        'shop_gold':'SHOP\nGold: {}','potion_price':'Health Potion - 15 Gold','shields':'SHIELDS','block':'{}% block',
        'inv':'INVENTORY','weapon':'Weapon','armor':'Armor','shield':'Shield','potions':'Potions','gold':'Gold','hero_stats':'HERO STATS','name':'Name','level':'Level','hp':'HP','energy':'Energy','attack_stat':'Attack','defense_stat':'Defense','shield_block':'Shield Block','xp':'XP','day':'Day',
        'guide_title':'HOW TO PLAY','guide_text':'1. Move between locations and explore the world.\n\n2. Explore costs Energy but can give Gold, XP, Potions, healing, or start a battle.\n\n3. In battle, ATTACK deals normal damage. POWER ATTACK costs 15 Energy and deals heavy damage.\n\n4. DEFENSE restores 10 Energy and reduces the next enemy hit by 50%.\n\n5. Your Shield reduces incoming damage by its Block percentage.\n\n6. Buy stronger weapons, armor, and shields in the Shop.\n\n7. Rest to recover HP and fully restore Energy.\n\n8. Reach the Castle and defeat the Dark King to win!','found_gold':'You found {} gold!','found_potion':'You found a health potion!','found_heal':'You found a healing herb: +{} HP.','found_xp':'You found an old book: +{} XP.','not_enough':'Not enough energy.','defeated_enemy':'You defeated {}!\n+{} Gold\n+{} XP','dark_win':'YOU DEFEATED THE DARK KING!\nThe kingdom is free!','buy_hint':'Buy stronger equipment by selecting an item.','purchase_failed':'You need more Gold or this item is not stronger than your current one.'
    },
    'fa': {
        'title':'پادشاهی گمشده','start':'شروع بازی جدید','continue':'ادامه بازی','exit':'خروج',
        'language':'زبان','english':'انگلیسی','persian':'فارسی','guide':'راهنما','back':'بازگشت',
        'choose_language':'زبان پیش‌فرض خود را انتخاب کنید','language_saved':'زبان انتخاب شد: فارسی',
        'hero_name':'نام قهرمان','enter_name':'نام قهرمان را وارد کنید','start_btn':'شروع',
        'move':'حرکت','explore':'جست‌وجو','fight':'مبارزه تصادفی','shop':'فروشگاه','inventory':'وسایل','stats':'آمار','rest':'استراحت','boss':'قلعه / رئیس','save':'ذخیره بازی','title_btn':'بازگشت به صفحه اصلی',
        'where':'کجا می‌خواهید بروید؟','not_energy':'انرژی کافی نیست.','combat':'مبارزه','your_hp':'جان شما','enemy_hp':'جان دشمن',
        'attack':'حمله','power':'حمله قدرتمند (۱۵ انرژی)','defense':'دفاع (+۱۰ انرژی)','potion':'استفاده از معجون','run':'فرار',
        'saved':'بازی ذخیره شد.','no_save':'فایل ذخیره‌ای پیدا نشد.','defeated':'شما شکست خوردید.','not_potion':'اکنون نمی‌توانید از معجون استفاده کنید.','rested':'استراحت کردید. جان و انرژی بازیابی شد.','reach_castle':'ابتدا به قلعه برسید.','boss_done':'شما قبلاً پادشاه تاریک را شکست داده‌اید.',
        'shop_gold':'فروشگاه\nطلا: {}','potion_price':'معجون سلامتی - ۱۵ طلا','shields':'سپرها','block':'{}٪ کاهش آسیب',
        'inv':'وسایل','weapon':'سلاح','armor':'زره','shield':'سپر','potions':'معجون','gold':'طلا','hero_stats':'آمار قهرمان','name':'نام','level':'سطح','hp':'جان','energy':'انرژی','attack_stat':'حمله','defense_stat':'دفاع','shield_block':'کاهش آسیب سپر','xp':'تجربه','day':'روز',
        'guide_title':'راهنمای بازی','guide_text':'۱. بین مکان‌ها حرکت کنید و جهان بازی را جست‌وجو کنید.\n\n۲. جست‌وجو انرژی مصرف می‌کند اما ممکن است طلا، تجربه، معجون یا سلامتی به دست آورید یا وارد مبارزه شوید.\n\n۳. در مبارزه، «حمله» آسیب عادی وارد می‌کند. «حمله قدرتمند» ۱۵ انرژی مصرف می‌کند و آسیب بیشتری وارد می‌کند.\n\n۴. «دفاع» ۱۰ انرژی به شما برمی‌گرداند و آسیب ضربه بعدی دشمن را ۵۰٪ کاهش می‌دهد.\n\n۵. سپر شما بر اساس درصد Block، آسیب دریافتی را کاهش می‌دهد.\n\n۶. در فروشگاه سلاح، زره و سپرهای قوی‌تر بخرید.\n\n۷. با استراحت، جان و تمام انرژی خود را بازیابی کنید.\n\n۸. به قلعه برسید و پادشاه تاریک را شکست دهید تا برنده شوید!', 'found_gold':'{} طلا پیدا کردید!','found_potion':'یک معجون سلامتی پیدا کردید!','found_heal':'گیاه شفابخش پیدا کردید: +{} جان.','found_xp':'یک کتاب قدیمی پیدا کردید: +{} تجربه.','not_enough':'انرژی کافی نیست.','defeated_enemy':'{} را شکست دادید!\n+{} طلا\n+{} تجربه','dark_win':'پادشاه تاریک را شکست دادید!\nپادشاهی آزاد شد!','buy_hint':'برای خرید تجهیزات قوی‌تر، یک مورد را انتخاب کنید.','purchase_failed':'طلای کافی ندارید یا این وسیله از وسیله فعلی قوی‌تر نیست.'
    }
}

ITEM_FA = {
    'Wooden Sword':'شمشیر چوبی','Iron Sword':'شمشیر آهنی','Steel Sword':'شمشیر فولادی','Legendary Sword':'شمشیر افسانه‌ای',
    'Simple Clothes':'لباس ساده','Leather Armor':'زره چرمی','Iron Armor':'زره آهنی','Guardian Armor':'زره نگهبان',
    'No Shield':'بدون سپر','Wooden Shield':'سپر چوبی','Iron Shield':'سپر آهنی','Steel Shield':'سپر فولادی','Guardian Shield':'سپر نگهبان',
    'Village':'روستا','Forest':'جنگل','Plains':'دشت','Market':'بازار','Cave':'غار','Castle':'قلعه',
    'Wild Wolf':'گرگ وحشی','Bandit':'راهزن','Skeleton Warrior':'جنگجوی اسکلت','Orc':'اورک','Dark King':'پادشاه تاریک'
}

def new_player(name='Hero', language='en'):
    return dict(name=name or ('قهرمان' if language=='fa' else 'Hero'), language=language, hp=100,max_hp=100,energy=50,max_energy=50,attack=20,defense=0,gold=20,xp=0,level=1,potions=2,weapon='Wooden Sword',armor='Simple Clothes',shield='No Shield',location='Village',day=1,boss=False)

class Game(App):
    def build(self):
        self.p=None; self.enemy=None; self.ehp=0; self.defending=False; self.first_launch=True
        self.root=BoxLayout(orientation='vertical',padding=12,spacing=8)
        self.language_screen(); return self.root
    def tr(self,key,*args):
        lang=self.p.get('language','en') if self.p else 'en'
        val=T[lang].get(key,key)
        return val.format(*args) if args else val
    def item(self,name): return ITEM_FA.get(name,name) if self.p and self.p.get('language')=='fa' else name
    def clear(self): self.root.clear_widgets()
    def label(self,t,s=18):
        return Label(text=t,font_size=s,halign='center',valign='middle')
    def btn(self,t,fn):
        b=Button(text=t,font_size=17,size_hint_y=None,height=55); b.bind(on_press=fn); return b
    def language_screen(self,*_):
        self.clear(); self.root.add_widget(self.label('THE LOST KINGDOM',28)); self.root.add_widget(self.label(T['en']['choose_language'],21))
        self.root.add_widget(self.btn('English',lambda *_:self.choose_language('en')))
        self.root.add_widget(self.btn('فارسی',lambda *_:self.choose_language('fa')))
        self.root.add_widget(self.btn('GUIDE / راهنما',lambda *_:self.guide('en')))
    def choose_language(self,lang):
        self.p=new_player(language=lang); self.menu()
    def menu(self,*_):
        self.clear(); self.root.add_widget(self.label(self.tr('title'),28))
        if not self.p:
            self.root.add_widget(self.btn(self.tr('start'),self.name_popup)); self.root.add_widget(self.btn(self.tr('continue'),self.load)); self.root.add_widget(self.btn(self.tr('guide'),lambda *_:self.guide('en'))); self.root.add_widget(self.btn(self.tr('exit'),lambda *_:self.stop())); return
        p=self.p; self.root.add_widget(self.label(f"{p['name']} | {self.tr('level') if self.p.get('language')=='fa' else 'Lv.'}{p['level']} | {self.item(p['location'])}\n{self.tr('hp')} {p['hp']}/{p['max_hp']} | {self.tr('energy')} {p['energy']}/{p['max_energy']} | {self.tr('gold')} {p['gold']}",15))
        g=GridLayout(cols=2,spacing=7)
        for t,f in [('move',self.move),('explore',self.explore),('fight',self.fight),('shop',self.shop),('inventory',self.inventory),('stats',self.stats),('rest',self.rest),('boss',self.boss),('save',self.save),('guide',lambda *_:self.guide(self.p.get('language','en'))),('language',self.language_screen),('title_btn',self.title)]: g.add_widget(self.btn(self.tr(t),f))
        self.root.add_widget(g)
    def title(self,*_): self.p=None; self.language_screen()
    def name_popup(self,*_):
        box=BoxLayout(orientation='vertical',padding=10,spacing=8); inp=TextInput(hint_text=self.tr('enter_name'),multiline=False); box.add_widget(inp); box.add_widget(self.btn(self.tr('start_btn'),lambda *_:self.start(inp.text)))
        self.pop=Popup(title=self.tr('hero_name'),content=box,size_hint=(.85,.4)); self.pop.open()
    def start(self,name): self.p=new_player(name,self.p.get('language','en') if self.p else 'en'); self.pop.dismiss(); self.menu()
    def save(self,*_):
        with open(SAVE,'w',encoding='utf8') as f: json.dump(self.p,f,ensure_ascii=False)
        self.info(self.tr('saved'))
    def load(self,*_):
        try:
            with open(SAVE,encoding='utf8') as f:self.p=json.load(f)
            self.menu()
        except: self.info(self.tr('no_save'))
    def info(self,t): Popup(title=self.tr('title'),content=self.label(t),size_hint=(.85,.35)).open()
    def guide(self,lang=None,*_):
        if lang in ('en','fa') and self.p: self.p['language']=lang
        lang=lang if lang in ('en','fa') else (self.p.get('language','en') if self.p else 'en')
        box=BoxLayout(orientation='vertical',padding=12,spacing=8); box.add_widget(self.label(T[lang]['guide_text'],16)); box.add_widget(self.btn(T[lang]['back'],self.menu if self.p else self.language_screen))
        Popup(title=T[lang]['guide_title'],content=box,size_hint=(.95,.9)).open()
    def levelup(self):
        while self.p['xp']>=50+(self.p['level']-1)*40:
            self.p['xp']-=50+(self.p['level']-1)*40; self.p['level']+=1; self.p['max_hp']+=15; self.p['max_energy']+=5; self.p['attack']+=4; self.p['defense']+=1; self.p['hp']=self.p['max_hp']; self.p['energy']=self.p['max_energy']
    def move(self,*_):
        self.clear(); self.root.add_widget(self.label(self.tr('where'),22))
        for x in LOC[self.p['location']]: self.root.add_widget(self.btn(self.item(x),lambda _,x=x:self.travel(x)))
        self.root.add_widget(self.btn(self.tr('back'),self.menu))
    def travel(self,x):
        if self.p['energy']<5:return self.info(self.tr('not_energy'))
        self.p['energy']-=5; self.p['location']=x; self.p['day']+=1; self.menu()
    def explore(self,*_):
        if self.p['energy']<8:return self.info(self.tr('not_energy'))
        self.p['energy']-=8
        if random.random()<.45:return self.start_combat(random.choice(ENEMIES))
        e=random.choice(['gold','potion','heal','xp'])
        if e=='gold': n=random.randint(10,30);self.p['gold']+=n;msg=self.tr('found_gold',n)
        elif e=='potion':self.p['potions']+=1;msg=self.tr('found_potion')
        elif e=='heal':n=random.randint(10,25);self.p['hp']=min(self.p['max_hp'],self.p['hp']+n);msg=self.tr('found_heal',n)
        else:n=random.randint(10,25);self.p['xp']+=n;self.levelup();msg=self.tr('found_xp',n)
        self.info(msg)
    def fight(self,*_): self.start_combat(random.choice(ENEMIES))
    def start_combat(self,e): self.enemy=e; self.ehp=e[1]; self.defending=False; self.combat()
    def combat(self,*_):
        self.clear();e=self.enemy;p=self.p
        self.root.add_widget(self.label(f"{self.tr('combat')}\n{self.item(e[0])}\n{self.tr('your_hp')}: {p['hp']}/{p['max_hp']}\n{self.tr('enemy_hp')}: {self.ehp}/{e[1]}",20))
        self.root.add_widget(self.btn(self.tr('attack'),self.attack_move)); self.root.add_widget(self.btn(self.tr('power'),self.power)); self.root.add_widget(self.btn(self.tr('defense'),self.defend)); self.root.add_widget(self.btn(self.tr('potion'),self.potion)); self.root.add_widget(self.btn(self.tr('run'),self.run))
    def enemy_turn(self):
        d=max(1,random.randint(*self.enemy[2])-self.p['defense'])
        shield=next((x[2] for x in SHIELDS if x[0]==self.p.get('shield','No Shield')),0); d=max(1,round(d*(100-shield)/100))
        if self.defending:d=max(1,round(d*0.5));self.defending=False
        self.p['hp']-=d
        if self.p['hp']<=0:self.p['hp']=0;self.info(self.tr('defeated'));self.title()
        else:self.combat()
    def attack_move(self,*_):
        self.ehp-=random.randint(max(1,self.p['attack']-3),self.p['attack']+5)
        self.win() if self.ehp<=0 else self.enemy_turn()
    def defend(self,*_):
        self.defending=True;self.p['energy']=min(self.p['max_energy'],self.p['energy']+10);self.enemy_turn()
    def power(self,*_):
        if self.p['energy']<15:return self.info(self.tr('not_energy'))
        self.p['energy']-=15;d=random.randint(self.p['attack']+8,self.p['attack']+18);d*=2 if random.random()<.2 else 1;self.ehp-=d
        self.win() if self.ehp<=0 else self.enemy_turn()
    def potion(self,*_):
        if self.p['potions']<=0 or self.p['hp']>=self.p['max_hp']:return self.info(self.tr('not_potion'))
        self.p['potions']-=1;self.p['hp']=min(self.p['max_hp'],self.p['hp']+random.randint(25,40));self.enemy_turn()
    def run(self,*_): self.menu() if random.random()<.55 else self.enemy_turn()
    def win(self):
        e=self.enemy;g=random.randint(e[3],e[4]);self.p['gold']+=g;self.p['xp']+=e[5];self.levelup()
        if e[0]=='Dark King':self.p['boss']=True;msg=self.tr('dark_win')
        else:msg=self.tr('defeated_enemy',self.item(e[0]),g,e[5])
        self.info(msg);self.menu()
    def shop(self,*_):
        self.clear();self.root.add_widget(self.label(self.tr('shop_gold',self.p['gold']),23));self.root.add_widget(self.btn(self.tr('potion_price'),self.buy_potion))
        for n,pr,pw in WEAPONS[1:]:self.root.add_widget(self.btn(f'{self.item(n)} - {pr} {self.tr("gold")}',lambda _,n=n,pr=pr,pw=pw:self.buy_weapon(n,pr,pw)))
        for n,pr,d in ARMORS[1:]:self.root.add_widget(self.btn(f'{self.item(n)} - {pr} {self.tr("gold")}',lambda _,n=n,pr=pr,d=d:self.buy_armor(n,pr,d)))
        self.root.add_widget(self.label(self.tr('shields'),18))
        for n,pr,b in SHIELDS[1:]:self.root.add_widget(self.btn(f'{self.item(n)} - {pr} {self.tr("gold")} ({self.tr("block",b)})',lambda _,n=n,pr=pr,b=b:self.buy_shield(n,pr,b)))
        self.root.add_widget(self.btn(self.tr('back'),self.menu))
    def buy_potion(self,*_):
        if self.p['gold']>=15:self.p['gold']-=15;self.p['potions']+=1
        self.shop()
    def buy_weapon(self,n,pr,pw):
        cur=next(x[2] for x in WEAPONS if x[0]==self.p['weapon'])
        if pw>cur and self.p['gold']>=pr:self.p['gold']-=pr;self.p['weapon']=n;self.p['attack']=10+pw
        self.shop()
    def buy_armor(self,n,pr,d):
        cur=next(x[2] for x in ARMORS if x[0]==self.p['armor'])
        if d>cur and self.p['gold']>=pr:self.p['gold']-=pr;self.p['armor']=n;self.p['defense']=d
        self.shop()
    def buy_shield(self,n,pr,b):
        cur=next((x[2] for x in SHIELDS if x[0]==self.p.get('shield','No Shield')),0)
        if b>cur and self.p['gold']>=pr:self.p['gold']-=pr;self.p['shield']=n
        self.shop()
    def inventory(self,*_):
        self.clear();p=self.p;self.root.add_widget(self.label(f"{self.tr('inv')}\n{self.tr('weapon')}: {self.item(p['weapon'])}\n{self.tr('armor')}: {self.item(p['armor'])}\n{self.tr('shield')}: {self.item(p.get('shield','No Shield'))}\n{self.tr('potions')}: {p['potions']}\n{self.tr('gold')}: {p['gold']}",20));self.root.add_widget(self.btn(self.tr('back'),self.menu))
    def stats(self,*_):
        self.clear();p=self.p;block=next((x[2] for x in SHIELDS if x[0]==p.get('shield','No Shield')),0)
        t=f"{self.tr('hero_stats')}\n\n{self.tr('name')}: {p['name']}\n{self.tr('level')}: {p['level']}\n{self.tr('hp')}: {p['hp']}/{p['max_hp']}\n{self.tr('energy')}: {p['energy']}/{p['max_energy']}\n{self.tr('attack_stat')}: {p['attack']}\n{self.tr('defense_stat')}: {p['defense']}\n{self.tr('shield_block')}: {block}%\n{self.tr('gold')}: {p['gold']}\n{self.tr('xp')}: {p['xp']}\n{self.tr('day')}: {p['day']}"
        self.root.add_widget(self.label(t,18));self.root.add_widget(self.btn(self.tr('back'),self.menu))
    def rest(self,*_):self.p['hp']=min(self.p['max_hp'],self.p['hp']+30);self.p['energy']=self.p['max_energy'];self.p['day']+=1;self.info(self.tr('rested'))
    def boss(self,*_):
        if self.p['location']!='Castle':return self.info(self.tr('reach_castle'))
        if self.p['boss']:return self.info(self.tr('boss_done'))
        self.enemy=('Dark King',180,(15,25),100,180,150);self.ehp=180;self.defending=False;self.combat()

if __name__=='__main__': Game().run()
