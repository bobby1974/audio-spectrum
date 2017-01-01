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

x = np.linspace(-np.pi, np.pi, 256, endpoint=True)
y1 = np.cos(x)
y2 = np.sin(x)

plt.plot(x,y1)
plt.plot(x,y2)

plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
       [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])

plt.yticks([-1, 0, +1],
       [r'$-1$', r'$0$', r'$+1$'])

#plt.plot(y1, 'k:', label='cosine')

plt.plot(x,y1,label="$cos(x)$",color="red",linewidth=2)
plt.plot(x,y2,label="$sin(x)$",color="blue",linewidth=1)

plt.xlabel('times')
plt.ylabel('amplitude')
plt.legend(loc='upper right', shadow=True, fontsize='x-large')
plt.grid()
plt.show()