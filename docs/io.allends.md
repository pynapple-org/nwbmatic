## Allen Brain Atlas Neuropixel Loading Tutorial ##

Author: Selen Calgin
Date created: 13/07/2023
Last edited: 28/07/2023

The beauty of Pynapple's IO and the NWBmatic package is that loaders can be customized for any format of data. NWBmatic has many pre-made loaders, one of which being for the Allen Brain Atlas' Neuropixels dataset. The Neuropixels dataset contains electrophysiological data of the visual cortex and thalamus of mice who are shown passive visual stimuli. For more details about the dataset, please see documentation here: https://allensdk.readthedocs.io/en/latest/visual_coding_neuropixels.html

This tutorial will demonstrate how to use NWMmatic's loader for the Allen Neuropixels data in conjunction with Pynapple for various analyses with the data. NWBmatic loads the data into Pynapple core objects, which can then be used for further analysis.

Before you begin, make sure you have sufficient storage to download sessions from the database. The session sizes average about ~2gb.

Let's get started!

First, import libraries.


```python
# import libraries
import nwbmatic as ntm
import pynapple as nap
```


```python
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
```

To load a Neuropixels session, as with all data loading in NWBmatic, call NWBmatic's **load_session()** function.
- ***path***= where the Neuropixels data is downloaded/where it has been downloaded if you've already worked with a specific data session
- ***session_type***="allends" indicates that we are loading data from the Allen Institute (DS = dataset).

When you run the following cell, a GUI will appear. Using the GUI, choose from the two types of sessions in the Neuropixels database: 1) Brain observatory or 2) Functional connectivity. Then select the session ID you would like to load.

Note: *If this is your first time loading this session with NWBmatic, the loading will take a while as the data is first downloaded to your local system (to the path you indicated). If you have already loaded this session, loading the data will take about a minute.*

Additional note: *In this tutorial, I am accessing session #715093703 in Brain Observatory. If you would like to follow along, choose the same session ID. All analyses will work with other sessions too, but may have different values than the ones I comment on here.*


```python
# path to where data will be donwloaded
path = r"C:\Users\scalgi\OneDrive - McGill University\Peyrache Lab\Data\pynapple_test"

# load the data
data = ntm.load_session(path, session_type="allends") # type: nap.io.allennp.AllenNP
```

From our ***data*** object, we can access the following attributes:
   - **epochs**: a dictionary of **IntervalSet** that holds the start and end times of session epochs. In this dataset, **epochs** is trivial: there is only one epoch which is the session itself, under the key *session*.
   - **stimulus_epochs_types**: a dictionary of **IntervalSet**s that holds the start and end times of stimulus epochs, defined by the name of the stimulus type
   - **stimulus_epochs_blocks**: a dictionary of **IntervalSet**s that holds the start and end times of stimulus epoch, defined by the block of the stimulus. Each stimulus block contains one type of stimulus, and the block number indicates the order of when this block of stimulus was shown. Lack of stimulus (i.e. "spontaneous") is not given a block number.
   - **stimulus_intervals**: a dictionary of **IntervalSet**s that holds the start and end times of each presentation of of each stimulus type
   - **optogenetic_stimulus_epochs**: an **IntervalSet** that holds the start and end times of optogenetic stimulus epochs. None if session doesn't have it.
   - **spikes**: a **TsGroup**, which holds spike times for each unit and metadata on each unit
   - **metadata**: a dictionary of various Pandas Dataframes that holds various types of information:
      - **stimulus_presentations**: information about each stimulus presentation
      - **stimulus_conditions**: Each distinct stimulus state is called a "stimulus condition". Table holds additional information about each unique stimulus
      - **stimulus_parameters**: Dictionary of all stimulus parameters as keys and their range of values as values
      - **channels**: Information about all channels
      - **probes**: Information about all probes used
      - **units**: information about each unit identified in the session, including location in the brain
   - **time_support**: an **IntervalSet** containing the global time support based on **epochs**
   - **stimulus_time_support**: an **IntervalSet** containing the intervals of all stimulus blocks, providing a time support for stimuli


# Analyzing Neural Activity in the Primary Visual Cortex #
In this tutorial, we will be analyzing the neural activity of neurons in the primary visual cortex while also understanding how to use NWBmatic's loader for Allen Neuropixel data and how this data can be used in conjunction with Pynapple.

## Overview of Metadata ##
First, let's get a grasp of the metadata we have access to.


```python
# data metadata
print("Stimulus presentations:")
stimulus_presentations = data.metadata["stimulus_presentations"]
print(stimulus_presentations)

print("Stimulus conditions")
stimulus_conditions = data.metadata["stimulus_conditions"]
print(stimulus_conditions)

print("Stimulus parameters:")
stimulus_parameters = data.metadata["stimulus_parameters"]
print(stimulus_parameters)

print("Probes:")
probes = data.metadata["probes"]
print(probes)

print("Channels:")
channels = data.metadata["channels"]
print(channels)
```

    Stimulus presentations:
                             color contrast frame orientation  \
    stimulus_presentation_id                                    
    0                         null     null  null        null   
    1                         null      0.8  null        45.0   
    2                         null      0.8  null         0.0   
    3                         null      0.8  null        45.0   
    4                         null      0.8  null         0.0   
    ...                        ...      ...   ...         ...   
    70383                     null      0.8  null        60.0   
    70384                     null      0.8  null        90.0   
    70385                     null      0.8  null        60.0   
    70386                     null      0.8  null        60.0   
    70387                     null      0.8  null        60.0   
    
                                                       phase            size  \
    stimulus_presentation_id                                                   
    0                                                   null            null   
    1                         [3644.93333333, 3644.93333333]    [20.0, 20.0]   
    2                         [3644.93333333, 3644.93333333]    [20.0, 20.0]   
    3                         [3644.93333333, 3644.93333333]    [20.0, 20.0]   
    4                         [3644.93333333, 3644.93333333]    [20.0, 20.0]   
    ...                                                  ...             ...   
    70383                                               0.75  [250.0, 250.0]   
    70384                                                0.0  [250.0, 250.0]   
    70385                                                0.0  [250.0, 250.0]   
    70386                                                0.5  [250.0, 250.0]   
    70387                                                0.0  [250.0, 250.0]   
    
                             spatial_frequency   start_time stimulus_block  \
    stimulus_presentation_id                                                 
    0                                     null    13.470683           null   
    1                                     0.08    73.537433            0.0   
    2                                     0.08    73.770952            0.0   
    3                                     0.08    74.021150            0.0   
    4                                     0.08    74.271349            0.0   
    ...                                    ...          ...            ...   
    70383                                 0.04  9133.889309           14.0   
    70384                                 0.02  9134.139517           14.0   
    70385                                 0.08  9134.389719           14.0   
    70386                                 0.32  9134.639920           14.0   
    70387                                 0.16  9134.890122           14.0   
    
                                stimulus_name    stop_time temporal_frequency  \
    stimulus_presentation_id                                                    
    0                             spontaneous    73.537433               null   
    1                                  gabors    73.770952                4.0   
    2                                  gabors    74.021150                4.0   
    3                                  gabors    74.271349                4.0   
    4                                  gabors    74.521547                4.0   
    ...                                   ...          ...                ...   
    70383                     static_gratings  9134.139517               null   
    70384                     static_gratings  9134.389719               null   
    70385                     static_gratings  9134.639920               null   
    70386                     static_gratings  9134.890122               null   
    70387                     static_gratings  9135.140323               null   
    
                             x_position y_position   duration  \
    stimulus_presentation_id                                    
    0                              null       null  60.066750   
    1                               0.0       30.0   0.233519   
    2                             -30.0      -10.0   0.250199   
    3                              10.0       20.0   0.250199   
    4                             -40.0      -40.0   0.250199   
    ...                             ...        ...        ...   
    70383                          null       null   0.250209   
    70384                          null       null   0.250201   
    70385                          null       null   0.250201   
    70386                          null       null   0.250201   
    70387                          null       null   0.250201   
    
                              stimulus_condition_id  
    stimulus_presentation_id                         
    0                                             0  
    1                                             1  
    2                                             2  
    3                                             3  
    4                                             4  
    ...                                         ...  
    70383                                      4886  
    70384                                      4806  
    70385                                      4874  
    70386                                      4789  
    70387                                      4809  
    
    [70388 rows x 16 columns]
    Stimulus conditions
                          color contrast  frame    mask opacity orientation  \
    stimulus_condition_id                                                     
    0                      null     null   null    null    null        null   
    1                      null      0.8   null  circle    True        45.0   
    2                      null      0.8   null  circle    True         0.0   
    3                      null      0.8   null  circle    True        45.0   
    4                      null      0.8   null  circle    True         0.0   
    ...                     ...      ...    ...     ...     ...         ...   
    5022                   null     null   35.0    null    null        null   
    5023                   null     null  104.0    null    null        null   
    5024                   null     null  112.0    null    null        null   
    5025                   null     null   48.0    null    null        null   
    5026                   null     null    4.0    null    null        null   
    
                                                    phase          size  \
    stimulus_condition_id                                                 
    0                                                null          null   
    1                      [3644.93333333, 3644.93333333]  [20.0, 20.0]   
    2                      [3644.93333333, 3644.93333333]  [20.0, 20.0]   
    3                      [3644.93333333, 3644.93333333]  [20.0, 20.0]   
    4                      [3644.93333333, 3644.93333333]  [20.0, 20.0]   
    ...                                               ...           ...   
    5022                                             null          null   
    5023                                             null          null   
    5024                                             null          null   
    5025                                             null          null   
    5026                                             null          null   
    
                          spatial_frequency   stimulus_name temporal_frequency  \
    stimulus_condition_id                                                        
    0                                  null     spontaneous               null   
    1                                  0.08          gabors                4.0   
    2                                  0.08          gabors                4.0   
    3                                  0.08          gabors                4.0   
    4                                  0.08          gabors                4.0   
    ...                                 ...             ...                ...   
    5022                               null  natural_scenes               null   
    5023                               null  natural_scenes               null   
    5024                               null  natural_scenes               null   
    5025                               null  natural_scenes               null   
    5026                               null  natural_scenes               null   
    
                          units x_position y_position    color_triplet  
    stimulus_condition_id                                               
    0                      null       null       null             null  
    1                       deg        0.0       30.0  [1.0, 1.0, 1.0]  
    2                       deg      -30.0      -10.0  [1.0, 1.0, 1.0]  
    3                       deg       10.0       20.0  [1.0, 1.0, 1.0]  
    4                       deg      -40.0      -40.0  [1.0, 1.0, 1.0]  
    ...                     ...        ...        ...              ...  
    5022                   null       null       null             null  
    5023                   null       null       null             null  
    5024                   null       null       null             null  
    5025                   null       null       null             null  
    5026                   null       null       null             null  
    
    [5027 rows x 15 columns]
    Stimulus parameters:
    {'color': array([-1.0, 1.0], dtype=object), 'contrast': array([0.8, 1.0], dtype=object), 'frame': array([0.0, 1.0, 2.0, ..., 3598.0, 3599.0, -1.0], dtype=object), 'orientation': array([45.0, 0.0, 90.0, 315.0, 225.0, 135.0, 270.0, 180.0, 120.0, 150.0,
           60.0, 30.0], dtype=object), 'phase': array(['[3644.93333333, 3644.93333333]', '[0.0, 0.0]',
           '[21211.93333333, 21211.93333333]', '0.5', '0.75', '0.0', '0.25'],
          dtype=object), 'size': array(['[20.0, 20.0]', '[300.0, 300.0]', '[250.0, 250.0]',
           '[1920.0, 1080.0]'], dtype=object), 'spatial_frequency': array(['0.08', '[0.0, 0.0]', '0.04', 0.32, 0.08, 0.04, 0.02, 0.16],
          dtype=object), 'temporal_frequency': array([4.0, 8.0, 2.0, 1.0, 15.0], dtype=object), 'x_position': array([0.0, -30.0, 10.0, -40.0, -10.0, 40.0, 30.0, 20.0, -20.0],
          dtype=object), 'y_position': array([30.0, -10.0, 20.0, -40.0, -20.0, 0.0, -30.0, 40.0, 10.0],
          dtype=object)}
    Probes:
              description                 location  sampling_rate  \
    id                                                              
    810755797      probeA  See electrode locations   29999.954846   
    810755799      probeB  See electrode locations   29999.906318   
    810755801      probeC  See electrode locations   29999.985470   
    810755803      probeD  See electrode locations   29999.908100   
    810755805      probeE  See electrode locations   29999.985679   
    810755807      probeF  See electrode locations   30000.028033   
    
               lfp_sampling_rate  has_lfp_data  
    id                                          
    810755797        1249.998119          True  
    810755799        1249.996097          True  
    810755801        1249.999395          True  
    810755803        1249.996171          True  
    810755805        1249.999403          True  
    810755807        1250.001168          True  
    Channels:
                                                       filtering  \
    id                                                             
    850261194  AP band: 500 Hz high-pass; LFP band: 1000 Hz l...   
    850261196  AP band: 500 Hz high-pass; LFP band: 1000 Hz l...   
    850261202  AP band: 500 Hz high-pass; LFP band: 1000 Hz l...   
    850261206  AP band: 500 Hz high-pass; LFP band: 1000 Hz l...   
    850261212  AP band: 500 Hz high-pass; LFP band: 1000 Hz l...   
    ...                                                      ...   
    850264894  AP band: 500 Hz high-pass; LFP band: 1000 Hz l...   
    850264898  AP band: 500 Hz high-pass; LFP band: 1000 Hz l...   
    850264902  AP band: 500 Hz high-pass; LFP band: 1000 Hz l...   
    850264908  AP band: 500 Hz high-pass; LFP band: 1000 Hz l...   
    850264912  AP band: 500 Hz high-pass; LFP band: 1000 Hz l...   
    
               probe_channel_number  probe_horizontal_position   probe_id  \
    id                                                                      
    850261194                     0                         43  810755801   
    850261196                     1                         11  810755801   
    850261202                     4                         43  810755801   
    850261206                     6                         59  810755801   
    850261212                     9                         11  810755801   
    ...                         ...                        ...        ...   
    850264894                   374                         59  810755797   
    850264898                   376                         43  810755797   
    850264902                   378                         59  810755797   
    850264908                   381                         11  810755797   
    850264912                   383                         27  810755797   
    
               probe_vertical_position structure_acronym  ecephys_structure_id  \
    id                                                                           
    850261194                       20                PO                1020.0   
    850261196                       20                PO                1020.0   
    850261202                       60                PO                1020.0   
    850261206                       80                PO                1020.0   
    850261212                      100                PO                1020.0   
    ...                            ...               ...                   ...   
    850264894                     3760              None                   NaN   
    850264898                     3780              None                   NaN   
    850264902                     3800              None                   NaN   
    850264908                     3820              None                   NaN   
    850264912                     3840              None                   NaN   
    
              ecephys_structure_acronym  anterior_posterior_ccf_coordinate  \
    id                                                                       
    850261194                        PO                             7648.0   
    850261196                        PO                             7651.0   
    850261202                        PO                             7660.0   
    850261206                        PO                             7665.0   
    850261212                        PO                             7674.0   
    ...                             ...                                ...   
    850264894                       NaN                             7112.0   
    850264898                       NaN                             7107.0   
    850264902                       NaN                             7102.0   
    850264908                       NaN                             7094.0   
    850264912                       NaN                             7089.0   
    
               dorsal_ventral_ccf_coordinate  left_right_ccf_coordinate  
    id                                                                   
    850261194                         3645.0                     7567.0  
    850261196                         3636.0                     7566.0  
    850261202                         3610.0                     7564.0  
    850261206                         3592.0                     7562.0  
    850261212                         3566.0                     7560.0  
    ...                                  ...                        ...  
    850264894                          -53.0                     7809.0  
    850264898                          -69.0                     7813.0  
    850264902                          -85.0                     7818.0  
    850264908                         -109.0                     7825.0  
    850264912                         -126.0                     7829.0  
    
    [2219 rows x 11 columns]
    

## Accessing Units of Interest (V1) ##

Recall that we want to look at neuronal activity in V1.

All unit information is stored within **data.spikes**, which is a Pynapple object called TsGroup. data.spikes holds spike times for each unit alongside metadata information about each unit, including in which brain structure they are recorded from.

Let's see the units we have in our session:


```python
spikes = data.spikes
print(spikes.index)
```

    [950910352 950910364 950910371 950910392 950910435 950910463 950910531
     950910549 950910558 950910576 950910603 950910651 950910664 950910671
     950910727 950910742 950910757 950910778 950910834 950910861 950910889
     950910897 950910904 950910941 950911006 950911040 950911088 950911195
     950911223 950911266 950911286 950911467 950911563 950911586 950911593
     950911601 950911656 950911677 950911684 950911691 950911698 950911704
     950911732 950911873 950911880 950911932 950911986 950912018 950912065
     950912109 950912164 950912190 950912214 950912226 950912249 950912283
     950912293 950912326 950912361 950912384 950912396 950912406 950912417
     950912427 950912448 950912460 950912473 950912511 950912601 950912646
     950912803 950912814 950912928 950912940 950912952 950913000 950913031
     950913096 950913409 950913422 950913456 950913470 950913506 950913517
     950913527 950913537 950913547 950913567 950913588 950913652 950913676
     950913684 950913766 950913796 950913806 950913850 950913877 950913893
     950913901 950913908 950913921 950913929 950913938 950913954 950913976
     950913983 950913990 950914026 950914067 950914103 950914130 950914157
     950914189 950914197 950914219 950914233 950914294 950914310 950914318
     950914348 950914359 950914413 950914424 950914435 950914538 950914625
     950914635 950914660 950914683 950914720 950914754 950914766 950914780
     950914791 950914812 950914832 950914856 950914868 950914882 950914923
     950914940 950914954 950914980 950915023 950915054 950915068 950915101
     950915304 950915378 950915441 950915483 950915921 950915947 950915984
     950915997 950916009 950916273 950916377 950916395 950916413 950916447
     950916519 950916603 950916733 950916754 950916921 950916980 950917063
     950917295 950917313 950917332 950917411 950917604 950917669 950917769
     950917785 950917849 950917899 950918052 950918175 950918191 950918246
     950918261 950918280 950918294 950918310 950918344 950918362 950918381
     950918422 950918491 950918570 950918695 950918745 950918802 950918821
     950918846 950918902 950918919 950918936 950918955 950919022 950919040
     950919054 950919086 950919104 950919120 950919154 950919212 950919249
     950919283 950919387 950919456 950919496 950919676 950919748 950919806
     950919863 950919900 950919921 950919945 950919993 950920017 950920092
     950920151 950920290 950920309 950920434 950920756 950920777 950920827
     950920843 950920912 950920929 950920961 950920998 950921013 950921034
     950921088 950921163 950921176 950921299 950921442 950921601 950921709
     950922041 950922122 950922146 950922174 950922208 950922234 950922258
     950922286 950922329 950922351 950922368 950922383 950922466 950922494
     950922551 950922576 950922600 950922641 950922659 950922684 950922706
     950922725 950922745 950922781 950922841 950922883 950922896 950922929
     950922961 950922994 950923011 950923049 950923089 950923121 950923165
     950923181 950923217 950923236 950923254 950923348 950923365 950923405
     950923464 950923485 950923606 950923669 950923690 950923730 950923754
     950923859 950923880 950923897 950923914 950923939 950923958 950923976
     950924072 950924089 950924107 950924147 950924173 950924212 950924231
     950924272 950924372 950924413 950924434 950924452 950924500 950924519
     950924598 950924635 950924693 950924735 950924753 950924800 950924845
     950924883 950924899 950925057 950925092 950925112 950925132 950925149
     950925166 950925187 950925212 950925267 950925332 950925368 950925383
     950925400 950925438 950925455 950925508 950925555 950925626 950925644
     950925664 950925707 950925730 950925749 950925786 950925850 950925902
     950925925 950925950 950925967 950925983 950926001 950926055 950926095
     950926208 950926709 950926787 950926805 950926867 950926886 950926928
     950927002 950927024 950927046 950927066 950927229 950927323 950927341
     950927745 950927775 950928113 950928160 950928179 950928198 950928255
     950928387 950928423 950928440 950928461 950928497 950928518 950928536
     950928588 950928686 950928759 950928795 950928855 950928873 950928891
     950928911 950928976 950928991 950929009 950929067 950929083 950929101
     950929134 950929153 950929171 950929188 950929206 950929227 950929245
     950929286 950929377 950929400 950929420 950929495 950929514 950929531
     950929570 950929592 950929663 950929697 950929750 950929787 950929804
     950929824 950929882 950930105 950930145 950930215 950930237 950930276
     950930340 950930358 950930375 950930392 950930407 950930423 950930437
     950930454 950930522 950930795 950930866 950930888 950930964 950930985
     950931004 950931043 950931118 950931164 950931181 950931236 950931254
     950931272 950931315 950931363 950931423 950931458 950931517 950931533
     950931565 950931581 950931617 950931656 950931727 950931751 950931770
     950931805 950931853 950931878 950931899 950931959 950932032 950932087
     950932102 950932445 950932563 950932578 950932696 950932820 950932888
     950932943 950932963 950932980 950933012 950933040 950933057 950933173
     950933208 950933226 950933426 950933536 950933555 950933606 950933660
     950933698 950933732 950933840 950933890 950933907 950933924 950933960
     950934028 950934044 950934181 950934229 950934268 950934286 950934304
     950934728 950934765 950934843 950934971 950934992 950935070 950935165
     950935201 950935269 950935285 950935317 950935402 950935460 950935478
     950935499 950935575 950935610 950935658 950935720 950935755 950935907
     950935925 950935942 950935975 950936008 950936025 950936093 950936113
     950936162 950936177 950936194 950936224 950936272 950936292 950936326
     950936345 950936412 950936465 950936482 950936572 950936639 950936656
     950936675 950936710 950936727 950936759 950936855 950936870 950936908
     950936941 950936979 950936992 950937050 950937068 950937114 950937333
     950937929 950937990 950938074 950938091 950938171 950938279 950938344
     950938459 950938511 950938598 950938629 950938657 950938700 950938797
     950938924 950938960 950938978 950939028 950939079 950939114 950939168
     950939257 950939347 950939479 950939509 950939523 950939641 950939678
     950939945 950940001 950940023 950940040 950940104 950940121 950940157
     950940171 950940185 950940200 950940219 950940237 950940311 950940389
     950940437 950940453 950940467 950940507 950940526 950940545 950940615
     950940631 950940649 950940671 950940688 950940718 950940859 950940928
     950941494 950941529 950941583 950941776 950941795 950942129 950942155
     950942199 950942235 950942252 950942304 950942974 950943198 950943517
     950943580 950943625 950943695 950943735 950943756 950943795 950943813
     950943830 950943877 950944146 950944160 950944212 950944228 950944247
     950944259 950944276 950944444 950944566 950944600 950944675 950944706
     950944769 950944784 950944815 950944827 950944858 950944872 950944952
     950944968 950944989 950945008 950945042 950945060 950945077 950945127
     950945180 950945232 950945252 950945295 950945314 950945467 950945518
     950945554 950945572 950945588 950945625 950945660 950945768 950945783
     950945817 950945986 950946003 950946022 950946068 950946155 950946176
     950946192 950946228 950946310 950946327 950946343 950946376 950946437
     950946497 950946641 950946658 950946673 950946741 950947140 950947156
     950947211 950947224 950947271 950947368 950947412 950947488 950947533
     950947555 950947626 950947647 950947665 950947763 950947778 950947798
     950947832 950947849 950947868 950947941 950947963 950947990 950948009
     950948026 950948063 950948092 950948139 950948174 950948210 950948246
     950948281 950948306 950948371 950948396 950948414 950948488 950948527
     950948547 950948564 950948631 950948648 950948683 950948716 950948744
     950948778 950948793 950948826 950948853 950948867 950948881 950948970
     950949089 950949118 950949200 950949248 950949428 950949449 950949628
     950949861 950949933 950949961 950949994 950950009 950950031 950950101
     950950116 950950160 950950176 950950224 950950270 950950308 950950382
     950950433 950950576 950950740 950950756 950950810 950950880 950950919
     950951153 950951364 950951511 950951525 950951577 950951613 950951636
     950951678 950951702 950951791 950951829 950951840 950951851 950951879
     950951891 950951902 950951940 950951950 950951979 950952002 950952213
     950952241 950952256 950952312 950952336 950952386 950952629 950952690
     950952704 950952719 950952734 950952748 950952845 950952881 950952969
     950952985 950953119 950953159 950953187 950953293 950953417 950953703
     950954163 950954180 950954195 950954630 950954647 950954737 950954793
     950954823 950954838 950954886 950954905 950954922 950954941 950954983
     950955053 950955181 950955212 950955361 950955399 950955414 950955543
     950955784 950955833 950955844 950955897 950955951 950955965 950955974
     950956019 950956030 950956043 950956100 950956148 950956205 950956259
     950956297 950956336 950956386 950956399 950956413 950956435 950956493
     950956504 950956514 950956527 950956541 950956563 950956592 950956604
     950956616 950956630 950956667 950956680 950956778 950956835 950956845
     950956870 950956911 950956952 950957053 950957270 950957282 950957295
     950957320 950957408]
    

To see what metadata is stored within **spikes**:


```python
print(spikes.metadata_columns)
```

    ['rate', 'waveform_PT_ratio', 'waveform_amplitude', 'amplitude_cutoff', 'cluster_id', 'cumulative_drift', 'd_prime', 'firing_rate', 'isi_violations', 'isolation_distance', 'L_ratio', 'local_index', 'max_drift', 'nn_hit_rate', 'nn_miss_rate', 'peak_channel_id', 'presence_ratio', 'waveform_recovery_slope', 'waveform_repolarization_slope', 'silhouette_score', 'snr', 'waveform_spread', 'waveform_velocity_above', 'waveform_velocity_below', 'waveform_duration', 'filtering', 'probe_channel_number', 'probe_horizontal_position', 'probe_id', 'probe_vertical_position', 'structure_acronym', 'ecephys_structure_id', 'ecephys_structure_acronym', 'anterior_posterior_ccf_coordinate', 'dorsal_ventral_ccf_coordinate', 'left_right_ccf_coordinate', 'probe_description', 'location', 'probe_sampling_rate', 'probe_lfp_sampling_rate', 'probe_has_lfp_data']
    

Now, we want to get the units that are in the primary visual cortex (V1), as these are neurons that are most likely to have orientation tuning and tuning to locations in space. The metadata column that corresponds to location in the brain is "ecephys_structure_acronym".

We can use **TsGroup**'s functionality to organize the units based on columns in the unit's metadata. This function is called **getby_category()**. Let's see how we can use it for our purposes:


```python
# organize units by structure
units_structures = spikes.getby_category("ecephys_structure_acronym")
```

*units_structures* is a dictionary of **TsGroups**, with the structure names as keys.

Let's look at the names of the structures we are working on by getting the keys of the dictionary.


```python
# take a look at the structure names
units_structures.keys()
```




    dict_keys(['APN', 'CA1', 'CA3', 'DG', 'LGd', 'LP', 'PO', 'PoT', 'VISam', 'VISl', 'VISp', 'VISpm', 'VISrl', 'grey'])



To get an overview of how the units are distributed by brain structure, let's quickly count the number of units per brain area and plot it:


```python
# getting a list of brain areas
brain_areas = units_structures.keys()
# counting the length of the TsGroup (i.e. number of units) associated with each brain structure
unit_count_by_brain_region = [len(units_structures[key]) for key in brain_areas]

# plot
plt.bar(brain_areas,unit_count_by_brain_region)
```




    <BarContainer object of 14 artists>




    
![png](nwbmatic-pynapple-allen-tutorial_files/nwbmatic-pynapple-allen-tutorial_17_1.png)
    


Nice! Looks like we have a decent number of units in the primary visual cortex ("VISp"). Let's retrieve these units from the dictionary *units_structures*.


```python
# get the TsGroup of units in V1
v1_units = units_structures["VISp"]

# how many units did we get?
print("Number of units in V1: %s" % len(v1_units))
```

    Number of units in V1: 60
    

Now, from the units in V1, we also want to get the units that have a high signal-to-noise (SNR) ratio. If you look above, you can see that this information is also stored in the metadata under "snr".

We can use the **TsGroup**'s *getby_threshold()* function to do this. Rather than a dictionary of TsGroups, this function just returns a new TsGroup with units that obey the given threshold.

Let's get units with an SNR > 4:


```python
v1_high_snr_units = v1_units.getby_threshold("snr", 4) # default operator is >, but other ones can be passed via an optional argument

# how many units did we get?
print("Number of units in V1: %s" % len(v1_high_snr_units))

# what are the IDs of the units?
v1_unit_IDs = v1_high_snr_units.keys()
print("V1 Unit IDs: %s" % v1_unit_IDs)
```

    Number of units in V1: 6
    V1 Unit IDs: [950930985, 950931458, 950931533, 950931727, 950931751, 950932696]
    

Awesome! We can quickly visualize the units' activity over time with **TsGroup**'s *count()* function, which counts the number of spikes of each unit within intervals of time.

The default intervals of the *count()* function are based on the global time support of the data. In this database, the global session epoch is the start and end time of the entire session. Let's first use the default interval and specify the bin size in seconds. Here, I'm setting the bin size to 1s.


```python
spike_counts = v1_high_snr_units.count(bin_size=1)
spike_counts
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>950930985</th>
      <th>950931458</th>
      <th>950931533</th>
      <th>950931727</th>
      <th>950931751</th>
      <th>950932696</th>
    </tr>
    <tr>
      <th>Time (s)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0.5</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1.5</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2.5</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3.5</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4.5</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>9636.5</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9637.5</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9638.5</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9639.5</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9640.5</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>9641 rows × 6 columns</p>
</div>



Nice! With this table, we have everything we need to plot spike counts per time interval.
Let's go ahead and plot it for each of our units. This will take a few minutes since the bin number is so high.


```python
# Create 1x6 grid of subplots
fig, axs = plt.subplots(1,6,figsize=(15,4))
time_intervals = spike_counts.index

# Iterate over each neuron and plot the spike count data
for i, (unit_id, ax) in enumerate(zip(v1_unit_IDs, axs)):
    ax.bar(time_intervals, spike_counts[unit_id])
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Spike Count')
    ax.set_title(unit_id)

plt.tight_layout()
plt.show()
```


    
![png](nwbmatic-pynapple-allen-tutorial_files/nwbmatic-pynapple-allen-tutorial_25_0.png)
    


## Understanding the Stimuli ##
Now that we've retrieved our units in V1, let's take a look at the kind of stimuli we are working with and how stimulus epochs are organized.

First, let's look at stimulus epochs by type and by block.


```python
stimulus_epochs_types = data.stimulus_epochs_types
stimulus_epochs_blocks = data.stimulus_epochs_blocks
print("Stimulus names: %s" % stimulus_epochs_types.keys())
print("Stimulus blocks: %s" % stimulus_epochs_blocks.keys())
```

    Stimulus names: dict_keys(['drifting_gratings', 'flashes', 'gabors', 'natural_movie_one', 'natural_movie_three', 'natural_scenes', 'spontaneous', 'static_gratings'])
    Stimulus blocks: dict_keys([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 'null'])
    

Each block interval provides the beginning and end of the given block of stimulus presentations, stored is *stimulus_epochs_blocks*
Each stimulus blocks contains only one type of stimulus, however, there are multiple blocks of one kind of stimulus. Each **IntervalSet** in *stimulus_epochs_types* represents one block of stimulus.
Individual stimulus interval of a given stimulus type is stored in *stimulus_intervals*.

To see a visualization of how the stimuli are organized, see here: chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://brainmapportal-live-4cc80a57cd6e400d854-f7fdcae.divio-media.net/filer_public/0f/5d/0f5d22c9-f8f6-428c-9f7a-2983631e72b4/neuropixels_cheat_sheet_nov_2019.pdf

For example, from Allen Neuropixels' documentation, we know that drifting gratings are shown in multiple blocks, specifically block 2, 5, and 7. Within these blocks, there are individual stimulus presentations of various conditions.

Let's take a look:


```python
# Drifting gratings epochs:
drifting_gratings = stimulus_epochs_types["drifting_gratings"]
print("Drifting gratings epochs: \n%s \n" %drifting_gratings)

# Block 2, 5 and 7 epochs
print("Block 2 intervals \n%s: " % stimulus_epochs_blocks[2])
print("Block 5 intervals \n%s: " % stimulus_epochs_blocks[5])
print("Block 7 intervals \n%s: " % stimulus_epochs_blocks[7])
```

    Drifting gratings epochs: 
             start          end
    0  1574.774823  2174.275707
    1  3166.137683  3765.638457
    2  4697.416823  5380.987797 
    
    Block 2 intervals 
             start          end
    0  1574.774823  2174.275707: 
    Block 5 intervals 
             start          end
    0  3166.137683  3765.638457: 
    Block 7 intervals 
             start          end
    0  4697.416823  5380.987797: 
    

Notice how the epochs defined by stimulus type and block line up? *type* and *block* are two ways of organizing the stimulus epochs, which one you use depends on your analysis goals.

Now, let's take a look at the stimulus presentation intervals of all drifting gratings:



```python
# get dictionary of stimulus intervals organized by stimulus type
stimulus_intervals = data.stimulus_intervals
# get stimulus intervals for drifting gratings
drifting_gratings_intervals = stimulus_intervals['drifting_gratings']
drifting_gratings_intervals
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>start</th>
      <th>end</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1574.774823</td>
      <td>1576.776513</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1577.777347</td>
      <td>1579.779027</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1580.779833</td>
      <td>1582.781563</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1583.782367</td>
      <td>1585.784047</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1586.784883</td>
      <td>1588.786553</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5366.976107</td>
      <td>5368.977777</td>
    </tr>
    <tr>
      <th>6</th>
      <td>5369.978603</td>
      <td>5371.980283</td>
    </tr>
    <tr>
      <th>7</th>
      <td>5372.981107</td>
      <td>5374.982807</td>
    </tr>
    <tr>
      <th>8</th>
      <td>5375.983663</td>
      <td>5377.985343</td>
    </tr>
    <tr>
      <th>9</th>
      <td>5378.986127</td>
      <td>5380.987797</td>
    </tr>
  </tbody>
</table>
<p>628 rows × 2 columns</p>
</div>



Notice that the first start time and the last end time matches that of the start and end time of the drifting gratings stimulus epochs.

To get the stimulus interval for only one of the blocks, you can use **IntervalSet**'s *intersect* function, which finds the common times between two **IntervalSet**s. Let's find the stimulus intervals of drifting gratings in block 2 as an example:


```python
block2_stimulus_epochs = stimulus_epochs_blocks[2] # get block 2 of stimulus epochs

# intersect block 2 intervals with drifting gratings intervals to get drifting gratings in block 2 only
drifting_gratings_block_2_intervals = drifting_gratings_intervals.intersect(block2_stimulus_epochs)

# what does this look like?
drifting_gratings_block_2_intervals
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>start</th>
      <th>end</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1574.774823</td>
      <td>1576.776513</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1577.777347</td>
      <td>1579.779027</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1580.779833</td>
      <td>1582.781563</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1583.782367</td>
      <td>1585.784047</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1586.784883</td>
      <td>1588.786553</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2160.263967</td>
      <td>2162.265657</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2163.266503</td>
      <td>2165.268183</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2166.269007</td>
      <td>2168.270667</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2169.271543</td>
      <td>2171.273213</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2172.274017</td>
      <td>2174.275707</td>
    </tr>
  </tbody>
</table>
<p>200 rows × 2 columns</p>
</div>



To look at the overall set of available parameters of the stimuli, we can access it through the metadata as follows:


```python
for key, values in stimulus_parameters.items():
    print(f'{key}:{values}')
```

    color:[-1.0 1.0]
    contrast:[0.8 1.0]
    frame:[0.0 1.0 2.0 ... 3598.0 3599.0 -1.0]
    orientation:[45.0 0.0 90.0 315.0 225.0 135.0 270.0 180.0 120.0 150.0 60.0 30.0]
    phase:['[3644.93333333, 3644.93333333]' '[0.0, 0.0]'
     '[21211.93333333, 21211.93333333]' '0.5' '0.75' '0.0' '0.25']
    size:['[20.0, 20.0]' '[300.0, 300.0]' '[250.0, 250.0]' '[1920.0, 1080.0]']
    spatial_frequency:['0.08' '[0.0, 0.0]' '0.04' 0.32 0.08 0.04 0.02 0.16]
    temporal_frequency:[4.0 8.0 2.0 1.0 15.0]
    x_position:[0.0 -30.0 10.0 -40.0 -10.0 40.0 30.0 20.0 -20.0]
    y_position:[30.0 -10.0 20.0 -40.0 -20.0 0.0 -30.0 40.0 10.0]
    

Great, now that we have a good understanding of the stimuli in this session, we can start examining the activity of the V1 units of interest in relation to the  stimuli.

## Analyzing the Neural Response in V1 to Visual Stimuli ##
Now that we've acquired units from V1 and have explored our data and stimuli, we now do some analysis. Specifically, we're going to look at the response of V1 neurons to visual stimuli.

## 1D Orientation Tuning Curves ##

*This section of the tutorial is adopted from Seigle et al (2021) Dataset Tutorial by Dhruv Mehrotra*: https://github.com/PeyracheLab/pynacollada/blob/main/pynacollada/Pynapple%20Paper%20Figures/Siegle%202021/Siegle_dataset.ipynb

V1 neurons are known to have orientation specific tuning. In this dataset, we have static grating stimuli which varies in orientation. We are going to compute the tuning curve of V1 neurons to the orientations.

To do this, first we need to get information about the static grating stimulus presentations, as follows:


```python
drifting_gratings_presentations = stimulus_presentations[stimulus_presentations['stimulus_name']=='drifting_gratings']
drifting_gratings_presentations
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>color</th>
      <th>contrast</th>
      <th>frame</th>
      <th>orientation</th>
      <th>phase</th>
      <th>size</th>
      <th>spatial_frequency</th>
      <th>start_time</th>
      <th>stimulus_block</th>
      <th>stimulus_name</th>
      <th>stop_time</th>
      <th>temporal_frequency</th>
      <th>x_position</th>
      <th>y_position</th>
      <th>duration</th>
      <th>stimulus_condition_id</th>
    </tr>
    <tr>
      <th>stimulus_presentation_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3798</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>315.0</td>
      <td>[21211.93333333, 21211.93333333]</td>
      <td>[250.0, 250.0]</td>
      <td>0.04</td>
      <td>1574.774823</td>
      <td>2.0</td>
      <td>drifting_gratings</td>
      <td>1576.776513</td>
      <td>4.0</td>
      <td>null</td>
      <td>null</td>
      <td>2.00169</td>
      <td>246</td>
    </tr>
    <tr>
      <th>3799</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>90.0</td>
      <td>[21211.93333333, 21211.93333333]</td>
      <td>[250.0, 250.0]</td>
      <td>0.04</td>
      <td>1577.777347</td>
      <td>2.0</td>
      <td>drifting_gratings</td>
      <td>1579.779027</td>
      <td>8.0</td>
      <td>null</td>
      <td>null</td>
      <td>2.00168</td>
      <td>247</td>
    </tr>
    <tr>
      <th>3800</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>225.0</td>
      <td>[21211.93333333, 21211.93333333]</td>
      <td>[250.0, 250.0]</td>
      <td>0.04</td>
      <td>1580.779833</td>
      <td>2.0</td>
      <td>drifting_gratings</td>
      <td>1582.781563</td>
      <td>2.0</td>
      <td>null</td>
      <td>null</td>
      <td>2.00173</td>
      <td>248</td>
    </tr>
    <tr>
      <th>3801</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>90.0</td>
      <td>[21211.93333333, 21211.93333333]</td>
      <td>[250.0, 250.0]</td>
      <td>0.04</td>
      <td>1583.782367</td>
      <td>2.0</td>
      <td>drifting_gratings</td>
      <td>1585.784047</td>
      <td>2.0</td>
      <td>null</td>
      <td>null</td>
      <td>2.00168</td>
      <td>249</td>
    </tr>
    <tr>
      <th>3802</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>135.0</td>
      <td>[21211.93333333, 21211.93333333]</td>
      <td>[250.0, 250.0]</td>
      <td>0.04</td>
      <td>1586.784883</td>
      <td>2.0</td>
      <td>drifting_gratings</td>
      <td>1588.786553</td>
      <td>8.0</td>
      <td>null</td>
      <td>null</td>
      <td>2.00167</td>
      <td>250</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>49426</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>135.0</td>
      <td>[21211.93333333, 21211.93333333]</td>
      <td>[250.0, 250.0]</td>
      <td>0.04</td>
      <td>5366.976107</td>
      <td>7.0</td>
      <td>drifting_gratings</td>
      <td>5368.977777</td>
      <td>15.0</td>
      <td>null</td>
      <td>null</td>
      <td>2.00167</td>
      <td>274</td>
    </tr>
    <tr>
      <th>49427</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>180.0</td>
      <td>[21211.93333333, 21211.93333333]</td>
      <td>[250.0, 250.0]</td>
      <td>0.04</td>
      <td>5369.978603</td>
      <td>7.0</td>
      <td>drifting_gratings</td>
      <td>5371.980283</td>
      <td>8.0</td>
      <td>null</td>
      <td>null</td>
      <td>2.00168</td>
      <td>260</td>
    </tr>
    <tr>
      <th>49428</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>0.0</td>
      <td>[21211.93333333, 21211.93333333]</td>
      <td>[250.0, 250.0]</td>
      <td>0.04</td>
      <td>5372.981107</td>
      <td>7.0</td>
      <td>drifting_gratings</td>
      <td>5374.982807</td>
      <td>1.0</td>
      <td>null</td>
      <td>null</td>
      <td>2.00170</td>
      <td>251</td>
    </tr>
    <tr>
      <th>49429</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>180.0</td>
      <td>[21211.93333333, 21211.93333333]</td>
      <td>[250.0, 250.0]</td>
      <td>0.04</td>
      <td>5375.983663</td>
      <td>7.0</td>
      <td>drifting_gratings</td>
      <td>5377.985343</td>
      <td>4.0</td>
      <td>null</td>
      <td>null</td>
      <td>2.00168</td>
      <td>282</td>
    </tr>
    <tr>
      <th>49430</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>270.0</td>
      <td>[21211.93333333, 21211.93333333]</td>
      <td>[250.0, 250.0]</td>
      <td>0.04</td>
      <td>5378.986127</td>
      <td>7.0</td>
      <td>drifting_gratings</td>
      <td>5380.987797</td>
      <td>4.0</td>
      <td>null</td>
      <td>null</td>
      <td>2.00167</td>
      <td>279</td>
    </tr>
  </tbody>
</table>
<p>628 rows × 16 columns</p>
</div>



Let's see what orientations we have:


```python
orientations = drifting_gratings_presentations['orientation'].values # get oreintations of the static gratings
orientations
```




    array([315.0, 90.0, 225.0, 90.0, 135.0, 0.0, 315.0, 315.0, 270.0, 90.0,
           0.0, 315.0, 270.0, 'null', 'null', 315.0, 315.0, 315.0, 180.0,
           'null', 45.0, 315.0, 90.0, 270.0, 135.0, 90.0, 135.0, 135.0, 135.0,
           45.0, 315.0, 0.0, 180.0, 0.0, 315.0, 315.0, 45.0, 90.0, 180.0,
           'null', 135.0, 225.0, 0.0, 135.0, 45.0, 315.0, 225.0, 0.0, 45.0,
           270.0, 135.0, 180.0, 180.0, 180.0, 90.0, 0.0, 0.0, 90.0, 225.0,
           90.0, 'null', 45.0, 'null', 270.0, 45.0, 180.0, 225.0, 225.0, 45.0,
           90.0, 315.0, 270.0, 270.0, 270.0, 0.0, 45.0, 270.0, 270.0, 225.0,
           270.0, 180.0, 180.0, 315.0, 45.0, 90.0, 270.0, 315.0, 135.0, 315.0,
           45.0, 135.0, 'null', 225.0, 180.0, 90.0, 225.0, 180.0, 90.0, 315.0,
           270.0, 135.0, 270.0, 180.0, 315.0, 0.0, 315.0, 225.0, 45.0, 90.0,
           0.0, 135.0, 0.0, 45.0, 90.0, 90.0, 135.0, 270.0, 270.0, 45.0,
           225.0, 45.0, 180.0, 180.0, 90.0, 90.0, 90.0, 270.0, 0.0, 315.0,
           225.0, 180.0, 270.0, 45.0, 315.0, 45.0, 135.0, 45.0, 45.0, 45.0,
           270.0, 'null', 180.0, 180.0, 90.0, 'null', 315.0, 180.0, 0.0,
           'null', 135.0, 315.0, 225.0, 45.0, 315.0, 270.0, 135.0, 'null',
           135.0, 270.0, 0.0, 225.0, 0.0, 135.0, 225.0, 225.0, 135.0, 45.0,
           90.0, 225.0, 45.0, 45.0, 0.0, 180.0, 180.0, 135.0, 315.0, 180.0,
           315.0, 0.0, 315.0, 180.0, 'null', 135.0, 270.0, 225.0, 90.0, 270.0,
           135.0, 270.0, 180.0, 225.0, 0.0, 0.0, 0.0, 270.0, 180.0, 270.0,
           'null', 'null', 45.0, 0.0, 'null', 135.0, 'null', 315.0, 135.0,
           0.0, 90.0, 225.0, 45.0, 315.0, 225.0, 0.0, 180.0, 0.0, 225.0, 0.0,
           270.0, 45.0, 225.0, 180.0, 315.0, 90.0, 90.0, 90.0, 270.0, 180.0,
           45.0, 0.0, 270.0, 45.0, 90.0, 45.0, 270.0, 0.0, 90.0, 0.0, 90.0,
           90.0, 225.0, 180.0, 180.0, 135.0, 135.0, 270.0, 180.0, 135.0,
           135.0, 45.0, 315.0, 225.0, 315.0, 90.0, 0.0, 135.0, 'null', 90.0,
           135.0, 135.0, 225.0, 45.0, 0.0, 0.0, 135.0, 315.0, 135.0, 225.0,
           315.0, 225.0, 270.0, 135.0, 135.0, 225.0, 135.0, 315.0, 'null',
           180.0, 315.0, 225.0, 0.0, 225.0, 180.0, 270.0, 45.0, 135.0, 45.0,
           270.0, 135.0, 270.0, 90.0, 270.0, 45.0, 45.0, 45.0, 135.0, 'null',
           90.0, 45.0, 225.0, 45.0, 225.0, 45.0, 45.0, 0.0, 'null', 45.0,
           270.0, 270.0, 45.0, 225.0, 90.0, 135.0, 45.0, 90.0, 180.0, 90.0,
           315.0, 0.0, 0.0, 225.0, 315.0, 180.0, 45.0, 90.0, 225.0, 45.0,
           180.0, 'null', 135.0, 0.0, 0.0, 135.0, 315.0, 135.0, 180.0, 270.0,
           270.0, 315.0, 180.0, 315.0, 90.0, 45.0, 0.0, 315.0, 90.0, 45.0,
           135.0, 180.0, 135.0, 135.0, 180.0, 0.0, 270.0, 225.0, 270.0, 45.0,
           180.0, 0.0, 225.0, 45.0, 90.0, 270.0, 45.0, 225.0, 270.0, 180.0,
           315.0, 225.0, 0.0, 225.0, 90.0, 315.0, 270.0, 45.0, 0.0, 45.0,
           90.0, 180.0, 0.0, 90.0, 90.0, 180.0, 45.0, 45.0, 90.0, 135.0,
           270.0, 135.0, 225.0, 'null', 315.0, 270.0, 135.0, 315.0, 270.0,
           0.0, 270.0, 180.0, 0.0, 270.0, 315.0, 225.0, 180.0, 180.0, 90.0,
           315.0, 0.0, 0.0, 45.0, 270.0, 315.0, 180.0, 270.0, 270.0, 0.0,
           270.0, 135.0, 270.0, 45.0, 90.0, 'null', 315.0, 90.0, 180.0, 90.0,
           225.0, 315.0, 0.0, 315.0, 225.0, 180.0, 0.0, 180.0, 180.0, 180.0,
           225.0, 90.0, 45.0, 225.0, 0.0, 0.0, 270.0, 225.0, 0.0, 90.0,
           'null', 135.0, 225.0, 315.0, 180.0, 135.0, 90.0, 0.0, 135.0, 180.0,
           270.0, 90.0, 0.0, 225.0, 180.0, 180.0, 90.0, 90.0, 90.0, 180.0,
           315.0, 180.0, 0.0, 270.0, 135.0, 45.0, 315.0, 'null', 225.0, 90.0,
           180.0, 315.0, 'null', 45.0, 90.0, 0.0, 90.0, 225.0, 90.0, 180.0,
           0.0, 45.0, 180.0, 270.0, 315.0, 315.0, 225.0, 90.0, 225.0, 90.0,
           315.0, 315.0, 0.0, 270.0, 90.0, 225.0, 225.0, 135.0, 45.0, 90.0,
           180.0, 45.0, 135.0, 270.0, 225.0, 135.0, 0.0, 0.0, 45.0, 90.0,
           315.0, 90.0, 45.0, 45.0, 315.0, 45.0, 90.0, 0.0, 45.0, 180.0,
           225.0, 0.0, 315.0, 180.0, 90.0, 225.0, 225.0, 270.0, 45.0, 0.0,
           90.0, 0.0, 315.0, 225.0, 270.0, 180.0, 45.0, 135.0, 225.0, 225.0,
           225.0, 135.0, 225.0, 270.0, 90.0, 'null', 270.0, 315.0, 135.0,
           225.0, 90.0, 180.0, 225.0, 135.0, 270.0, 315.0, 45.0, 180.0, 0.0,
           0.0, 225.0, 135.0, 315.0, 135.0, 135.0, 90.0, 225.0, 0.0, 315.0,
           270.0, 180.0, 'null', 315.0, 135.0, 45.0, 0.0, 135.0, 45.0, 180.0,
           'null', 270.0, 180.0, 270.0, 135.0, 225.0, 225.0, 'null', 270.0,
           135.0, 0.0, 135.0, 270.0, 180.0, 315.0, 270.0, 315.0, 225.0, 135.0,
           315.0, 315.0, 0.0, 90.0, 180.0, 270.0, 225.0, 135.0, 90.0, 135.0,
           45.0, 180.0, 270.0, 315.0, 0.0, 135.0, 315.0, 225.0, 45.0, 225.0,
           135.0, 180.0, 0.0, 180.0, 270.0], dtype=object)



We can see that there are some null values. Let's convert these values to floats for better handling.


```python
orientations[orientations=='null'] = np.nan # replace all null values to NaN
orientations = orientations.astype(float) # convert to float array
angle_range = np.unique(orientations)[0:-1] # find all unique values excluding NaNs
angle_range
```




    array([  0.,  45.,  90., 135., 180., 225., 270., 315.])



These are the 8 orientations of the driftig gratings, sampling 360 degrees at 45 degree intervals.

Now we need to access information from *stimulus_presentations* metadata and load it as a Pynapple object. Specifically, we need to create a dictionary of IntervalSets for each orientation.

First, we need stimulus intervals for drifting gratings to organize by orientation.


```python
drifting_gratings_intervals =  stimulus_intervals['drifting_gratings']
drifting_gratings_intervals
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>start</th>
      <th>end</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1574.774823</td>
      <td>1576.776513</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1577.777347</td>
      <td>1579.779027</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1580.779833</td>
      <td>1582.781563</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1583.782367</td>
      <td>1585.784047</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1586.784883</td>
      <td>1588.786553</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5366.976107</td>
      <td>5368.977777</td>
    </tr>
    <tr>
      <th>6</th>
      <td>5369.978603</td>
      <td>5371.980283</td>
    </tr>
    <tr>
      <th>7</th>
      <td>5372.981107</td>
      <td>5374.982807</td>
    </tr>
    <tr>
      <th>8</th>
      <td>5375.983663</td>
      <td>5377.985343</td>
    </tr>
    <tr>
      <th>9</th>
      <td>5378.986127</td>
      <td>5380.987797</td>
    </tr>
  </tbody>
</table>
<p>628 rows × 2 columns</p>
</div>



Great. Now let's proceed to sorting these intervals into **IntervalSet**s by their orientation


```python
dict_ori = {}

for angle in angle_range:
    tokeep = [] # list of trials to keep

    for i in range(len(drifting_gratings_presentations)): # loop over all gabors trials
        if float(orientations[i]==angle): # find trials with given orientation
            tokeep.append(i)
    dict_ori[angle] = drifting_gratings_intervals.loc[tokeep] # make dictionary of IntervalSets

dict_ori
```




    {0.0:           start          end
     0   1589.787377  1591.789047
     1   1604.799993  1606.801573
     2   1667.852587  1669.854267
     3   1673.857607  1675.859277
     4   1700.880223  1702.881873
     ..          ...          ...
     69  5237.868283  5239.869913
     70  5279.903393  5281.905073
     71  5312.930947  5314.932627
     72  5348.961047  5350.962727
     73  5372.981107  5374.982807
     
     [74 rows x 2 columns],
     45.0:           start          end
     0   1634.824993  1636.826683
     1   1661.847597  1663.849267
     2   1682.865123  1684.866833
     3   1706.885213  1708.886883
     4   1718.895253  1720.896963
     ..          ...          ...
     70  5180.820607  5182.822277
     71  5234.865757  5236.867417
     72  5243.873283  5245.874953
     73  5336.951027  5338.952697
     74  5360.971097  5362.972757
     
     [75 rows x 2 columns],
     90.0:           start          end
     0   1577.777347  1579.779027
     1   1583.782367  1585.784047
     2   1601.797417  1603.799097
     3   1640.830033  1642.831703
     4   1649.837547  1651.839217
     ..          ...          ...
     70  5144.790507  5146.792167
     71  5162.805557  5164.807227
     72  5207.843153  5209.844843
     73  5315.933463  5317.935153
     74  5330.945997  5332.947677
     
     [75 rows x 2 columns],
     135.0:           start          end
     0   1586.784883  1588.786553
     1   1646.834993  1648.836703
     2   1652.840073  1654.841743
     3   1655.842567  1657.844227
     4   1658.845063  1660.846763
     ..          ...          ...
     69  5303.923423  5305.925113
     70  5327.943483  5329.945163
     71  5333.948513  5335.950203
     72  5351.963563  5353.965203
     73  5366.976107  5368.977777
     
     [74 rows x 2 columns],
     180.0:           start          end
     0   1628.820023  1630.821703
     1   1670.855103  1672.856783
     2   1688.870163  1690.871853
     3   1727.902757  1729.904427
     4   1730.905303  1732.906953
     ..          ...          ...
     70  5288.910887  5290.912557
     71  5318.935957  5320.937647
     72  5339.953523  5341.955183
     73  5369.978603  5371.980283
     74  5375.983663  5377.985343
     
     [75 rows x 2 columns],
     225.0:           start          end
     0   1580.779833  1582.781563
     1   1697.877687  1699.879357
     2   1712.890213  1714.891913
     3   1748.920323  1750.922013
     4   1772.940363  1774.942053
     ..          ...          ...
     70  5267.893343  5269.895043
     71  5300.920927  5302.922597
     72  5324.940987  5326.942657
     73  5357.968573  5359.970233
     74  5363.973593  5365.975283
     
     [75 rows x 2 columns],
     270.0:           start          end
     0   1598.794933  1600.796563
     1   1610.804943  1612.806633
     2   1643.832527  1645.834217
     3   1721.897747  1723.899427
     4   1763.932867  1765.934547
     ..          ...          ...
     70  5285.908373  5287.910063
     71  5294.915917  5296.917577
     72  5321.938523  5323.940153
     73  5342.956047  5344.957707
     74  5378.986127  5380.987797
     
     [75 rows x 2 columns],
     315.0:           start          end
     0   1574.774823  1576.776513
     1   1592.789903  1594.791563
     2   1595.792407  1597.794077
     3   1607.802437  1609.804107
     4   1619.812457  1621.814137
     ..          ...          ...
     70  5297.918423  5299.920093
     71  5306.925927  5308.927607
     72  5309.928463  5311.930133
     73  5345.958553  5347.960203
     74  5354.966067  5356.967737
     
     [75 rows x 2 columns]}



This dictionary has the *drifting_gratings_intervals* sorted by orientation. We can use these to compute orientation tuning curves. Since the stimuli are presented in discrete orientations (i.e. not spanning all angular values from 0 to 360 degrees), we will be using Pynapple's *compute_discrete_tuning_curves*.

We can calculate tuning curves with one line with Pynapple!


```python
# Plot firing rate of V1 units as a function of orientation, i.e. an orientation tuning curve
discrete_tuning_curves = nap.compute_discrete_tuning_curves(v1_high_snr_units, dict_ori)

discrete_tuning_curves
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>950930985</th>
      <th>950931458</th>
      <th>950931533</th>
      <th>950931727</th>
      <th>950931751</th>
      <th>950932696</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0.0</th>
      <td>29.995305</td>
      <td>10.423757</td>
      <td>1.829558</td>
      <td>23.304928</td>
      <td>2.848980</td>
      <td>0.067511</td>
    </tr>
    <tr>
      <th>45.0</th>
      <td>44.840722</td>
      <td>15.482074</td>
      <td>3.244307</td>
      <td>23.389656</td>
      <td>3.430838</td>
      <td>0.133236</td>
    </tr>
    <tr>
      <th>90.0</th>
      <td>33.685112</td>
      <td>16.839225</td>
      <td>1.825138</td>
      <td>14.194774</td>
      <td>3.084083</td>
      <td>0.006661</td>
    </tr>
    <tr>
      <th>135.0</th>
      <td>17.431332</td>
      <td>16.000099</td>
      <td>4.793279</td>
      <td>19.017840</td>
      <td>3.659094</td>
      <td>0.567092</td>
    </tr>
    <tr>
      <th>180.0</th>
      <td>33.585341</td>
      <td>13.109074</td>
      <td>1.971690</td>
      <td>27.217315</td>
      <td>4.336386</td>
      <td>0.686095</td>
    </tr>
    <tr>
      <th>225.0</th>
      <td>45.734898</td>
      <td>14.614385</td>
      <td>4.782647</td>
      <td>22.894093</td>
      <td>3.843437</td>
      <td>0.293087</td>
    </tr>
    <tr>
      <th>270.0</th>
      <td>38.394459</td>
      <td>14.281353</td>
      <td>1.731881</td>
      <td>13.681856</td>
      <td>2.804314</td>
      <td>0.079933</td>
    </tr>
    <tr>
      <th>315.0</th>
      <td>19.910011</td>
      <td>14.840918</td>
      <td>4.216473</td>
      <td>20.476204</td>
      <td>2.930882</td>
      <td>0.526226</td>
    </tr>
  </tbody>
</table>
</div>



Each column is a unit, and each row is the orientation of the stimulus in degrees. The values in the table represent the firing rate of the unit in Hz. Let's plot them!


```python
plt.figure(figsize=(12,9))
for i in range(len(v1_unit_IDs)): # loop over all unit IDs
    plt.subplot(2,3,i+1) # plot tuning curves in 2 rows and 3 columns
    plt.plot(discrete_tuning_curves[v1_unit_IDs[i]], 'o-', color='k', linewidth=2)
    plt.xlabel('Orientation (deg)')
    plt.ylabel('Firing rate (Hz)')
    plt.title("Unit %d" % v1_unit_IDs[i], fontsize=10)
    plt.subplots_adjust(wspace=0.5, hspace=1, top=0.4)
```


    
![png](nwbmatic-pynapple-allen-tutorial_files/nwbmatic-pynapple-allen-tutorial_50_0.png)
    


Nice! Looks like some of these neurons have some degree of orientation tuning.

### 2D Spatial Tuning Curves ###
Neurons in V1 are known to have spatial tuning based on the location of the stimulus in space.

The gabors stimuli are shown on various locations on the screen. The x-y location of stimuli can be found in the *stimulus_presentations* metadata. Here, we will go through how we can access this metadata and use it to calculate 2D spatial tuning curves.

Let's first get a table of stimulus presentations for gabors to look at the metadata for this stimulus.


```python
# get gabors informatiom from stimulus_presentations metadata
gabors_presentations = stimulus_presentations[stimulus_presentations['stimulus_name']=='gabors']
gabors_presentations
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>color</th>
      <th>contrast</th>
      <th>frame</th>
      <th>orientation</th>
      <th>phase</th>
      <th>size</th>
      <th>spatial_frequency</th>
      <th>start_time</th>
      <th>stimulus_block</th>
      <th>stimulus_name</th>
      <th>stop_time</th>
      <th>temporal_frequency</th>
      <th>x_position</th>
      <th>y_position</th>
      <th>duration</th>
      <th>stimulus_condition_id</th>
    </tr>
    <tr>
      <th>stimulus_presentation_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>45.0</td>
      <td>[3644.93333333, 3644.93333333]</td>
      <td>[20.0, 20.0]</td>
      <td>0.08</td>
      <td>73.537433</td>
      <td>0.0</td>
      <td>gabors</td>
      <td>73.770952</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>30.0</td>
      <td>0.233519</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>0.0</td>
      <td>[3644.93333333, 3644.93333333]</td>
      <td>[20.0, 20.0]</td>
      <td>0.08</td>
      <td>73.770952</td>
      <td>0.0</td>
      <td>gabors</td>
      <td>74.021150</td>
      <td>4.0</td>
      <td>-30.0</td>
      <td>-10.0</td>
      <td>0.250199</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>45.0</td>
      <td>[3644.93333333, 3644.93333333]</td>
      <td>[20.0, 20.0]</td>
      <td>0.08</td>
      <td>74.021150</td>
      <td>0.0</td>
      <td>gabors</td>
      <td>74.271349</td>
      <td>4.0</td>
      <td>10.0</td>
      <td>20.0</td>
      <td>0.250199</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>0.0</td>
      <td>[3644.93333333, 3644.93333333]</td>
      <td>[20.0, 20.0]</td>
      <td>0.08</td>
      <td>74.271349</td>
      <td>0.0</td>
      <td>gabors</td>
      <td>74.521547</td>
      <td>4.0</td>
      <td>-40.0</td>
      <td>-40.0</td>
      <td>0.250199</td>
      <td>4</td>
    </tr>
    <tr>
      <th>5</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>90.0</td>
      <td>[3644.93333333, 3644.93333333]</td>
      <td>[20.0, 20.0]</td>
      <td>0.08</td>
      <td>74.521547</td>
      <td>0.0</td>
      <td>gabors</td>
      <td>74.771764</td>
      <td>4.0</td>
      <td>-10.0</td>
      <td>-10.0</td>
      <td>0.250216</td>
      <td>5</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>3641</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>45.0</td>
      <td>[3644.93333333, 3644.93333333]</td>
      <td>[20.0, 20.0]</td>
      <td>0.08</td>
      <td>984.281513</td>
      <td>0.0</td>
      <td>gabors</td>
      <td>984.531719</td>
      <td>4.0</td>
      <td>30.0</td>
      <td>-10.0</td>
      <td>0.250206</td>
      <td>192</td>
    </tr>
    <tr>
      <th>3642</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>45.0</td>
      <td>[3644.93333333, 3644.93333333]</td>
      <td>[20.0, 20.0]</td>
      <td>0.08</td>
      <td>984.531719</td>
      <td>0.0</td>
      <td>gabors</td>
      <td>984.781925</td>
      <td>4.0</td>
      <td>-20.0</td>
      <td>10.0</td>
      <td>0.250206</td>
      <td>39</td>
    </tr>
    <tr>
      <th>3643</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>0.0</td>
      <td>[3644.93333333, 3644.93333333]</td>
      <td>[20.0, 20.0]</td>
      <td>0.08</td>
      <td>984.781925</td>
      <td>0.0</td>
      <td>gabors</td>
      <td>985.032131</td>
      <td>4.0</td>
      <td>-30.0</td>
      <td>40.0</td>
      <td>0.250206</td>
      <td>186</td>
    </tr>
    <tr>
      <th>3644</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>45.0</td>
      <td>[3644.93333333, 3644.93333333]</td>
      <td>[20.0, 20.0]</td>
      <td>0.08</td>
      <td>985.032131</td>
      <td>0.0</td>
      <td>gabors</td>
      <td>985.282337</td>
      <td>4.0</td>
      <td>10.0</td>
      <td>-30.0</td>
      <td>0.250206</td>
      <td>232</td>
    </tr>
    <tr>
      <th>3645</th>
      <td>null</td>
      <td>0.8</td>
      <td>null</td>
      <td>45.0</td>
      <td>[3644.93333333, 3644.93333333]</td>
      <td>[20.0, 20.0]</td>
      <td>0.08</td>
      <td>985.282337</td>
      <td>0.0</td>
      <td>gabors</td>
      <td>985.532551</td>
      <td>4.0</td>
      <td>-40.0</td>
      <td>40.0</td>
      <td>0.250214</td>
      <td>153</td>
    </tr>
  </tbody>
</table>
<p>3645 rows × 16 columns</p>
</div>



Now, we need to extract the x- and y-position from the metadata and load it into a **TsdFrame**.


```python
# extract x- and y-position columns
x_positions = np.array(gabors_presentations['x_position']).tolist()
y_positions = np.array(gabors_presentations['y_position']).tolist()

# load into x and y positions into a vstack
xy_positions = np.vstack((x_positions,y_positions)).T

# what does this look like?
xy_positions
```




    array([[  0.,  30.],
           [-30., -10.],
           [ 10.,  20.],
           ...,
           [-30.,  40.],
           [ 10., -30.],
           [-40.,  40.]])



Now let's load the xy positions into a **TsdFrame**. Since we will use the absolute start times as the time index (see below), we don't need to provide additional time support. When no time support is passed, the default global time support is used.


```python
# get start time as start time of the stimulus presentations
time_index = (gabors_presentations['start_time']).values

# load TsdFrame
xy_features = nap.TsdFrame(t=time_index, d=xy_positions, time_units="s", columns=['x','y'])

# what does this look like?
xy_features
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x</th>
      <th>y</th>
    </tr>
    <tr>
      <th>Time (s)</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>73.537433</th>
      <td>0.0</td>
      <td>30.0</td>
    </tr>
    <tr>
      <th>73.770952</th>
      <td>-30.0</td>
      <td>-10.0</td>
    </tr>
    <tr>
      <th>74.021150</th>
      <td>10.0</td>
      <td>20.0</td>
    </tr>
    <tr>
      <th>74.271349</th>
      <td>-40.0</td>
      <td>-40.0</td>
    </tr>
    <tr>
      <th>74.521547</th>
      <td>-10.0</td>
      <td>-10.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>984.281513</th>
      <td>30.0</td>
      <td>-10.0</td>
    </tr>
    <tr>
      <th>984.531719</th>
      <td>-20.0</td>
      <td>10.0</td>
    </tr>
    <tr>
      <th>984.781925</th>
      <td>-30.0</td>
      <td>40.0</td>
    </tr>
    <tr>
      <th>985.032131</th>
      <td>10.0</td>
      <td>-30.0</td>
    </tr>
    <tr>
      <th>985.282337</th>
      <td>-40.0</td>
      <td>40.0</td>
    </tr>
  </tbody>
</table>
<p>3645 rows × 2 columns</p>
</div>



Great! Almost there. To compute the 2D tuning curve, it just takes one line with Pynapple!


```python
# using bin size of 9 since x-y stimulus is shown in a 9x9 grid (-40,-30,-20,-10,0,10,20,30,40)
spatial_tuning_curve, binsxy = nap.compute_2d_tuning_curves(group=v1_high_snr_units,feature=xy_features, nb_bins=9)
```


```python
spatial_tuning_curve
```




    {950930985: array([[39.71176567, 44.15379762, 44.7756821 , 42.82118804, 39.00104056,
             41.13321589, 43.70959443, 40.60017206, 37.40190905],
            [35.62509627, 45.04220401, 47.79626383, 45.21988529, 43.44307251,
             40.2448095 , 37.57959033, 36.33582138, 40.15596886],
            [41.31089717, 45.13104465, 46.55249488, 44.15379762, 41.75510037,
             43.53191315, 35.26973372, 38.645678  , 39.97828759],
            [37.49074969, 44.7756821 , 45.39756657, 39.97828759, 41.13321589,
             38.29031544, 39.71176567, 40.51133142, 39.35640311],
            [45.39756657, 39.88944695, 37.31306841, 41.31089717, 36.86886522,
             38.11263417, 41.66625973, 39.53408439, 37.49074969],
            [45.75292913, 38.82335928, 39.00104056, 40.2448095 , 41.75510037,
             39.26756247, 39.0898812 , 42.64350676, 45.39756657],
            [41.93278165, 44.06495698, 44.15379762, 43.35423187, 39.71176567,
             35.09205244, 39.44524375, 42.99886932, 38.46799672],
            [41.04437526, 42.82118804, 44.15379762, 40.60017206, 42.37698484,
             36.24698075, 36.42466202, 40.60017206, 39.0898812 ],
            [40.06712823, 42.91002868, 43.44307251, 41.66625973, 38.2014748 ,
             36.51350266, 38.82335928, 37.13538714, 39.80060631]]),
     950931458: array([[12.08232692, 11.19392052, 11.72696436, 13.32609586, 11.99348628,
             11.63812372, 12.88189267, 10.39435477, 12.88189267],
            [12.70421139, 13.4149365 , 14.21450225, 12.79305203, 12.26000819,
             14.48102417, 11.72696436, 14.21450225, 13.68145842],
            [13.68145842, 15.28058992, 16.52435887, 14.83638673, 15.014068  ,
             13.14841458, 11.72696436, 12.61537075, 13.14841458],
            [13.77029906, 17.0574027 , 20.25566571, 21.05523146, 15.4582712 ,
             14.39218353, 13.32609586, 13.14841458, 11.815805  ],
            [15.4582712 , 18.92305612, 23.72045063, 27.45175748, 17.32392462,
             15.19174928, 11.28276116, 13.59261778, 13.59261778],
            [12.52653011, 16.34667759, 23.09856616, 22.83204424, 14.56986481,
             13.05957394, 10.21667349, 12.88189267, 12.97073331],
            [12.70421139, 13.77029906, 14.83638673, 13.14841458, 13.23725522,
             14.56986481, 11.46044244, 12.43768947, 14.39218353],
            [14.30334289, 13.68145842, 11.46044244, 13.32609586, 12.43768947,
             11.63812372, 14.21450225, 12.52653011, 11.63812372],
            [12.79305203, 13.14841458, 12.34884883, 12.08232692, 12.61537075,
             11.72696436, 12.17116755, 10.74971733, 12.79305203]]),
     950931533: array([[1.15492831, 0.97724703, 0.97724703, 1.5991315 , 1.33260959,
             1.06608767, 0.88840639, 0.71072511, 1.06608767],
            [1.06608767, 2.22101598, 2.57637853, 2.22101598, 1.77681278,
             0.79956575, 0.97724703, 0.71072511, 0.4442032 ],
            [1.33260959, 3.19826301, 4.0866694 , 3.90898812, 2.30985662,
             1.51029086, 0.4442032 , 1.33260959, 1.24376895],
            [0.71072511, 2.39869726, 4.61971323, 4.53087259, 1.86565342,
             1.15492831, 1.51029086, 1.06608767, 0.88840639],
            [0.97724703, 1.5991315 , 2.66521917, 3.28710365, 0.53304383,
             1.42145023, 0.79956575, 2.30985662, 1.42145023],
            [0.62188447, 1.15492831, 1.42145023, 1.51029086, 1.42145023,
             1.24376895, 1.06608767, 0.71072511, 0.71072511],
            [1.51029086, 1.42145023, 0.97724703, 1.15492831, 1.15492831,
             1.15492831, 1.86565342, 1.33260959, 1.42145023],
            [0.88840639, 0.71072511, 1.68797214, 1.42145023, 0.88840639,
             0.26652192, 1.5991315 , 0.97724703, 0.53304383],
            [1.06608767, 1.06608767, 1.95449406, 1.51029086, 0.71072511,
             1.5991315 , 0.97724703, 0.62188447, 1.24376895]]),
     950931727: array([[16.52435887, 15.10290864, 15.99131503, 15.014068  , 14.83638673,
             16.25783695, 15.99131503, 14.03682097, 16.16899631],
            [16.25783695, 14.74754609, 16.79088079, 17.14624334, 18.12349037,
             18.92305612, 15.9024744 , 15.10290864, 16.79088079],
            [16.25783695, 20.16682507, 24.7865383 , 21.5882753 , 19.90030315,
             15.36943056, 15.9024744 , 14.21450225, 18.12349037],
            [16.16899631, 29.49509217, 33.58176157, 27.89596067, 17.32392462,
             16.43551823, 16.96856206, 16.16899631, 15.63595248],
            [20.52218763, 34.02596477, 31.3607456 , 31.89378943, 19.5449406 ,
             18.74537485, 15.4582712 , 14.65870545, 16.25783695],
            [21.41059402, 32.33799263, 36.33582138, 35.80277755, 20.78870954,
             15.4582712 , 13.59261778, 17.59044654, 20.25566571],
            [17.94580909, 28.60668578, 33.22639902, 29.76161409, 20.96639082,
             17.32392462, 18.03464973, 17.0574027 , 17.32392462],
            [18.39001229, 21.76595657, 25.05306022, 21.5882753 , 17.85696846,
             15.99131503, 18.39001229, 16.61319951, 16.52435887],
            [17.59044654, 18.39001229, 22.38784105, 21.85479721, 18.30117165,
             16.08015567, 16.79088079, 14.39218353, 16.25783695]]),
     950931751: array([[3.10942237, 1.06608767, 1.51029086, 1.33260959, 2.22101598,
             2.75405981, 1.5991315 , 1.24376895, 1.5991315 ],
            [2.57637853, 2.66521917, 2.93174109, 2.84290045, 2.84290045,
             2.75405981, 2.22101598, 1.5991315 , 2.0433347 ],
            [1.51029086, 5.06391643, 6.21884474, 3.90898812, 1.86565342,
             1.42145023, 1.51029086, 1.68797214, 1.95449406],
            [1.68797214, 7.37377304, 8.1733388 , 5.33043834, 3.02058173,
             1.77681278, 1.42145023, 1.77681278, 2.30985662],
            [3.37594429, 7.64029496, 8.43986071, 4.88623515, 2.84290045,
             4.17551004, 2.13217534, 2.0433347 , 2.57637853],
            [2.0433347 , 4.97507579, 7.55145432, 2.66521917, 1.95449406,
             1.86565342, 1.5991315 , 2.30985662, 2.57637853],
            [1.95449406, 2.57637853, 3.99782876, 2.57637853, 2.22101598,
             2.75405981, 2.13217534, 2.39869726, 1.68797214],
            [1.86565342, 3.82014748, 2.57637853, 1.86565342, 1.15492831,
             1.86565342, 2.93174109, 1.06608767, 2.30985662],
            [2.75405981, 1.77681278, 1.68797214, 2.0433347 , 2.30985662,
             2.0433347 , 1.68797214, 1.95449406, 2.30985662]]),
     950932696: array([[0.        , 0.        , 0.        , 0.08884064, 0.        ,
             0.        , 0.08884064, 0.        , 0.08884064],
            [0.08884064, 0.08884064, 0.08884064, 0.        , 0.17768128,
             0.        , 0.08884064, 0.        , 0.08884064],
            [0.08884064, 0.        , 0.        , 0.17768128, 0.        ,
             0.        , 0.        , 0.        , 0.08884064],
            [0.        , 0.        , 0.17768128, 0.17768128, 0.08884064,
             0.        , 0.08884064, 0.        , 0.35536256],
            [0.        , 0.        , 0.08884064, 0.17768128, 0.08884064,
             0.        , 0.        , 0.        , 0.17768128],
            [0.08884064, 0.        , 0.35536256, 0.        , 0.17768128,
             0.26652192, 0.08884064, 0.        , 0.26652192],
            [0.        , 0.08884064, 0.08884064, 0.17768128, 0.26652192,
             0.        , 0.08884064, 0.08884064, 0.08884064],
            [0.        , 0.        , 0.        , 0.        , 0.26652192,
             0.08884064, 0.08884064, 0.26652192, 0.        ],
            [0.08884064, 0.08884064, 0.26652192, 0.17768128, 0.17768128,
             0.08884064, 0.17768128, 0.        , 0.        ]])}



Now we have calculated the 2D spatial tuning curve for our neurons in V1! Let's plot it with a heat map.


```python
#set the x and y axis limits
extent = [-40, 40, -40, 40]

# Create a 2x3 grid of subplots
fig, axs = plt.subplots(2, 3, figsize=(12, 8))

# Iterate over each unit and plot the heatmap in a subplot
for i, unit in enumerate(v1_unit_IDs):
    values = spatial_tuning_curve[unit]

    # Select the current subplot
    ax = axs[i // 3, i % 3]

    # Create the heatmap using seaborn with adjusted aspect ratio
    ax.imshow(spatial_tuning_curve[unit], cmap='jet', extent=extent, vmin=np.min(values), vmax=np.max(values))

    # Set the title and axis labels
    ax.set_title(f'Unit: {unit}')
    ax.set_xlabel('X-position')
    ax.set_ylabel('Y-postition')

# Adjust the spacing between subplots
plt.tight_layout()

# Display the plot
plt.show()
```


    
![png](nwbmatic-pynapple-allen-tutorial_files/nwbmatic-pynapple-allen-tutorial_62_0.png)
    


Awesome! Looks like some of our units show a great deal of spatial tuning.


