from KAI.policy.sequence_accumulate import  SeqAccumulator
from KAI.basic.basic_objects import BasJson, BasPoly
import os
from KAI.utils.proc_utils import isexists
import json
import cv2

class DotaMaker(SeqAccumulator, BasJson, BasPoly):
    def load_params(self, args):
        super().load_params(args=args)
        self.ann_dir = os.path.join(self.args.root_dir, self.args.ann_dir)
        assert isexists(self.ann_dir)

    def process(self, rgbd, filename='unnamed'):
        # read polygon from json
        filename, _ = os.path.splitext(filename)
        json_path = os.path.join(self.ann_dir, filename + '.json')
        ann_dict = self.read_json(json_path=json_path)

        classes = ann_dict['Classes']
        polygons = ann_dict['Polygons']

        if self.args.show_steps:
            out = self.draw_polys_from_json(json_path=json_path, im=rgbd.rgb)
            cv2.imshow('out', out)



        if self.args.show_steps:
            if cv2.waitKey()==27: exit()

if __name__=='__main__':
    DotaMaker(cfg_path='configs/dataset/make_grip_dota_db.cfg').run()






