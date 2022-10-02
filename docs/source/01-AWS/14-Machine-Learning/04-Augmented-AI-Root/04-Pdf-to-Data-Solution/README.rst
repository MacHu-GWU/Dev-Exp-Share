PDF to Data Solution
==============================================================================

.. raw:: html
    :file: ./pdf-to-data-solution.drawio.html


Architect
------------------------------------------------------------------------------
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


.. tab:: 1. Raw Data

    S3 Folder Structure:

    - Raw File: ``2022-01-01-financial-report.pdf``
    - S3 Object: ``s3://my-bucket/my-folder/01-raw/${45781d436b1c285fbf11eb90e60a2a93_MD5}.dat``, the ``4578...`` is the MD5 of ``2022-01-01-financial-report.pdf`` for deduplication. The original file name can be stored as a S3 Object Tag

.. tab:: 2. Trigger Text Tract

    NA

.. tab:: 3. Textract

    .. code-block:: python

        print("Hello")


1. Raw Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
S3 Folder Structure:

- Raw File: ``2022-01-01-financial-report.pdf``
- S3 Object: ``s3://my-bucket/my-folder/01-raw/${45781d436b1c285fbf11eb90e60a2a93_MD5}.dat``, the ``4578...`` is the MD5 of ``2022-01-01-financial-report.pdf`` for deduplication. The original file name can be stored as a S3 Object Tag


2. Trigger Text Tract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


3. Textract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Example output:


4. Extracted Text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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


5. SNS Topic
------------------------------------------------------------------------------
