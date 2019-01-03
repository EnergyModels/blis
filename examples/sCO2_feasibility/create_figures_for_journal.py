#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""
BLIS - Balancing Load of Intermittent Solar:
A characteristic-based transient power plant model

Copyright (C) 2018. University of Virginia Licensing & Ventures Group (UVA LVG). All Rights Reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Note: This code uses the results generated from run_monte_carlo1,run_monte_carlo2,run_monte_carlo3 and run_single_case_sCO2

# General imports
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np

# Set Color Palette
colors = sns.color_palette("colorblind")
# Set resolution for saving figures
DPI = 1000

#%%=============================================================================#
# Figure 6 - LCOE
results_filename = "Results_MonteCarlo1.csv"
savename = "Fig6_LCOE.png"
#=============================================================================#
# Import results
df = pd.read_csv(results_filename)

# Prepare results for plotting
    # Create series for plantType
df = df.assign(plantType=df.sheetname)
df.loc[(df.plantType == 'OCGT_Batt'),'plantType']='OCGT'
df.loc[(df.plantType == 'CCGT_Batt'),'plantType']='CCGT'
df.loc[(df.plantType == 'sCO2_Batt'),'plantType']='sCO2'
    # Create series for pct_solar
df = df.assign(pct_solar=df.solarCapacity_MW)
df.loc[(df.pct_solar == 0.513),'pct_solar']=1.0
df.loc[(df.pct_solar == 32.3),'pct_solar']=63.0

# Create Plots
f,a = plt.subplots(2,2,sharex=True, sharey=True )
a = a.ravel()

# Collect statistics
labels = ['plantType','battSize','pct_solar','min','avg','max']
stats = []

for idx,ax in enumerate(a):
        
    # Variable Plotted
    y_var = 'LCOE'
    y_label = 'LCOE ($/kWh)'
    y_convert  = 1.0        

    # Configurations
    if idx == 0 or idx == 2:
        battSize  = 0.0
    elif idx == 1 or idx == 3:    
        battSize  =30.0
    
    if idx == 0 or idx == 1:
        pct_solar = 1.0
    elif idx == 2 or idx == 3:    
        pct_solar = 63.0
                
    # Organize row/columns based on pct_solar and battSize
    plantTypes = ['OCGT','CCGT','sCO2']

    # Plot
    for plantType in plantTypes:
        # Set Color and label
        if plantType =='sCO2':
            color =     colors[0]
            label = 'sCO$_2$'
        elif plantType =='OCGT':
            color = colors[1]
            label = 'OCGT'
        elif plantType =='CCGT':
            color = colors[2]
            label = 'CCGT'
        # Plot
        df2 = df[(df.plantType == plantType) &(df.pct_solar == pct_solar) & (df.battSize == battSize)]
        
        bin_size = 0.001; min_edge = 0.06; max_edge = 0.14
#        bin_size = 0.001; min_edge = 0.02; max_edge = 0.14
        N = int((max_edge-min_edge)/bin_size); Nplus1 = N + 1
        bin_list = np.linspace(min_edge, max_edge, Nplus1)
        ax.hist(df2.loc[:,y_var]*y_convert,label=label,color=color,bins=bin_list,histtype='step',fill=False)#,facecolor=False)
        
        # Collect statistics
        stats.append([plantType,battSize,pct_solar,df2.loc[:,y_var].min(),df2.loc[:,y_var].mean(),df2.loc[:,y_var].max()])
        
    # Axes Labels
    # X-axis Labels (Only bottom)
    if idx ==2 or idx==3:
        ax.set_xlabel(y_label)
    else:
        ax.get_xaxis().set_visible(False)

    # Set Y-limits
    ax.set_ylim(top=30)

    # Legend
#    ax.legend()
    
    # Caption labels
    caption_labels = ['A','B','C','D','E','F']
    plt.text(0.1, 0.9, caption_labels[idx], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,fontsize='medium',fontweight='bold')
        
# Adjust layout
plt.tight_layout()
    
a[2].legend(bbox_to_anchor=(1.75, -0.3),ncol=3)
# Adjust layout
plt.tight_layout()

# Save Figure
plt.savefig(savename,dpi=DPI,bbox_inches="tight")
plt.close()

# Collect statistics
df_stats = pd.DataFrame(stats)

#%%=============================================================================#
# Figure 7 - sCO2 Sensitivity
results_filename = "Results_MonteCarlo1.csv"
savename = "Fig7_sCO2_Sensitivity.png"
#=============================================================================#
# Import results
df = pd.read_csv(results_filename)

# Prepare results for plotting
    # Create series for plantType
df = df.assign(plantType=df.sheetname)
df.loc[(df.plantType == 'OCGT_Batt'),'plantType']='OCGT'
df.loc[(df.plantType == 'CCGT_Batt'),'plantType']='CCGT'
df.loc[(df.plantType == 'sCO2_Batt'),'plantType']='sCO2'
    # Create series for pct_solar
df = df.assign(pct_solar=df.solarCapacity_MW)
df.loc[(df.pct_solar == 0.513),'pct_solar']=1.0
df.loc[(df.pct_solar == 32.3),'pct_solar']=63.0

# Create Plots
f,a = plt.subplots(2,3)#,sharex=True, sharey=True
a = a.ravel()

for idx,ax in enumerate(a):
        
    # Y-Variable (Vary by row)
    if idx == 0 or idx == 1 or idx == 2:
        y_var = 'fuelCost_dollars'
        y_label = 'Fuel Cost (M$)'
        y_convert  = [1./1E6]
        ylims = [10,18]
    elif idx == 3 or idx == 4 or idx == 5:    
        y_var = 'solarCurtail_pct'
        y_label = 'Curtailment (%)'
        y_convert  = [1.0]
        ylims = [0,60]
    
    # X-Variable (vary by column)
    if idx == 0 or idx == 3:
        # X variables
        x_var = 'maxEfficiency'
        x_label = 'Max Efficiency (%)'
        x_convert = [1.0]
        xlims = [40,60]
        xticks       =  [] # Leave empty if unused
        xtick_labels =  []
        
    elif idx == 1 or idx == 4:    
        x_var = 'rampRate'
        x_label = 'Ramp Rate (%/min)'
        x_convert = [1.0]
        xlims = [30,110]
        xticks       =  [30,75,110]
        xtick_labels =  ['30','75','110']
    elif idx == 2 or idx == 5:    
        x_var = 'minRange'
        x_label = 'Min. Load (%)'
        x_convert = [1.0]
        xlims = [15,60]
        xticks       =  (30,75,110)
        xtick_labels =  ('30','75','110')
        
    #  Configurations
    plantTypes = ['sCO2','sCO2','sCO2']
    battSizes   = [0.0,0.0,30.0]
    pct_solars  = [1.0,63.0,63.0]
    # Corresponding labels, colors, and marker size
    labels     = ['1% Solar w/o Batt','63% Solar w/o Batt','63% Solar 30.0 MWh Batt']
    dot_colors = [colors[0],colors[2],colors[1]]
    markers    = ['o','x','+']
    
    # Plot by configuration
    for plantType,battSize,pct_solar,label,dot_color,marker in zip(plantTypes,battSizes,pct_solars,labels,dot_colors,markers):

        # Select entries of interest
        df2 = df[(df.plantType == plantType) &(df.pct_solar == pct_solar) & (df.battSize == battSize)]
        
        # Plot
        x = df2.loc[:,x_var]*x_convert
        y = df2.loc[:,y_var]*y_convert
        ax.scatter(x.values,y.values,c=dot_color,marker=marker,label=label)
    
    # Set X and Y Limits
    ax.set_xlim(left=xlims[0],right=xlims[1])
    ax.set_ylim(bottom=ylims[0],top=ylims[1])
    
    # X-axis Labels (Only bottom)
    if idx ==3 or idx==4 or idx==5:
        ax.set_xlabel(x_label)
    else:
        ax.get_xaxis().set_visible(False)
    
    #Y-axis labels (Only left side)
    if idx == 0 or idx==3:  
        ax.set_ylabel(y_label)
#    else:
#        ax.get_yaxis().set_visible(False)

    # Legend (only for middle bottom)
    if idx==4:
        ax.legend(bbox_to_anchor=(2.6, -0.4),ncol=3)
                
    # Caption labels
    caption_labels = ['A','B','C','D','E','F']
    plt.text(0.1, 0.9, caption_labels[idx], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,fontsize='medium',fontweight='bold')
        
# Adjust layout
plt.tight_layout()

# Save Figure
plt.savefig(savename,dpi=DPI,bbox_inches="tight")
plt.close()
#%%=============================================================================#
# Figure 8 - Ramp Rate Sensitivity
results_filename1 = "Results_MonteCarlo2.csv"  # 63% solar
results_filename2 = "Results_MonteCarlo3.csv"  # 1% solar
savename = "Fig8_RampRate_Deficit.png"
#=============================================================================#
# Import results
df1 = pd.read_csv(results_filename1)
df2 = pd.read_csv(results_filename2)
df = pd.concat([df1,df2],axis=0)

# Prepare results for plotting
    # Create series for pct_solar
df = df.assign(pct_solar=df.solarCapacity_MW)
df.loc[(df.pct_solar == 0.513),'pct_solar']=1.0
df.loc[(df.pct_solar == 32.3),'pct_solar']=63.0

# Create Plots
ax = plt.subplot(111)

# Y-Variable (Vary by row)
y_var = 'deficit_min'
y_label = 'Peak Deficit (MW)'
y_convert  = [-1.]
ylims = [0,14]
    
# X-Variable (vary by column)
x_var = 'rampRate'
x_label = 'Ramp Rate (%/min)'
x_convert = [1.0]
xlims = [0,30]

#  Configurations
plantTypes = ['sCO2_Ramp0','sCO2_Ramp0','sCO2_Ramp1']
battSizes   = [0.0,0.0,30.0]
pct_solars  = [1.0,63.0,63.0]
# Corresponding labels, colors, and marker size
labels     = ['1% Solar w/o Batt','63% Solar w/o Batt','63% Solar 30.0 MWh Batt']
dot_colors = [colors[0],colors[2],colors[1]]
markers    = ['o','x','+']

# Plot by configuration
for plantType,battSize,pct_solar,label,dot_color,marker in zip(plantTypes,battSizes,pct_solars,labels,dot_colors,markers):

    # Select entries of interest
    df2 = df[(df.sheetname == plantType) &(df.pct_solar == pct_solar) & (df.battSize == battSize)]
    
    # Plot
    x = df2.loc[:,x_var]*x_convert
    y = df2.loc[:,y_var]*y_convert
    ax.scatter(x.values,y.values,c=dot_color,marker=marker,label=label)

# Set X and Y Limits
ax.set_xlim(left=xlims[0],right=xlims[1])
ax.set_ylim(bottom=ylims[0],top=ylims[1])

# X-axis Labels
ax.set_xlabel(x_label)

#Y-axis labels
ax.set_ylabel(y_label)

# Legend (only for middle bottom)
ax.legend(ncol=1)
        
# Adjust layout
plt.tight_layout()

# Save Figure
plt.savefig(savename,dpi=DPI,bbox_inches="tight")
plt.close()

#%%=============================================================================#
# Figure 9 - Control Scheme
results_filename = "Results_SampleDay_Oct30th_sCO2.csv"
savename = "Fig9_ControlScheme.png"
#=============================================================================#
# Customize Time Shown
file_t_start  = -4.0
t_start = 7.0
t_end   = 22.0

# Import results
df = pd.read_csv(results_filename)

for n in range(3):
#   if n<3 :
#      plt.tick_params(labelbottom='off')
    x = df.loc[:,'t']/60.0 - df.loc[0,'t']/60.0 + file_t_start
    if n ==0:
#       x = df.loc[:,'t']
       y1 = df.loc[:,'PowerOutput']
       y2 = df.loc[:,'solar']
       y3 = df.loc[:,'battDischargeRate']
       
       y = np.vstack((y1,y2,y3))
       pal = [colors[2],colors[4],colors[0]]
       labels = ['Natural Gas','Solar PV','Battery']
       y_label = "Generation\n(MW)"
       # Don't label bottom
       labelbottom = 'off'
       
    elif n==1:       
       y1 = df.loc[:,'demand']
       y2 = df.loc[:,'solar']-df.loc[:,'solarUsed']
       y3 = df.loc[:,'battChargeRate']
       
       y = np.vstack((y1,y2,y3))
       pal = [colors[1],colors[4],colors[0]]
       
#       y = np.vstack((y1,y3))
#       pal = [colors[1],colors[0]]
       
       labels = ['Demand','Solar Curtailment','Battery']
#       labels = ['Demand','Battery']
       
       y_label = 'Use\n(MW)'
       # Don't label bottom
       labelbottom = 'off'
#       plt.tick_params(labelbottom='off')
       
    elif n==2:       
       y = df.loc[:,'battCharge']/60.0
       labels = ['Battery']
       pal = [colors[0]]
       y_label = 'Storage\n(MWh)'
       labelbottom = 'on'

    ax = plt.subplot(3 ,1, n + 1)
   
    if n==0 or n==1:
       ax.stackplot(x, y, labels=labels,colors=pal)
       ax.set_ylim(bottom=10.0,top = 50.0)
    else:
       ax.plot(x,y,label=labels[0])
       ax.set_ylim(bottom=0.0,top = 30.0)
#   plt.title(v)
    ax.set_ylabel(y_label)
    plt.xlim(left=t_start,right=t_end)
   
   # Legend
    ax.legend(loc='center left',bbox_to_anchor=(1.0, 0.5),fancybox=True)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height, box.width*0.8, box.height])
    ax.legend(loc='center left',bbox_to_anchor=(1.0, 0.5),fancybox=True)
       
    plt.tick_params(labelbottom=labelbottom)
       
    # Set aspect ratio https://jdhao.github.io/2017/06/03/change-aspect-ratio-in-mpl/
    ratio = 0.25
    xleft, xright = ax.get_xlim() # the abs method is used to make sure that all numbers are positive
    ybottom, ytop = ax.get_ylim() # because x and y axis of an axes maybe inversed.  
    ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
       
       # Caption labels
    caption_labels = ['A','B','C','D','E','F']
    plt.text(0.05, 0.85, caption_labels[n], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,fontsize='medium',fontweight='bold')

# Adjust layout
plt.tight_layout()

# Save Figure
plt.savefig(savename,dpi=DPI,bbox_inches="tight")
plt.close()

#%%=============================================================================#
# Figure 10 - Curtailment
results_filename = "Results_MonteCarlo1.csv"
savename = "Fig10_Curtailment.png"
#=============================================================================#
# Import results
df = pd.read_csv(results_filename)

# Prepare results for plotting
    # Create series for plantType
df = df.assign(plantType=df.sheetname)
df.loc[(df.plantType == 'OCGT_Batt'),'plantType']='OCGT'
df.loc[(df.plantType == 'CCGT_Batt'),'plantType']='CCGT'
df.loc[(df.plantType == 'sCO2_Batt'),'plantType']='sCO2'
    # Create series for pct_solar
df = df.assign(pct_solar=df.solarCapacity_MW)
df.loc[(df.pct_solar == 0.513),'pct_solar']=1.0
df.loc[(df.pct_solar == 32.3),'pct_solar']=63.0

# Create Plots
# https://stackoverflow.com/questions/20174468/how-to-create-subplots-of-pictures-made-with-the-hist-function-in-matplotlib-p
f,a = plt.subplots(2,2,sharex=True, sharey=True)#, figsize = (6,3) )
a = a.ravel()

for idx,ax in enumerate(a):
        
    # Variable Plotted
    if idx == 0 or idx == 2:
        y_var = 'solarCurtail_pct'
        y_label = 'Solar Curtailment (%)'
        y_convert  = 1.0        
    elif idx == 1 or idx == 3:    
        y_var = 'loadShed_pct_energy'
        y_label = 'Natural Gas Load Shed (%)'
        y_convert  = 1.

    # Configurations
    if idx == 0 or idx == 1:
        pct_solar = 63.0
        battSize = 0.0       
    elif idx == 2 or idx == 3:    
        pct_solar = 63.0
        battSize = 30.0   
    
    # Organize row/columns based on pct_solar and battSize
    plantTypes = ['sCO2','OCGT','CCGT']

    # Plot
    for plantType in plantTypes:
        # Set Color
        
        if plantType =='sCO2':
            color =     colors[0]
            label = 'sCO$_2$'
        elif plantType =='OCGT':
            color = colors[1]
            label = 'OCGT'
        elif plantType =='CCGT':
            color = colors[2]
            label = 'CCGT'
        # Plot
        
        # Access Data
        df2 = df[(df.plantType == plantType) &(df.pct_solar == pct_solar) & (df.battSize == battSize)]
        
        # Set Bin Size
        bin_size =2.0; min_edge = 0.0; max_edge = 60.0
        N = int((max_edge-min_edge)/bin_size); Nplus1 = N + 1
        bin_list = np.linspace(min_edge, max_edge, Nplus1)
        
        # Plot
        ax.hist(df2.loc[:,y_var]*y_convert,label=label,color=color,bins=bin_list,histtype='step',fill=False)#,facecolor=False)
         
    # X-axis Labels (Only bottom)
    if idx ==2 or idx==3:
        ax.set_xlabel(y_label)
    else:
        ax.get_xaxis().set_visible(False)
       
    # Caption labels
    caption_labels = ['A','B','C','D','E','F']
    plt.text(0.12, 0.9, caption_labels[idx], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,fontsize='medium',fontweight='bold')
    
a[2].legend(bbox_to_anchor=(1.7, -0.2),ncol=3)

# Adjust layout
plt.tight_layout()

# Save Figure
plt.savefig(savename,dpi=DPI,bbox_inches="tight")
plt.close()

#%%=============================================================================#
# Figure 11 - Impact of battery size
results_filename = "Results_MonteCarlo2.csv"
savename = "Fig11_BatterySize.png"
#=============================================================================#
# Import results
df = pd.read_csv(results_filename)

# Prepare results for plotting
    # Create series for plantType
df = df.assign(plantType=df.sheetname)
df.loc[(df.plantType == 'OCGT_Batt'),'plantType']='OCGT'
df.loc[(df.plantType == 'CCGT_Batt'),'plantType']='CCGT'
df.loc[(df.plantType == 'sCO2_Batt'),'plantType']='sCO2'
    # Create series for pct_solar
df = df.assign(pct_solar=df.solarCapacity_MW)
df.loc[(df.pct_solar == 0.513),'pct_solar']=1.0
df.loc[(df.pct_solar == 32.3),'pct_solar']=63.0

# Create Plots
f,a = plt.subplots(3,1,sharex=True,figsize=(5,5))
a = a.ravel()

for idx,ax in enumerate(a):
        
      
    # Y-Variable (Vary by row)
    if idx == 0:
        y_var = 'solarCurtail_pct'
        y_label = 'Curtailment (%)'
        y_convert  = [1.0]
        ylims = [0,40]
    elif idx == 1:
        y_var = 'fuelCost_dollars'
        y_label = 'Fuel Cost (M$)'
        y_convert  = [1./1.E6]
        ylims = [11,17] 
    elif idx == 2:
        y_var = 'LCOE'
        y_label = 'LCOE ($/kWh)'
        y_convert  = [1.]
        ylims = [0.05,0.15] 
    
    # X-Variable (vary by column)
    x_var = 'battSize'
    x_label = 'Batt Size (MWh)'
    x_convert = [1.0]
    xlims = [0,100]
#    xtick       =  [] # Leave empty if unused
#    xtick_label =  []
        
        
    #  Configurations
    plantTypes  = ['sCO2_Batt30','sCO2_Batt40','sCO2_Batt50']
    pct_solars  = [63.0,63.0,63.0]
    minLoads    = [30.,40.,50.]
    # Corresponding labels, colors, and marker size
    labels     = ['30% Min Load','40% Min Load','50% Min Load']
    dot_colors = [colors[0],colors[2],colors[1]]
    markers    = ['o','x','+']
    
    # Plot by configuration
    for plantType,pct_solar,label,dot_color,marker,minLoad in zip(plantTypes,pct_solars,labels,dot_colors,markers,minLoads):

        # Select entries of interest
        df2 = df[(df.plantType == plantType) &(df.pct_solar == pct_solar) &(df.minRange == minLoad)]
        
        # Plot
        x = df2.loc[:,x_var]*x_convert
        y = df2.loc[:,y_var]*y_convert
        ax.scatter(x.values,y.values,c=dot_color,marker=marker,label=label)
    
    # Set Aspect Ratio
#    AR = 3
#    ax.set_aspect(AR)
    
    # Set X and Y Limits
    ax.set_xlim(left=xlims[0],right=xlims[1])
    ax.set_ylim(bottom=ylims[0],top=ylims[1])
    
    # X-axis Labels (Only bottom)
    if idx ==2:
        ax.set_xlabel(x_label)
        ax.legend(ncol=3,bbox_to_anchor=(1.1, -0.5))
    else:
        ax.get_xaxis().set_visible(False)
    
    #Y-axis labels (Only left side)
#    if idx == 0 or idx==3:  
    ax.set_ylabel(y_label)
#    else:
#        ax.get_yaxis().set_visible(False)

    # Legend (only for middle bottom)
#    if idx==2:
    
#        print "success"
        
    # Set X-Tick labels
#    if len(xticks) >2:
#        ax.set_xticks = xticks
#        ax.set_xticklabels = xtick_labels
#        print "success"
        
    
    # Caption labels
    caption_labels = ['A','B','C','D','E','F']
    plt.text(0.1, 0.9, caption_labels[idx], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,fontsize='medium',fontweight='bold')

# Adjust layout
# plt.tight_layout()

# Save Figure
plt.savefig(savename,dpi=DPI,bbox_inches="tight")
plt.close()