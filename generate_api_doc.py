import argparse
import os
import sys
from pathlib import Path
import tqdm

from app.domain.errors import ApiKindNotMatched
from app.domain.value_objects.setting import SettingParseError
from app.parser.parse_error import ActionNotFound, EntityNotFound
from app.parser.parser import parse_sentences
from app.repository.translate import TranslationRepository
from app.utils.pyyaml_util import output_yaml
from app.utils.text_util import round_text
from app.writer.openapi_yaml.openapi_yaml_writer import OpenAPIYamlFormatWriter
from app.writer.openapi_yaml.openapi_setting import OpenAPIYamlSetting

parser = argparse.ArgumentParser()
parser.add_argument("--doc", type=str, required=True,
                    help='Path of document described API in "Japanese natural language".')
parser.add_argument("--out", type=str, required=True, help="Result documents directory path.")
parser.add_argument("--setting", type=str, required=False,
                    default=os.path.dirname(os.path.abspath(__file__)) + "/sample_setting.json",
                    help="Setting file path.")
parser.add_argument("--debug", action='store_true', required=False, default=False, help="debug mode")

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
api_sentences = []
try:
    with open(args.doc, "r", encoding="utf-8") as file:
        api_sentences = list(map(lambda row: row.replace("\n", ""), file.readlines()))
except FileNotFoundError:
    on_error(f"Doc file not found:  {args.doc}")

# Setup output files/directories
root = Path("./docs/reference")
common_path = root.joinpath("common")
api_root_path = root.joinpath("paths")
common_path.mkdir(parents=True, exist_ok=True)
api_root_path.mkdir(parents=True, exist_ok=True)

# Parse natural language api lines
try:
    entities = parse_sentences(api_sentences, show_progress=True, verbose=args.debug)
except ActionNotFound as e:
    on_error(e.message)
except EntityNotFound as e:
    on_error(e.message)
except ApiKindNotMatched as e:
    on_error(e.message)

print("\n\nParsing finished🙌🙌🙌\n\n")

# Automatically generate API documents in OpenAPI format
pbar = tqdm.tqdm(entities)
for entity in pbar:
    out_text = round_text(entity.to_inline_string(is_rest=setting.is_rest), 50)
    pbar.set_description("[Generating {:50s}]".format(out_text))
    f = OpenAPIYamlFormatWriter(entity, setting)
    f.parse()
    output_yaml(f.get_tree(), str(api_root_path.joinpath(f"{entity.entity_ja_name}.yaml")))

setting.output_auth_model(str(common_path.joinpath("Authorization.yaml")))
setting.output_error_response_model(str(common_path.joinpath("ErrorResponse.yaml")))

print("\n\nGenerating finished🙌🙌🙌")
