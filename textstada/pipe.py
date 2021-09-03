
import textstada
from tqdm import tqdm

class Pipeline:
    def __init__(self, text, steps, verbose=False):
        self.text_input = text
        self.steps = steps
        self._steps = self._evaluate_steps()
        self._verbose = verbose
        self.text_output = None


    def _evaluate_steps(self):
        eval_steps = []
        for step in self.steps:
            try:
                eval_steps.append(eval(f"textstada.{step}"))
            except:
                raise TypeError(f"'{step}' not recognised in function list.")
        return eval_steps


    def _run_func(self, t, func, *args, **kwargs):
        return func(t, *args, **kwargs)


    def run(self):
        t = self.text_input
        for step in tqdm(self._steps, disable=not self._verbose):
            t = self._run_func(t, step)
        self.text_output = t
