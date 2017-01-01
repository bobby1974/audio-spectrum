# -*- coding: utf-8 -*-
# |----------------------------------------------------------------------| #
# | Copyright (C) Bobby, BH7PRM, 2016                                    | #
# |                                                                      | #
# | This program is free software: you can redistribute it and/or modify | #
# | it under the terms of the GNU General Public License as published by | #
# | the Free Software Foundation, either version 3 of the License, or    | #
# | any later version.                                                   | #
# |                                                                      | #
# | This program is distributed in the hope that it will be useful,      | #
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       | #
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        | #
# | GNU General Public License for more details.                         | #
# |                                                                      | #
# | You should have received a copy of the GNU General Public License    | #
# | along with this program.  If not, see <http://www.gnu.org/licenses/>.| #
# |----------------------------------------------------------------------| #

import numpy as np

import pylab as plt

t  = np.arange(0.0, 5.0, 0.02)

fc1= 1
fc2= 2

y1 = np.sin(2.*np.pi*fc1*t)
y2 = np.sin(2.*np.pi*fc2*t)
y3=y1+y2

#plt.plot(t,y1,label="$y1$",color="green",linewidth=2)
#plt.plot(t,y2,label="$y2$",color="red",linewidth=2)
plt.plot(t,y3,label="$y1+y2$",color="blue",linewidth=2)

plt.xlabel('times')
plt.ylabel('amplitude')
plt.legend(loc='left', shadow=True, fontsize='x-large')
plt.grid()
plt.show()