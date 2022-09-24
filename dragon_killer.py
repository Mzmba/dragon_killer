# import detect_sift

import cv2
import imageio
import glob
import numpy as np
import os
import aiohttp
import cv2
from hoshino import Service
from hoshino.typing import CQEvent, MessageSegment

sv = Service('dragon_killer', help_='ltjc')
# RUN_PATH = os.getcwd()
FILE_FOLDER_PATH = os.path.dirname(__file__)
print("16",FILE_FOLDER_PATH)
# RELATIVE_PATH = os.path.relpath(FILE_FOLDER_PATH, RUN_PATH)
PIC_PATH = os.path.join(FILE_FOLDER_PATH, 'gg.jpg')

def read_img(name) :
    if not (name.endswith(".gif")):
        return cv2.cvtColor(imageio.imread(name), cv2.COLOR_RGB2BGR)

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image
    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)
    # return the resized image
    return resized

def minEnclosingCircleArea(pts) :
    _, r = cv2.minEnclosingCircle(pts)
    return r * r * np.pi

class DragonDetector(object) :
    def __init__(self, template_image_pattern = os.path.abspath(os.path.join(FILE_FOLDER_PATH, 'template*.png')), image_resolutions = [20, 60, 100, 200, 400], match_point_threshold = 5, circle_area_threshold = 0.2) :
       # print(glob.glob("/root/qqbot/HoshinoBot/hoshino/modules/dragon_killer/template*.png"))
        self.templates = [read_img(fn) for fn in glob.glob(template_image_pattern)]
        self.match_point_threshold = match_point_threshold
        self.circle_area_threshold = circle_area_threshold
        self.image_resolutions = image_resolutions
        self.sift = cv2.SIFT_create()
        self.template_sifts = [(self.sift.detectAndCompute(img, None), img.shape) for img in self.templates]
        # FLANN parameters
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)   # or pass empty dictionary
        self.flann = cv2.FlannBasedMatcher(index_params,search_params)
        print(f' -- {len(self.templates)} templates loaded.')

    def is_dragon_impl(self, kps, imgnp) :
        (kp1, des1), template_shape = kps
        kp2, des2 = self.sift.detectAndCompute(imgnp, None)
        try :
            matches = self.flann.knnMatch(des1, des2, k = 2)
        except Exception :
            return False
        good = []
        for m, n in matches :
            if m.distance < 0.7 * n.distance:
                good.append(m)
        if len(good) > self.match_point_threshold :
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            h, w, d = template_shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            try :
                dst = cv2.perspectiveTransform(pts,M)
                if cv2.contourArea(dst) > self.circle_area_threshold * minEnclosingCircleArea(dst) :
                    return True
            except Exception :
                pass
        return False

    def is_dragon(self, img_np) :
        found = False
        for template in self.template_sifts :
            for w in self.image_resolutions :
                found = found or self.is_dragon_impl(template, image_resize(img_np, width = w, inter = cv2.INTER_LINEAR))
        return found

class DragonDetectorFast(DragonDetector) :
    def __init__(self) :
        super().__init__('template1.png', [200])


det = DragonDetector()

async def check_gif(bot, img):
    r = await bot.call_action(action='get_image', file=img)
    return r['filename'].endswith('gif')

async def gg_image(bot, ev, img): #是gif就放过
    check_gif_result = await check_gif(bot, img)
    return not (check_gif_result)

async def download(url, path):
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            content = await resp.read()
            with open(path, 'wb') as f:
                f.write(content)


async def check_image(bot, ev, img):
    try:
        image_path = f'{FILE_FOLDER_PATH}/{img}.jpg'
        image_info = await bot.call_action(action='get_image', file=img)
        await download(image_info['url'], image_path)
        imgfordetctd = cv2.imread(image_path)
        qr_img = det.is_dragon(imgfordetctd)
        if os.path.exists(image_path):
            os.remove(image_path)
        if qr_img:
            return True
        else:
            return False
    except:
        return False


@sv.on_message()
async def on_input_image(bot, ev: CQEvent):
    for seg in ev.message:
        if seg.type == 'image':
            img = seg.data['file']
            not_gif = await gg_image(bot, ev, img)  #是gif返回False
            if not_gif:
                need_shama_msg = await check_image(bot, ev, img)
                if need_shama_msg:
                    try:
                        await bot.send(ev, str(MessageSegment.image(f'file:///{os.path.abspath(PIC_PATH)}')) + '\n龙图小鬼GCK!', at_sender=False)
                    except:
                        print("反制失败")