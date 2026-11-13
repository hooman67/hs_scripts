```markdown
# Jupyter and Conda

## Jupyter

* **Auto reload jupyter modules:**
    ```python
    %load_ext autoreload
    %autoreload 2
    ```

## Conda

* **I have an env that should be accessible from all machines here:** `/mnt/localssd/hshariati/hs_AD_3.10.13_mc-mds3`
    Run:
    ```bash
    conda activate /mnt/localssd/hshariati/hs_AD_3.10.13_mc-mds3
    ```
    Might need to run: `conda init` first.

## Install Conda and Get the New Env Working with Jupyter

* **To install conda on runai box:**
    ```bash
    #sudo chmod 777 /opt/
    # bash scripts/DockerDev/install_conda.sh /opt/conda    #put this in the run engine script
    #source /opt/conda/etc/profile.d/conda.sh
    ```
* **Remove env:**
    ```bash
    conda remove --name ENV_NAME --all
    ```
* **Create env:**
    ```bash
    conda create -n hs_AD_3.10.13 python=3.10.13
    ```
* **Create conda env in a location other than default:**
    ```bash
    conda create -p /mnt/localssd/hshariati/hs_AD_3.10.13 python=3.10.13
    ```
* **Create from file you exported before:**
    ```bash
    conda env create -f /sensei-fs/users/hshariati/condaEnv__hs_AD_3.10.13__02-20-24.yml
    ```
* **Export env to file:** **Note:** this won't work for adobe packages.
    ```bash
    conda activate your_environment_name
    conda env export > environment.yml
    ```
* **To see the newly created env in your jupyter:**
    ```bash
    conda create -n hs_AD_3.10.13 python=3.10.13 -y;
    conda activate hs_AD_3.10.13;
    #can't run these two on the same line as above
    conda install ipykernel -y;
    # (or: <d>)
    python -m ipykernel install --user --name hs_AD_3.10.13;
    ```
    **install the jupter plugin and reload vscode window if it doesn’t work**
    *install ipykernle in your conda env, then run the command, then referesh the webpage with jupyter in it, restart the jupyter kernel in your note book, and you should see the new env.*

## Pickle and Load an Object

```python
import pickle
with open(
    "/sensei-fs/users/hshariati/worktree_AdobeDiffusion/hshariati/mc-dmd2/hs_temp/omega_config.pkl", "wb"
) as file:
    pickle.dump(omega_config, file)

# Load the pickled object
with open("/sensei-fs/users/hshariati/AdobeDiffusion/hs_text_prompt.pkl", "rb") as file:
    loaded_text_prompt = pickle.load(file)
```

## Save and Load a Torch Tensor

```python
import torch
+        torch.save(
+            hs_temp_t5_text_embedding,
+            "/sensei-fs/users/hshariati/AdobeDiffusion/hs_temp_t5_text_embedding_noPad_xxl.pkl",
+        )


# Load the torch model
loaded_t5_text_embedding = torch.load(
    "/sensei-fs/users/hshariati/AdobeDiffusion/hs_temp_t5_text_embedding_noPad_xxl.pkl"
)
```

You can also use the `.pt` format: (the format doesn't affect anything)

```python
import torch.testing

# Your tensor
my_tensor = torch.tensor([1, 2, 3, 4, 5])

# Save the tensor to a file
torch.save(my_tensor, "my_tensor.pt")

# Load the tensor back
loaded_tensor = torch.load("my_tensor.pt")

# Assert that tensors are almost equal
torch.testing.assert_allclose(my_tensor, loaded_tensor)

***And I can attach a debugger anywhere in the script (just put a break point) and run the cell with debug.
```

## To Save a Decoded (Colligo Tensor) Image

```python
from torchvision.transforms.functional import to_pil_image
k = to_pil_image(response.images.as_torch()[0])
k.save("/sensei-fs/users/hshariati/colligo_files_backup/shayan_colligo/colligo/delete/test.png")
```

## Pickle the Scheduler State (All the Member Variables)

Use this to pickle the scheduler:

```python
scheduler_state = {}
for attr in dir(scheduler):
    if not attr.startswith('_') and not callable(getattr(scheduler, attr)):
        try:
            value = getattr(scheduler, attr)
            if is_picklable(value):
                scheduler_state[attr] = value
        except:
            continue
inputs = {

    'scheduler_state': scheduler_state
}
save_dir = "/sensei-fs/users/hshariati/del/"
# Save inputs to pickle file with proper error handling
pickle_path = os.path.join(save_dir, 'scheduler_inputs.pkl')
try:
    with open(pickle_path, 'wb') as f:
        pickle.dump(inputs, f)

    # Verify the file was written correctly
    with open(pickle_path, 'rb') as f:
        test_load = pickle.load(f)
    print(f"Successfully saved and verified inputs to {pickle_path}")
    print(f"Saved scheduler attributes: {list(scheduler_state.keys())}")
except Exception as e:
    print(f"Error saving inputs: {str(e)}")
```

## Pickle the Input to Diffusion

```python
# save_dir = "/sensei-fs/users/hshariati/del/"
# os.makedirs(save_dir, exist_ok=True)
# # Prepare inputs dictionary
# # Prepare inputs dictionary with actual values being passed to diffusion_loop
# inputs = {
#     "latents": latents,
#     "cond_latents": _to_torch_sync(request.cond_latents),
#     "cond_latent_inds": request.cond_latent_inds,
#     "avoid_cond_latents": _to_torch_sync(request.avoid_cond_latents),
#     "avoid_cond_latent_inds": request.avoid_cond_latent_inds,
#     "text_emb": _to_torch_sync(request.text_embedding, dtype=dtype),
#     "text_emb_uncond": _to_torch_sync(request.avoid_text_embedding, dtype=dtype),
#     "image_emb": _to_torch_sync(request.image_embedding, dtype=dtype),
#     "image_emb_uncond": _to_torch_sync(request.avoid_image_embedding, dtype=dtype),
#     "data_info": data_info,
# }
# # Save inputs to pickle file with proper error handling
# pickle_path = os.path.join(save_dir, "from_colligo_512_t5.pkl")
# try:
#     with open(pickle_path, "wb") as f:
#         pickle.dump(inputs, f)

#     # Verify the file was written correctly
#     with open(pickle_path, "rb") as f:
#         test_load = pickle.load(f)
#     print(f"Successfully saved and verified inputs to {pickle_path}")
# except Exception as e:
#     print(f"Error saving inputs: {str(e)}")
```

## Turn Off Disable Mypy for an Entire File

Put this as the first line in a file:

```python
# type: ignore
```

## Attaching Debuggers

* **For a python command you run:** ***I haven't gotten this to work yet. I think I can use "docker Expose PortNb" to expose the port. But for now instead I just learned how to import the script from within Jupyter notebook. I then attach the debugger from there. (Just select debug by clicking on the arrow next to play button of the cell). You can put the same command you run your script with in commandLIne by starting it with !.***

* ****If you're running your Python code inside a Docker container on a remote machine and connecting to it using VS Code's Remote Explorer, you'll need to make sure that the debugger port is accessible from your local machine.**

    1.  Modify the `launch.json` file to include a configuration for attaching the debugger. You can add a configuration like this:

        ```json
        {
            "name": "Attach to Python Program",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "."
                }
            ]
        }
        ```

    2.  Add a break point where you want it.
    3.  Run your command normally like this for example:
        ```bash
        python3 scripts/clio3/run_inference_clio3_mc.py --config CONFIG_PATH --save_to SAVE_TO --prompt /sensei-fs/users/fchen/controlnet/test_clio-mm_v2.txt --application text2image_mc --control canny --aesthetic_class 6.0
        ```
    4.  Now, click on the "Run and Debug" icon in the sidebar or press F5.
    5.  Select the "Attach to Python Program" configuration you created earlier.
    6.  The debugger will attach to your running Python script, and execution will pause at the breakpoint you set.

* **For jupyter notebook:** Just click on arrow next to the cell debug button and select debug cell.

* **For unit-test:** Just put the cursor on the unit test, right click, and select debug at cursor. You need this extension: [https://marketplace.visualstudio.com/items?itemName=LittleFoxTeam.vscode-python-test-adapter](https://marketplace.visualstudio.com/items?itemName=LittleFoxTeam.vscode-python-test-adapter)

* **Expose the functions of a python script with main file:**
    ```python
    import sys
    sys.path.append('path/to/your/script')
    import your_script_name
    # Now you can call the functions defined in your script:
    your_script_name.foo()
    your_script_name.bar()
    ```

    **Example:** I have a script here: `/sensei-fs/users/hshariati/worktree_AdobeDiffusion/hshariati/mc-dmd2/scripts/clio3/run_inference_clio3_mc.py`

    Then in a juypter cell I write:
    ```python
    import sys
    sys.path.append('/sensei-fs/users/hshariati/worktree_AdobeDiffusion/hshariati/mc-dmd2/scripts/clio3/')
    import run_inference_clio3_mc
    ```

    Then I can do: `run_inference_clio3_mc.run_text2image_mc(inputs)`

## Formatters

To run off formatters, in your `.vscode/settings.json` set these:

```json
"[python]": {
    "editor.defaultFormatter": null,
    "editor.formatOnSave": false,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "off"
    }
}
```

## Syntax

`maybe_blocked_prompt: ClioMDResponse | None = should_block_prompty(request_context, prompty_errors)`

1.  **Variable Name:** `maybe_blocked_prompt` - This seems to be a variable name, indicating that it might represent a value that could potentially be a blocked prompt.
2.  **Type Annotation:** `: ClioMDResponse | None` - This is a type hint or type annotation. It specifies the expected type of the variable `maybe_blocked_prompt`. In this case, it can be either an instance of the `ClioMDResponse` class or `None`.
3.  **Assignment:** `= should_block_prompty(request_context, prompty_errors)` - It assigns a value to the variable `maybe_blocked_prompt`. The value is the result of calling the function `should_block_prompty` with arguments `request_context` and `prompty_errors`.

Putting it all together, it appears that this line of code is assigning the result of the `should_block_prompty` function to the variable `maybe_blocked_prompt`, and this result is expected to be either an instance of the `ClioMDResponse` class or `None`.

## Colligo

### Profiling

Colligo has annotations for profiling. This is memory, gpu, time, etc. [https://git.corp.adobe.com/pages/colligo/dev-guidelines/profiling.html](https://git.corp.adobe.com/pages/colligo/dev-guidelines/profiling.html)

```python
@annotate.func(zone="...")
@annotate.func(log_code=LogCode.PERF_ZONE)
```

## Pydantic Vs DataClass

**pydantic is a third party library but dataclass is a built in python feature.** **Both pydantic.BaseModels and dataclass provide data validation. But the BaseModel is a lot more sophisticated.** **BaseModel provides serialization, parsing, default values, optional values, and type hint support. Dataclass has none of these.**

### Pydantic

Pydantic is a data validation and parsing library for Python that is primarily used for defining and validating data models, especially when working with complex data structures like JSON payloads, configuration settings, or API requests and responses. The `BaseModel` class provides a way to define data models using a simple and intuitive syntax, and it automatically generates methods for validation, serialization, and parsing based on the model's field definitions.

**Model Definition:** You define your data model by creating a class that inherits from `BaseModel` and includes attributes representing the fields of your model.

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
```

**Data Validation:** Pydantic automatically validates the data against the specified model during instantiation. If the data doesn't match the expected types or constraints, Pydantic raises validation errors.

```python
data = {"name": "John Doe", "age": 30}
person = Person(**data)  # Validation happens here
```

**Data Parsing and Serialization:** Pydantic can parse data into a Python object based on the model, and it can serialize the object back into the original data format.

```python
# Parsing JSON into a Python object
json_data = '{"name": "Jane Doe", "age": 25}'
person = Person.parse_raw(json_data)

# Serializing the object back to JSON
json_output = person.json()
```

**Default Values and Optional Fields:** You can specify default values for fields and mark them as optional using the `Optional` type from the `typing` module.

```python
from typing import Optional

class Person(BaseModel):
    name: str
    age: Optional[int] = 18  # Default age is 18 if not provided
```

### `BaseModelArbitraryAllowed` vs `BaseModel`

```python
class BaseModelArbitraryAllowed(BaseModel, arbitrary_types_allowed=True):
    pass
```

Adding the `arbitrary_types_allowed` means we can have our own python classes as types:

```python
class MyType:
    pass

class ModelWithoutArbitraryTypesAllowed(BaseModel):
    my_attr: MyType

try:
    model_instance = ModelWithoutArbitraryTypesAllowed(my_attr=MyType())
except ValueError as e:
    print(e)  # This will raise a validation error because MyType is not a recognized type


class MyType:
    pass

class ModelWithArbitraryTypesAllowed(BaseModelArbitraryAllowed):
    my_attr: MyType

model_instance = ModelWithArbitraryTypesAllowed(my_attr=MyType())
print(model_instance)  # This will work fine because arbitrary types are allowed
```

### Setting `frozen = True` on a `BaseModel` object

```python
class ClinetoRequest(BaseModelArbitraryAllowed, frozen=True):
```

This will make the objects of this class immutable. And it makes them hashable (they can be used as keys in dictionaries and can be added to sets)

```python
from pydantic import BaseModel

class MyModel(BaseModel, frozen=True):
    id: int
    name: str

# Creating an instance of MyModel
instance = MyModel(id=1, name="Example")

# Trying to modify an attribute will raise an error
try:
    instance.id = 2
except TypeError as e:
    print(e)  # Output: "Cannot assign to field 'id'"
```

## Decorators

They are denoted by the `@decorator` syntax and are applied to functions or classes by placing them directly above the function or class definition. Decorators can be thought of as wrappers around functions or classes, allowing you to add or modify functionality. Decorators are functions that take another function or class as input and return a new function or class with modified behavior.

### `@dataclass`

The `dataclass` decorator is a built-in decorator provided by the `dataclasses` module in Python. It is used to automatically generate special methods like `__init__`, `__repr__`, `__eq__`, and others, based on the class attributes. This is particularly useful for creating simple classes to store data without writing a lot of boilerplate code.

**Example from adobe:**

```python
@dataclass
class MultidiffusionCropInputs:
    global_image: Image.Image | torch.Tensor
```

**Official example:**

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

# Automatically generates __init__, __repr__, and other methods
point = Point(1, 2)
print(point)  # Output: Point(x=1, y=2)
```

```python
def dataclass(cls=None, /, *, init=True, repr=True, eq=True, order=False,
              unsafe_hash=False, frozen=False, match_args=True,
              kw_only=False, slots=False):
    """Returns the same class as was passed in, with dunder methods
    added based on the fields defined in the class.
    ...
    """
```

* `cls`: This parameter is set to `None` by default. It is used to pass the class to the decorator.
* `/`: The `/` symbol in the function signature is a syntax feature introduced in Python 3.8. It indicates that all parameters before it must be positional-only. In this case, it means `cls` must be passed as a positional argument.
* `*`: The `*` symbol in the function signature indicates the start of keyword-only arguments. All parameters after `*` must be specified using keyword syntax.
* `init`: If `True`, an `__init__()` method is added to the class. This method initializes the instance attributes based on the provided arguments.
* `repr`: If `True`, a `__repr__()` method is added. This method returns a string representation of the object, useful for debugging.
* `eq`: If `True`, rich comparison dunder methods (`__eq__`, `__lt__`, etc.) are added for comparing instances.
* `order`: If `True`, rich comparison methods are added, and instances can be sorted.
* `unsafe_hash`: If `True`, a `__hash__()` method is added. This method is necessary for instances to be used in hash-based data structures like sets and dictionaries.
* `frozen`: If `True`, it makes the class immutable by preventing assignment to its attributes after instance creation.
* `match_args`: If `True`, a `__match_args__` tuple is added. This is useful for pattern matching.
* `kw_only`: If `True`, all fields are treated as keyword-only arguments in the `__init__` method.
* `slots`: If `True`, an `__slots__` attribute is added to the class. This can reduce memory usage but limits attribute assignment.

**Advantages and Use Cases:**

4.  **Reduced Boilerplate Code:** The primary advantage of using `dataclass` is that it reduces the amount of boilerplate code you need to write. You don't have to explicitly define `__init__`, `__repr__`, and other methods for simple data storage classes.
5.  **Readability:** Code becomes more readable and concise, making it easier to understand and maintain.
6.  **Consistency:** By using `dataclass`, you ensure a consistent and standard way of defining data classes in your codebase.
7.  **Integration with Type Hints:** It works well with type hints, enhancing code readability and providing better tooling support.

## Download Videos from S3 with Curl

```bash
curl -O [https://clio-web-app.s3.amazonaws.com/video/data_set/abobe_stock/HD/255000570.mp4](https://clio-web-app.s3.amazonaws.com/video/data_set/abobe_stock/HD/255000570.mp4)
```

This script takes a csv (or text) file with the S3 urls and downloads them all: `/Users/hshariati/download_videos_from_s3.sh`

```zsh
#!/bin/zsh
# File containing the URLs
input_file="EvalSetForFlickerDebugging.csv"

# Loop through each line in the file
while IFS= read -r url;
do
  # Trim any leading/trailing spaces and make sure the line isn't empty
  url=$(echo "$url" | xargs)
  if [[ -n "$url" ]];
  then
    # Use curl to download the file
    echo "Downloading $url..."
    curl -O "$url"
  else
    echo "Skipping empty line..."
  fi
done < "$input_file"
echo "Download completed."
```

## Async Await Asyncio Concurrency

Any function that has `await` in it needs to be `async`.

```python
async def func():
  k = await some_other_async_func()
```

If you want to make an async function sync, you can call it with `asyncio.run`.

```python
def func():
	k = asyncio.run(some_other_async_func())
```

This doesn't require async or await.

## TORCH

### To Save a Decoded (Colligo Tensor) Image

```python
from torchvision.transforms.functional import to_pil_image
k = to_pil_image(response.images.as_torch()[0])
k.save("/sensei-fs/users/hshariati/colligo_files_backup/shayan_colligo/colligo/delete/test.png")
```

### The `squeeze()` Function in PyTorch

The `squeeze()` function in PyTorch removes dimensions with size 1 from the shape of the tensor. If you provide a specific dimension as an argument to `squeeze(dim)`, it only removes the dimension if its size is 1; otherwise, the tensor remains unchanged.

Let's consider different scenarios:

8.  `elm.squeeze()` (without arguments): This removes all dimensions with size 1 from the tensor `elm`.
9.  `elm.squeeze(0)`:
    * This removes the dimension at index 0 if its size is 1.
    * If `elm` has shape `(1, A, B, C)`, the result will have shape `(A, B, C)`.
    * If the size of the dimension at index 0 is not 1, the tensor remains unchanged.
10. `elm.squeeze(1)`:
    * This removes the dimension at index 1 if its size is 1.
    * If `elm` has shape `(A, 1, B, C)`, the result will have shape `(A, B, C)`.
    * If the size of the dimension at index 1 is not 1, the tensor remains unchanged.

Here's a simple example:

```python
import torch

# Example tensor with size (1, 3, 1, 4)
elm = torch.randn(1, 3, 1, 4)

# Remove dimensions with size 1
result_default = elm.squeeze()

# Remove dimension at index 0 if size is 1
result_dim0 = elm.squeeze(0)

# Remove dimension at index 1 if size is 1
result_dim1 = elm.squeeze(1)

Hs = elm.squeeze(2)

print(result_default.shape)  # Output: (3, 4)
print(result_dim0.shape)     # Output: (3, 1, 4)
print(result_dim1.shape)     # Output: (1, 3,  4)
```

**to expand a dimension you can use the `unsqueeze` command.**

## Save and Load a Torch Tensor
```python
import torch
+        torch.save(
+            hs_temp_t5_text_embedding,
+            "/sensei-fs/users/hshariati/AdobeDiffusion/hs_temp_t5_text_embedding_noPad_xxl.pkl",
+        )


# Load the torch model
loaded_t5_text_embedding = torch.load(
    "/sensei-fs/users/hshariati/AdobeDiffusion/hs_temp_t5_text_embedding_noPad_xxl.pkl"
)
```


## streamlit
on pluto you can start streamlit applications like this
```bash
export PLUTO_MACHINE=<NAME_OF_YOUR_PLUTO_MACHINE>
contrib/clio_demos/clineto_global_view
streamlit run global_view_demo.py --server.port 8000 --server.baseUrlPath 'streamlit' --server.enableXsrfProtection=false --browser.gatherUsageStats=false --browser.serverAddress=$PLUTO_MACHINE-8000.colligo.dev
```

For example:
```bash
streamlit run app.py --server.port 8000 --server.baseUrlPath 'streamlit' --server.enableXsrfProtection=false --browser.gatherUsageStats=false --browser.serverAddress=pluto-prod-hshariati-viq-4gpu-dev-2-0-8000.colligo.dev
```

And you can access the demo in:
https://pluto-prod-hshariati-viq-4gpu-dev-2-0-8000.colligo.dev/streamlit/

*Note that the commandline will give you the url with port at the end but that's not correct.