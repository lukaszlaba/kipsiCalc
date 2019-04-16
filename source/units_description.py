'''
--------------------------------------------------------------------------
Copyright (C) 2016-2017 Lukasz Laba <lukaszlab@o2.pl>

This file is part of ksipsiCalc.
ksipsiCalc - simple calculator supporting unit calculations.

ksipsiCalc is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

ksipsiCalc is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ksipsiCalc; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

description = {}

# metric
description['kg'] = 'mass: metric kilogram'

description['m'] = 'length: metric meter'
description['mm'] = 'length: metric millimeter'

# imperial
description['inch'] = 'length: imperial inch'
description['ft'] = 'length: imperial foot'
description['yd'] = 'length: imperial yard'
description['mile'] = 'length: imperial mile'

description['lb'] = 'mass: imperial pound'

description['lbf'] = 'force: imperial pound-force'
description['kip'] = 'force: imperial kilo pound-force'




def unit_description(unit):
    if unit in description.keys():
        return description[unit]
    else:
     return '-'