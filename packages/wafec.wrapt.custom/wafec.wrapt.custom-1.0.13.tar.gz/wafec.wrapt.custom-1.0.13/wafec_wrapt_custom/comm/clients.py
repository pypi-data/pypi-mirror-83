import os
import psutil
import requests
import threading

from wafec_wrapt_custom.utility import fullname

base_url = os.environ.get('WWC_URL')
base_url = base_url if base_url else 'http://localhost:6543'


def _safe_run(target, args, kwargs):
    try:
        target(*args, **kwargs)
    except:
        pass


def _post_async(*args, **kwargs):
    thread = threading.Thread(target=_safe_run, args=(requests.post, args, kwargs))
    thread.start()


def add_proxy_interception_info(name, x=None, trace=None):
    p = psutil.Process()
    ps = p.name()
    data = {'ps': ps, 'name': name, 'x': fullname(x), 'trace': trace}
    _post_async(url=f'{base_url}/api/proxy/interception/add', json=data)
