from epanetmsx import toolkit as msx
import ctypes

MINUTE = 60
HOUR = 60 * 60

def make_array(values):
    arr = msx.floatArray(len(values))
    for i in range(len(values)):
        arr[i] = values[i]
    return arr

def batchExample(fname):
    err = 0
    msx.open()


    # Builing the network from batch-nh2cl.inp
    msx.setFlowFlag(msx.GPM)
    msx.setTimeParameter(msx.DURATION, 168*HOUR)
    msx.setTimeParameter(msx.HYDSTEP, 1*HOUR)
    msx.setTimeParameter(msx.QUALSTEP, 5*MINUTE)
    msx.setTimeParameter(msx.REPORTSTEP, 1*HOUR)
    msx.setTimeParameter(msx.REPORTSTART, 0)
    msx.setTimeParameter(msx.PATTERNSTEP, 1*HOUR)
    msx.setTimeParameter(msx.PATTERNSTART, 0)

    # Add nodes
    msx.addNode("2")
    msx.addTank("1", 19634.953125,0,39269.906250)

    # Add links
    msx.addLink("1", "1", "2", 1000, 12, 100)

    # Add Options
    msx.addOption(msx.AREA_UNITS_OPTION, "FT2")
    msx.addOption(msx.RATE_UNITS_OPTION, "HR")
    msx.addOption(msx.SOLVER_OPTION, "ROS2")
    msx.addOption(msx.COUPLING_OPTION, "FULL")
    msx.addOption(msx.TIMESTEP_OPTION, "300")
    msx.addOption(msx.RTOL_OPTION, "0.0001")
    msx.addOption(msx.ATOL_OPTION, "1.0e-8")

    # Add Species
    msx.setSize(msx.SPECIES, 14)
    msx.addSpecies("HOCL", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("NH3", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("NH2CL", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("NHCL2", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("I", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("OCL", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("NH4", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("ALK", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("H", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("OH", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("CO3", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("HCO3", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("H2CO3", msx.BULK, msx.MOLE, 0.0, 0.0)
    msx.addSpecies("chloramine", msx.BULK, msx.MMOLE, 0.0, 0.0)

    #Add Coefficents
    msx.addCoefficeint(msx.PARAMETER, "k1", 1.5e10)
    msx.addCoefficeint(msx.PARAMETER, "k2", 7.6e-2)
    msx.addCoefficeint(msx.PARAMETER, "k3", 1.0e6)
    msx.addCoefficeint(msx.PARAMETER, "k4", 2.3e-3)
    msx.addCoefficeint(msx.PARAMETER, "k6", 2.2e8)
    msx.addCoefficeint(msx.PARAMETER, "k7", 4.0e5)
    msx.addCoefficeint(msx.PARAMETER, "k8", 1.0e8)
    msx.addCoefficeint(msx.PARAMETER, "k9", 3.0e7)
    msx.addCoefficeint(msx.PARAMETER, "k10", 55.0)

    #Add terms
    msx.addTerm("k5", "(2.5e7*H) + (4.0e4*H2CO3) + (800*HCO3)")
    msx.addTerm("a1", "k1*HOCL*NH3")
    msx.addTerm("a2", "k2*NH2CL")
    msx.addTerm("a3", "k3*HOCL*NH2CL")
    msx.addTerm("a4", "k4*NHCL2")
    msx.addTerm("a5", "k5*NH2CL*NH2CL")
    msx.addTerm("a6", "k6*NHCL2*NH3*H")
    msx.addTerm("a7", "k7*NHCL2*OH")
    msx.addTerm("a8", "k8*I*NHCL2")
    msx.addTerm("a9", "k9*I*NH2CL")
    msx.addTerm("a10", "k10*NH2CL*NHCL2")

    #Add Expressions
    msx.addExpression(msx.LINK, msx.RATE, "HOCL", "-a1 + a2 - a3 + a4 + a8")
    msx.addExpression(msx.LINK, msx.RATE, "NH3", "-a1 + a2 + a5 - a6")
    msx.addExpression(msx.LINK, msx.RATE, "NH2CL", "a1 - a2 - a3 + a4 - a5 + a6 - a9 - a10")
    msx.addExpression(msx.LINK, msx.RATE, "NHCL2", "a3 - a4 + a5 - a6 - a7 - a8 - a10")
    msx.addExpression(msx.LINK, msx.RATE, "I", "a7 - a8 - a9")
    msx.addExpression(msx.LINK, msx.RATE, "H", "0")
    msx.addExpression(msx.LINK, msx.RATE, "ALK", "0")

    msx.addExpression(msx.LINK, msx.EQUIL, "OCL", "H*OCL - 3.16E-8*HOCL")
    msx.addExpression(msx.LINK, msx.EQUIL, "NH4", "H*NH3 - 5.01E-10*NH4")
    msx.addExpression(msx.LINK, msx.EQUIL, "CO3", "H*CO3 - 5.01E-11*HCO3")
    msx.addExpression(msx.LINK, msx.EQUIL, "H2CO3", "H*HCO3 - 5.01E-7*H2CO3")
    msx.addExpression(msx.LINK, msx.EQUIL, "HCO3", "ALK - HCO3 - 2*CO3 - OH + H")
    msx.addExpression(msx.LINK, msx.EQUIL, "OH", "H*OH - 1.0E-14")

    msx.addExpression(msx.LINK, msx.FORMULA, "chloramine", "1000*NH2CL")

    
    #Add Quality
    msx.addQuality("GLOBAL", "NH2CL", 0.05E-3, "")
    msx.addQuality("GLOBAL", "ALK", 0.004, "")
    msx.addQuality("GLOBAL", "H", 2.82e-8, "")

    # Finish Setup
    msx.init()

    # Run
    demands = make_array([0.0, 0.0])
    heads = make_array([10.0, 10.0])
    flows = make_array([0.0])

    msx.setHydraulics(demands, heads, flows)

    t = 0
    tleft = 1
    oldHour = -1
    newHour = 0

    # Example of using the printQuality function in the loop rather than
    # saving results to binary out file and then calling the msx.report function
    while (tleft >= 0 and err == 0):
        if ( oldHour != newHour ):
            print(f"\r  o Computing water quality at hour {newHour}", flush=True, end="")
            msx.printQuality(msx.NODE, "1", "chloramine", fname)
            oldHour = newHour
        t, tleft = msx.step(t, tleft)
        newHour = t // 3600
    
    print("\n")


    # Close
    msx.close()

    return err

# Main
if __name__ == "__main__":
    err = 0
    err = batchExample("out.rpt")