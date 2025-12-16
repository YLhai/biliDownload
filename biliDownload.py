import json
import os
import sys
import shutil
import time
import requests, re
import subprocess
import tkinter
from threading import Thread

main_end = False
main_start=False
width = 500
height = 500
model_c = [1]
text_state = '开始下载'
text_name = ""
text_num=""
not_del=[]
headers = {
    'cookie': "buvid3=0534DBBC-5D18-1D42-28F5-7C676066870262512infoc; b_nut=1666176562; i-wanna-go-back=-1; _uuid=7E967C36-9237-E72E-C6A7-11979958845562837infoc; buvid4=360F6098-EC6D-5825-93A5-7D221838B8AE63767-022101918-7KoX5iDW5yoNuvEf1qoPJg%3D%3D; fingerprint=80554a4ae055464ce48c7d5993e6a7e0; buvid_fp_plain=undefined; SESSDATA=b0b9a285%2C1681728610%2C9d50f%2Aa2; bili_jct=9fc9ce7f874d8bba2144b231947111b8; DedeUserID=630896292; DedeUserID__ckMd5=1b87bdd42cdb88bb; sid=6p3x1o3x; buvid_fp=80554a4ae055464ce48c7d5993e6a7e0; rpdid=|(ummY~ml)mY0J'uYYYu~YYRJ; CURRENT_QUALITY=0; LIVE_BUVID=AUTO2616661806681329; b_ut=5; go_old_video=1; fingerprint3=c84c8af8a6576ca58f52ee005f3aeb4f; bp_video_offset_630896292=719006357640970200; b_lsid=E95C4A51_18404934367; bsource=search_baidu; PVID=1; innersign=1; CURRENT_FNVAL=4048",
    'referer': 'https://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}
path1 = './视频正在下载不要动我/'
path = './正在下载不要动我/'

#退出确定
def isquit():
    del_files(path, path1)
    os._exit(0)
def dataup():
    global main_end,main_start,text_num,text_name,text_state,not_del,path,path1,model_c
    main_end = False
    main_start = False
    model_c = [1]
    text_state = '开始下载'
    text_name = ""
    text_num = ""
    not_del = []
    path1 = './视频正在下载不要动我/'
    path = './正在下载不要动我/'
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path1):
        os.mkdir(path1)
def del_files(path, path1):
    if os.path.exists(path):
        shutil.rmtree(path)
    if os.path.exists(path1):
        os.rename(path1, f"./{time.strftime('%Y%m%d%H%M%S', time.localtime())}")

# 视频下载
def down_34(dict,path1=path1):
    global text_name,text_state,text_num
    page = requests.get(url=dict["url"], headers=headers).text
    text_state = '正在下载:'
    text_name = dict["name"]
    e = '<script>window.__playinfo__=(.*?)</script>'
    ex = re.findall(e, page)[0]
    json_data = json.loads(ex)
    v_mp3_url = json_data["data"]["dash"]["audio"][0]["baseUrl"]
    v_mp4_url = json_data["data"]["dash"]["video"][0]["baseUrl"]
    v_mp3 = requests.get(v_mp3_url, headers=headers).content
    v_mp4 = requests.get(v_mp4_url, headers=headers).content

    title = dict["name"]
    title = ''.join(title.split())
    try:
        if os.path.exists(f'{path + title}.mp4'):
            title = title + time.strftime('%H%M%S', time.localtime())
        with open(f'{path + title}.mp3', 'wb')as f:
            f.write(v_mp3)
        with open(f'{path + title}.mp4', 'wb')as f1:
            f1.write(v_mp4)
    except:
        title = time.strftime('%Y%m%d%H%M%S', time.localtime())
        # title="11"
        if os.path.exists(f'{path + title}.mp4'):
            title = title + "1"
        with open(f'{path + title}.mp3', 'wb')as f:
            f.write(v_mp3)
        with open(f'{path + title}.mp4', 'wb')as f1:
            f1.write(v_mp4)
    title1= title
    if os.path.exists(f'{path1 + title1}.mp4'):
        title1 = title + "1"
    cmd = f"ffmpeg -i {path + title}.mp4 -i {path + title}.mp3 -c:v copy -c:a aac -strict experimental {path1 + title1}.mp4"
    subprocess.run(cmd, shell=True)
    if os.path.exists(f'{path + title}.mp4'):
        os.remove(f'{path + title}.mp4')
        os.remove(f'{path + title}.mp3')
    text_state = '成功下载:'

# URL获取
def v_url(url_in, num, seat=(1, 1)):
    global text_state
    v_details = []
    # 收藏型
    if 'fid=' in url_in:
        if num % 20 != 0:
            a = num // 20 + 1
        else:
            a = num // 20
        id = re.findall(r'fid=+(\d*)', url_in)[-1]
        cc = 0
        for i in range(seat[0] - 1, a + seat[0] - 1):

            page_url = f"https://api.bilibili.com/x/v3/fav/resource/list?media_id={id}&pn={i + 1}&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp"
            page_url_collect = f'https://api.bilibili.com/x/space/fav/season/list?season_id={id}&pn={i + 1}&ps=20&jsonp=jsonp'
            try:
                page_text = requests.get(url=page_url, headers=headers).text
            except:
                break
            json_data = json.loads(page_text)
            v_list = json_data["data"]["medias"]
            if type(v_list) != list:
                try:
                    page_text = requests.get(url=page_url_collect, headers=headers).text
                except:
                    break
                json_data = json.loads(page_text)
                v_list = json_data["data"]["medias"]
                if type(v_list) != list:
                    break
            url = 'https://www.bilibili.com/video/'
            try:
                for i in v_list:
                    cc += 1
                    if cc >= seat[1]:
                        v_details.append({'name': i["title"], 'url': url + i["bvid"]})
            except:
                text_state="下载出现不明错误！"
    # 合集型
    elif 'sid=' in url_in:

        sid = re.findall(r'sid=+(\d*)', url_in)[-1]
        if num % 30 != 0:
            a = num // 30 + 1
        else:
            a = num // 30
        if 'bilibili.com/' in url_in:
            id = re.findall(r'bilibili.com/+(\d*)', url_in)[-1]
        else:
            sys.exit()
        cc = 0
        for i in range(seat[0] - 1, a + seat[0] - 1):
            page_url = f'https://api.bilibili.com/x/polymer/space/seasons_archives_list?mid={id}&season_id={sid}&sort_reverse=false&page_num={i + 1}&page_size=30'

            try:
                page_text = requests.get(url=page_url, headers=headers).text
            except:
                break
            json_data = json.loads(page_text)
            v_list = json_data["data"]["archives"]
            url = 'https://www.bilibili.com/video/'
            try:
                for i in v_list:
                    cc += 1
                    if cc >= seat[1]:
                        v_details.append({'name': i["title"], 'url': url + i["bvid"]})
            except:
                text_state = "下载出现不明错误！"
    # 主页型
    else:

        if num % 30 != 0:
            a = num // 30 + 1
        else:
            a = num // 30
        if 'tid=' in url_in:
            tid = re.findall(r'tid=+(\d*)', url_in)[-1]
        else:
            tid = 0
        if 'bilibili.com/' in url_in:
            id = re.findall(r'bilibili.com/+(\d*)', url_in)[-1]
        else:
            sys.exit()
        cc = 0
        for i in range(seat[0] - 1, a + seat[0] - 1):
            page_url = f'https://api.bilibili.com/x/space/arc/search?mid={id}&ps=30&tid={tid}&pn={i + 1}&keyword=&order=pubdate&order_avoided=true&jsonp=jsonp'
            try:
                page_text = requests.get(url=page_url, headers=headers).text
            except:
                break
            json_data = json.loads(page_text)
            v_list = json_data["data"]["list"]["vlist"]
            url = 'https://www.bilibili.com/video/'
            try:
                for i in v_list:
                    cc += 1
                    if cc >= seat[1]:
                        v_details.append({'name': i["title"], 'url': url + i["bvid"]})
            except:
                text_state = "下载出现不明错误！"
                text_state="下载出现不明错误！"


    return v_details

# 运行函数（url,下载数量）
def run(list):
    global text_state,text_name,text_num

    if not os.path.exists(path1):
        os.mkdir(path1)
    url = list[2]
    num = list[0]
    seat = list[1]
    content = 0
    url_list = v_url(url, num, seat)
    if num >= len(url_list):
        num = len(url_list)
    d = 0
    for i in url_list:
        d += 1
        try:
            down_34(i)
            content += 1
        except:
            text_state = "出现一个视频无法下载，可能是网络波动"
            text_name=''
            text_num = f"还有{num - d}个文件需要下载"
            continue
        if num - d <= 0:
            text_num = f"下载结束！！成功下载{content}个视频"
            break
        text_num = f"还有{num - d}个文件需要下载"
    del_files(path, path1)

    time.sleep(1)

def in_data(Url,num,seat):
    Urls = []
    # Url输入
    while True:
        if ',' in Url:
            Urls = Url.split(',')
            break
        if '，' in Url:
            Urls = Url.split('，')

            break
        # Url = input(f"视频地址{d}(直接回车可结束输入)：")
        if Url == '':
            if len(Urls) > 0:
                break
        if len(Url) >= 5:
            Urls.append(Url)
            break
        else:
            break
    # num输入
    while True:
        # num = input("下载数(默认10):")
        try:
            if num == '':
                num = 10
                break
            num = eval(num)
            if num > 0:
                break
        except:
            break
    # 开始位置输入
    while True:
        # seatin = input("下载开始位置(默认1,1)(如:'1,2'):")
        try:
            if seat == '':
                seat = (1, 1)
                break
            if "，" in seat:
                seat = seat.replace("，", ",")
            seat = eval(seat)
            if type(seat) == tuple:
                break
        except:
            break
    # （url（必须参数）,下载数量（默认10)）
    return Urls,num,seat

def main_batch(li):
    global main_end
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path1):
        os.mkdir(path1)
    Urls = li[0]
    num = li[1]
    seat = li[2]
    # # （url（必须参数）,下载数量（默认10)）
    global main_end
    for i in Urls:
        run((num, seat, i))
    main_end=True

def main_single(li):
    global main_end,path1
    path2='./singlevideo/'
    if not os.path.exists(path2):
        os.mkdir(path2)
    if not os.path.exists(path):
        os.mkdir(path)
    down_34({'url': li[0][0], 'name': time.strftime('%H%M%S', time.localtime())},path2)
    main_end=True
    del_files(path, '')

class Window:
    w_seat = [100,100]
    url=None
    num = None
    seat = None
    text  = '注意事项：\n1、必须输入地址\n2、下载数默认值：10\n3、开始位置默认为第一个，输入格式:如第1页第3个为“1,3”'
    def __init__(self):
        self.root = tkinter.Tk()
        # self.width=int(min(self.root.winfo_screenwidth(),self.root.winfo_screenmmheight())/3)
        self.width = 20*25
        self.height=int(self.width/1.5)

        self.root.geometry(f'{self.width}x{self.height}+{self.w_seat[0]}+{self.w_seat[1]}')
        self.root.resizable(False,False)
        self.root.title("b站视频下载")
        self.root.protocol("WM_DELETE_WINDOW", isquit)

    def run1(self):
        self.url = self.inp1.get()
        self.num = self.inp2.get()
        self.seat = self.inp3.get()
        li = in_data(self.url, self.num, self.seat)
        self.url = li[0]
        self.num = li[1]
        self.seat = li[2]
        for i in self.root.winfo_children():
            if i not in not_del:
                i.destroy()
        self.root.quit()

    def inp(self):
        return self.url, self.num, self.seat
    def downing(self):
        self.main_menu.destroy()
        font = ('黑体', 15)
        font1 = ('黑体', 15)

        lab1 = tkinter.Label(self.root, text=text_state,font = font)
        lab1.place(relx=0.05, rely=0.05, relheight=0.05)

        lab2 = tkinter.Message(self.root, text=text_name, width=500*0.8,font=font1, fg='green')
        lab2.place(relx=0.1, rely=0.15, relheight=0.1)

        lab3 = tkinter.Label(self.root, text=text_num,font = font)
        lab3.place(relx=0.1, rely=0.3, relheight=0.1,relwidth=0.8)

        while True:
            self.root.update()
            self.root.after(50)
            if main_end==True:
                t = '退出'
                t1='继续下载'
                lab1["text"] = text_state
                bt1 = tkinter.Button(self.root, text=t, command=isquit)
                bt1.place(relx=0.4, rely=0.6, relwidth=0.3, relheight=0.1)
                bt1 = tkinter.Button(self.root, text=t1, command=lambda :self.model(3))
                bt1.place(relx=0.2, rely=0.6, relwidth=0.3, relheight=0.1)
                break
            else:
                lab2["text"] = text_name
                lab1["text"] = text_state
            lab3["text"]=text_num

        self.root.mainloop()

    def model(self,a):
        global main_end,main_start
        for i in self.root.winfo_children():
            if i not in not_del:
                i.destroy()
        text1 = "    地址："
        text2 = "  下载数："
        text3 = "开始位置："
        font = ('黑体', 15)
        x = 0
        y = 0.1
        lab_h = 0.1
        title = tkinter.Message(self.root, text=self.text, width=500)

        title.place(relx=0, rely=0.7)

        label1 = tkinter.Label(self.root, text=text1, font=font)
        label1.place(relx=x, rely=y, relwidth=0.2, relheight=lab_h)
        self.inp1 = tkinter.Entry(self.root)
        self.inp1.place(relx=x + 0.2, rely=y, relwidth=0.7, relheight=lab_h)

        label2 = tkinter.Label(self.root, text=text2, font=font)
        label2.place(relx=x, rely=y + lab_h, relwidth=0.2, relheight=lab_h)
        self.inp2 = tkinter.Entry(self.root)
        self.inp2.place(relx=x + 0.2, rely=y + lab_h, relwidth=0.7, relheight=lab_h)

        label3 = tkinter.Label(self.root, text=text3, font=font)
        label3.place(relx=x, rely=y + 2 * lab_h, relwidth=0.2, relheight=lab_h)
        self.inp3 = tkinter.Entry(self.root)
        self.inp3.place(relx=0.2 + x, rely=y + 2 * lab_h, relwidth=0.7, relheight=lab_h)
        text1 = '确定'
        bt1 = tkinter.Button(self.root, text=text1, command=self.run1, font=('黑体', 15), bg='blue', fg='white')
        bt1.place(relx=0.4 + x, rely=0.4 + y, relwidth=0.3, relheight=0.1)
        model_c[0]=a
        if a==3:
            dataup()
            self.num=None
            self.url=None
            self.seat=None
            self.root.destroy()
        if a == 1:
            label3.place_forget()
            label2.place_forget()
            self.inp2.place_forget()
            self.inp3.place_forget()

    def draw_screen(self,text='',a=model_c[0]):

        for i in self.root.winfo_children():
            if i not in not_del:
                i.destroy()
        if text=='':
            text=self.text
        text1="    地址："
        text2 = "  下载数："
        text3 = "开始位置："
        font = ('黑体',15)
        font_v = ('黑体', 20)
        x = 0
        y = 0.1
        lab_h = 0.1

        # 主菜单
        self.main_menu = tkinter.Menu(self.root)
        not_del.append(self.main_menu)
        # 模式选择下拉菜单
        self.file = tkinter.Menu(self.main_menu, tearoff=False)
        self.file.add_command(label="单个下载", command=lambda: self.model(1))
        self.file.add_command(label="批量下载", command=lambda: self.model(2))

        self.main_menu.add_cascade(label="模式选择", menu=self.file)

        self.root.config(menu=self.main_menu)


        title = tkinter.Message(self.root,text=self.text,width=500)
        if text!=self.text:
            label_lert = tkinter.Label(self.root, text="输入有误!!",font=font_v,fg='red')
            label_lert.place(relx=x+0.05, rely=0.5, relwidth=0.3, relheight=lab_h,)
            self.root.after(1000,func=lambda:label_lert.destroy())
        title.place(relx=0, rely=0.7)

        label1= tkinter.Label(self.root,text=text1,font=font)
        label1.place(relx=x, rely=y, relwidth=0.2, relheight=lab_h)
        self.inp1=tkinter.Entry(self.root)
        self.inp1.place(relx = x+0.2,rely = y,relwidth=0.7,relheight=lab_h)

        label2 = tkinter.Label(self.root, text=text2,font=font)
        label2.place(relx=x, rely=y+lab_h, relwidth=0.2, relheight=lab_h)
        self.inp2 = tkinter.Entry(self.root)
        self.inp2.place(relx=x+0.2, rely=y+lab_h, relwidth=0.7, relheight=lab_h)

        label3 = tkinter.Label(self.root, text=text3,font=font)
        label3.place(relx=x, rely=y+2*lab_h, relwidth=0.2, relheight=lab_h)
        self.inp3 = tkinter.Entry(self.root)
        self.inp3.place(relx=0.2+x, rely=y+2*lab_h, relwidth=0.7, relheight=lab_h)
        text1='确定'
        bt1 = tkinter.Button(self.root,text=text1,command=self.run1,font = ('黑体',15),bg='blue',fg='white')
        bt1.place(relx=0.4+x,rely=0.4+y,relwidth=0.3, relheight=0.1)
        if a==1:
            label3.place_forget()
            label2.place_forget()
            self.inp2.place_forget()
            self.inp3.place_forget()

        self.root.mainloop()


def main1():
    global li,main_start
    w = Window()
    t_eor = w.text
    w.draw_screen(t_eor)
    li = w.inp()
    while len(li[0]) == 0:

        t_eor = "输入有误\n" + w.text
        w.draw_screen(t_eor,model_c[0])
        li = w.inp()

    main_start=True
    w.downing()

if __name__ == "__main__":
    while True:
        if main_end==False:
            try:
                t = Thread(target=main1, )
                t.start()
                while main_start==False:
                    time.sleep(0.1)
                if model_c[0]==1:
                    main_single(li)
                else:
                    main_batch(li)
            except:
                sys.exit()



