# -*- coding: utf-8 -*-
from postprocess.config import default_config

#home= '/home/ana/projects/XCmodels/'
#home= '/home/ana/projects/XCmodels/OXapp/embedded_beams/'
home= '/home/ana/projects/XCmodels/OXapp/embedded_beams/ramp/'

# Default configuration of environment variables.
cfg=default_config.envConfig(language='en',intForcPath= home + 'results/internalForces/',verifPath= home + 'results/verifications/',annexPath= home + 'annex/',grWidth='\linewidth')
