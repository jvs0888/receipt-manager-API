import multiprocessing


workers: int = multiprocessing.cpu_count() * 2 + 1
worker_class: str = 'uvicorn.workers.UvicornWorker'
