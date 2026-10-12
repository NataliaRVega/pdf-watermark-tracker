# PDF Watermark Tracker
### User Guide — codigo by natty

PDF Watermark Tracker is a Windows desktop application that creates personalized PDF copies with watermarks. It helps you prepare, identify, and organize individual copies of a document.

No programming knowledge or Python installation is required.

---

## 1. Getting Started

### What do I need?

- A Windows computer.
- The file `PDF Watermark Tracker.exe`.
- A PDF document you want to personalize.
- A folder where you want to save the generated copies.

### How do I open the application?

1. Download `PDF Watermark Tracker.exe`.
2. Save it somewhere easy to find, such as your Desktop or Documents folder.
3. Double-click the file to open the application.
4. If Windows displays a security warning because the application is not recognized, only proceed if you trust the person or source that provided the file. Do not bypass warnings for files from unknown sources.

You do not need to install Python or any programming tools.

---

## 2. How to Generate PDF Copies

Follow these steps in order.

### Step 1 — Select the original PDF

Choose the PDF document you want to use as the source.

The application uses this document to create the personalized copies. Your original document should remain unchanged.

**Tip:** Keep a backup of important documents before processing them.

### Step 2 — Choose the output folder

Select the folder where the new PDF files will be saved.

For example:

`Documents/Generated PDFs`

Make sure you can find this folder later.

### Step 3 — Choose the number of copies

Enter how many individual copies you want to generate.

For example, if you enter `5`, the application will attempt to create five separate PDF files.

### Step 4 — Set the copy code prefix

The copy code identifies an individual copy. The prefix is the text that appears at the beginning of that code.

For example, if the prefix is:

`COPY`

the codes might be:

- `COPY001`
- `COPY002`
- `COPY003`

The exact appearance of the watermark depends on the application's watermark settings.

**Important:** A copy code is an identifier. It does not automatically identify a person unless you deliberately connect that code to a person in your own records.

### Step 5 — Choose the filename pattern

The filename pattern determines how each generated PDF is named.

The default pattern is:

`{nombre}_unidad{numero}`

You can customize the text around the two special placeholders explained below.

#### Understanding `{nombre}`

`{nombre}` represents the name of the original PDF file, without its file extension.

For example, if your original file is:

`claveles.pdf`

then `{nombre}` becomes:

`claveles`

#### Understanding `{numero}`

`{numero}` represents the sequential number assigned to each generated copy.

The number format is controlled by the **Number Padding** setting.

For example, with three-digit padding:

- `001`
- `002`
- `003`

### Step 6 — Choose Number Padding

Number Padding controls how many digits are used for the sequential number. When necessary, zeros are added to the beginning of the number.

| Padding | Example for the first three copies |
|---|---|
| `1` | `1`, `2`, `3` |
| `2` | `01`, `02`, `03` |
| `3` | `001`, `002`, `003` |

For most situations, three-digit padding is a good choice because it keeps filenames consistent and easy to sort.

### Step 7 — Check the preview and watermark

Review the PDF preview and watermark settings before generating the copies.

Make sure the watermark is positioned and displayed as you expect.

### Step 8 — Generate the copies

Click **Generate**.

The application creates the requested PDF copies in your selected output folder and creates a CSV manifest to record the batch.

Wait for the operation to finish and check the application's confirmation message.

---

## 3. Filename Patterns Explained

A filename pattern is a template. The application replaces the special placeholders with the appropriate values for each copy.

The default pattern is:

`{nombre}_unidad{numero}`

Suppose the original PDF is named `claveles.pdf` and you generate three copies with Number Padding set to `3`.

The output files will be:

- `claveles_unidad001.pdf`
- `claveles_unidad002.pdf`
- `claveles_unidad003.pdf`

### Example A — The default pattern

Pattern:

`{nombre}_unidad{numero}`

Example output:

`claveles_unidad001.pdf`

Useful when you want the original document name and a sequential unit number.

### Example B — Use "copy" instead of "unidad"

Pattern:

`{nombre}_copy{numero}`

Example output:

`claveles_copy001.pdf`

Useful when you want filenames in English or prefer the word "copy."

### Example C — Use a dash

Pattern:

`{nombre}-{numero}`

Example output:

`claveles-001.pdf`

Useful for short, clean filenames.

### Example D — Add a descriptive label

Pattern:

`{nombre}_distribucion_{numero}`

Example output:

`claveles_distribucion_001.pdf`

Useful when you want filenames to indicate the purpose of the copies.

### Example E — Put the number first

Pattern:

`unidad{numero}_{nombre}`

Example output:

`unidad001_claveles.pdf`

Useful when you want all files to be grouped by their sequential numbers when sorted by filename.

### Pattern rules

- `{nombre}` is replaced with the original PDF's filename, without `.pdf`.
- `{numero}` is replaced with the sequential copy number.
- You may add descriptive words before, between, or after the placeholders.
- Both `{nombre}` and `{numero}` must be included in the pattern.
- Use ordinary filename characters. Avoid characters that Windows does not allow in filenames, such as `\ / : * ? " < > |`.
- The `.pdf` extension is added to the generated filename automatically.

**Important:** The filename pattern controls the output filename. It does not, by itself, change the watermark text or the copy code printed on the PDF.

---

## 4. What Is a `copy_code`?

A `copy_code` is a unique identifier assigned to a generated copy.

Think of it as a serial number. It helps you distinguish one copy from another.

For example:

| Copy | Example copy code |
|---|---|
| First copy | `COPY001` |
| Second copy | `COPY002` |
| Third copy | `COPY003` |

The actual code format depends on the copy-code prefix and the application's numbering behavior.

### Why are copy codes useful?

Copy codes can help you:

- Distinguish copies of the same document.
- Keep track of which copy was generated.
- Match a PDF with an entry in your records.
- Investigate which copy was distributed if you maintain a separate distribution log.

### Do not confuse the copy code with the filename

The **copy code** identifies the copy.

The **filename** tells you what the file is called on your computer.

For example:

- Filename: `claveles_unidad001.pdf`
- Copy code: `COPY001`

These values can be related by the order in which copies are generated, but they serve different purposes.

If you need a reliable relationship between a copy code and a recipient, keep a separate record of who received each copy.

---

## 5. Understanding the CSV Manifest

After generating a batch, the application creates a CSV manifest.

A CSV file is a simple table that can be opened with Excel, many spreadsheet applications, or a text editor.

The manifest records information about the generated batch.

### What information does it contain?

| Column | Meaning |
|---|---|
| `copy_code` | Identifier assigned to the copy. |
| `unit_number` | Sequential number of the copy. |
| `generated_at` | Date and time recorded for generation. |
| `input_file` | Original PDF used as the source. |
| `output_file` | Name of the generated PDF. |
| `status` | Result recorded for the generation of that copy. |

### Why is the manifest important?

The manifest provides a record of what the application attempted to generate and the status recorded for each copy.

For example, you can use it to check:

- How many copies were recorded.
- Which source PDF was used.
- Which output filename corresponds to a copy code.
- Whether a copy was recorded as successful or otherwise.

Keep the manifest together with your generated PDFs. It is particularly useful if you need to identify a copy later.

**Privacy tip:** If you associate copy codes with individual recipients, store that mapping securely. The manifest is not automatically a recipient list unless you add that information yourself.

---

## 6. Recommended Workflow

For a clean and organized process:

1. Create a dedicated folder for the source PDF.
2. Create a separate output folder for each batch.
3. Select the original PDF and review the preview.
4. Choose the number of copies and the desired filename pattern.
5. Generate the copies.
6. Confirm that the expected files exist.
7. Open a sample generated PDF and verify its watermark.
8. Keep the manifest with the generated files.
9. If the copies are distributed to people, maintain a separate recipient log when appropriate.
10. Back up the generated PDFs and manifest if they are important.

Example folder organization:

`Generated PDFs/`

- `claveles_unidad001.pdf`
- `claveles_unidad002.pdf`
- `claveles_unidad003.pdf`
- `manifest_YYYYMMDD_HHMMSS.csv`

The manifest's actual filename contains the date and time recorded by the application.

---

## 7. Troubleshooting

### The application does not open

- Confirm that the download completed.
- Try opening the file again.
- Check whether Windows security software has blocked the file.
- Only run the application if you trust its source.

### The generated PDFs are not in the folder I expected

Check the output folder selected in the application. The generated copies are saved there, not necessarily beside the original PDF.

### The filenames do not look right

Review the filename pattern and make sure both `{nombre}` and `{numero}` are included.

For example:

`{nombre}_unidad{numero}`

### A file already exists

The application is designed to avoid overwriting existing output files. Choose a different output folder or change the naming pattern, then try again.

### The watermark is not as expected

Check the watermark settings and preview before generating another batch. Open one of the generated PDFs to confirm the result.

### I cannot open the manifest in Excel

The manifest is a CSV file. Open Excel and use its file-opening option to select the CSV, or open it with another spreadsheet application.

---

## 8. Important Notes

- The application creates PDF copies; always review the generated output before distributing it.
- Keep a backup of important source documents.
- The manifest is a record of the batch, not a guarantee that a recipient received a particular file.
- A watermark and copy code may help identify a copy, but they do not prevent screenshots, photography, or every form of redistribution.
- Keep the application and its files in a trusted location.
- The single-file executable may take longer to open the first time because it unpacks its bundled components.

---

## PDF Watermark Tracker

**codigo by natty**

A simple tool for generating, identifying, and organizing personalized PDF copies.
