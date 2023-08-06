# Ahri - ahri_mime

## [Github](https://github.com/fox-ahri/djangowebsocket)

### Contact me ahriknow@gmail.com


### How to use
- install
    ```sh
    pip install ahri_mime
    ```

- import
    ```python
    from ahri_mime import get_ext, get_exts, get_type, get_types
    ```

- The ahri_mime hasattr:

    | attribute   | type     | explain                                  |
    |-------------|----------|------------------------------------------|
    | MIME        | file     | include  `EXT_TO_TYPE` and `TYPE_TO_EXT` |
    | EXT_TO_TYPE | dict     | key is `Extension`, value is `Type`      |
    | TYPE_TO_EXT | dict     | key is `Type`, value is `Extension`      |
    | get_ext     | function | get `Extension` by type                  |
    | get_exts    | function | get all `Extension`s by type             |
    | get_type    | function | get `Type` by ext                        |
    | get_types   | function | get `Type`s by ext                       |

- Example
    ```python
    from ahri_mime import get_ext, get_exts, get_type, get_types


    def handle():
        print(get_ext('x-world/x-3dmf'))
        print(get_exts('x-world/x-3dmf', dot=False))
        print(get_type('docx', dot=False))
        print(get_types('.docx'))

    if __name__ == "__main__":
        handle()
    ```
    ```sh
    .3dm
    ['3dm', '3dmf', 'qd3', 'qd3d']
    application/vnd.openxmlformats-officedocument.wordprocessingml.document
    ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    ```
