import pytest
from epanetmsx import toolkit as msx

def make_array(values):
    arr = msx.floatArray(len(values))
    for i in range(len(values)):
        arr[i] = values[i]
    return arr

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


def test_getindex():
    create_example()
    assert msx.getindex(msx.NODE, "second") == 2
    assert msx.getindex(msx.NODE, "source") == 5
    assert msx.getindex(msx.TANK, "source") == 1
    assert msx.getindex(msx.LINK, "2") == 2
    assert msx.getindex(msx.SPECIES, "AS5") == 2
    assert msx.getindex(msx.CONSTANT, "Kb") == 2
    msx.close()

def test_getIDlen():
    create_example()
    assert msx.getIDlen(msx.NODE, 2) == 6
    assert msx.getIDlen(msx.NODE, 5) == 6
    assert msx.getIDlen(msx.TANK, 1) == 6
    assert msx.getIDlen(msx.LINK, 2) == 1
    assert msx.getIDlen(msx.SPECIES, 2) == 3
    assert msx.getIDlen(msx.CONSTANT, 2) == 2
    msx.close()

def test_getID():
    create_example()
    assert msx.getID(msx.NODE, 2, msx.MAXID) == "second"
    assert msx.getID(msx.NODE, 5, msx.MAXID) == "source"
    assert msx.getID(msx.TANK, 1, msx.MAXID) == "source"
    assert msx.getID(msx.LINK, 2, msx.MAXID) == "2"
    assert msx.getID(msx.SPECIES, 2, msx.MAXID) == "AS5"
    assert msx.getID(msx.CONSTANT, 2, msx.MAXID) == "Kb"
    msx.close()


def test_getcount():
    create_example()
    assert msx.getcount(msx.NODE) == 5
    assert msx.getcount(msx.TANK) == 1
    assert msx.getcount(msx.LINK) == 5
    assert msx.getcount(msx.SPECIES) == 5
    assert msx.getcount(msx.PARAMETER) == 0
    assert msx.getcount(msx.CONSTANT) == 5
    assert msx.getcount(msx.PATTERN) == 0
    msx.close()

def test_getspecies():
    msx.open()
    msx.addSpecies("AS3", msx.BULK, msx.UG, 3.0, 5.0)
    msx.addSpecies("AS5", msx.BULK, msx.MG, 6.0, 10.0)
    msx.addSpecies("AStot", msx.WALL, msx.UG, 90.0, 5.0)
    type, units, aTol, rTol = msx.getspecies(1)
    assert type == msx.BULK and units == "UG" and aTol == 3.0 and rTol == 5.0
    type, units, aTol, rTol = msx.getspecies(2)
    assert type == msx.BULK and units == "MG" and aTol == 6.0 and rTol == 10.0
    type, units, aTol, rTol = msx.getspecies(3)
    assert type == msx.WALL and units == "UG" and aTol == 90.0 and rTol == 5.0
    msx.close()

def test_sim1():
    create_example()
    msx.init()
    demands = make_array([0.040220, 0.033353, 0.053953, 0.022562, -0.150088])
    heads = make_array([327.371979, 327.172974, 327.164185, 326.991211, 328.083984])
    flows = make_array([0.150088, 0.039916, 0.069952, 0.006563, 0.022562])
    msx.setHydraulics(demands, heads, flows)
    t = 0
    tleft = -1
    qual = []
    for _ in range(5):
        t, tleft = msx.step(t, tleft)
        qual.append(round(msx.getQualityByID(msx.LINK, "5", "AS5s"), 5))
    assert qual == [0.00013, 0.00009, 0.00004, 0.54024, 3.69831]


    





