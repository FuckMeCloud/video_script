import logging
import os

import ffmpeg

logger = logging.getLogger(__name__)


class WaterMark:
    def __init__(self, text, font_path, font_size=64, font_color='white', pos=(10, 10)):
        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.font_color = font_color
        self.pos = pos


class Video:
    def __init__(self, path, min_width=1920):
        self._prob = ffmpeg.probe(path)
        self.path = path
        self.min_width = min_width

    @property
    def width(self):
        return int(self._prob['streams'][0]['width'])

    @property
    def height(self):
        return int(self._prob['streams'][0]['height'])

    @property
    def name(self):
        return os.path.basename(self.path)

    def scale_video(self, out_put):
        out_put_path = format(os.path.join(out_put, "scale_{}".format(self.name)))
        ffmpeg.input(self.path). \
            filter('scale', self.min_width, -1). \
            output(out_put_path). \
            global_args('-loglevel', 'error'). \
            run(overwrite_output=True)
        return out_put_path

    def add_watermark(self, ws, out_put='./'):
        if not ws:
            return
        logger.info("视频的大小为: {}x{}".format(self.width, self.height))
        if not os.path.exists(out_put):
            os.makedirs(out_put)
        input_path = self.path
        if self.width < self.min_width:
            logger.info("视频宽度小于 {}, 进行缩放".format(self.min_width))
            input_path = self.scale_video(out_put)
        logger.info("添加水印中: {}".format(self.name))
        input = ffmpeg.input(input_path)

        for w in ws:
            input = input.drawtext(text=w.text,
                                   fontfile=w.font_path,
                                   fontcolor=w.font_color,
                                   fontsize=w.font_size,
                                   x=w.pos[0],
                                   y=w.pos[1])

        input.output(os.path.join(out_put, self.name)). \
            global_args('-loglevel', 'error'). \
            run(overwrite_output=True)
        logger.info("清理中间文件: {}".format(self.name))
        if input_path != self.path:
            os.remove(input_path)
        logger.info("添加水印完成: {}".format(self.name))
