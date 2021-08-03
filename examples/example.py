from epanetmsx import toolkit as msx

MINUTE = 60
HOUR = 60 * 60

def make_array(values):
    arr = msx.floatArray(len(values))
    for i in range(len(values)):
        arr[i] = values[i]
    return arr

def example(fname):
    err = 0
    msx.open()

    # Builing the network from example.inp
    msx.setFlowFlag(msx.CMH)
    msx.setTimeParameter(msx.DURATION, 80*HOUR)
    msx.setTimeParameter(msx.HYDSTEP, 1*HOUR)
    msx.setTimeParameter(msx.QUALSTEP, 8*HOUR)
    msx.setTimeParameter(msx.REPORTSTEP, 8*HOUR)
    msx.setTimeParameter(msx.REPORTSTART, 0)

    # Add nodes
    msx.addNode("a")
    msx.addNode("b")
    msx.addNode("c")
    msx.addNode("e")
    msx.addReservoir("source", 0,0,0)
    # Add links
    msx.addLink("1", "source", "a", 1000, 200, 100)
    msx.addLink("2", "a", "b", 800, 150, 100)
    msx.addLink("3", "a", "c", 1200, 200, 100)
    msx.addLink("4", "b", "c", 1000, 150, 100)
    msx.addLink("5", "c", "e", 2000, 150, 100)

    # Add Options
    msx.addOption(msx.AREA_UNITS_OPTION, "M2")
    msx.addOption(msx.RATE_UNITS_OPTION, "HR")
    msx.addOption(msx.SOLVER_OPTION, "RK5")
    msx.addOption(msx.TIMESTEP_OPTION, "28800")
    msx.addOption(msx.RTOL_OPTION, "0.001")
    msx.addOption(msx.ATOL_OPTION, "0.0001")

    # Add Species
    msx.addSpecies("AS3", msx.BULK, msx.UG, 0.0, 0.0)
    msx.addSpecies("AS5", msx.BULK, msx.UG, 0.0, 0.0)
    msx.addSpecies("AStot", msx.BULK, msx.UG, 0.0, 0.0)
    msx.addSpecies("AS5s", msx.WALL, msx.UG, 0.0, 0.0)
    msx.addSpecies("NH2CL", msx.BULK, msx.MG, 0.0, 0.0)
    
    #Add Coefficents
    msx.addCoefficeint(msx.CONSTANT, "Ka", 10.0)
    msx.addCoefficeint(msx.CONSTANT, "Kb", 0.1)
    msx.addCoefficeint(msx.CONSTANT, "K1", 5.0)
    msx.addCoefficeint(msx.CONSTANT, "K2", 1.0)
    msx.addCoefficeint(msx.CONSTANT, "Smax", 50)

    #Add terms
    msx.addTerm("Ks", "K1/K2")

    #Add Expressions
    msx.addExpression(msx.LINK, msx.RATE, "AS3", "-Ka*AS3*NH2CL")
    msx.addExpression(msx.LINK, msx.RATE, "AS5", "Ka*AS3*NH2CL-Av*(K1*(Smax-AS5s)*AS5-K2*AS5s)")
    msx.addExpression(msx.LINK, msx.RATE, "NH2CL", "-Kb*NH2CL")
    msx.addExpression(msx.LINK, msx.EQUIL, "AS5s", "Ks*Smax*AS5/(1+Ks*AS5)-AS5s")
    msx.addExpression(msx.LINK, msx.FORMULA, "AStot", "AS3 + AS5")

    msx.addExpression(msx.TANK, msx.RATE, "AS3", "-Ka*AS3*NH2CL")
    msx.addExpression(msx.TANK, msx.RATE, "AS5", "Ka*AS3*NH2CL")
    msx.addExpression(msx.TANK, msx.RATE, "NH2CL", "-Kb*NH2CL")
    msx.addExpression(msx.TANK, msx.FORMULA, "AStot", "AS3+AS5")

    #Add Quality
    msx.addQuality("NODE", "AS3", 10.0, "source")
    msx.addQuality("NODE", "NH2CL", 2.5, "source")

    #Setup Report
    msx.setReport("NODE", "c", 2)
    msx.setReport("NODE", "e", 2)
    msx.setReport("LINK", "5", 2)
    msx.setReport("SPECIE", "AStot", 2)
    msx.setReport("SPECIE", "AS3", 2)
    msx.setReport("SPECIE", "AS5", 2)
    msx.setReport("SPECIE", "AS5s", 2)
    msx.setReport("SPECIE", "NH2CL", 2)

    # Finish Setup
    msx.init()

    # Run
    demands = make_array([0.040220, 0.033353, 0.053953, 0.022562, -0.150088])
    heads = make_array([327.371979, 327.172974, 327.164185, 326.991211, 328.083984])
    flows = make_array([0.150088, 0.039916, 0.069952, 0.006563, 0.022562])
    msx.setHydraulics(demands, heads, flows)
    t = 0
    tleft = 1
    oldHour = -1
    newHour = 0

    # Example of using the printQuality function in the loop rather than
    # saving results to binary out file and then calling the MSXreport function
    while (tleft >= 0 and err == 0):
        if ( oldHour != newHour ):
            print(f"\r  o Computing water quality at hour {newHour}", flush=True)
            msx.printQuality(msx.LINK, "4", "AS5s", fname)
            msx.printQuality(msx.LINK, "5", "AS5s", fname)
            oldHour = newHour
        t, tleft = msx.step(t, tleft)
        newHour = t / 3600
    print("\n")





    # Close
    msx.close()

    return err

# Main
if __name__ == "__main__":
    err = 0
    err = example("")