from epanetmsx import toolkit as msx
import ctypes

def call(err, f):
    if err > 100:
        return err
    else:
        return f

MINUTE = 60
HOUR = 60 * 60

def make_array(values):
    arr = msx.floatArray(len(values))
    for i in range(len(values)):
        arr[i] = values[i]
    return arr

def batchExample(fname):
    err = 0
    call(err, msx.open())


    # Builing the network from batch-nh2cl.inp
    call(err, msx.setFlowFlag(msx.GPM))
    call(err, msx.setTimeParameter(msx.DURATION, 168*HOUR))
    call(err, msx.setTimeParameter(msx.HYDSTEP, 1*HOUR))
    call(err, msx.setTimeParameter(msx.QUALSTEP, 5*MINUTE))
    call(err, msx.setTimeParameter(msx.REPORTSTEP, 1*HOUR))
    call(err, msx.setTimeParameter(msx.REPORTSTART, 0))
    call(err, msx.setTimeParameter(msx.PATTERNSTEP, 1*HOUR))
    call(err, msx.setTimeParameter(msx.PATTERNSTART, 0))

    # Add nodes
    call(err, msx.addNode("2"))
    call(err, msx.addTank("1", 19634.953125,0,39269.906250))

    # Add links
    call(err, msx.addLink("1", "1", "2", 1000, 12, 100))

    # Add Options
    call(err, msx.addOption(msx.AREA_UNITS_OPTION, "FT2"))
    call(err, msx.addOption(msx.RATE_UNITS_OPTION, "HR"))
    call(err, msx.addOption(msx.SOLVER_OPTION, "ROS2"))
    call(err, msx.addOption(msx.COUPLING_OPTION, "FULL"))
    call(err, msx.addOption(msx.TIMESTEP_OPTION, "300"))
    call(err, msx.addOption(msx.RTOL_OPTION, "0.0001"))
    call(err, msx.addOption(msx.ATOL_OPTION, "1.0e-8"))
    # Add Species
    call(err, msx.setSize(msx.SPECIES, 14))
    call(err, msx.addSpecies("HOCL", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("NH3", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("NH2CL", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("NHCL2", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("I", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("OCL", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("NH4", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("ALK", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("H", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("OH", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("CO3", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("HCO3", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("H2CO3", msx.BULK, msx.MOLE, 0.0, 0.0))
    call(err, msx.addSpecies("chloramine", msx.BULK, msx.MMOLE, 0.0, 0.0))

    #Add Coefficents
    call(err, msx.addCoefficeint(msx.PARAMETER, "k1", 1.5e10))
    call(err, msx.addCoefficeint(msx.PARAMETER, "k2", 7.6e-2))
    call(err, msx.addCoefficeint(msx.PARAMETER, "k3", 1.0e6))
    call(err, msx.addCoefficeint(msx.PARAMETER, "k4", 2.3e-3))
    call(err, msx.addCoefficeint(msx.PARAMETER, "k6", 2.2e8))
    call(err, msx.addCoefficeint(msx.PARAMETER, "k7", 4.0e5))
    call(err, msx.addCoefficeint(msx.PARAMETER, "k8", 1.0e8))
    call(err, msx.addCoefficeint(msx.PARAMETER, "k9", 3.0e7))
    call(err, msx.addCoefficeint(msx.PARAMETER, "k10", 55.0))

    #Add terms
    call(err, msx.addTerm("k5", "(2.5e7*H) + (4.0e4*H2CO3) + (800*HCO3)"))
    call(err, msx.addTerm("a1", "k1*HOCL*NH3"))
    call(err, msx.addTerm("a2", "k2*NH2CL"))
    call(err, msx.addTerm("a3", "k3*HOCL*NH2CL"))
    call(err, msx.addTerm("a4", "k4*NHCL2"))
    call(err, msx.addTerm("a5", "k5*NH2CL*NH2CL"))
    call(err, msx.addTerm("a6", "k6*NHCL2*NH3*H"))
    call(err, msx.addTerm("a7", "k7*NHCL2*OH"))
    call(err, msx.addTerm("a8", "k8*I*NHCL2"))
    call(err, msx.addTerm("a9", "k9*I*NH2CL"))
    call(err, msx.addTerm("a10", "k10*NH2CL*NHCL2"))

    #Add Expressions
    call(err, msx.addExpression(msx.LINK, msx.RATE, "HOCL", "-a1 + a2 - a3 + a4 + a8"))
    call(err, msx.addExpression(msx.LINK, msx.RATE, "NH3", "-a1 + a2 + a5 - a6"))
    call(err, msx.addExpression(msx.LINK, msx.RATE, "NH2CL", "a1 - a2 - a3 + a4 - a5 + a6 - a9 - a10"))
    call(err, msx.addExpression(msx.LINK, msx.RATE, "NHCL2", "a3 - a4 + a5 - a6 - a7 - a8 - a10"))
    call(err, msx.addExpression(msx.LINK, msx.RATE, "I", "a7 - a8 - a9"))
    call(err, msx.addExpression(msx.LINK, msx.RATE, "H", "0"))
    call(err, msx.addExpression(msx.LINK, msx.RATE, "ALK", "0"))

    call(err, msx.addExpression(msx.LINK, msx.EQUIL, "OCL", "H*OCL - 3.16E-8*HOCL"))
    call(err, msx.addExpression(msx.LINK, msx.EQUIL, "NH4", "H*NH3 - 5.01E-10*NH4"))
    call(err, msx.addExpression(msx.LINK, msx.EQUIL, "CO3", "H*CO3 - 5.01E-11*HCO3"))
    call(err, msx.addExpression(msx.LINK, msx.EQUIL, "H2CO3", "H*HCO3 - 5.01E-7*H2CO3"))
    call(err, msx.addExpression(msx.LINK, msx.EQUIL, "HCO3", "ALK - HCO3 - 2*CO3 - OH + H"))
    call(err, msx.addExpression(msx.LINK, msx.EQUIL, "OH", "H*OH - 1.0E-14"))

    call(err, msx.addExpression(msx.LINK, msx.FORMULA, "chloramine", "1000*NH2CL"))

    
    #Add Quality
    call(err, msx.addQuality("GLOBAL", "NH2CL", 0.05E-3, ""))
    call(err, msx.addQuality("GLOBAL", "ALK", 0.004, ""))
    call(err, msx.addQuality("GLOBAL", "H", 2.82e-8, ""))

    #Setup Report
    call(err, msx.setReport("NODE", "1", 0))
    call(err, msx.setReport("SPECIE", "chloramine", 4))

    # Finish Setup
    call(err, msx.init())

    # Run
    demands = make_array([0.0, 0.0])
    heads = make_array([10.0, 10.0])
    flows = make_array([0.0])

    call(err, msx.setHydraulics(demands, heads, flows))

    t = 0
    tleft = 1
    oldHour = -1
    newHour = 0

    # Example of using the printQuality function in the loop rather than
    # saving results to binary out file and then calling the msx.report function
    while (tleft >= 0 and err == 0):
        if ( oldHour != newHour ):
            print(f"\r  o Computing water quality at hour {newHour}")
            call(err, msx.printQuality(msx.NODE, "1", "chloramine", fname))
            oldHour = newHour
        t, tleft = msx.step(t, tleft)
        newHour = t // 3600
    
    print("\n")


    # Close
    call(err, msx.close())

    return err



if __name__ == "__main__":
    err = 0
    err = batchExample("")
    print(err)