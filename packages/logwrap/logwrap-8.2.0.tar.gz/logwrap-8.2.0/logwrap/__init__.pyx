#    Copyright 2018 - 2020 Alexey Stepanov aka penguinolog
##
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""logwrap module.

Contents: 'logwrap', 'pretty_repr', 'pretty_str'

Original code was made for Mirantis Inc by Alexey Stepanov,
later it has been reworked and extended for support of special cases.
"""

# Package Implementation
from logwrap.log_on_access import LogOnAccess
from logwrap.log_wrap import BoundParameter
from logwrap.log_wrap import LogWrap
from logwrap.log_wrap import bind_args_kwargs
from logwrap.log_wrap import logwrap
from logwrap.repr_utils import PrettyFormat
from logwrap.repr_utils import PrettyRepr
from logwrap.repr_utils import PrettyStr
from logwrap.repr_utils import pretty_repr
from logwrap.repr_utils import pretty_str


cpdef tuple __all__ = (
    "LogWrap",
    "logwrap",
    "PrettyFormat",
    "PrettyRepr",
    "PrettyStr",
    "pretty_repr",
    "pretty_str",
    "BoundParameter",
    "bind_args_kwargs",
    "LogOnAccess",
)

cpdef str __version__

try:
    # Local Implementation
    from ._version import version as __version__
except ImportError:
    pass

cpdef str __author__ = "Alexey Stepanov"
cpdef str __author_email__ = "penguinolog@gmail.com"
cpdef dict __maintainers__ = {
    "Alexey Stepanov": "penguinolog@gmail.com",
    "Antonio Esposito": "esposito.cloud@gmail.com",
    "Dennis Dmitriev": "dis-xcom@gmail.com",
}
cpdef str __url__ = "https://github.com/python-useful-helpers/logwrap"
cpdef str __description__ = "Decorator for logging function arguments and return value by human-readable way"
cpdef str __license__ = "Apache License, Version 2.0"
