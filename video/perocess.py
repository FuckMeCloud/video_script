import logging
import os

from celery import Celery

from video.video import WaterMark

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class Config:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def load_video_files(input_dir, excludes=None, formats=None):
    if formats is None:
        formats = list()
    if excludes is None:
        excludes = list()
    files = []
    for f in os.listdir(input_dir):
        if f in excludes:
            continue
        if formats and not f.endswith(tuple(formats)):
            continue
        files.append(os.path.join(input_dir, f))
    return files


app = Celery('video_script', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@app.task
def video_handler(file, config):
    cfg = Config(**config)
    from video.video import Video
    logger.info("开始处理视频: {}".format(file))
    v = Video(file)
    ws = [
        WaterMark("测试水印", font_path='font/lazy.ttf'),
    ]
    v.add_watermark(ws, cfg.output)
    logger.info("处理完成: {}".format(file))


def run(config):
    logging.basicConfig(level=config.loglevel)
    files = load_video_files(config.input, config.excludes, config.formats)
    logger.info("共找到 {} 个视频文件".format(len(files)))

    if config.celery:
        app.conf.update(
            broker_url=config.broker,
            result_backend=config.backend,
            worker_concurrency=config.worker,
        )
        results = []
        for f in files:
            result = video_handler.delay(f, config.__dict__)
            results.append(result)
            logger.info("任务已发布: {}".format(result.id))
        for r in results:
            r.get()
    else:
        for f in files:
            video_handler(f, config.__dict__)
