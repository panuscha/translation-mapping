import glob

from PIL import Image


def make_gif(frame_folder):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.PNG")]
    frame_one = frames[0]
    frame_one.save("translation_1960_2020_ma_5.gif", format="GIF", append_images=frames,
               save_all=True, duration=500, loop=0)
    

if __name__ == "__main__":
    make_gif("C:/Users/Panuskova/Nextcloud/translation-mapping/plots/individual years ma")