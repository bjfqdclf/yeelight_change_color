import time
from haishoku.haishoku import Haishoku
from yeelight import Bulb
from PIL import ImageGrab


class YeelightChangeWithDisplay:
    ip_addr_list = ["192.168.5.167"]
    request_time = 1

    def __init__(self):
        bulb_list = []
        for ip_addr in self.ip_addr_list:
            bulb = Bulb(ip_addr, effect="smooth", duration=1000)
            bulb_list.append(bulb)
        self.change_color(bulb_list)

    def change_color(self, bulb_list):
        while (True):
            im = ImageGrab.grab()
            im = im.convert('RGB')
            im.save(".yeelight_change_color.jpg")
            # 截个图然后存下来

            haishoku = Haishoku.loadHaishoku(".yeelight_change_color.jpg")
            # 判断主色调RGB
            h, s, v = self.rgb_to_hsv(haishoku.dominant[0], haishoku.dominant[1], haishoku.dominant[2])
            for bulb in bulb_list:
                bulb.set_hsv(h, s, v)  # 传给灯带
            print(h, s, v)
            time.sleep(self.request_time)

    def rgb_to_hsv(self, r, g, b):
        """RGB to HSV"""
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        m = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            if g >= b:
                h = ((g - b) / m) * 60
            else:
                h = ((g - b) / m) * 60 + 360
        elif mx == g:
            h = ((b - r) / m) * 60 + 120
        elif mx == b:
            h = ((r - g) / m) * 60 + 240
        if mx == 0:
            s = 0
        else:
            s = m / mx
        v = mx
        H = h
        S = s * 100.0  # 这里应该是100的，我觉得太亮了改成了50
        V = (v + 0.02) * 50.0  # 同上，加0.02是因为如果V=0灯带会报错
        return H, S, V


if __name__ == '__main__':
    YeelightChangeWithDisplay()

