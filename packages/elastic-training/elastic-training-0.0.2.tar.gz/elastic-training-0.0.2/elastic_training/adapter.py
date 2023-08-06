import torch
import os
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class Adapter(object):
    def __init__(self):
        self.world_size = -1
        self.global_batch_size = -1
        self.batch_size = -1
        self.force_divisible = False
        self.gradient_accumulation_steps = -1
        self.real_global_batch_size = -1

        self.restore_idx = None
        self.first_restore = True

    def adapt_gradient_accumulation_step(self, global_batch_size, world_size, batch_size, force_divisible=False):
        gradient_accumulation_steps = int(round(global_batch_size // world_size // batch_size))
        if gradient_accumulation_steps < 1:
            raise ValueError("invalid gradient_accumulation_steps parameter: {}, should be >= 1".format(
                             gradient_accumulation_steps))

        real_global_batch_size = batch_size * world_size * gradient_accumulation_steps
        if force_divisible and real_global_batch_size != global_batch_size:
            raise ValueError("the global batch size cannot be divisible by given paramenters, world_size:", world_size)

        logger.info("complete adapting gradient_accumulation_step: real global batch size: {}, \
            gradient_accumulation_steps: {} \
            world_size: {}".format(
            real_global_batch_size,
            gradient_accumulation_steps,
            world_size))

        self.world_size = world_size
        self.global_batch_size = global_batch_size
        self.batch_size = batch_size
        self.force_divisible = force_divisible
        self.gradient_accumulation_steps = gradient_accumulation_steps
        self.real_global_batch_size = real_global_batch_size

        return real_global_batch_size, gradient_accumulation_steps

    def save_checkpoint(self, state, filename, global_step, restore_idx=None):
        idx = None
        if restore_idx is not None:
            idx = restore_idx * self.world_size
            state['restore_idx'] = idx
        file_name = filename + '_' + str(global_step) + '.pt'
        logger.info("start saving checkpoint to {}, for global step {}".format(file_name, global_step))
        save_temp_name = file_name + '.temp'
        torch.save(state, save_temp_name)
        os.rename(save_temp_name, file_name)
        logger.info("complete saving checkpoint. restore idx: {}".format(idx))
        return file_name

    def resume_from_checkpoint(self, ckpt_output_dir, map_location=None):
        latest_ckpt_names = [f for f in os.listdir(ckpt_output_dir) if f.endswith(".pt")]
        if len(latest_ckpt_names) == 0:
            logger.info("no latest checkpoint found from {}".format(ckpt_output_dir))
            return (None, None)

        resume_step = max([int(x.split('.pt')[-2].split('_')[-1].strip()) for x in latest_ckpt_names])
        name_prefix = latest_ckpt_names[0].split('_')[-2].strip()
        ckpt_name_to_load = os.path.join(ckpt_output_dir, name_prefix + "_" + str(resume_step) + ".pt")

        logger.info("start loading checkpoint from {}, resume from global step {}".format(ckpt_name_to_load, resume_step))
        checkpoint = torch.load(ckpt_name_to_load, map_location)
        logger.info("complete loading checkpoint.")

        if 'restore_idx' in checkpoint:
            self.restore_idx = checkpoint['restore_idx']

        return (checkpoint, resume_step)

    def resume_from_restore_batch_idx(self, cond, iter_idx):
        if not cond:
            return True

        if self.restore_idx is None:
            return True

        if iter_idx < self.restore_idx // self.world_size:
            return False

        if self.first_restore:
            logger.info("restore training from iter_idx: {}, restore_idx: {}, world_size: {}".format(
                iter_idx, self.restore_idx, self.world_size))
            self.first_restore = False
        return True