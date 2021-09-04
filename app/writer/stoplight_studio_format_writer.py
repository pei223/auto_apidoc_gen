from typing import List, Tuple
from pathlib import Path
from ..domain.value_objects.api_kinds import ApiKind
from ..domain.value_objects.endpoint_info import EndpointInfo
from ..domain.value_objects.setting import Setting


def write_for_stoplight_studio_format(endpoint_info_ls: EndpointInfo, setting: Setting, output_dir: str):
    root_dir, paths_dir, common_dir = _setup_out_dirs(output_dir)



def _setup_out_dirs(out_dir: str) -> Tuple[Path, Path, Path]:
    output_dir = Path(out_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    root_dir = output_dir.joinpath("reference")
    paths_dir = output_dir.joinpath("paths")
    common_dir = output_dir.joinpath("common")
    if not root_dir.exists():
        root_dir.mkdir()
    if not paths_dir.exists():
        paths_dir.mkdir()
    if not common_dir.exists():
        common_dir.mkdir()
    return root_dir, paths_dir, common_dir
