#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 13:07:38 2020
@author: Ajit Johnson Nirmal
visualization option for understanding average distance between phenotypes of interest.
Pre-run `sm.tl.spatial_distance` before running this function.
"""

# library
import pandas as pd
import matplotlib
import seaborn as sns; sns.set(color_codes=True)
sns.set_style("white")

# Heatmap of mean or median distance
# if single cell-type given, distance across all images
# if two cell-type or more given distance across single image

def spatial_distance (adata, spatial_distance_label='spatial_distance',phenotype='phenotype',imageid='imageid',
                      method='heatmap',heatmap_summarize=True,heatmap_nonsig_color='grey',heatmap_cmap='vlag_r',
                      heatmap_row_cluster=False,heatmap_col_cluster=False,heatmap_standard_scale=0,
                      distance_from=None,distance_to=None,
                      **kwargs):
    
    
    # set color for heatmap
    cmap_updated = matplotlib.cm.get_cmap(heatmap_cmap)
    cmap_updated.set_bad(color=heatmap_nonsig_color)
    
    
    # Copy the spatial_distance results from anndata object
    try:
        diatance_map = adata.uns[spatial_distance_label].copy()
    except KeyError:
        raise ValueError('spatial_distance not found- Please run sm.tl.spatial_distance first')
        
    # Method
    if method=='heatmap':
        if heatmap_summarize is True:
            # create the necessary data
            data = pd.DataFrame({'phenotype': adata.obs[phenotype]})
            data = pd.merge(data, diatance_map, how='outer',left_index=True, right_index=True) # merge with the distance map
            k = data.groupby(['phenotype']).mean() # collapse the whole dataset into mean expression
            k = k[k.index]
        else:
            # create new naming scheme for the phenotypes
            non_summary = pd.DataFrame({'imageid': adata.obs[imageid], 'phenotype': adata.obs[phenotype]})
            non_summary['imageid'] = non_summary['imageid'].astype(str) # convert the column to string
            non_summary['phenotype'] = non_summary['phenotype'].astype(str) # convert the column to string
            non_summary['image_phenotype'] = non_summary['imageid'].str.cat(non_summary['phenotype'],sep="_")
            # Merge distance map with phenotype
            data = pd.DataFrame(non_summary[['image_phenotype']])
            data = pd.merge(data, diatance_map, how='outer',left_index=True, right_index=True)
            k = data.groupby(['image_phenotype']).mean()
            k = k.sort_index(axis=1)
        # Generate the heatmap
        mask = k.isnull() # identify the NAN's for masking 
        k = k.fillna(0) # replace nan's with 0 so that clustering will work
        # Heatmap
        sns.clustermap(k, cmap=heatmap_cmap, row_cluster=heatmap_row_cluster, 
                       col_cluster=heatmap_col_cluster, mask=mask, 
                       standard_scale=heatmap_standard_scale, **kwargs)
    
    if method=='distribution_plot':
        # start
                    
        data = pd.DataFrame({'phenotype': adata.obs[phenotype]})
        data = pd.merge(data, diatance_map, how='outer',left_index=True, right_index=True) # merge with the distance map
        
        # condition-1
        if distance_from and distance_to is None:
            raise ValueError('Please include distance_from and/or distance_from parameters')
        
        # condition-2
        if distance_from is not None and distance_to is None:
            data = data[data['phenotype'] == distance_from]
            data = data.drop(['phenotype'], axis=1) # drop the phenotype column before stacking
            d = data.stack().reset_index() # collapse everything to one column
            d.columns = ['cellid', 'group', 'value']
            
            # Plot
            sns.violinplot(x="value", y="group", data=d, **kwargs)
        
        # condition-3
        if distance_from is not None and distance_to is not None:
            non_summary = pd.DataFrame({'imageid': adata.obs[imageid], 'phenotype': adata.obs[phenotype]})
            diatance_map = diatance_map[distance_to]
            data = pd.merge(non_summary, diatance_map, how='outer',left_index=True, right_index=True)
            # subset data
            d = data[data['phenotype'] == distance_from]
            d.columns = ['cellid', 'group', 'value']
            
            # Plot
            sns.violinplot(x="value", y="group", data=d, **kwargs)
            
            sns.violinplot(x="value", y="cellid", data=d)



        



