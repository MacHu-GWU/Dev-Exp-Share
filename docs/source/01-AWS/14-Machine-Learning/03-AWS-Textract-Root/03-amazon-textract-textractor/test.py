import os
import json
from pathlib_mate import Path
from s3pathlib import S3Path, context

from boto_session_manager import BotoSesManager
from textractor import Textractor
from textractor.data.constants import TextractFeatures
from textractgeofinder.ocrdb import AreaSelection
from textractgeofinder.tgeofinder import (
    KeyValue,
    TGeoFinder,
    AreaSelection,
    SelectionElement,
)
from textractprettyprinter.t_pretty_print import get_forms_string
from textractcaller import call_textract
from textractcaller.t_call import Textract_Features
import trp.trp2 as t2
from textractcaller import Textract_Call_Mode


aws_profile = "aws_data_lab_sanhe_us_east_1"

bsm = BotoSesManager(profile_name=aws_profile)
extractor = Textractor(profile_name=aws_profile)

context.attach_boto_session(bsm.boto_ses)

# --- Local
dir_here = Path(os.getcwd()).absolute()

path_cms1500_pdf = dir_here / "cms1500-carrie-rodgers.pdf"
path_cms1500_png = dir_here / "page-1.ppm"

# --- S3
s3dir_root = S3Path(
    "aws-data-lab-sanhe-for-everything", "poc", "2022-12-04-textractor"
).to_dir()
s3dir_input = s3dir_root.joinpath("input").to_dir()
s3dir_output = s3dir_root.joinpath("output").to_dir()
s3path_cms1500_pdf = s3dir_input / path_cms1500_pdf.basename
s3path_cms1500_png = s3dir_input / path_cms1500_png.basename

# --- Upload
print(f"preview: {s3dir_root.console_url}")

# s3path_cms1500_pdf.upload_file(path_cms1500_pdf.abspath, overwrite=True)
# s3path_cms1500_png.upload_file(path_cms1500_png.abspath, overwrite=True)

def test1():
    analyzed_document = extractor.analyze_document(
        file_source=s3path_cms1500_png.uri,
        features=[
            TextractFeatures.FORMS,
            TextractFeatures.TABLES,
        ],
    )
    key_value_I = analyzed_document.get(key="I")[0]
    print(key_value_I)
    Path(dir_here, "test_1.json").write_text(json.dumps(analyzed_document.response, indent=4))


# test1()

def test2():
    js: dict = call_textract(
        input_document=s3path_cms1500_png.uri,
        features=[
            Textract_Features.FORMS,
            Textract_Features.TABLES,
        ],
        call_mode=Textract_Call_Mode.FORCE_SYNC,
    )
    document: t2.TDocument = t2.TDocumentSchema().load(js)
    doc_width = 2480
    doc_height = 3509
    geofinder_doc = TGeoFinder(js, doc_height=doc_height, doc_width=doc_width)
    # key_21_phrase = geofinder_doc.find_phrase_on_page("DIAGNOSIS OR NATURE OF ILLNESS OR INJURY")[0]
    # key_diagnosis_pointer = geofinder_doc.find_phrase_on_page("DIAGNOSIS POINTER")[0]
    # top_left = t2.TPoint(x=50, y=key_21_phrase.ymin - 50)
    # lower_right = t2.TPoint(x=key_diagnosis_pointer.xmax + 50, y=key_diagnosis_pointer.ymin + 100)

    a_to_l_fields = geofinder_doc.get_form_fields_in_area(
        area_selection=AreaSelection(
            top_left=t2.TPoint(x=0, y=0),
            lower_right=t2.TPoint(x=doc_width, y=doc_height),
            page_number=1,
        )
    )
    print(len(a_to_l_fields))
    for field in sorted(
        a_to_l_fields,
        key=lambda x: x.key.text,
    ):
        # print(field.key.text, field.value.text)
        # print(field.key.text, field.value)
        print(field.key.text)

    Path(dir_here, "test_2.json").write_text(json.dumps(js, indent=4))

# test2()
