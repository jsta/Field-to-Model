TEM Warming Experiment (and TEM Introduction)
=================================================================

What are we trying to model?
-------------------------------------------------------------

NGEE Arctic has worked on numerous experiments and field equipment over the last decade+, one of which being the zero-power warming 
chambers (see Lewin et at. (2017) https://bg.copernicus.org/articles/14/4071/2017/bg-14-4071-2017.pdf) 
The chambers passively warm the mean daily temperature inside the chamber by 2.6◦C above ambient temperatures during the summer months. 
Modeling such field experiments allows us to evaluate how well the model is able to capture the ecosystem responses to warming, 
and thus how adequate the model is for predicting future ecosystem changes.

At Utqiagvik, the chambers were deployed over a single season in multiple locations from 2017-2021 from mid-June through to mid-September (Ely et al. 2024). 
In this example, we model the 2019 summer warming experiment and compare the modeled and measured soil temperatures at 10cm depth 
for the warmed and control site. The 2019 experiment focused on *Eriophorum angustifolium*, a common sedge species in Arctic tundra which 
in the model DVM-DOS-TEM is represented by the sedge plant functional type (PFT) and grows for example in the wet sedge tundra 
community type (CMT). We model the warming experiment at a single pixel representing the wet sedge tundra CMT at Utqiagvik and compare the 
soil temperature at 10cm depth between the control and warmed runs to the observed soil temperatures at the site (Ely et al. 2024).


Lewin, K. F., McMahon, A. M., Ely, K. S., Serbin, S. P., & Rogers, A. (2017). A zero-power warming chamber for investigating plant responses to rising temperature. Biogeosciences, 14(18), 4071-4083.

Ely, Kim, Anderson, Jeremiah, Serbin, Shawn, & Rogers, Alistair (2024). Vegetation Warming Experiment: Thaw depth and dGPS locations, Utqiagvik, Alaska, 2019. https://doi.org/10.5440/1887568


.. note:: TODO

   Add some links to the text above into the relevant sections of the TEM 
   User Guide. For example linking to the description of Community Types, PFTs, 
   etc.



Setup
-----

.. warning:: 

   Waiting on Tobey to finalize input data prep. For now, just use the 
   demo data that is shipped with the TEM install...in the modex model container
   you can find it at :code:`/home/modex_user/install_dvmdostem/demo-data`.

.. note:: Prerequisites

   Assumes you have done the following container setup after downloading
   the container image from the cloud:

   .. code:: shell

      docker volume create inputdata
      docker volume create output
      docker run -it --rm \
         -p 9000:9000 \ 
         -v $(pwd)/model_examples:/home/modex_user/model_examples \ 
         -v inputdata:/home/modex_user/inputdata \
         -v output:/home/modex_user/output \
         model-container:latest

      # Alternate ways, mount might work better if you plan to edit files on the
      # host side and have them show up in the container right away....
      # -v $(pwd)/model_examples:/home/modex_user/model_examples \
      # --mount type=bind,src=$(pwd)/model_examples,dst=/home/modex_user/model_examples \


   Which should give you a shell prompt inside the container with two
   volumes mounted for input data and workshop runs.

   .. code:: shell

      modex_user@5cf5a55dff62:~$


Copy the input data that you'd like to use to the input data directory:

.. tip:: 
   
   Once we have inputs prepared for the workshop you can skip this step and
   just browse the input data folder to find data you want to use.

.. code:: shell

   cp -r install_dvmdostem/demo-data/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10 inputdata/

Next, to make the experiment and analysis easier, we will glue together the 
historic and projected (scenario) climate data into a single continuous dataset.
This will allow us to run the model in a single stage from 1901-2100 rather than
having to do a transient run followed by a scenario run. Use the helper script
in the :code:`model_examples/TEM` directory to do this:

.. code:: shell

   ./model_examples/TEM/glue_transient_scenario.py inputdata/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10
      
Now if you look in the new directory, you should see a new file called
:code:`transient-historic-climate.nc` which contains the glued together climate.

Now we are going to make copy of this dataset to create our "treatment" or
"warming" dataset. We will then modify this copy to increase the air temperatures
by 2.6 degrees Celsius during the summer months (June, July, August, September)
for the year 2019.

.. code:: shell

   cp -r inputdata/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10 \
     inputdata/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10_warming_2.6C_JJAS_2019

Now we will run the helper script to modify the air temperatures in the new
dataset:

.. code:: shell

   ./model_examples/TEM/modify_air_temperature.py \
   --input-file inputdata/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10_warming_2.6C_JJAS_2019/transient-scenario-climate.nc \
   --years 2019 \
   --months 6 7 8 9 \
   --years 2019 \
   --deviation 2.6

   
As you will see in the statements that are printed out from this scritp it will 
actually create an new file alongside the existing one. Here we throw out the original file and rename
the modified version to clean things up.

.. code:: shell

   mv inputdata/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10_warming_2.6C_JJAS_2019/modified_transient-scenario-climate.nc \
      inputdata/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10_warming_2.6C_JJAS_2019/transient-scenario-climate.nc

.. note:: 

   The modification script uses :code:`xarray` under the hood to manipulate
   the netCDF data. It creates a boolean mask for the time dimension based
   on the specified years and months, and then applies the temperature deviation
   only to those selected time points.

.. note:: TODO

   Do we want to clean up the historic and scenario files in each input now that
   we've got the glue together version? Probably not necessary but could help
   avoid confusion....

.. note:: 

   The modification script can take additional arguments to modify multiple
   years and different months as needed. See the help message for details:

Now we have two datasets:

  * the control dataset: :code:`inputdata/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10`
  * the warming treatment dataset: :code:`inputdata/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10_warming_2.6C_JJAS_2019`

.. note:: TODO

   would be nice to show some viz of this...need to use the other container??

Now that we have the datasets set up, we can create two run folders using the 
:code:`pyddt-swd` utility helper tool. For this we will work in the 
:code:`~/workshop_runs/tem_ee3_warming` directory.


.. code:: shell

   mkdir -p ~/output/tem/tem_ee3_warming
   cd ~/output/tem/tem_ee3_warming

   pyddt-swd \
      --input-data ~/inputdata/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10 \
      control

   pyddt-swd \
      --input-data ~/inputdata/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10_warming_2.6C_JJAS_2019 \
      treatment

You should now have two run folders set up for the control and treatment runs:

.. code:: shell

   $ pwd
   /home/modex_user/output/tem/tem_ee3_warming/control

   $ ls -l
   drwxr-xr-x 6 modex_user modex_user 4096 Oct 20 22:17 control
   drwxr-xr-x 6 modex_user modex_user 4096 Oct 20 22:17 warming_2.6C_JJAS_2019   

Now we can start a run in each folder.

.. warning:

   Make sure you do this each of these for both the control and the treatment runs!! Take care to note the 
   correct path for the the climate file, note the difference in the directory for control and treatment!!

Take care of the last setup steps. **DO THIS FOR EACH RUN**:

   #. :code:`cd` into the run folder

   #. fiddle with the run mask

      .. code::

         pyddt-runmask --reset --yx 0 0 run-mask.nc

   #. setup the output_spec

      .. code::

         pyddt-outspec config/output_spec.csv --on LAYERDZ m l
         pyddt-outspec config/output_spec.csv --on TLAYER m l

         # Print it out to see what vars we have at what resolution...
         pyddt-outspec config/output_spec.csv -s             
                  Name                Units       Yearly      Monthly        Daily          PFT Compartments       Layers    Data Type     Description
                  GPP            g/m2/time            y                   invalid                                invalid       double     GPP
               LAYERDZ                    m            y            m      invalid      invalid      invalid            l       double     Thickness of layer
               TLAYER             degree_C            y            m      invalid      invalid      invalid            l       double     Temperature by layer

   #. adjust the config file to the right climate file

      - this could be alleviated by doing some file shuffling above...i.e.
         renaming the stitched file to 'historic-climate.nc' in each input folder
         This would allow the config files to simply point to 'historic-climate.nc' without needing to change the paths for each run.

      .. code:: python
         :number-lines:

         # Adjust config file...
         import json

         with open('config/config.js') as f:
            jd = json.load(f)

         jd['IO']['hist_climate_file'] = "/home/modex_user/inputdata/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10/transient-scenario-climate.nc"

         with open('config/config.js', 'w') as f:
            json.dump(jd, f, indent=4)


   #. Annoyances out of the way, now we can start the run.

      .. code:: shell

         dvmdostem -f config/config.js -p 15 -e 10 -s 10 -t 150 -l monitor


.. note:: from 10/14 brainstorming session

   #. User starts by finding the inputs provided for workshop (distribution method TBD, but end result will be a folder mounted into the container at :code:`/home/modex_user/workshop_data` )
   #. User makes a copy of the input dataset they wish to use
   #. User modifies the copy to create a "treatment" dataset. TODO: consider naming recommendations
   #. User uses :code:`pyddt-swd` to create a "working directory" for each run (base, treatment)

      - Each run's config will point to the appropriate input dataset (base or treatment)

   #. User runs the model for each configuration
   #. User analyzes the outputs
   #. Repeat as needed (more treatments - by copying and adjusting the inputs,
      or more model runs with different settings by using :code:`pyddt-swd`
      again)
   

   
   

.. note:: draft ...edit rinse, repeat :-)

   We will be running the model at the Toolik Field Station (note from Hannah: Utquiagvik for this one ideally). We will use the demo
   demonstration data that is shipped with the TEM model for our "control" or
   "base" run. This data is based on the CRU TS 4.0 dataset.

   We will then create a second input dataset that is identical to the first except
   that the air temperatures have been increased by 2 degrees Celsius during the
   summer months (June, July, August) for the years 2000-2015. Update from Hannah: 2019 only, min-July to mid-Sept, 
   increase temperature by 2.6C.

   This will be our "treatment" or "warming" run.

   We will then compare the outputs of the two runs to see how the warming has
   affected the model's predictions of various ecosystem variables. Hannah: soil temperature at 10cm depth comparison to observations and between
   control and warming runs.


.. note:: draft of the actual instructions for participants

   do the setup

   make copy of input dataset

   create warming treatment dataset (increase air temp by 2.6C in June-Sept 2019) out of the copy

   create two runfolders, one for control pointing to original input data, one for warming pointing to modified input data

   run both experiments

   analyze the outputs (for that locate the observational data)

.. collapse:: Draft API ideas for creating altered input data
   :class: workshop-collapse
   :name: draft-api

   .. code:: python

      warming_experiment(deviation=2, sign='+', year=2015, month=May, 
                        original_data=/path/to/data 
                        altered_data=/path/to/users/experiment/director)  

      warming_experiment(deviation=2, sign='+', year=2015, month=May, 
                        original_data=/path/to/data 
                        altered_data=/path/to/users/experiment/director)

   Similar for precipitation

   .. code:: python

      precip_experiment(
         mm=2,
         sign='+',
         year=2020,
         month=January,
         original_data=/path/to/data
         altered_data=/path/to/users/experiment/director
      )

Technical Experiment Setup
----------------------------


.. note:: Draft outline steps from a brainstorming session. Please edit and improve.

   #. What spatial (geographic) area(s) do you want to run. Single or multi-pixel run?
   
      Single pixel at Utqiagvik

   #. Is this experiment designed around a single run or multiple runs? If multiple describe what is different between each run.

      Two different runs: the control run and a warming experiment (treatment)

   #. Decide what variables and resolutions you want to have output.
   
     soil temperature at 10cm depth, monthly resolution (compared to daily observations but that should be ok)

   #. Which stages to run? How many years for each stage?
   
      :code:`-p 100 -e 2000 -s 250 -t 115 -n 85`, Potentially with the option of combining transient and scenario? 
      Also consider using the restart capability to avoid running eq over and over? In this case we could even shorten 
      the scenario and just run until 2025 or something. Plot the outputs for 2018 - 2025? 

   #. From which stages do we need to save the output?
   
      Transient and scenario; combined, see above

   #. Which Community Type(s) to use?
   
      Wet sedge tundra (target PFT from the experiment was a sedge species)

   #. Is this run a calibration (parameter estimation) run? If so, elaborate.
   
      No

   #. List some ideas for how you expect to analyze the outputs
   
      Plot the control and warming soil temperature at 10cm depth time series for comparison to observations. 
      Designate control vs warming by color, observations vs model by line style?

   #. What computer will the runs be on?
      
      Laptop with Docker container pulled from cloud

   #. Decide where on your computer you want to store your model run(s).
      
      User will have a folder on their host, i.e. :code:`~/ngee-modex-2025/workflows` that is mounted inside the container

   #. Decide how to organize the outputs (important if the experiment dictates multiple runs)
      
      One folder for "control" one folder for each "treatment case" (I think we said creating a separate 
      input dataset for each treatment that is stored in the input datda folder, and then creating hte different experiments from the input data folders)

   #. Are the driving inputs and parameters for the specified run(s) available?
      
      The specific warming experiment driver will be created as part of the example, the field observation data should be 
      available somewhere - it's the citation in the header. 

   #. If the experiment is a multi-run experiment, can the different runs be scripted?
      
      Not sure yet...see example API above in the intro; only 2 runs so no need to fully automate...

   #. Is the run a single pixel (site) run or a multi pixel?
      
      single

   #. Decide on all other run settings/parameters:

      * Is the community type (CMT) fixed or driven by input vegetation.nc map? Fixed: wet sedge tundra
      * Any other command line options or special environment settings? I don't think so?

   #. Will the plotting happen in the run-time environment or will the data need to be copied to a different environment?
   
      

Analysis
----------------------------

.. note:: TODO, write this...

   What kinds of plots and analyses do we want to provide? What variables are we
   most interested in? How do we want to visualize the differences between the
   control and warming runs?

   Some ideas:
   
   * Time series plots of key variables (e.g. GPP, NEE, soil carbon) for control vs warming
   * Seasonal cycle plots
   * Difference maps if multi-pixel
   * Statistical summaries (means, variances, trends)
   * Comparison to observational data if available

   We can use Jupyter notebooks for interactive analysis and visualization.   