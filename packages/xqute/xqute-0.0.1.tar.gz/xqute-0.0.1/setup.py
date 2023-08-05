# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xqute', 'xqute.schedulers']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.5.0,<0.6.0',
 'diot',
 'psutil>=5.0.0,<6.0.0',
 'rich>=9.0.0,<10.0.0',
 'simplug']

setup_kwargs = {
    'name': 'xqute',
    'version': '0.0.1',
    'description': 'A job management system for python',
    'long_description': '# xqute\n\nA job management system for python\n\n## Features\n\n- Written in async\n- Plugin system\n- Scheduler adaptor\n- Job retrying/pipeline halting when failed\n\n## Installation\n\n```\npip install xqute\n```\n\n## A toy example\n```python\nimport asyncio\nfrom xqute import Xqute\n\nasync def main():\n    xqute = Xqute()\n    await xqute.push([\'echo\', 1])\n    await xqute.push([\'echo\', 2])\n    await xqute.run_until_complete()\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```\n\n## API\nhttps://pwwang.github.io/xqute/\n\n## Usage\n\n### Producer\n\nA producer is initialized by:\n```python\nxqute = Xqute(...)\n```\nAvailable arguments are:\n\n- scheduler: The scheduler class or name\n- job_metadir: The job meta directory (Default: `./.xqute/`)\n- job_error_strategy: The strategy when there is error happened\n- job_num_retries: Max number of retries when job_error_strategy is retry\n- scheduler_forks: Max number of job forks\n- **kwargs: Additional keyword arguments for scheduler\n\nNote that the producer must be initialized in an event loop.\n\nTo push a job into the queue:\n```python\nawait xqute.push([\'echo\', 1])\n```\n\n### Using SGE scheduler\n```python\nxqute = Xqute(\'sge\',\n              scheduler_forks=100,\n              qsub=\'path to qsub\',\n              qdel=\'path to qdel\',\n              qstat=\'path to qstat\',\n              sge_q=\'1-day\',\n              ...)\n```\nKeyword-arguments with names starting with `sge_` will be interpreted as `qsub` options. `list` or `tuple` option values will be expanded. For example:\n`sge_l=[\'h_vmem=2G\', \'gpu=1\']` will be expanded in wrapped script like this:\n```shell\n# ...\n\n#$ -l h_vmem=2G\n#$ -l gpu=1\n\n# ...\n```\n\n### Plugins\n\nTo write a plugin for `xqute`, you will need to implement the following hooks:\n\n- `on_init(scheduler)`: Right after scheduler object is initialized\n- `on_shutdown(scheduler, consumer)`: When scheduler is shutting down\n- `on_job_init(scheduler, job)`: When the job is initialized\n- `on_job_queued(scheduler, job)`: When the job is queued\n- `on_job_submitted(scheduler, job)`: When the job is submitted\n- `on_job_killing(scheduler, job)`: When the job is being killed\n- `on_job_killed(scheduler, job)`: When the job is killed\n- `on_job_failed(scheduler, job)`: When the job is failed\n- `on_job_succeeded(scheduler, job)`: When the job is succeeded\n- `on_complete(scheduler)`: When all jobs complete\n\nNote that all hooks are corotines, that means you should also implement them as corotines (sync implementations are allowed but will be warned).\n\nTo implement a hook, you have to fetch the plugin manager:\n\n```python\nfrom simplug import Simplug\npm = Simplug(\'xqute\')\n\n# or\nfrom xqute import simplug as pm\n```\n\nand then use the decorator `pm.impl`:\n\n```python\n@pm.impl\nasync def on_init(scheduler):\n    ...\n```\n\n### Implementing a scheduler\n\nCurrently there are only 2 builtin schedulers: `local` and `sge`.\n\nOne can implement a scheduler by subclassing the `Scheduler` abstract class. There are three abstract methods that have to be implemented in the subclass:\n\n```python\nfrom xqute import Scheduer\n\nclass MyScheduler(Scheduler):\n    name = \'my\'\n    job_class: MyJob\n\n    async def submit_job(self, job):\n        """How to submit a job, return a unique id in the scheduler system\n        (the pid for local scheduler for example)\n        """\n\n    async def kill_job(self, job):\n        """How to kill a job"""\n\n    async def job_is_running(self, job):\n        """Check if a job is running\n\n        The uid can be retrieved from job.lock_file\n        """\n```\n\nAs you may see, we may also need to implement a job class before `MyScheduler`. The only abstract method to be implemented is `wrap_cmd`:\n```python\nfrom xqute import Job\n\nclass MyJob(Job):\n\n    async def wrap_cmd(self, scheduler):\n        ...\n```\n\nYou have to use the trap command in the wrapped script to update job status, return code and clear the lock file.\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwwang/xqute',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
