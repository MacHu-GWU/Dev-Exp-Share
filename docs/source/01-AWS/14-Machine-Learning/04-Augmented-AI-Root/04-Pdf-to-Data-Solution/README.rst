Text Insight Solution
==============================================================================
Keywords: text insight solution, unstructured document to structured data, pdf to data


Summary
------------------------------------------------------------------------------
"Text Insight" is an "Unstructured Document to Structured Data" solution that can extract high quality, machine readable, structured data from PDF, Image, or any None Text data format (has potential to extend to process Audio / Video). Target vertical industry include:

- Law Service
- Financial Document
- Insurance Document
- Health Care Document


Architect
------------------------------------------------------------------------------
.. raw:: html
    :file: ./pdf-to-data-solution.drawio.html


.. tab:: 1. Raw Data

    User or Machine uploads raw document to S3 bucket.

    S3 Folder Structure:

    - Raw File: ``2022-01-01-financial-report.pdf``
    - S3 Object: ``s3://my-bucket/my-folder/01-raw/${45781d436b1c285fbf11eb90e60a2a93_MD5}.dat``, the ``4578...`` is the MD5 of ``2022-01-01-financial-report.pdf`` for deduplication. The original file name can be stored as a S3 Object Tag

.. tab:: 2. Trigger Text Tract

    Once the raw file been uploaded to S3 bucket, the S3 put object event will trigger a Lambda Function, and the Lambda Function calls the Textract **async** API.

.. tab:: 3. Textract

    Once the text-extract operation is done, Textract will store the "machine readable extracted data" in JSON format in S3 bucket. Since this process may takes long (if it is 100+ pages PDF), you can configure to send an notification to the SNS topic when it is done.

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

    Once the detect-entity operation is done, it will store the machine readable detected entities data in JSON in S3 Bucket.

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

    A HIL task is created by the Lambda Function.

.. tab:: 11. Human Review

    The Human workers receive the assign HIL, and be able to provide feed back in HIL GUI.

    Sample GUI:

    .. image:: ./hil-ui.png

.. tab:: 12. HIL Output

    The HIL output data will be saved to S3 bucket.

    Sample HIL Output:

    .. code-block:: python

        [
          {
            "Change Reason1": "looks weird",
            "True Prediction1": "sanhe prediction",
            "predicted1": "0.1544346809387207",
            "predicted2": "0.4938497543334961",
            "predicted3": "0.23486430943012238",
            "rating1": {
              "agree": true,
              "disagree": false
            },
            "rating2": {
              "agree": false,
              "disagree": true
            },
            "rating3": {
              "agree": true,
              "disagree": false
            }
          }
        ]

.. tab:: 13. Save to Data Store

    The creation HIL Output event will trigger a Lambda Function that merges HIL output with the Textract / Comprehend output, and store validated data to final Data Store.

.. tab:: 14. Data Store

    The required structured data of the original document will be stored in proper data store backend for future use.

.. tab:: 15. Status Tracker Dynamodb

    The entire workflow has multiple steps, we could store the status information for each step in Dynamodb and be able to use a simple query to continues the workflow from any step.
