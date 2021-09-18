import argparse
import os
import sys
from pathlib import Path
import tqdm
from app.domain.value_objects.endpoint_info import aggregate_by_entity
from app.domain.value_objects.setting import SettingParseError
from app.parser.parser import parse
from app.repository.translate import TranslationRepository
from app.utils.pyyaml_util import output_yaml
from app.utils.text_util import round_text
from app.writer.openapi_yaml.openapi_yaml_writer import OpenAPIYamlFormatWriter
from app.writer.openapi_yaml.openapi_setting import OpenAPIYamlSetting

parser = argparse.ArgumentParser()
parser.add_argument("--doc", required=True, help='Path of document described API in "Japanese natural language".')
parser.add_argument("--out", required=True, help="Result documents directory path.")
parser.add_argument("--setting", required=False,
                    default=os.path.dirname(os.path.abspath(__file__)) + "/sample_setting.json",
                    help="Setting file path.")
args = parser.parse_args()


def on_error(message: str):
    print(f"[Error] {message}", file=sys.stderr)
    exit(1)


# Load setting
setting = None
try:
    setting = OpenAPIYamlSetting.from_file(args.setting)
except FileNotFoundError:
    on_error(f"Setting file not found:  {args.setting}")
except SettingParseError as e:
    on_error(e.message)

TranslationRepository.inject_custom_translate_dict(setting.custom_translate_dict)

# Load natural language api lines
api_nl_text_ls = []
try:
    with open(args.doc, "r", encoding="utf-8") as file:
        api_nl_text_ls = list(map(lambda row: row.replace("\n", ""), file.readlines()))
except FileNotFoundError:
    on_error(f"Doc file not found:  {args.doc}")

# Setup output files/directories
root = Path("./docs/reference")
common_path = root.joinpath("common")
api_root_path = root.joinpath("paths")
common_path.mkdir(parents=True, exist_ok=True)
api_root_path.mkdir(parents=True, exist_ok=True)

entities, api_types = [], []

# Parse natural language api lines
pbar = tqdm.tqdm(api_nl_text_ls)
for text in pbar:
    pbar.set_description("[Parsing {:20s}]".format(round_text(text, 20)))
    entity, api_type = parse(text)
    entities.append(entity)
    api_types.append(api_type)
print("\n\nParsing finished🙌🙌🙌\n\n")

endpoints = aggregate_by_entity(api_nl_text_ls, entities, api_types)

# Automatically generate API documents in OpenAPI format
pbar = tqdm.tqdm(endpoints)
for endpoint in pbar:
    out_text = round_text(endpoint.to_inline_string(is_REST=setting.is_rest), 50)
    pbar.set_description("[Generating {:50s}]".format(out_text))
    f = OpenAPIYamlFormatWriter(endpoint, setting)
    f.parse()
    output_yaml(f.get_tree(), str(api_root_path.joinpath(f"{endpoint.entity.entity_nl_name}.yaml")))

setting.output_auth_model(str(common_path.joinpath("Authorization.yaml")))
setting.output_error_response_model(str(common_path.joinpath("ErrorResponse.yaml")))

print("\n\nGenerating finished🙌🙌🙌")
