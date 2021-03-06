#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals, print_function
import argparse
from .planet import *
from . import bbox
from .bbox import load_feature_string, load_features_csv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('osmpath', help='Name or path to OSM planet file. Use planet_update if you do not have a copy locally.')
    parser.add_argument('--outpath', help='Extract output directory', default='.')
    parser.add_argument('--csv', help='Path to CSV file with bounding box definitions.')
    parser.add_argument('--geojson', help='Path to GeoJSON file: bbox for each feature is extracted.')
    parser.add_argument('--name', help='Name to give to extract file.')
    parser.add_argument('--bbox', help='Bounding box for extract file. Format for coordinates: left,bottom,right,top')
    parser.add_argument('--verbose', help="Verbose output", action='store_true')
    parser.add_argument('--toolchain', help='OSM toolchain', default='osmosis')
    parser.add_argument('--strategy', help='Osmium extract strategy: simple, complete_ways, or smart', default='complete_ways')
    parser.add_argument('--commands', help='Output a command list instead of performing action, e.g. for parallel usage', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        log.set_verbose()

    if args.toolchain == 'osmosis':
        p = PlanetExtractorOsmosis(args.osmpath)
    elif args.toolchain == 'osmctools':
        p = PlanetExtractorOsmconvert(args.osmpath)
    elif args.toolchain == 'osmium':
        p = PlanetExtractorOsmium(args.osmpath)
    else:
        parser.error('unknown toolchain: %s'%args.toolchain)

    bboxes = {}
    if args.csv:
        bboxes = bbox.load_features_csv(args.csv)        
    elif args.geojson:
        bboxes = bbox.load_features_geojson(args.geojson)
    elif (args.bbox and args.name):
        bboxes[args.name] = bbox.load_feature_string(args.bbox)
    else:
        parser.error('must specify --csv, --geojson, or --bbox and --name')

    if args.commands:
        commands = p.extract_commands(bboxes, outpath=args.outpath, strategy=args.strategy)
        for i in commands:
            print(" ".join(i))
    else:
        p.extract_bboxes(bboxes, outpath=args.outpath, strategy=args.strategy)

if __name__ == '__main__':
    main()
