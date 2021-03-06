#!/usr/bin/python
#
# Copyright 2013 Tails developers <tails@boum.org>
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#
"""Tails-greeter exceptions

"""

class TailsGreeterError(Exception):
    pass

class LivePersistError(TailsGreeterError):
    pass

class WrongPassphraseError(LivePersistError):
    pass

class GdmServerNotReady(TailsGreeterError):
    """Called something that needs GDM server to be ready, which is not the case yet."""
    pass
