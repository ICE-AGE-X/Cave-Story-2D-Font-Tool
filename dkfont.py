from PIL import Image, ImageDraw, ImageFont
import libs
font_w = 12
tex_w = 1024
tex_h = 512
font = ImageFont.truetype('simsun.ttc', font_w)
image = Image.new(mode='RGBA', size=(tex_w, tex_h))
draw_table = ImageDraw.Draw(im=image)

y = 1

charMapF = open("CSE3.tbl", "r", encoding="utf-16")
chars = []
while(True):
    text = charMapF.readline()
    if(text):
        text.replace("\n", "")
        r = text.split('=')
        v = r[1].replace("\n", "")
        # print(ord(v))
        chars.append((r[0], v))
    else:
        break
charMapF.close()

fntTmp = open("font.temp", "rb")
tempDatas = fntTmp.read(-1)
fntTmp.close()

f3d = open("font.fnt", 'wb')
f3d.write(tempDatas)
libs.writeInt4(f3d,0x14*len(chars))

char_idx = 0
end_idx = len(chars)
while(y < tex_h-font_w):
    x = 1
    if(char_idx >= end_idx):
        break
    while(x < tex_w):
        if(char_idx >= end_idx):
            break
        size = font.getsize(chars[char_idx][1])
        if(x+size[0] > tex_w):
            break
        cid = int(chars[char_idx][0], 16)

        if(cid < 0x7f):
            libs.writeInt1(f3d, cid)  # page
            libs.writeInt1(f3d, 0)  # page
        else:
            libs.writeInt2BE(f3d, cid)  # id
        libs.writeInt2(f3d, 0)  # fix
        libs.writeInt2(f3d, x)  # x
        libs.writeInt2(f3d, y)  # y
        libs.writeInt2(f3d, size[0])  # w
        libs.writeInt2(f3d, font_w+1)  # h
        libs.writeInt2(f3d, 0)  # xo
        libs.writeInt2(f3d, 0)  # yo
        libs.writeInt2(f3d, size[0])  # xadv
        libs.writeInt1(f3d, 0)  # page
        libs.writeInt1(f3d, 0xf)  # chnl
        draw_table.text(xy=(
            x, y), spacing=0, text=chars[char_idx][1], fill='#ffffff', font=font, align="center")
        # x = x+size[0]
        x += size[0]+1
        char_idx += 1
    y += font_w+2
f3d.close()
# print(ary)
image.save('font_0.png', 'PNG')
image.close()
