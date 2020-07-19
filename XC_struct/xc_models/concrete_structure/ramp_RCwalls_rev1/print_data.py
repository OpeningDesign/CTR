print ('Ramp walls and steel structure bearing hollowcore 2nd floor')

print('* Materials \\\\')
print('Concrete grade & C4000 \\\\')
print('Reinforcing steel grade & ASTM A615 Gr60  \\\\')
print('Structural steel & ASTM A36 \\\\')

print('* Loads \\\\')

print('** Earth pressure \\\\')
print('Internal friction angle (radians) & ', round(firad,3), '\\\\')
print('Coefficient of earth pressure at rest  & ', round(KearthPress,2), '\\\\')
print('Mass density of the soil (kg/m3)  & ', round(densSoil,2), '\\\\')
print('Horizontal force [N/m] due to earth pressure over East wall & ',Earth_E1F
, '\\\\')

print('**Dead load \\\\')
print('DL West \& East walls 2nd floor [N/m] & ', Dead_WE2F, '\\\\')
print('DL East wall 1st floor [N/m] & ', Dead_E1F, '\\\\')
print('DL steel beam North facade [N/m] & ', Dead_stbeam, '\\\\')
print('DL steel cantilever (West side) [N/m]  & ', Dead_Ccant, '\\\\')
print('DL steel cantilever (Central) [N/m]  & ', Dead_Ccant, '\\\\')
print('DL steel cantilever  (East side) [N/m]  & ', round(Dead_Ecant,1), '\\\\')

print('**Live load \\\\')
print('LL West \& East walls 2nd floor [N/m] & ', Live_WE2F, '\\\\')
print('LL East wall 1st floor [N/m] & ', Live_E1F, '\\\\')
print('LL steel beam North facade [N/m] & ', Live_stbeam, '\\\\')
print('LL steel cantilever (West side) [N/m]  & ', Live_Ccant, '\\\\')
print('LL steel cantilever (Central) [N/m]  & ', Live_Ccant, '\\\\')
print('LL steel cantilever  (East side) [N/m]  & ', round(Live_Ecant,1), '\\\\')

print('**Snow load \\\\')
print('SL West \& East walls 2nd floor [N/m] & ', Snow_WE2F, '\\\\')
print('SL East wall 1st floor [N/m] & ', Snow_E1F, '\\\\')
print('SL steel beam North facade [N/m] & ', Snow_stbeam, '\\\\')
print('SL steel cantilever (West side) [N/m]  & ', Snow_Ccant, '\\\\')
print('SL steel cantilever (Central) [N/m]  & ', Snow_Ccant, '\\\\')
print('SL steel cantilever  (East side) [N/m]  & ', round(Snow_Ecant,1), '\\\\')


print('**Wind load \\\\')
print('WL West \& East walls 2nd floor [N/m] (vertical) & ',-Wind_WE2F, '\\\\')
print('WL West \& East walls 2nd floor [N/m] (horizontal) & ', WindH_E2F, '\\\\')
print('WL East wall 1st floor [N/m]  (vertical) & ',-Wind_E1F, '\\\\')
