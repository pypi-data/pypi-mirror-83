from typing import List, Optional, Union, Dict, TypeVar

from .core import (
    Output,
    Task,
    InOut,
    DynamicTask,
    AbstractTask,
    Storage,
    NotFound,
    Workflow,
    _flatten,
)


T_io = TypeVar("T_io", bound=InOut)


def assign_storage_to_output(output: T_io, storage: Storage) -> T_io:
    if isinstance(output, Output):
        return output.assign_storage(storage)
    elif isinstance(output, dict):
        return {  # type: ignore
            key: assign_storage_to_output(value, storage)
            for key, value in output.items()
        }
    elif isinstance(output, (list, tuple)):
        # Case of namedtuple
        if hasattr(output, "_fields"):
            return output.__class__(  # type: ignore
                **{  # type: ignore
                    key: assign_storage_to_output(value, storage)
                    for key, value in zip(output._fields, output)  # type: ignore
                }
            )
        return output.__class__(  # type: ignore
            assign_storage_to_output(value, storage) for value in output  # type: ignore
        )
    else:
        assert output is None, f"output value ({output}) must to be Output object"
    return output


def flatten(inout: Optional[InOut]) -> List[Output]:
    """Make inout into list of outputs
    """
    return _flatten(inout)


def is_completed(task: AbstractTask, storage: Storage) -> bool:
    """Respond the completion status of the task.

    Notes:
        If there is no outputs given, then the task will
        always executed.
    """
    try:
        outputs = task.output()

        # Case if task is dynamic and output is not defined, then try to check all the generated task's complete status.
        if isinstance(task, DynamicTask) and outputs is None:
            inputs = assign_storage_to_output(task.input(), storage)

            tasks = task.generate(inputs, None)
            if not isinstance(tasks, (list, tuple)):
                assert isinstance(tasks, AbstractTask)
                tasks = [tasks]

            return all([is_completed(task, storage=storage) for task in tasks])

        if outputs is None:
            return False

        output_list: List[Output] = flatten(outputs)

        return all(
            [
                assign_storage_to_output(output, storage).exists()
                for output in output_list
            ]
        )
    except NotFound:
        return False


def run_task(task: AbstractTask, storage: Storage):

    input = assign_storage_to_output(task.input(), storage)

    output = assign_storage_to_output(task.output(), storage)

    return task.run(input, output)


def generate_task(task: DynamicTask, storage: Storage) -> Union[Task, List[Task]]:
    """Generate task from DynamicTask
    """

    input = assign_storage_to_output(task.input(), storage)

    output = assign_storage_to_output(task.output(), storage)

    return task.generate(input, output)


def remove_output(output: Output, storage: Storage):
    output = assign_storage_to_output(output, storage)
    return output.remove()


def load_output(output: Output, storage: Storage):
    output = assign_storage_to_output(output, storage)
    return output.load()


def exists_output(output: Output, storage: Storage) -> bool:
    output = assign_storage_to_output(output, storage)
    return output.exists()


def workflow_to_task_map(workflow: Workflow) -> Dict[str, dict]:
    """Transform workflow to task dictionary with task_id key.
    """

    task_map: Dict[str, dict] = {}

    tasks = {task.task_id: task for task in workflow.tasks.values()}

    while len(tasks) > 0:

        next_tasks: Dict[str, Task] = {}

        for task_id, task in tasks.items():

            if task_id in task_map:
                continue

            inputs = flatten(task.input())

            dependent_tasks = {inp.src_task.task_id: inp.src_task for inp in inputs}

            dependent_task_ids = list(dependent_tasks.keys())

            task_map[task_id] = {
                "task_id": task_id,
                "dependent_task_ids": dependent_task_ids,
                "task": task,
            }

            for dependent_task_id, task in dependent_tasks.items():
                next_tasks[dependent_task_id] = task

        tasks = next_tasks

    return task_map
