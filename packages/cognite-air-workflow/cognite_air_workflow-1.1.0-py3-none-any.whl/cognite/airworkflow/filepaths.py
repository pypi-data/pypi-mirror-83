from pathlib import Path
from typing import List
import cognite.airworkflow.constants as const
from cognite.airworkflow.master_config import get_master_config
from cognite.airworkflow.util.functions import get_relative_function_path


def get_function_paths(paths: List[Path]) -> List[str]:
    return sorted(map(get_relative_function_path, paths))


def getpathstring(function_names: List[str], work_flows: List[Path]) -> None:
    start = '{"function":'
    escape_string = '"'
    escaped_string = list(map(lambda v: escape_string + v + escape_string, function_names))
    function_names_str = f"[{', '.join(escaped_string)}]"
    final_string = start + function_names_str + "}"
    print(final_string)


if __name__ == "__main__":
    master_config, project_to_config = get_master_config()
    getpathstring(get_function_paths(list(master_config.keys())), const.WORK_FLOWS)
