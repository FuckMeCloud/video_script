import click

from video.perocess import run, Config


@click.command()
@click.option("--input", default="input", help="输入目录")
@click.option("--excludes", default="", help="排除文件")
@click.option("--output", default="output", help="输出目录")
@click.option("--font", default="font", help="字体目录")
@click.option("--formats", default=['mp4'], help="需要处理的格式", type=list)
@click.option("--celery", default=False, help="是否使用 celery 异步处理", type=bool)
@click.option("--broker", default='redis://localhost:6379/0', help="任务发布地址")
@click.option("--backend", default='redis://localhost:6379/0', help="结果存储地址")
@click.option("--worker", default=4, help="工作进程数", type=int)
@click.option("--loglevel", default='INFO', help="日志级别")
def main(input, excludes, output, font, formats, celery, broker, backend, worker, loglevel):
    c = {
        "input": input,
        "excludes": excludes,
        "output": output,
        "font": font,
        "formats": formats,
        "celery": celery,
        "broker": broker,
        "backend": backend,
        "worker": worker,
        "loglevel": loglevel,
    }
    cfg = Config(**c)
    run(cfg)


if __name__ == '__main__':
    main()
