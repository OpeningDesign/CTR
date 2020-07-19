from materials.ec3 import EC3Beam as ec3b
from materials.ec3 import EC3_limit_state_checking as EC3lsc

# ** Steel beams
# Support coefficients (1==free, 0.5==prevented) (all default to 1)
# ky: lateral bending, kw: warping, k1: warping and lateral bending at left
# end, k2:  warping and lateral bending at right end

supCf_free=EC3lsc.SupportCoefficients(ky=1.0,kw=1.0,k1=1.0,k2=1.0)
supCf=EC3lsc.SupportCoefficients(ky=1.0,kw=1.0,k1=0.5,k2=1.0)

# Beams definition
col01a_ln=gridGeom.getLstLinRange(gm.IJKRange((0,lastYpos,0),(0,lastYpos,1)))
col01a=ec3b.EC3Beam(name='col01a',ec3Shape=columnZsteel_mat,sectionClass=1,supportCoefs=supCf_free,lstLines=col01a_ln)
col01a.setControlPoints()
col01a.installULSControlRecorder(recorderType="element_prop_recorder")

col01b_ln=gridGeom.getLstLinRange(gm.IJKRange((0,lastYpos,1),(0,lastYpos,lastZpos)))
col01b=ec3b.EC3Beam(name='col01b',ec3Shape=columnZsteel_mat,sectionClass=1,supportCoefs=supCf_free,lstLines=col01b_ln)
col01b.setControlPoints()
col01b.installULSControlRecorder(recorderType="element_prop_recorder")

col02a_pnt=gridGeom.getLstPntRange(gm.IJKRange((lastXpos,lastYpos,0),(lastXpos,lastYpos,1)))
col02a=ec3b.EC3Beam(name='col02a',ec3Shape=columnZsteel_mat,sectionClass=1,supportCoefs=supCf_free,lstPoints=col02a_pnt)
col02a.setControlPoints()
col02a.installULSControlRecorder(recorderType="element_prop_recorder")

col02b_pnt=gridGeom.getLstPntRange(gm.IJKRange((lastXpos,lastYpos,1),(lastXpos,lastYpos,lastZpos)))
col02b=ec3b.EC3Beam(name='col02b',ec3Shape=columnZsteel_mat,sectionClass=1,supportCoefs=supCf_free,lstPoints=col02b_pnt)
col02b.setControlPoints()
col02b.installULSControlRecorder(recorderType="element_prop_recorder")

col03_ln=gridGeom.getLstLinRange(gm.IJKRange((1,lastYpos,0),(1,lastYpos,1)))
col03=ec3b.EC3Beam(name='col03',ec3Shape=columnZsteel_mat,sectionClass=1,supportCoefs=supCf,lstLines=col03_ln)
col03.setControlPoints()
col03.installULSControlRecorder(recorderType="element_prop_recorder")

beam01_pnt=gridGeom.getLstPntRange(gm.IJKRange((0,2,lastZpos),(lastXpos,2,lastZpos)))
beam01=ec3b.EC3Beam(name='beam01',ec3Shape=beamXsteel_mat,sectionClass=1,supportCoefs=supCf_free,lstPoints=beam01_pnt)
beam01.setControlPoints()
beam01.installULSControlRecorder(recorderType="element_prop_recorder")
