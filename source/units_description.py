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


description['kg'] = 'mass: metric kilogram'
description['lb'] = 'mass: imperial pound'


description['um'] = 'length: metric micrometer'
description['mm'] = 'length: metric millimeter'
description['cm'] = 'length: metric centimeter'
description['dm'] = 'length: metric decimeter'
description['m'] = 'length: metric meter'
description['km'] = 'length: metric kilometer'

description['inch'] = 'length: imperial inch'
description['ft'] = 'length: imperial foot'
description['yd'] = 'length: imperial yard'
description['mile'] = 'length: imperial mile'

description['mm2'] = 'area: metric square millimeter'
description['cm2'] = 'area: metric square centimeter'
description['m2'] = 'area: metric square meter'
description['ha'] = 'area: metric hectare'

description['inch2'] = 'area: imperial square inch'
description['ft2'] = 'area: imperial square foot'
description['yd2'] = 'area: imperial square yard'


description['mm3'] = 'volume: metric cubic millimeter'
description['cm3'] = 'volume: metric cubic centimeter'
description['m3'] = 'volume: metric cubic meter'

description['inch3'] = 'volume: imperial cubic inch'
description['ft3'] = 'volume: imperial cubic foot'


description['lbf'] = 'force: imperial pound-force'
description['kip'] = 'force: imperial kilopound-force'


description['lbfinch'] = 'moment of force: imperial pound-force at inch arm'
description['lbfft'] = 'moment of force: imperial pound-force at foot arm'
description['kipft'] = 'moment of force: imperial kip at foot arm'
description['kipinch'] = 'moment of force: imperial kip at inch arm'


description['psi'] = 'pressure: imperial pound-force per square inch'
description['ksi'] = 'pressure: imperial kilopound-force per square inch'
description['psf'] = 'pressure: imperial pound-force per square foot'
description['ksf'] = 'pressure: imperial kilopound-force per square foot'


description['plf'] = 'force per length: imperial pound-force per foot'


description['s'] = 'time: second'
description['h'] = 'time: hour'

def unit_description(unit):
    if unit in description.keys():
        return description[unit]
    else:
     return ' ( - )'