# Lisp Parser

A Lisp parser based on Python's regular expression.


## Usage

- **Parse text:**

    ```python
    root = lisp.ParseLisp(text)
    ```

- **Search node by name:**

    ```python
    for node in root['name']:
        print(node)
    ```

- **Search node by index:**

    ```python
    node = root[0, 2, 1]
    ```

- **Get node's parent:**

    ```python
    parent = node[...]
    ```

- **Get node by chain:**

    ```python
    node = root['name', -1, ..., 2, 1, 0]
    ```

- **Get node's children:**

    ```python
    for child in node:
        print(child)
    ```

- **Get children's count:**

    ```python
    count = len(node)
    ```

- **Get node's name:**

    ```python
    node_name = str(node)
    ```
    
- **Compare with node's name:**

    ```python
    print(node == 'name')
    ```

- **Check sub-node in node:**

    ```python
    print('name' in node)
    ```
