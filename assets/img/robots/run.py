#!/usr/env python

# Generate a crapton of robots, every color for each of the bases!
import pandas
import os
import json
from glob import glob
from colorthief import ColorThief
# https://github.com/fengsp/color-thief-py

colors = pandas.read_csv('colors.csv',header=None)
colors.columns = ['identifier','color_name','code','R','G','B']
bases = glob('bases/*.png')
basepath = "assets/img/robots"

print('Found %s robot bases!' %len(bases))

# Generate a json file for the robots
robots = []

# We will keep a record of primary colors
lookup = dict()
groups = dict()

def get_primary_color(image):
    color_thief = ColorThief(image)
    return color_thief.get_color(quality=1)


count=1
for index,color in colors.iterrows():
    group = []
    for base in bases:
        robot = {'name': color.color_name,
                 'color': color.code,
                 'uri': color.identifier }

        if base not in lookup:
            lookup[base] = get_primary_color(base)
            groups[lookup[base]] = []
        primary_color = lookup[base]

        # Compute scale factors to get differences
        scaleR = color.R / primary_color[0]
        scaleG = color.G / primary_color[1]
        scaleB = color.B / primary_color[2]

        robot['base'] = "%s/%s" %(basepath,base)
        robot_file = "robot%s.png" %count
        robot['url'] = "%s/%s" %(basepath,robot_file)
        #os.system('/bin/bash makeColorVariants.sh %s %s %s %s %s' %(base, robot_file, scaleR, scaleG, scaleB))
        robots.append(robot)
        group.append(robot)
        count+=1
    groups[color.identifier] = group


# Finally, make a robot manifest
robot_manifest = 'robot-manifest.json'
with open(robot_manifest, 'w') as filey:
    filey.writelines(json.dumps(robots, indent=4, separators=(',',': ')))


manifest = []

# And robot data, we will write one file per color family
for colorid, robot_set in groups.items():
    robot_data = 'robots_%s.json' %(colorid)
    color_meta =  colors[colors.identifier==colorid].to_dict(orient='records')
    base ='https://vsoch.github.io/robots/'
    new_entry = {'robots': "%sassets/img/robots/%s" %(base,robot_data),
                 'color': color_meta,
                 'base': base }
    manifest.append(new_entry)
    with open(robot_data, 'w') as filey:
        filey.writelines(json.dumps(robot_set, indent=4, separators=(',',': ')))


# Write manifest to base
database = os.path.abspath('../../../')
robot_manifest = '%s/robot-manifest.json' %database
with open(robot_manifest, 'w') as filey:
    filey.writelines(json.dumps(manifest, indent=4, separators=(',',': ')))


# Colors will drive the site
database = os.path.abspath('../../../_data')
color_file = "%s/colors.csv" %database
colors.to_csv(color_file,index=False)
