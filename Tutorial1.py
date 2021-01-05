from parcels import FieldSet, ParticleSet, JITParticle, AdvectionRK4

# 1. Setting up the velocity fields in a FieldSet object

fname = 'GlobCurrent_example_data/*.nc'
filenames = {'U': fname, 'V': fname}
variables = {'U': 'eastward_eulerian_current_velocity', 'V': 'northward_eulerian_current_velocity'}
dimensions = {'U': {'lat': 'lat', 'lon': 'lon', 'time': 'time'},
              'V': {'lat': 'lat', 'lon': 'lon', 'time': 'time'}}
fieldset = FieldSet.from_netcdf(filenames, variables, dimensions)


# 2. Defining the particles type and initial conditions in a ParticleSet object

pset = ParticleSet(fieldset=fieldset,   # the fields on which the particles are advected
                   pclass=JITParticle,  # the type of particles (JITParticle or ScipyParticle)
                   lon=28,              # release longitudes 
                   lat=-33)             # release latitudes


# 3. Executing an advection kernel on the given fieldset

output_file = pset.ParticleFile(name="GCParticles.nc", outputdt=3600) # the file name and the time step of the outputs
pset.execute(AdvectionRK4,                 # the kernel (which defines how particles move)
             runtime=86400*6,              # the total length of the run
             dt=300,                       # the timestep of the kernel
             output_file=output_file)


# 4. Exporting the simulation output to a netcdf file

output_file.export()