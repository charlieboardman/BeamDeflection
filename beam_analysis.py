#I got moments of inertia from this tool: https://skyciv.com/free-moment-of-inertia-calculator/
#I got deflection calculations from this page: https://mechanicalc.com/reference/beam-deflection-tables
#I got the normal stress due to bending moment from here: https://www.bu.edu/moss/mechanics-of-materials-bending-normal-stress/#:~:text=The%20stress%20is%20a%20function,Science%20Foundation%20under%20Grant%20No.
#I got wood mechanical properties from here: https://www.fhwa.dot.gov/publications/research/safety/04097/sec130.cfm
#I got the L/360 deflection standard from here: https://www.tcnatile.com/faqs/30-deflection.html#:~:text=The%20L%2F360%20standard%20means,the%20center%20and%20the%20end.
#I got steel dimensions from here: https://www.engineeringtoolbox.com/american-standard-steel-channels-d_1321.html
#Here's a span table that might be useful: https://www.bmp-group.com/docs/default-source/literature/c-joist-span-tables-and-detailsb7dd4bcfd1de6413ac21ff00002d9a3e.pdf?sfvrsn=81032fe2_0

material_to_elastic_modulus = { #all values in psi
    "steel":29000000,
    "wood":1636460.8, #southern yellow pine, saturated, converted from MPa https://www.fhwa.dot.gov/publications/research/safety/04097/sec130.cfm
    }

material_to_rupture = { #all values in psi
    "steel":36000/2, #fatigue
    #"steel":36000,
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


#Point load functions
def max_deflection_point_load(beam,load,span): #Calculates the maximum deflection
    #span (ft), load (lbf)
    d = load*((span*12)**3)/(48*beam.modulus*beam.moment) #inch
    allowable = True if (span*12)/360 > d * FoS else False
    return (d,allowable)

def max_normal_stress_point_load(beam,load,span):
    max_moment = load*span*12/4
    max_sigma = beam.height/2*max_moment/beam.moment
    allowable = True if max_sigma * FoS < beam.yield_stress else False
    return(max_sigma,allowable)

#Uniform distributed load functions
def max_deflection_uniform_load(beam,w,span): #Load in lb/in
    #span (ft), w (load) (lbf/in)
    span_inch = span*12
    x = span_inch/2
    d = w*x*(span_inch**3 - 2*span_inch*(x**2) + x**3)/(24*beam.modulus*beam.moment)
    allowable = True if d * FoS < span_inch/360 else False
    return (d,allowable)

def max_normal_stress_uniform_load(beam,w,span):
    #span (ft), w (load) (lbf/in)
    span_inch = span*12
    max_moment = w*(span_inch**2)/8
    max_sigma = beam.height/2*max_moment/beam.moment
    allowable = True if max_sigma * FoS < beam.yield_stress else False
    return (max_sigma,allowable)

#Loading requirements are generally given in psf (pounds per square foot) so we need to translate that to a load in lbf/in
def psf_to_w(psf,spacing): #Spacing is the distance between joists in your design, in inches
    w = psf * spacing/12 #If spacing is 12 inches, each pound in psf is distributed over 12 inchs of joist
    return w

#Determine how close a beam is to yield stress under maximum psf
def percent_to_yield(beam,psf,span,spacing):
    return max_normal_stress_uniform_load(beam,psf_to_w(psf,spacing),span)[0]/beam.yield_stress

#beams
#Steel channels info: https://www.engineeringtoolbox.com/american-standard-steel-channels-d_1321.html
b2x4 = beam(5.359375,1.5*3.5,3.5,'wood')
b2x6 = beam(20.796875,1.5*5.5,5.5,'wood')
b2x8 = beam(47.634765625,1.5*7.25,7.25,'wood')
b2x10 = beam(98.9316400625,1.5*9.25,9.25,'wood')
b2x12 = beam(177.978515625,1.5*11.25,11.25,'wood')
c4x7_25 = beam(4.59,2.13,4,'steel')