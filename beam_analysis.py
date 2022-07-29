material_to_elastic_modulus = { #all values in psi
    "steel":29000000,
    "wood":1636460.8, #southern yellow pine, saturated, converted from MPa https://www.fhwa.dot.gov/publications/research/safety/04097/sec130.cfm
    }

material_to_rupture = { #all values in psi
    "steel":36000,
    "wood":7106.85 #southern yellow pine, saturated, converted from MPa https://www.fhwa.dot.gov/publications/research/safety/04097/sec140.cfm
    }

FoS = 1.5 #factor of safety

class beam:
    def __init__(self,moment,area,height,material):
        self.moment = moment #inch^4
        self.area = area #inch^2
        self.height = height #inch
        self.material = material
        self.yield_stress = material_to_rupture[self.material]
        self.modulus = material_to_elastic_modulus[self.material]

def max_deflection(beam,load,span): #Calculates the maximum deflection
    #span (ft), load (lbf)
    d = load*((span*12)**3)/(48*beam.modulus*beam.moment) #inch
    allowable = True if (span*12)/360 > d * FoS else False
    return (d,allowable)

def max_normal_stress(beam,load,span):
    max_moment = load*span*12/4
    max_sigma = beam.height/2*max_moment/beam.moment
    allowable = True if max_sigma * FoS < beam.yield_stress else False
    return(max_sigma,allowable)

#beams
#Steel channels info: https://www.engineeringtoolbox.com/american-standard-steel-channels-d_1321.html
b2x4 = beam(5.359375,1.5*3.5,3.5,'wood')
b2x6 = beam(20.796875,1.5*5.5,5.5,'wood')
b2x8 = beam(47.634765625,1.5*7.25,7.25,'wood')
c4x7_25 = beam(4.59,2.13,4,'steel')