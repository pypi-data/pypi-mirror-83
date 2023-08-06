# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_redis_session']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.61.1,<0.62.0', 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'fastapi-redis-session',
    'version': '0.1.2',
    'description': 'A redis-based session backend for Fastapi apps',
    'long_description': '# fastapi-redis-session\n\n![CI](https://github.com/duyixian1234/fastapi-redis-session/workflows/CI/badge.svg?branch=master)\n\nA redis-based session backend for Fastapi apps\n\n## Install\n\n```bash\npip install -U fastapi-redis-session\n```\n\n## Use\n\n```python\nfrom typing import Any\n\nfrom fastapi import Depends, FastAPI, Request, Response\n\nfrom fastapi_redis_session import getSession, setSession\nfrom fastapi_redis_session.deps import getSessionStorage\nfrom fastapi_redis_session.session import SessionStorage\n\napp = FastAPI(title=__name__)\n\n\n@app.post("/setSession")\nasync def _setSession(\n    request: Request, response: Response, sessionStorage: SessionStorage = Depends(getSessionStorage)\n):\n    sessionData = await request.json()\n    setSession(response, sessionData, sessionStorage)\n\n\n@app.get("/getSession")\nasync def _setSession(session: Any = Depends(getSession)):\n    return session\n\n\n @application.post("/deleteSession")\nasync def _deleteSession(\n    sessionId: str = Depends(getSessionId), sessionStorage: SessionStorage = Depends(getSessionStorage)\n):\n    deleteSession(sessionId, sessionStorage)\n    return None\n\n```\n\n## Config\n\n### Deafult Config\n\n- url of Redis: redis://localhost:6379/0\n- name of sessionId: ssid\n- generator function of sessionId: `lambda :uuid.uuid4().hex`\n- expire time of session in redis: 6 hours\n\n### Custom Config\n\n```python\nfrom fastapi_redis_session.config import basicConfig\nbasicConfig(\n    redisURL="redis://localhost:6379/1",\n    sessionIdName="sessionId",\n    sessionIdGenerator=lambda: str(random.randint(1000, 9999)),\n    expireTime=timedelta(days=1),\n    )\n```\n',
    'author': 'duyixian',
    'author_email': 'duyixian1234@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/duyixian1234/fastapi-redis-session',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
