import os

try:
    from .version import __version__, __jsbsim_version__  # noqa: F401
except ImportError:
    pass

from gym.envs.registration import registry, register, make, spec
from gym_jsbsim.envs import TASKS
from gym_jsbsim.catalogs import Catalog

"""

This script registers JSBSimEnv

with OpenAI Gym so that they can be instantiated with a gym.make(id)

 command.


 To use do:

       env = gym.make('GymJsbsim-{task}-v0')

"""

if "JSBSIM_ROOT_DIR" not in os.environ:
    os.environ["JSBSIM_ROOT_DIR"] = os.path.join(os.path.dirname(__file__), "jsbsim-" + __jsbsim_version__)

for task_name in TASKS:
    register(
        id=f"GymJsbsim-{task_name}-v0",
        entry_point="gym_jsbsim.jsbsim_env:JSBSimEnv",
        kwargs=dict(task=TASKS[task_name]),
    )
