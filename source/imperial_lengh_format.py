'''
--------------------------------------------------------------------------
Copyright (C) 2019 Łukasz Laba (e-mail : lukaszlaba@gmail.pl)

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

from units import *

def imperial_lengh_format(dist = 22.9*ft):
    
    foot_mumber = (int((dist / ft).asNumber()))
    inch_number = (int(( (dist- foot_mumber*ft)/ inch).asNumber()))
    rest = dist - (foot_mumber*ft + inch_number*inch)
    rest_inch = round((rest/inch).asNumber(), 3)
    
    return '%s*ft + %s*inch'%(foot_mumber, (inch_number + rest_inch))
     
if __name__ == '__main__':     
    print (imperial_lengh_format())