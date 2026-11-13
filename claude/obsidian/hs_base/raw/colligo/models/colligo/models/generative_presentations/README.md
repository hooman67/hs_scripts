# Introduction

[PRD - Generative Presentations](https://adobe-my.sharepoint.com/:w:/p/mnaum/EU-T85uRmZBFhOVBphdeWscBUcizXJlDFY3Qb2Q2poZpyw?e=bHgFZh). “PDF to Presentation” (aka. "Doc to Presentation") is a component of Generative Presentations, enabling the user to start from existing PDF content and automatically summarize & generate a stylized Presentation in Adobe Express.

# Architecture

- [Architecture document](https://adobe-my.sharepoint.com/:w:/p/abucur/EbKJgLCcclFMhXe-Hb91wGwBiHrtNNmCY7L9NcQXGze2eg?e=XjbA6O)

#### Diagrams

- [High-level system diagram](https://lucid.app/lucidchart/2911f658-2435-4d1f-92ab-5a266a77da25/edit?invitationId=inv_6729389d-0130-46ec-9eae-7f8cf945d449&page=YUUlh4DYX3Uj#)
- [Detailed colligo modules diagram](https://adobe-my.sharepoint.com/:u:/r/personal/mironica_adobe_com/_layouts/15/Doc.aspx?sourcedoc=%7B02B340D9-7714-43F0-9490-F2F05FBB0AD8%7D&file=Pdf2Presentation%20ML%20Diagram.vsdx&fromShare=true&action=default&mobileredirect=true&cid=1a1e5454-488c-4b37-8119-31f6ae833819)

### Components

#### Doc2Outline

1. Extract the content (text, images) from the given PDFs using Colorado API and generate a Document Tree
2. Determine a section structure (sections, subsections, section topics) and the document metadata (presentation title, subtitle, topic)
3. Generate a presentation outline using GPT-4

#### Outline2Content

1. Use the previously generated presentation outline to produce presentation slides (e.g., title slide, agenda slide, text slides, etc.)
2. The slides populated with content by the previous step will be transposed by the Doc Producer (Hz app) into an actual Express document

#### Semantic Inference

This is a standalone colligo service which provides semantic metadata for the templates used as a base for the generated presentations.
In the future, it will eventually generate these metadata dynamically, through an ML model which can analyze the structure and content of Express documents.

### Pipeline flow and error handling

#### Outline2Presentation generation

1. Get presentation params: *deck type, *length hint, *image strategy, *target audience, *generate background, charts_enabled, *brand, \*seed

   - If required (\*) params are missing:

     🔴 Return error to the client
     <details>
     <summary>HTTP 400</summary>

     ```json
     {
       "error_code": "bad_request",
       "message": "Data with key=image_strategy not found in session storage"
     }
     ```

     </details>

   - If any param is invalid:

     🔴 Return error to the client
     <details>
     <summary>HTTP 422</summary>

     ```json
     {
       "error_code": "validation_error",
       "message": "A validation error occured.",
       "validation_errors": [
         {
           "loc": ["body", "image_strategy"],
           "msg": "value is not a valid enumeration member; permitted: 'stock', 'firefly', 'stock_with_firefly_ref', 'best'",
           "type": "type_error.enum",
           "ctx": {
             "enum_values": [
               "stock",
               "firefly",
               "stock_with_firefly_ref",
               "best"
             ]
           }
         },
         {
           "loc": ["body", "brand", "colors", 0],
           "msg": "String should match pattern '^#[0-9a-fA-F]{6}$'",
           "type": "string_pattern_mismatch",
           "ctx": {
             "pattern": "^#[0-9a-fA-F]{6}$"
           }
         }
       ]
     }
     ```

     </details>

   - If all params are valid, continue 🟢

2. Update the outline if it was initially generated and then edited by the user

   - If any error is encountered during outline editing:

     - 📝 Log "Error at outline editing"
     - 🟡 Continue with the user's (non-edited) outline (best-effort)

3. Generate the presentation blueprint

- Check if user-provided outline is unsafe

  - If the outline is unsafe:

    🔴 Return error to the client
    <details>
    <summary>HTTP 451</summary>

    ```json
    {
      "error_code": "prompt_unsafe"
    }
    ```

    </details>

  - If the outline is safe, continue 🟢

- GPT blueprint generation request

  See [OpenAI error handling](#openai-error-handling).

  - If only some slide blueprints failed:

    - 📝 Log "Failed GPT-generated slide blueprint parsing" errors
    - 🟡 Continue with the available slide blueprints (best-effort)

  - If it succeeds, continue 🟢

- Generate background image

  See [Image Provider error handling](#image-provider-error-handling).

  - If it fails:

    - 📝 Log "Failed background image generation" error
    - 🟡 Continue without a background image (best-effort)

  - If it succeeds, attach the background image data to the blueprint 🟢

4. Generate the presentation slides

- GPT slides generation request

  See [OpenAI error handling](#openai-error-handling).

  - If only some slides failed at GPT generation or parsing:

    - 📝 Log "Failed GPT-generated slide parsing" errors
    - 🟡 Continue with the available slides (best-effort)

  - If it succeeds, continue 🟢

- Images search/generation per slide

  See [Image Provider error handling](#image-provider-error-handling).

  - If only some slide image requests failed:

    - 📝 Log "Stock image search failed"/"Firefly image generation failed" errors
    - 🟡 Add slide media resources only for the successful images (best-effort)

5. Return the generated presentation

#### OpenAI error handling

- If request fails after some partial results with **length finish** reason:

  - 📝 Log "[OpenAI] Length limit error" error
  - 🟡 Try to go on with the response generated so far (best-effort)

- If request fails after some partial results with **content filter** reason:

  - 📝 Log "[OpenAI] Content filter error" error
  - 🔴 Return error to the client
    <details>
    <summary>HTTP 451</summary>

    ```json
    {
      "error_code": "prompt_unsafe"
    }
    ```

- If request fails after some partial results with **rate limit** reason:

  - 📝 Log "[OpenAI] Rate limit exceeded" error
  - 🔴 Return error to the client
    <details>
    <summary>HTTP 500</summary>

    ```json
    {
      "error_code": "runtime_error",
      "message": "OpenAI request failed. reason=RateLimit)"
    }
    ```

    </details>

- If request fails completely with **API status**/**API connection** error / other OpenAI error:

  - 📝 Log "[OpenAI] API error"/"[OpenAI] The server could not be reached"/"[OpenAI] Unexpected error" error
  - 🔴 Return error to the client
    <details>
    <summary>HTTP 500</summary>

    ```json
    {
      "error_code": "runtime_error",
      "message": "OpenAI request failed. reason=APIError({status_code})",
      // or
      "message": "OpenAI request failed. reason=ConnectionError",
      // or
      "message": "OpenAI request failed. reason=UnexpectedError"
    }
    ```

    </details>

- If request fails completely, even after retries:

  🔴 Return error to the client
  <details>
  <summary>HTTP 500</summary>

  ```json
  {
    "error_code": "runtime_error"
  }
  ```

  </details>

#### Image Provider error handling

The image providers are handling the errors internally and returning a best-effort result:

- Produce image

  - If Adobe Stock image search fails:

    - 📝 Log "Stock image search failed" error
    - 🟡 Try to fallback to the Firefly image generation **if** the requested `ImageGenerationStrategy` allows the use of Firefly

  - If Adobe Firefly image generation fails:

    - 📝 Log "Firefly image generation failed" error
    - 🟡 Try to fallback to the Stock image search **if** the requested `ImageGenerationStrategy` allows the use of Stock

  - If the images are successfuly generated, 🟢 continue

- Select the most suitable image

  - If the scoring fails:

    - 📝 Log "Failed to compute image-text match scores" error
    - 🟡 Prefer the Stock image

- Compute the image saliency mask

  - If it fails:
    - 📝 Log "Failed to compute saliency mask" error
    - 🟡 Continue without a saliency mask

# Development

### Running the code without colligo

For quick ML research development, it may be desirable to run a module or the entire Generative Presentations pipeline without the colligo overhead (i.e. Redis cluster, bootstrap code, etc.).

To run a module in isolation, without starting colligo services, you can use the `main.py` files from each module's folder. Run or Debug the file directly from VSCode or by running `python main.py` in a terminal.

To run the entire Generative Presentations pipeline, you can use the `main.py` file from the generative*presentations root folder. It chaines all the modules \_synchronously* (waiting for a module to finish in order to start the next one, which receives the needed previous results in the request).
