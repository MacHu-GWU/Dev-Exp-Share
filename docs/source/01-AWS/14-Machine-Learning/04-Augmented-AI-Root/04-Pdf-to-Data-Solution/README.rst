PDF to Data Solution
==============================================================================

.. raw:: html
    :file: ./pdf-to-data-solution.drawio.html


Architect
------------------------------------------------------------------------------
.. tab:: 1. Raw Data

    S3 Folder Structure:

    - Raw File: ``2022-01-01-financial-report.pdf``
    - S3 Object: ``s3://my-bucket/my-folder/01-raw/${45781d436b1c285fbf11eb90e60a2a93_MD5}.dat``, the ``4578...`` is the MD5 of ``2022-01-01-financial-report.pdf`` for deduplication. The original file name can be stored as a S3 Object Tag

.. tab:: 2. Trigger Text Tract

    Once the raw file been uploaded to S3 bucket, the S3 put object event will trigger a Lambda Function, and the Lambda Function calls the Textract **async** API.

.. tab:: 3. Textract

    Once the text extract is done, Textract will store the Machine Readable extracted data in JSON to S3 bucket. Since this process may takes long (if it is 100+ pages PDF), you can configure to send an notification to the SNS topic when it is done.

.. tab:: 4. Extracted Text

    The extracted text data is stored in S3 bucket

    The Machine readable extracted data:

    .. code-block:: python

        # Sample textract output JSON
        {
            "Blocks": [
                {
                    "Id": "c6dac97a-ec9d-4b74-b9f4-554853bd88a4",
                    "BlockType": "PAGE | LINE | WORD",
                    "Text": "your text here",
                    "Geometry": {
                        "BoundingBox": {...},
                        "Polygon": [...]
                    },
                    "Relationships": [...],
                    ...
                },
                ...
            ]
        }

    Convert to Human readable extracted text:

    .. code-block:: python

        # Create a pure-text merged view of the extracted text data
        data = json.loads(s3path.read_text())
        lines = list()
        for block in data["Blocks"]:
            s.add(block["BlockType"])
            if block["BlockType"] == "LINE":
                lines.append(block["Text"])
        content = "\n".join(lines)

.. tab:: 5. SNS Topic

    Textract will send a message to SNS topic when the async operation is done. It can trigger subsequence job as required.

.. tab:: 6. Trigger Comprehend

    The SNS message triggers a Lambda Function that invoke the Comprehend API, try to detect entities from extracted text. The input of the comprehend is the "Human readable extracted text" data.

.. tab:: 7. Comprehend

    Once the detect entity operation is done, it will store the machine readable detected entities data in JSON to S3 Bucket.

.. tab:: 8. Detected Entities

    Sample comprehend output data:

    .. code-block:: python

        # Machine readable extracted text
        {
            "Entities": [
                {
                    "Score": 0.851378858089447,
                    "Type": "ORGANIZATION",
                    "Text": "CENTER FOR MEDICARE",
                    "BeginOffset": 0,
                    "EndOffset": 86
                },
                ...
            ]
        }

.. tab:: 9. Trigger HIL

    The Comprehend output JSON file creation event will trigger a Lambda Function, and the Lambda Function can do necessary post process on Textract and Comprehend output, and it will trigger the Human in Loop to verify the quality of extracted data.

.. tab:: 10. Human In Loop

    A HIL task is created by the Lambda Function

.. tab:: 11. Human Review

    The Human workers receive the assign HIL, and be able to provide feed back in HIL GUI.

.. tab:: 12. HIL Output

    The HIL output data will be saved to S3 bucket.

.. tab:: 13. Save to Data Store

    The creation HIL Output event will trigger a Lambda Function that merges HIL output with the Textract / Comprehend output, and store validated data to final Data Store.

.. tab:: 14. Data Store

    The required structured data of the original document will be stored in proper data store backend for future use.
