# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from misc_utils import log_messages as lmsg

lmsg.warning('Implementation pending. Do not use.')
quit()

execfile("../env_config_deck.py")
execfile("../model_gen.py") #FE model generation
execfile(path_loads_def+"loadComb_deck.py")

combs=combContainer.SLS.rare

found_wink.displayMaxPressures(FEcase=FEcase,combs=combs,caption="Zapata estribo. Presiones máximas en el terreno",fUnitConv=1e-6,unitDescription='[MPa]',rgMinMax=None,fileName='pp')


