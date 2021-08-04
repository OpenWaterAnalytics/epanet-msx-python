import pytest
from epanetmsx import toolkit as msx


def create_example():
    msx.open()
    HOUR = 60 * 60
    # Builing the network from example.inp
    msx.setFlowFlag(msx.CMH)
    msx.setTimeParameter(msx.DURATION, 80*HOUR)
    msx.setTimeParameter(msx.HYDSTEP, 1*HOUR)
    msx.setTimeParameter(msx.QUALSTEP, 8*HOUR)
    msx.setTimeParameter(msx.REPORTSTEP, 8*HOUR)
    msx.setTimeParameter(msx.REPORTSTART, 0)

    # Add nodes
    msx.addNode("first")
    msx.addNode("second")
    msx.addNode("third")
    msx.addNode("fourth")
    msx.addReservoir("source", 0,0,0)

    # Add links
    msx.addLink("1", "source", "first", 1000, 200, 100)
    msx.addLink("2", "first", "second", 800, 150, 100)
    msx.addLink("3", "first", "third", 1200, 200, 100)
    msx.addLink("4", "second", "third", 1000, 150, 100)
    msx.addLink("5", "third", "fourth", 2000, 150, 100)

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
    return


def test_get_count():
    create_example()
    assert msx.getcount(msx.NODE) == 5
    assert msx.getcount(msx.TANK) == 1
    assert msx.getcount(msx.LINK) == 5
    assert msx.getcount(msx.SPECIES) == 5
    assert msx.getcount(msx.PARAMETER) == 0
    assert msx.getcount(msx.CONSTANT) == 5
    assert msx.getcount(msx.PATTERN) == 0
    msx.close()

