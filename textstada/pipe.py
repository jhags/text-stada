
import inspect
import json

from tqdm import tqdm

import textstada


class Pipeline:
    def __init__(self, steps, text=None, verbose=False):
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

        if t is None:
            raise ValueError("Please add text to 'self.text_input' before running pipe.")

        for step in tqdm(self._steps, disable=not self._verbose):
            t = self._run_func(t, step)
        self.text_output = t


    def save_pipe(self, filepath):
        output = {}
        for i, f in enumerate(self._steps):
            sig = inspect.signature(f)

            kwargs = {}
            for p in sig.parameters.values():
                arg = p.name
                val = p.default
                if val is not p.empty:
                    kwargs[arg] = val

            output[i] = {
                "step": f.__name__,
                "kwargs": kwargs
            }

        return json.dump(output, open(filepath, 'w'))
