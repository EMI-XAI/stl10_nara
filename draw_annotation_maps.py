# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from tqdm.auto import tqdm

#---------------------------------------------------------------------
def make_argparser():
    parser = argparse.ArgumentParser(
        "Draw annotation maps from geometry information of attentional"
        " region that is output from our annotation tool.")

    parser.add_argument("--input_name", default="./stl10_nara.csv",
                        help="A list of Geometry of attentional regions."
                        " (default: ./stl10_nara.csv)")
    parser.add_argument("--output_dir", default="./maps",
                        help="Output directory. (default: ./maps)")
    parser.add_argument("--map_size", type=int, default=96,
                        help="Image size of result annotation maps. Usually,"
                        " this should be the same as the oribinal images."
                        " (default: 96)")
    parser.add_argument("--annotations", type=int, nargs="+", default=[1, 2, 3],
                        help="Annotation IDs to be used for map generation."
                        " (default: 1 2 3)")
    parser.add_argument("--fixed_radius", type=int, default=-1,
                        help="This option overwrites radius information"
                        " of attentional region. Negative number means"
                        " that annotated radii are used as is."
                        " (default: -1)")

    return parser

#---------------------------------------------------------------------
def get_image_info(df, index):
    img_type = df.loc[index, "Split"]
    img_id = int(df.loc[index, "Image"].split(".")[0])

    return img_type, img_id

def get_annotation_info(df, index):
    category = df.loc[index, "Category"]
    cent_x   = df.loc[index, "CenterX"]
    cent_y   = df.loc[index, "CenterY"]
    size_x   = df.loc[index, "RadiusX"]
    size_y   = df.loc[index, "RadiusY"]
    angle    = df.loc[index, "Angle"]

    return category, cent_x, cent_y, size_x, size_y, angle

def get_time_info(df, index):
    sec = df.loc[index, "WorkTime"]

    return sec,

#---------------------------------------------------------------------
def gen_blank_image(img_size, base_val=0):
    return Image.new("RGB", (img_size, img_size), (base_val,) * 3)

def draw_ellipse(draw, cent, radius, angle, fill):
    assert len(cent) == 2 and len(radius) == 2
    cos, sin = np.cos(angle), np.sin(angle)

    rads = np.arange(360) / 180 * np.pi
    xs = np.cos(rads) * radius[0]
    ys = np.sin(rads) * radius[1]

    coords = []
    for x, y in zip(xs, ys):
        rx = cos * x - sin * y + cent[0]
        ry = sin * x + cos * y + cent[1]
        coords.append((rx, ry))

    draw.polygon(coords, fill=fill)

def calc_mean_image(image_list):
    mean = np.stack([np.asarray(img) for img in image_list]).mean(axis=0)
    return Image.fromarray(mean.astype(np.uint8))

#---------------------------------------------------------------------
def main(args):
    df = pd.read_csv(args.input_name)

    # Read annotation information.
    anno_list = {}
    for index in range(len(df)):
        img_type, img_id = get_image_info(df, index)
        (category, cent_x, cent_y, size_x, size_y, angle) \
            = get_annotation_info(df, index)

        if args.fixed_radius > 0:
            # Force to use fixed-size circles.
            size_x = size_y = args.fixed_radius

        items = cent_x, cent_y, size_x, size_y, angle
        if (img_type, img_id) not in anno_list:
            anno_list[(img_type, img_id)] = [items]
        else:
            anno_list[(img_type, img_id)].append(items)

    for img_type, img_id in tqdm(anno_list):
        items_list = anno_list[(img_type, img_id)]

        # Draw annotation maps.
        maps = []
        for cent_x, cent_y, size_x, size_y, angle in items_list:
            map = gen_blank_image(args.map_size)
            draw = ImageDraw.Draw(map)
            draw_ellipse(draw, (cent_x, cent_y), (size_x, size_y), angle,
                         fill=(255, 255, 255))
            maps.append(map)

        # Combine maps.
        result_map = calc_mean_image([maps[i - 1] for i in args.annotations])

        # Save the combined map.
        map_fname = Path(args.output_dir) / img_type / f"{img_id:05d}.png"
        map_fname.parent.mkdir(parents=True, exist_ok=True)
        result_map.save(map_fname)

#---------------------------------------------------------------------
if __name__ == "__main__":
    parser = make_argparser()
    args = parser.parse_args()
    main(args)
