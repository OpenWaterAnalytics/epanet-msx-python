import pytest
from epanetmsx import toolkit as msx

def make_floatarray(values):
    arr = msx.floatArray(len(values))
    for i in range(len(values)):
        arr[i] = values[i]
    return arr

def make_doublearray(values):
    arr = msx.doubleArray(len(values))
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

def test_getconstant():
    msx.open()
    msx.addCoefficeint(msx.CONSTANT, "a", 100.0)
    msx.addCoefficeint(msx.CONSTANT, "b", 1.0)
    msx.addCoefficeint(msx.CONSTANT, "c", 88.0)
    values = []
    values.append(msx.getconstant(1))
    values.append(msx.getconstant(2))
    values.append(msx.getconstant(3))
    assert values == [100.0, 1.0, 88.0]
    msx.close()

def test_getparameter():
    msx.open()
    msx.addNode("a")
    msx.addNode("b")
    msx.addLink("1", "a", "b", 1000, 4, 100)
    msx.addCoefficeint(msx.PARAMETER, "a", 100.0)
    msx.addParameter("PIPE", "a", 100.0, "1")
    values = msx.getparameter(msx.LINK, 1, 1)
    assert values == 100.0
    msx.close()

def test_getsource():
    msx.open()
    msx.addNode("a")
    msx.addNode("b")
    msx.addLink("1", "a", "b", 1000, 4, 100)
    msx.addSpecies("nh2cl", msx.BULK, msx.UG, 1.0, 2.0)
    arr = make_doublearray([3.3, 4.4, 5.5])
    msx.addpattern("p")
    msx.setpattern(1, arr, 3)
    msx.addSource(msx.CONCEN, "a", "nh2cl", 900.0, "p")
    t, level, pat = msx.getsource(1, 1)
    assert t == msx.CONCEN and level == 900.0 and pat == 1
    msx.close()

def test_getpatternlen():
    msx.open()
    msx.addNode("a")
    msx.addNode("b")
    msx.addLink("1", "a", "b", 1000, 4, 100)
    msx.addSpecies("nh2cl", msx.BULK, msx.UG, 1.0, 2.0)
    arr = make_doublearray([3.3, 4.4, 5.5])
    msx.addpattern("p")
    msx.setpattern(1, arr, 3)
    length = msx.getpatternlen(1)
    assert length == 3
    msx.close()

def test_getpattern():
    msx.open()
    msx.addNode("a")
    msx.addNode("b")
    msx.addLink("1", "a", "b", 1000, 4, 100)
    msx.addSpecies("nh2cl", msx.BULK, msx.UG, 1.0, 2.0)
    arr = make_doublearray([3.3, 4.4, 5.5])
    msx.addpattern("p")
    msx.setpattern(1, arr, 3)
    values = []
    values.append(msx.getpatternvalue(1,1))
    values.append(msx.getpatternvalue(1,2))
    values.append(msx.getpatternvalue(1,3))
    assert values == [3.3, 4.4, 5.5]
    msx.close()

def test_getinitqual():
    create_example()
    init = msx.getinitqual(msx.NODE, 1, 2)
    assert init == 0
    msx.close()

def test_quality_by_index():
    create_example()
    msx.init()
    demands = make_floatarray([0.040220, 0.033353, 0.053953, 0.022562, -0.150088])
    heads = make_floatarray([327.371979, 327.172974, 327.164185, 326.991211, 328.083984])
    flows = make_floatarray([0.150088, 0.039916, 0.069952, 0.006563, 0.022562])
    msx.setHydraulics(demands, heads, flows)
    t = 0
    qual = []
    for _ in range(5):
        t, tleft = msx.step(t)
        species_index = msx.getindex(msx.SPECIES, "AS5s")
        qual.append(round(msx.getQualityByIndex(msx.LINK, 5, species_index), 5))
    assert qual == [0.00013, 0.00009, 0.00004, 0.54024, 3.69831]
    msx.close()

def test_quality_by_id():
    create_example()
    msx.init()
    demands = make_floatarray([0.040220, 0.033353, 0.053953, 0.022562, -0.150088])
    heads = make_floatarray([327.371979, 327.172974, 327.164185, 326.991211, 328.083984])
    flows = make_floatarray([0.150088, 0.039916, 0.069952, 0.006563, 0.022562])
    msx.setHydraulics(demands, heads, flows)
    t = 0
    qual = []
    for _ in range(5):
        t, tleft = msx.step(t)
        qual.append(round(msx.getQualityByID(msx.LINK, "5", "AS5s"), 5))
    assert qual == [0.00013, 0.00009, 0.00004, 0.54024, 3.69831]
    msx.close()


    





