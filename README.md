# 2nd NGEE Arctic Field-to-Model Workshop

<img src=".assets/NGEE Arctic logo_large (002).png" align="left" width="300">

Welcome to the 2nd NGEE Arctic Field-to-Model Workshop in Santa Fe, NM! Following the project's 
tradition of bringing modelers to the field, our goal over this 2.5-day workshop is to bring empiricists
to the models. We will be providing an introduction to land surface modeling by providing overviews of
three different land surface models used across the project - the Energy Exascale Earth System (E3SM) Land Model (ELM),
the Advanced Terrestrial Simulator (ATS), and DVM-DOS-TEM (Dynamic Vegetation, Dynamic Organic Soil, Terrestrial
Ecosystem Model, often shortened to TEM) - that illustrate different design philosophies, approaches, and tradeoffs
in representing land surface processes. We will also introduce the ILAMB (International LAnd Model Benchmarking) and
DaPPER (Data PreParation for ELM Runs) python packages. ILAMB is designed to improve model-data integration and 
allow for validation of land surface models against observations, while DaPPER allows for the generation of 
necessary ELM input data from gridded datasets on Google Earth Engine. 

A major component of this workshop will be three breakout groups that will focus in greater detail on 
a specific set of Arctic processes in the models. The breakout groups will focus on 1) permafrost hydrology, 
2) snow/vegetation/permafrost interactions, and 3) hillslope hydrology impacts on biogeochemistry. We have tried
to structure the breakout groups to include experts from at least two of these models in each breakout group. Our
hope is this structure will help facilitate conversations not only between the empiricists and modelers, but also
to identify and discuss transferable insights across models.

Over the duration of the workshop, you will be running and analyzing example cases for all three models, learning more about how you
might be able to apply these models to your research and what their limitations might be, and hopefully finding 
opportunities for future collaboration and ideas for future publications. We hope that you are as excited for the 
workshop as we are! 

## Key Links:

> [!NOTE]
> It is highly recommended that you download the workshop containers and input data ahead of time.
> More information can be found [here](https://github.com/NGEE-Arctic/Field-to-Model/issues/38)

> [!WARNING]
> Windows users will have a longer setup procedure than macOS or Linux users. It is even more strongly
> recommended that attendees hoping to run the models on a Windows computer work through the setup instructions
> ahead of the workshop.

- [Workshop Setup Instructions](https://ngee-arctic.github.io/Field-to-Model/setup.html)
- [Workshop Agenda](https://ngee-arctic.github.io/Field-to-Model/modex_agenda_2025.html)
- More information about ELM
    - [E3SM's ELM Documentation](https://docs.e3sm.org/E3SM/ELM) (note: this is under development)
    - [CLM 4.5 Technical Note]
    - [Development repository](https://github.com/E3SM-Project/E3SM/tree/master/components/elm)
- More information about TEM
    - [DVM-DOS-TEM documentation](http://uaf-arctic-eco-modeling.github.io/dvm-dos-tem/)
    - [Development repository](https://github.com/uaf-arctic-eco-modeling/dvm-dos-tem)
- More information about ATS
    - [Amanzi-ATS documentation](https://amanzi.github.io)
    - [Development repository](https://github.com/amanzi/ats)
- More information about ILAMB
    - [ILAMB documentation](https://www.ilamb.org)
    - [Development repository](https://github.com/rubisco-sfa/ILAMB)
- Breakout groups:
    - [Permafrost Hydrology](https://ngee-arctic.github.io/Field-to-Model/breakout/permafrost_hydrology.html)
    - [Snow/Vegetation/Permafrost Interactions](https://ngee-arctic.github.io/Field-to-Model/breakout/snow_veg_permafrost.html)
    - [Hillslope Hydrology impacts on Biogeochemistry](https://ngee-arctic.github.io/Field-to-Model/breakout/hillslope_bgc.html)

## Additional resources
- [Introduction to version control using Git](https://swcarpentry.github.io/git-novice/)

### Known issues:
- ERA5 for Bayelva not working currently
